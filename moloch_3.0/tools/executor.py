#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Tool Executor
==================================
Central tool execution dispatcher
"""

from typing import Dict, Any
import json

from tools.bash import BashTool
from tools.files import FileTool
from tools.search import SearchTool
from tools.web import WebTool


class ToolExecutor:
    """
    Tool Execution Dispatcher

    Executes tool calls from Claude API and returns results
    """

    def __init__(self):
        """Initialize Tool Executor"""
        self.bash = BashTool()
        self.files = FileTool()
        self.search = SearchTool()
        self.web = WebTool()

    def execute(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute a tool

        Args:
            tool_name: Name of tool to execute
            tool_input: Tool input parameters

        Returns:
            Tool result (as string)
        """
        try:
            # Dispatch to appropriate tool
            if tool_name == "bash":
                return self._execute_bash(tool_input)

            elif tool_name == "read_file":
                return self._execute_read_file(tool_input)

            elif tool_name == "write_file":
                return self._execute_write_file(tool_input)

            elif tool_name == "search_code":
                return self._execute_search_code(tool_input)

            elif tool_name == "web_search":
                return self._execute_web_search(tool_input)

            else:
                return f"❌ Unknown tool: {tool_name}"

        except Exception as e:
            return f"❌ Tool execution error: {e}"

    # ═══════════════════════════════════════════════════════════════════════════
    # TOOL IMPLEMENTATIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def _execute_bash(self, tool_input: Dict) -> str:
        """Execute bash command"""
        command = tool_input.get("command", "")
        timeout = tool_input.get("timeout", 30)

        if not command:
            return "❌ No command provided"

        stdout, stderr, returncode = self.bash.execute(command, timeout=timeout)

        # Build result
        result = []
        if returncode == 0:
            result.append(f"✅ Command successful (exit code {returncode})")
        else:
            result.append(f"⚠️ Command failed (exit code {returncode})")

        if stdout:
            result.append(f"\nSTDOUT:\n{stdout}")

        if stderr:
            result.append(f"\nSTDERR:\n{stderr}")

        return "\n".join(result)

    def _execute_read_file(self, tool_input: Dict) -> str:
        """Read file"""
        path = tool_input.get("path", "")

        if not path:
            return "❌ No path provided"

        content = self.files.read(path)

        if content is None:
            return f"❌ Failed to read file: {path}"

        return content

    def _execute_write_file(self, tool_input: Dict) -> str:
        """Write file"""
        path = tool_input.get("path", "")
        content = tool_input.get("content", "")

        if not path:
            return "❌ No path provided"

        success = self.files.write(path, content)

        if success:
            return f"✅ File written: {path}"
        else:
            return f"❌ Failed to write file: {path}"

    def _execute_search_code(self, tool_input: Dict) -> str:
        """Search code"""
        pattern = tool_input.get("pattern", "")
        path = tool_input.get("path", ".")

        if not pattern:
            return "❌ No pattern provided"

        results = self.search.grep(pattern, path=path, max_results=20)

        if not results:
            return f"No matches found for pattern: {pattern}"

        # Format results
        lines = [f"Found {len(results)} matches:\n"]

        for result in results:
            file_path = result["file"]
            line_num = result["line"]
            content = result["content"].strip()

            lines.append(f"{file_path}:{line_num}")
            lines.append(f"  {content}")
            lines.append("")

        return "\n".join(lines)

    def _execute_web_search(self, tool_input: Dict) -> str:
        """Web search"""
        query = tool_input.get("query", "")

        if not query:
            return "❌ No query provided"

        results = self.web.search(query, max_results=5)

        if not results:
            return f"No results found for: {query}"

        # Format results
        lines = [f"Search results for '{query}':\n"]

        for i, result in enumerate(results, 1):
            title = result.get("title", "N/A")
            url = result.get("url", "N/A")
            snippet = result.get("snippet", "")

            lines.append(f"{i}. {title}")
            if url != "N/A":
                lines.append(f"   URL: {url}")
            if snippet:
                lines.append(f"   {snippet}")
            lines.append("")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n⚡ M.O.L.O.C.H. 3.0 Tool Executor Test\n")

    executor = ToolExecutor()

    # Test bash
    print("🔧 Testing bash tool...")
    result = executor.execute("bash", {"command": "echo 'Test'"})
    print(f"   Result:\n{result}\n")

    # Test read_file
    print("📖 Testing read_file tool...")
    result = executor.execute("read_file", {"path": "/etc/hostname"})
    if result and not result.startswith("❌"):
        print(f"   ✅ Read successful: {result[:50]}...")
    else:
        print(f"   {result}")

    # Test search_code
    print("\n🔍 Testing search_code tool...")
    result = executor.execute("search_code", {"pattern": "def execute", "path": "."})
    lines = result.split("\n")
    print(f"   Result: {lines[0]}")

    print()
