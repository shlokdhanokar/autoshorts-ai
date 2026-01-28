"""
Agent Orchestrator for AutoShorts AI.
Manages agent lifecycle, message routing, and workflow execution.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import asyncio

from config import log, settings
from core.base_agent import BaseAgent, AgentStatus


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class AgentOrchestrator:
    """
    Central coordinator for managing multiple agents.
    
    Responsibilities:
    - Agent lifecycle management
    - Message routing between agents
    - Workflow execution
    - System health monitoring
    - Error recovery and retry strategies
    """
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: List[Dict[str, Any]] = []
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.current_workflow: Optional[str] = None
        self.workflow_status = WorkflowStatus.PENDING
        
        log.info("Agent Orchestrator initialized")
    
    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the orchestrator.
        
        Args:
            agent: Agent instance to register
        """
        self.agents[agent.agent_id] = agent
        log.info(f"Registered agent: {agent.agent_id} ({agent.agent_type})")
    
    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister an agent from the orchestrator.
        
        Args:
            agent_id: ID of agent to unregister
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            log.info(f"Unregistered agent: {agent_id}")
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Get an agent by ID.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(agent_id)
    
    def get_agents_by_type(self, agent_type: str) -> List[BaseAgent]:
        """
        Get all agents of a specific type.
        
        Args:
            agent_type: Type of agents to retrieve
            
        Returns:
            List of matching agents
        """
        return [agent for agent in self.agents.values() if agent.agent_type == agent_type]
    
    async def route_message(self, sender_id: str, recipient_id: str, message: Dict[str, Any]) -> None:
        """
        Route a message from one agent to another.
        
        Args:
            sender_id: Sender agent ID
            recipient_id: Recipient agent ID
            message: Message data
        """
        sender = self.get_agent(sender_id)
        recipient = self.get_agent(recipient_id)
        
        if not sender:
            log.error(f"Sender agent not found: {sender_id}")
            return
        
        if not recipient:
            log.error(f"Recipient agent not found: {recipient_id}")
            return
        
        # Send message
        sender.send_message(recipient_id, message)
        recipient.receive_message(sender_id, message)
        
        log.debug(f"Routed message: {sender_id} -> {recipient_id}")
    
    async def execute_workflow(self, workflow_name: str, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a workflow with multiple agents.
        
        Args:
            workflow_name: Name of the workflow
            workflow_config: Workflow configuration with steps
            
        Returns:
            Workflow execution results
        """
        workflow_id = f"{workflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_workflow = workflow_id
        self.workflow_status = WorkflowStatus.RUNNING
        
        log.info(f"Starting workflow: {workflow_id}")
        
        workflow_results = {
            "workflow_id": workflow_id,
            "workflow_name": workflow_name,
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "status": "running"
        }
        
        try:
            steps = workflow_config.get("steps", [])
            step_outputs = {}
            
            for idx, step in enumerate(steps):
                step_name = step.get("name", f"step_{idx}")
                agent_type = step.get("agent_type")
                input_data = step.get("input", {})
                
                # Resolve input references from previous steps
                if "input_from_step" in step:
                    prev_step = step["input_from_step"]
                    if prev_step in step_outputs:
                        input_data = step_outputs[prev_step]
                
                log.info(f"Executing workflow step: {step_name} ({agent_type})")
                
                # Get agent of specified type
                agents = self.get_agents_by_type(agent_type)
                if not agents:
                    raise ValueError(f"No agent found for type: {agent_type}")
                
                agent = agents[0]  # Use first available agent of this type
                
                # Execute agent
                try:
                    output = await agent.run(input_data)
                    step_outputs[step_name] = output
                    
                    workflow_results["steps"].append({
                        "step_name": step_name,
                        "agent_type": agent_type,
                        "agent_id": agent.agent_id,
                        "status": "success",
                        "output": output
                    })
                    
                except Exception as e:
                    log.error(f"Step {step_name} failed: {str(e)}")
                    
                    # Check if step is optional
                    if step.get("optional", False):
                        log.warning(f"Optional step {step_name} failed, continuing workflow")
                        workflow_results["steps"].append({
                            "step_name": step_name,
                            "agent_type": agent_type,
                            "status": "failed_optional",
                            "error": str(e)
                        })
                        continue
                    else:
                        # Critical step failed
                        raise
            
            # Workflow completed successfully
            workflow_results["status"] = "completed"
            workflow_results["end_time"] = datetime.now().isoformat()
            self.workflow_status = WorkflowStatus.COMPLETED
            
            log.info(f"Workflow completed: {workflow_id}")
            
        except Exception as e:
            workflow_results["status"] = "failed"
            workflow_results["error"] = str(e)
            workflow_results["end_time"] = datetime.now().isoformat()
            self.workflow_status = WorkflowStatus.FAILED
            
            log.error(f"Workflow failed: {workflow_id} - {str(e)}")
            raise
        
        finally:
            self.current_workflow = None
        
        return workflow_results
    
    def get_system_health(self) -> Dict[str, Any]:
        """
        Get overall system health status.
        
        Returns:
            System health metrics
        """
        agent_statuses = {}
        for agent_id, agent in self.agents.items():
            metrics = agent.get_performance_metrics()
            agent_statuses[agent_id] = {
                "type": agent.agent_type,
                "status": agent.status.value,
                "success_rate": metrics["success_rate"],
                "total_executions": metrics["total_executions"]
            }
        
        return {
            "total_agents": len(self.agents),
            "agents_by_status": {
                "idle": len([a for a in self.agents.values() if a.status == AgentStatus.IDLE]),
                "running": len([a for a in self.agents.values() if a.status == AgentStatus.RUNNING]),
                "completed": len([a for a in self.agents.values() if a.status == AgentStatus.COMPLETED]),
                "failed": len([a for a in self.agents.values() if a.status == AgentStatus.FAILED])
            },
            "current_workflow": self.current_workflow,
            "workflow_status": self.workflow_status.value,
            "agent_details": agent_statuses
        }
    
    def reset_all_agents(self) -> None:
        """Reset all agents to initial state."""
        for agent in self.agents.values():
            agent.reset()
        log.info("All agents reset to initial state")
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the orchestrator."""
        log.info("Shutting down orchestrator...")
        
        # Wait for current workflow to complete if running
        if self.workflow_status == WorkflowStatus.RUNNING:
            log.warning("Workflow still running, waiting for completion...")
            # In production, implement proper cancellation
        
        # Clear all agents
        self.agents.clear()
        self.message_queue.clear()
        
        log.info("Orchestrator shutdown complete")
