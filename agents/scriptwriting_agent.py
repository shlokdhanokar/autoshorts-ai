"""
Scriptwriting Agent for AutoShorts AI.
Generates optimized scripts for short-form video content.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import asyncio

from openai import AsyncOpenAI

from core import BaseAgent
from config import log, settings


@dataclass
class ScriptScene:
    """Data class for script scenes."""
    timestamp: str
    text: str
    visual_cue: str
    on_screen_text: Optional[str] = None


class ScriptwritingAgent(BaseAgent):
    """
    Agent responsible for generating short-form optimized scripts.
    
    Responsibilities:
    - Generate 15-60 second scripts using LLM
    - Structure: Hook (0-3s) → Core (3-40s) → CTA (final)
    - Create scene-by-scene breakdown
    - Generate A/B variants and select best
    """
    
    def __init__(self, agent_id: str = "scriptwriting_001"):
        """Initialize the Scriptwriting Agent."""
        super().__init__(agent_id=agent_id, agent_type="scriptwriting")
        
        # Initialize LLM client
        self.llm_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute script generation.
        
        Args:
            input_data: Input data containing:
                - topic: Topic for the script
                - niche: Content niche
                - hook: Suggested hook line
                - target_emotion: Target emotion
                - duration: Target duration in seconds (default: 45)
                - tone: Script tone (educational, motivational, entertaining)
                
        Returns:
            Dictionary with generated script and scene breakdown
        """
        topic = input_data["topic"]
        niche = input_data.get("niche", "general")
        hook = input_data.get("hook", "")
        target_emotion = input_data.get("target_emotion", "curiosity")
        duration = input_data.get("duration", 45)
        tone = input_data.get("tone", "educational")
        
        log.info(f"Generating script for topic: {topic}")
        
        # Generate multiple script variants
        num_variants = 3
        variants = []
        
        for i in range(num_variants):
            variant = await self._generate_script_variant(
                topic=topic,
                niche=niche,
                hook=hook,
                target_emotion=target_emotion,
                duration=duration,
                tone=tone,
                variant_num=i
            )
            variants.append(variant)
        
        # Select best variant
        best_script = await self._select_best_variant(variants, target_emotion)
        
        # Create scene breakdown
        scenes = self._create_scene_breakdown(best_script, duration)
        
        # Generate on-screen text suggestions
        on_screen_texts = self._generate_on_screen_text(best_script)
        
        # Store successful patterns
        await self._learn_from_script(best_script, topic, niche)
        
        result = {
            "script": best_script,
            "scenes": [self._scene_to_dict(s) for s in scenes],
            "on_screen_text": on_screen_texts,
            "estimated_duration": duration,
            "tone": tone,
            "niche": niche,
            "variants_generated": num_variants
        }
        
        # Store in memory
        self.memory.store_long_term(
            f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            result
        )
        
        return result
    
    async def _generate_script_variant(
        self,
        topic: str,
        niche: str,
        hook: str,
        target_emotion: str,
        duration: int,
        tone: str,
        variant_num: int
    ) -> str:
        """
        Generate a single script variant using LLM.
        
        Args:
            topic: Script topic
            niche: Content niche
            hook: Suggested hook
            target_emotion: Target emotion
            duration: Target duration
            tone: Script tone
            variant_num: Variant number for variation
            
        Returns:
            Generated script text
        """
        # Retrieve successful script patterns from memory
        learnings = self.memory.retrieve_learnings("successful_script_structure", min_confidence=0.6)
        learning_context = "\n".join([l["content"] for l in learnings[:3]]) if learnings else ""
        
        # Build prompt
        system_prompt = f"""You are an expert short-form video scriptwriter specializing in {niche} content.
Your scripts are optimized for maximum retention and engagement on platforms like YouTube Shorts and Instagram Reels.

Key principles:
- Hook viewers in the first 3 seconds
- Maintain high energy and pacing
- Use pattern interrupts every 10-15 seconds
- End with a clear call-to-action
- Write in a {tone} tone
- Target emotion: {target_emotion}

{f"Successful patterns from past scripts: {learning_context}" if learning_context else ""}

Script structure:
1. Hook (0-3s): Grab attention immediately
2. Core Content (3-{duration-5}s): Deliver value with engaging pacing
3. CTA ({duration-5}-{duration}s): Clear call-to-action

Write naturally as if speaking directly to the viewer."""

        user_prompt = f"""Create a {duration}-second script for a short-form video about: "{topic}"

{f"Suggested hook: {hook}" if hook else ""}

Requirements:
- Total duration: approximately {duration} seconds when spoken
- Start with a powerful hook
- Keep sentences short and punchy
- Use conversational language
- Include natural pauses for visual emphasis
- End with engagement (like, follow, comment)

Write the complete script now:"""

        try:
            response = await self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature + (variant_num * 0.1),  # Vary temperature for diversity
                max_tokens=500
            )
            
            script = response.choices[0].message.content.strip()
            log.debug(f"Generated script variant {variant_num + 1}")
            return script
            
        except Exception as e:
            log.error(f"Failed to generate script variant: {str(e)}")
            # Fallback to template-based script
            return self._generate_fallback_script(topic, hook, duration)
    
    def _generate_fallback_script(self, topic: str, hook: str, duration: int) -> str:
        """Generate a simple fallback script if LLM fails."""
        return f"""{hook if hook else "You won't believe this..."}

{topic} - and I'm going to show you exactly how.

Here's what you need to know.

First, understand the basics.

Then, take action on what you learned.

Finally, stay consistent and you'll see results.

If you found this helpful, make sure to follow for more tips like this!"""
    
    async def _select_best_variant(self, variants: List[str], target_emotion: str) -> str:
        """
        Select the best script variant using LLM evaluation.
        
        Args:
            variants: List of script variants
            target_emotion: Target emotion
            
        Returns:
            Best script variant
        """
        if len(variants) == 1:
            return variants[0]
        
        # Use LLM to evaluate and select best variant
        evaluation_prompt = f"""You are evaluating short-form video scripts for maximum engagement.

Target emotion: {target_emotion}

Here are {len(variants)} script variants:

{chr(10).join([f"VARIANT {i+1}:{chr(10)}{script}{chr(10)}" for i, script in enumerate(variants)])}

Evaluate each variant based on:
1. Hook strength (first 3 seconds)
2. Retention potential (pacing, pattern interrupts)
3. Emotional impact (matches target emotion: {target_emotion})
4. Call-to-action clarity

Respond with ONLY the number of the best variant (1, 2, or 3)."""

        try:
            response = await self.llm_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": evaluation_prompt}],
                temperature=0.3,  # Lower temperature for more consistent evaluation
                max_tokens=10
            )
            
            selection = response.choices[0].message.content.strip()
            variant_num = int(selection) - 1
            
            if 0 <= variant_num < len(variants):
                log.info(f"Selected variant {variant_num + 1} as best")
                return variants[variant_num]
            
        except Exception as e:
            log.warning(f"Failed to evaluate variants: {str(e)}, using first variant")
        
        # Fallback to first variant
        return variants[0]
    
    def _create_scene_breakdown(self, script: str, duration: int) -> List[ScriptScene]:
        """
        Break script into scenes with timestamps.
        
        Args:
            script: Full script text
            duration: Total duration
            
        Returns:
            List of scenes with timestamps
        """
        # Split script into sentences/segments
        segments = [s.strip() for s in script.split('\n') if s.strip()]
        
        if not segments:
            return []
        
        # Calculate time per segment
        time_per_segment = duration / len(segments)
        
        scenes = []
        current_time = 0
        
        for i, segment in enumerate(segments):
            # Determine visual cue based on content
            visual_cue = self._determine_visual_cue(segment, i)
            
            # Calculate timestamp
            start_time = int(current_time)
            end_time = int(current_time + time_per_segment)
            timestamp = f"{start_time}-{end_time}s"
            
            scene = ScriptScene(
                timestamp=timestamp,
                text=segment,
                visual_cue=visual_cue
            )
            scenes.append(scene)
            
            current_time += time_per_segment
        
        return scenes
    
    def _determine_visual_cue(self, text: str, position: int) -> str:
        """Determine appropriate visual cue for a text segment."""
        text_lower = text.lower()
        
        # Hook (first segment)
        if position == 0:
            return "close-up face, direct eye contact"
        
        # Keywords for specific visuals
        if any(word in text_lower for word in ["show", "look", "see", "watch"]):
            return "b-roll footage, demonstration"
        elif any(word in text_lower for word in ["first", "second", "third", "step"]):
            return "animated text overlay, numbered list"
        elif any(word in text_lower for word in ["result", "outcome", "success"]):
            return "before/after comparison"
        else:
            return "medium shot, engaging expression"
    
    def _generate_on_screen_text(self, script: str) -> List[str]:
        """
        Generate key phrases for on-screen text overlays.
        
        Args:
            script: Full script
            
        Returns:
            List of key phrases
        """
        # Extract important phrases (simplified version)
        # In production, use NLP to extract key phrases
        
        lines = [line.strip() for line in script.split('\n') if line.strip()]
        
        # Take first line (hook) and any short, impactful lines
        on_screen_texts = []
        
        for line in lines:
            if len(line) < 50 and any(char in line for char in ['!', '?']):
                on_screen_texts.append(line)
        
        return on_screen_texts[:5]  # Limit to 5 key phrases
    
    async def _learn_from_script(self, script: str, topic: str, niche: str) -> None:
        """
        Learn patterns from generated script.
        
        Args:
            script: Generated script
            topic: Topic
            niche: Niche
        """
        # Store successful script structure
        lines = script.split('\n')
        if lines:
            hook = lines[0]
            self.memory.store_learning(
                "successful_hook_pattern",
                hook[:100],  # Store first 100 chars of hook
                confidence=0.7
            )
        
        # Store successful topic-niche combination
        self.memory.store_learning(
            "successful_topic_niche",
            f"{niche}:{topic}",
            confidence=0.6
        )
    
    def _scene_to_dict(self, scene: ScriptScene) -> Dict[str, Any]:
        """Convert ScriptScene to dictionary."""
        return {
            "timestamp": scene.timestamp,
            "text": scene.text,
            "visual_cue": scene.visual_cue,
            "on_screen_text": scene.on_screen_text
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        return "topic" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output data."""
        required_keys = ["script", "scenes", "on_screen_text", "estimated_duration"]
        return all(key in output_data for key in required_keys)
