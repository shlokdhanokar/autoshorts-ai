"""
Base Agent class for AutoShorts AI system.
All specialized agents inherit from this base class.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import json
from tenacity import retry, stop_after_attempt, wait_exponential

from config import log, settings
from core.agent_memory import AgentMemory


class AgentStatus(Enum):
    """Agent execution status."""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    
    Provides:
    - Memory management (short-term and long-term)
    - Decision-making framework
    - Inter-agent communication
    - Error handling and retry logic
    - Logging and telemetry
    """
    
    def __init__(self, agent_id: str, agent_type: str):
        """
        Initialize the base agent.
        
        Args:
            agent_id: Unique identifier for this agent instance
            agent_type: Type of agent (e.g., "trend_research", "scriptwriting")
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = AgentStatus.IDLE
        self.memory = AgentMemory(agent_id=agent_id, agent_type=agent_type)
        self.execution_history: List[Dict[str, Any]] = []
        self.created_at = datetime.now()
        
        log.info(f"Initialized {agent_type} agent with ID: {agent_id}")
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method for the agent.
        Must be implemented by all subclasses.
        
        Args:
            input_data: Input data for the agent to process
            
        Returns:
            Output data from the agent's execution
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data before execution.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    @abstractmethod
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """
        Validate output data after execution.
        
        Args:
            output_data: Output data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the agent with retry logic and error handling.
        
        Args:
            input_data: Input data for execution
            
        Returns:
            Output data from execution
            
        Raises:
            Exception: If execution fails after all retries
        """
        execution_id = f"{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            self.status = AgentStatus.RUNNING
            log.info(f"[{self.agent_type}] Starting execution: {execution_id}")
            
            # Validate input
            if not self.validate_input(input_data):
                raise ValueError(f"Invalid input data for {self.agent_type}")
            
            # Store input in memory
            self.memory.store_short_term("last_input", input_data)
            
            # Execute agent logic
            start_time = datetime.now()
            output_data = await self.execute(input_data)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Validate output
            if not self.validate_output(output_data):
                raise ValueError(f"Invalid output data from {self.agent_type}")
            
            # Store output in memory
            self.memory.store_short_term("last_output", output_data)
            
            # Record execution history
            execution_record = {
                "execution_id": execution_id,
                "timestamp": datetime.now().isoformat(),
                "input": input_data,
                "output": output_data,
                "execution_time": execution_time,
                "status": "success"
            }
            self.execution_history.append(execution_record)
            self.memory.store_long_term(f"execution_{execution_id}", execution_record)
            
            self.status = AgentStatus.COMPLETED
            log.info(f"[{self.agent_type}] Completed execution: {execution_id} in {execution_time:.2f}s")
            
            return output_data
            
        except Exception as e:
            self.status = AgentStatus.FAILED
            log.error(f"[{self.agent_type}] Execution failed: {execution_id} - {str(e)}")
            
            # Record failure
            failure_record = {
                "execution_id": execution_id,
                "timestamp": datetime.now().isoformat(),
                "input": input_data,
                "error": str(e),
                "status": "failed"
            }
            self.execution_history.append(failure_record)
            self.memory.store_long_term(f"failure_{execution_id}", failure_record)
            
            raise
    
    def make_decision(self, context: Dict[str, Any], options: List[Any]) -> Any:
        """
        Make a decision based on context and available options.
        Can be overridden by subclasses for custom decision logic.
        
        Args:
            context: Context information for decision-making
            options: Available options to choose from
            
        Returns:
            Selected option
        """
        # Default: return first option
        # Subclasses should implement more sophisticated logic
        if not options:
            raise ValueError("No options available for decision-making")
        
        log.debug(f"[{self.agent_type}] Making decision with {len(options)} options")
        return options[0]
    
    def send_message(self, recipient_agent_id: str, message: Dict[str, Any]) -> None:
        """
        Send a message to another agent.
        
        Args:
            recipient_agent_id: ID of the recipient agent
            message: Message data to send
        """
        message_data = {
            "from": self.agent_id,
            "to": recipient_agent_id,
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        
        # Store in memory for tracking
        self.memory.store_short_term(f"sent_message_{recipient_agent_id}", message_data)
        log.debug(f"[{self.agent_type}] Sent message to {recipient_agent_id}")
    
    def receive_message(self, sender_agent_id: str, message: Dict[str, Any]) -> None:
        """
        Receive a message from another agent.
        
        Args:
            sender_agent_id: ID of the sender agent
            message: Message data received
        """
        message_data = {
            "from": sender_agent_id,
            "to": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        
        # Store in memory
        self.memory.store_short_term(f"received_message_{sender_agent_id}", message_data)
        log.debug(f"[{self.agent_type}] Received message from {sender_agent_id}")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for this agent.
        
        Returns:
            Dictionary of performance metrics
        """
        successful_executions = [e for e in self.execution_history if e.get("status") == "success"]
        failed_executions = [e for e in self.execution_history if e.get("status") == "failed"]
        
        avg_execution_time = 0
        if successful_executions:
            avg_execution_time = sum(e.get("execution_time", 0) for e in successful_executions) / len(successful_executions)
        
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "total_executions": len(self.execution_history),
            "successful_executions": len(successful_executions),
            "failed_executions": len(failed_executions),
            "success_rate": len(successful_executions) / len(self.execution_history) if self.execution_history else 0,
            "average_execution_time": avg_execution_time,
            "current_status": self.status.value,
            "uptime": (datetime.now() - self.created_at).total_seconds()
        }
    
    def reset(self) -> None:
        """Reset agent to initial state."""
        self.status = AgentStatus.IDLE
        self.memory.clear_short_term()
        log.info(f"[{self.agent_type}] Agent reset to initial state")
    
    def __repr__(self) -> str:
        return f"<{self.agent_type.title()}Agent id={self.agent_id} status={self.status.value}>"
