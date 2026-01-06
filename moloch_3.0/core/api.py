#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - API Client
==============================
Claude API Client with Tools Support
"""

import anthropic
import base64
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL


class MolochAPI:
    """
    Claude API Client for M.O.L.O.C.H. 3.0
    Supports: Text, Vision, Tools
    """

    def __init__(self, api_key: str = None, model: str = CLAUDE_MODEL):
        """
        Initialize API Client

        Args:
            api_key: Anthropic API Key (defaults to config)
            model: Claude model to use
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set!")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model

    def chat(
        self,
        messages: List[Dict],
        system_prompt: str,
        tools: Optional[List[Dict]] = None,
        image_path: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 1.0
    ) -> Tuple[str, Optional[List]]:
        """
        Main chat function

        Args:
            messages: Chat history [{"role": "user", "content": "..."}]
            system_prompt: System prompt (M.O.L.O.C.H. DNA)
            tools: Optional tool definitions
            image_path: Optional path to image (for vision)
            max_tokens: Max response tokens
            temperature: Response randomness

        Returns:
            (response_text, tool_calls)
        """
        try:
            # Build message content
            if image_path:
                # Vision mode - add image
                content = self._build_vision_content(messages[-1]["content"], image_path)
                messages[-1]["content"] = content

            # API Call
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "system": system_prompt,
                "messages": messages
            }

            if tools:
                kwargs["tools"] = tools

            response = self.client.messages.create(**kwargs)

            # Extract response
            response_text = self._extract_text(response)
            tool_calls = self._extract_tool_calls(response) if tools else None

            return response_text, tool_calls

        except anthropic.APIError as e:
            print(f"❌ API Error: {e}")
            return f"[API Error: {e}]", None
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return f"[Error: {e}]", None

    def _build_vision_content(self, text: str, image_path: str) -> List[Dict]:
        """
        Builds content with image for vision mode

        Args:
            text: User text
            image_path: Path to image

        Returns:
            Content array with image + text
        """
        # Encode image to base64
        image_b64 = self._encode_image(image_path)

        content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_b64
                }
            },
            {
                "type": "text",
                "text": text
            }
        ]

        return content

    def _encode_image(self, image_path: str) -> str:
        """
        Encodes image to base64

        Args:
            image_path: Path to image file

        Returns:
            Base64 encoded string
        """
        try:
            with open(image_path, "rb") as f:
                return base64.standard_b64encode(f.read()).decode("utf-8")
        except Exception as e:
            print(f"❌ Image encoding error: {e}")
            raise

    def _extract_text(self, response) -> str:
        """
        Extracts text from API response

        Args:
            response: Claude API response

        Returns:
            Response text
        """
        text_blocks = [
            block.text
            for block in response.content
            if block.type == "text"
        ]
        return "\n".join(text_blocks) if text_blocks else ""

    def _extract_tool_calls(self, response) -> Optional[List[Dict]]:
        """
        Extracts tool calls from API response

        Args:
            response: Claude API response

        Returns:
            List of tool calls or None
        """
        tool_blocks = [
            {
                "id": block.id,
                "name": block.name,
                "input": block.input
            }
            for block in response.content
            if block.type == "tool_use"
        ]
        return tool_blocks if tool_blocks else None

    def chat_with_tools(
        self,
        messages: List[Dict],
        system_prompt: str,
        tools: List[Dict],
        max_iterations: int = 5
    ) -> Tuple[str, List[Dict]]:
        """
        Chat with tools - handles tool execution loop

        Args:
            messages: Chat history
            system_prompt: System prompt
            tools: Tool definitions
            max_iterations: Max tool call iterations

        Returns:
            (final_response, tool_results_history)
        """
        from tools.executor import ToolExecutor

        executor = ToolExecutor()
        tool_results_history = []
        iteration = 0

        while iteration < max_iterations:
            # API Call
            response_text, tool_calls = self.chat(
                messages=messages,
                system_prompt=system_prompt,
                tools=tools
            )

            # No tool calls? Done!
            if not tool_calls:
                return response_text, tool_results_history

            # Execute tools
            tool_results = []
            for tool_call in tool_calls:
                result = executor.execute(
                    tool_name=tool_call["name"],
                    tool_input=tool_call["input"]
                )

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call["id"],
                    "content": result
                })

                tool_results_history.append({
                    "tool": tool_call["name"],
                    "input": tool_call["input"],
                    "output": result
                })

            # Add tool results to messages
            messages.append({
                "role": "assistant",
                "content": tool_calls
            })
            messages.append({
                "role": "user",
                "content": tool_results
            })

            iteration += 1

        # Max iterations reached
        return response_text, tool_results_history


# ═══════════════════════════════════════════════════════════════════════════════
# TOOL DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

# NOTE: MOLOCH_TOOLS is now defined in core/tools.py (with all 9 tools!)
# This file (core/api.py) is deprecated - use moloch3_unified.py instead!
# Import MOLOCH_TOOLS from core/tools if needed:
#   from core.tools import MOLOCH_TOOLS, execute_tool


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🤖 M.O.L.O.C.H. 3.0 API Client Test\n")

    # Test initialization
    try:
        api = MolochAPI()
        print(f"✅ API Client initialized")
        print(f"   Model: {api.model}")
        print(f"   API Key: {api.api_key[:20]}...")
    except Exception as e:
        print(f"❌ API Client Error: {e}")

    # Test chat (simple)
    try:
        print("\n📝 Testing simple chat...")
        response, tools = api.chat(
            messages=[{"role": "user", "content": "Sag mir nur 'TEST OK' - sonst nichts!"}],
            system_prompt="Du bist M.O.L.O.C.H. Antworte genau wie gefragt.",
            max_tokens=50
        )
        print(f"✅ Response: {response}")
    except Exception as e:
        print(f"❌ Chat Error: {e}")

    print()
