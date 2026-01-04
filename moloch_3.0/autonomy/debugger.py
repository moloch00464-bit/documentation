#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Self Debugger
==================================
Autonomous error detection and fixing
"""

from typing import Optional, Dict, Tuple
from pathlib import Path
import traceback

from core.api import MolochAPI
from autonomy.logger import SmartLogger


class SelfDebugger:
    """
    Self-Debugging System for M.O.L.O.C.H. 3.0

    Features:
    - Analyze errors
    - Suggest fixes
    - Apply fixes (with backup)
    - Test fixes
    """

    def __init__(self):
        """Initialize Self Debugger"""
        self.api = MolochAPI()
        self.logger = SmartLogger("debugger")

    # ═══════════════════════════════════════════════════════════════════════════
    # ERROR ANALYSIS
    # ═══════════════════════════════════════════════════════════════════════════

    def analyze_error(
        self,
        error: Exception,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze an error

        Args:
            error: Exception object
            context: Optional context (code, variables, etc.)

        Returns:
            Analysis dict with suggested fix
        """
        self.logger.info(f"Analyzing error: {type(error).__name__}: {error}")

        # Extract error info
        error_info = {
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }

        # Ask Claude for analysis
        analysis = self._ask_claude_for_fix(error_info)

        self.logger.info(f"Analysis complete: {analysis.get('diagnosis', 'Unknown')}")

        return analysis

    def _ask_claude_for_fix(self, error_info: Dict) -> Dict:
        """
        Ask Claude API to analyze error and suggest fix

        Args:
            error_info: Error information

        Returns:
            Analysis with suggested fix
        """
        # Build prompt
        prompt = f"""
Ich bin M.O.L.O.C.H. und habe einen Fehler. Analysiere und schlage einen Fix vor!

ERROR TYPE: {error_info['type']}
ERROR MESSAGE: {error_info['message']}

TRACEBACK:
{error_info['traceback']}

CONTEXT:
{error_info.get('context', 'No context')}

Antworte im JSON Format:
{{
    "diagnosis": "Was ist das Problem?",
    "fix_description": "Wie kann ich es fixen?",
    "fix_code": "Python code für den Fix (wenn applicable)",
    "preventive_measure": "Wie kann ich das in Zukunft vermeiden?"
}}
"""

        try:
            # API call
            system_prompt = """Du bist M.O.L.O.C.H.'s Self-Debugger.
Analysiere Fehler präzise und schlage konkrete Fixes vor.
Antworte immer im JSON Format."""

            response, _ = self.api.chat(
                messages=[{"role": "user", "content": prompt}],
                system_prompt=system_prompt,
                max_tokens=1024
            )

            # Parse response
            import json
            import re

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                return analysis
            else:
                return {
                    "diagnosis": response,
                    "fix_description": "See diagnosis",
                    "fix_code": None,
                    "preventive_measure": "Unknown"
                }

        except Exception as e:
            self.logger.error(f"Claude analysis failed: {e}")
            return {
                "diagnosis": f"Analysis failed: {e}",
                "fix_description": "Manual intervention needed",
                "fix_code": None,
                "preventive_measure": "Unknown"
            }

    # ═══════════════════════════════════════════════════════════════════════════
    # FIX APPLICATION
    # ═══════════════════════════════════════════════════════════════════════════

    def apply_fix(
        self,
        fix: Dict,
        file_path: Optional[str] = None,
        auto_backup: bool = True
    ) -> bool:
        """
        Apply suggested fix

        Args:
            fix: Fix dict from analyze_error()
            file_path: File to fix (if fix_code requires file modification)
            auto_backup: If True, backup file before fixing

        Returns:
            Success status
        """
        self.logger.info(f"Applying fix: {fix.get('fix_description', 'Unknown')}")

        fix_code = fix.get("fix_code")

        if not fix_code:
            self.logger.warning("No fix code provided - manual fix needed")
            return False

        # If file modification is needed
        if file_path:
            if auto_backup:
                self._backup_file(file_path)

            # Apply fix to file
            # (Implementation depends on fix type)
            self.logger.info(f"Would apply fix to: {file_path}")
            # TODO: Implement actual file fixing

        # If Python code execution is needed
        else:
            try:
                # Execute fix code
                exec(fix_code)
                self.logger.info("Fix code executed successfully")
                return True
            except Exception as e:
                self.logger.error(f"Fix execution failed: {e}")
                return False

        return False

    def _backup_file(self, file_path: str):
        """Backup file before modification"""
        import shutil
        from datetime import datetime

        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            shutil.copy2(file_path, backup_path)
            self.logger.info(f"Backup created: {backup_path}")
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    # TESTING
    # ═══════════════════════════════════════════════════════════════════════════

    def test_fix(self, test_func) -> Tuple[bool, Optional[Exception]]:
        """
        Test if fix worked

        Args:
            test_func: Function to test (should raise exception if fix didn't work)

        Returns:
            (success, error_if_any)
        """
        try:
            test_func()
            self.logger.info("✅ Fix test passed")
            return True, None
        except Exception as e:
            self.logger.error(f"❌ Fix test failed: {e}")
            return False, e

    # ═══════════════════════════════════════════════════════════════════════════
    # AUTO-DEBUG WORKFLOW
    # ═══════════════════════════════════════════════════════════════════════════

    def auto_debug(
        self,
        error: Exception,
        context: Optional[Dict] = None,
        file_path: Optional[str] = None
    ) -> bool:
        """
        Full auto-debug workflow

        Args:
            error: Exception
            context: Context
            file_path: File to fix (if applicable)

        Returns:
            Success status
        """
        self.logger.info("🤖 Starting auto-debug workflow...")

        # Step 1: Analyze
        analysis = self.analyze_error(error, context)

        # Step 2: Apply fix
        if analysis.get("fix_code"):
            success = self.apply_fix(analysis, file_path)

            if success:
                self.logger.info("✅ Auto-debug successful!")
                return True
            else:
                self.logger.error("❌ Auto-debug failed")
                return False
        else:
            self.logger.warning("⚠️ No automatic fix available - manual intervention needed")
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🤖 M.O.L.O.C.H. 3.0 Self Debugger Test\n")

    debugger = SelfDebugger()

    # Test error analysis
    print("🔍 Testing error analysis...")

    try:
        # Create a test error
        x = 1 / 0
    except Exception as e:
        analysis = debugger.analyze_error(e, context={"operation": "division"})

        print(f"   Diagnosis: {analysis.get('diagnosis', 'N/A')}")
        print(f"   Fix: {analysis.get('fix_description', 'N/A')}")

    print("\n💡 Auto-debug features ready!")
    print()
