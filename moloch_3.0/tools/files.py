#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - File Tools
==============================
File operations: Read, Write, Edit, Glob
"""

import os
from pathlib import Path
from typing import List, Optional
import glob as glob_module


class FileTool:
    """
    File Operations Tool

    Features:
    - Read file contents
    - Write files
    - Edit files (search & replace)
    - Glob pattern matching
    """

    def __init__(self):
        """Initialize File Tool"""
        pass

    # ═══════════════════════════════════════════════════════════════════════════
    # READ
    # ═══════════════════════════════════════════════════════════════════════════

    def read(self, path: str, max_size_mb: int = 10) -> Optional[str]:
        """
        Read file contents

        Args:
            path: File path
            max_size_mb: Max file size in MB (safety limit)

        Returns:
            File contents or None
        """
        try:
            path_obj = Path(path).expanduser()

            if not path_obj.exists():
                print(f"❌ File not found: {path}")
                return None

            if not path_obj.is_file():
                print(f"❌ Not a file: {path}")
                return None

            # Check file size
            size_mb = path_obj.stat().st_size / (1024 * 1024)
            if size_mb > max_size_mb:
                print(f"⚠️ File too large: {size_mb:.1f} MB (max {max_size_mb} MB)")
                return None

            # Read
            with open(path_obj, "r", encoding="utf-8") as f:
                content = f.read()

            return content

        except UnicodeDecodeError:
            print(f"⚠️ Binary file (can't read as text): {path}")
            return None

        except Exception as e:
            print(f"❌ Read error: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════════════════
    # WRITE
    # ═══════════════════════════════════════════════════════════════════════════

    def write(self, path: str, content: str, backup: bool = True) -> bool:
        """
        Write content to file

        Args:
            path: File path
            content: Content to write
            backup: If True, backup existing file before overwriting

        Returns:
            Success status
        """
        try:
            path_obj = Path(path).expanduser()

            # Backup existing file
            if backup and path_obj.exists():
                backup_path = str(path_obj) + ".backup"
                try:
                    import shutil
                    shutil.copy2(path_obj, backup_path)
                    print(f"💾 Backup: {backup_path}")
                except Exception as e:
                    print(f"⚠️ Backup failed: {e}")

            # Create parent directory if needed
            path_obj.parent.mkdir(parents=True, exist_ok=True)

            # Write
            with open(path_obj, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"✅ Written: {path}")
            return True

        except Exception as e:
            print(f"❌ Write error: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # EDIT
    # ═══════════════════════════════════════════════════════════════════════════

    def edit(
        self,
        path: str,
        old_string: str,
        new_string: str,
        backup: bool = True
    ) -> bool:
        """
        Edit file (search & replace)

        Args:
            path: File path
            old_string: String to find
            new_string: String to replace with
            backup: If True, backup before editing

        Returns:
            Success status
        """
        # Read file
        content = self.read(path)
        if content is None:
            return False

        # Check if string exists
        if old_string not in content:
            print(f"⚠️ String not found: {old_string[:50]}...")
            return False

        # Replace
        new_content = content.replace(old_string, new_string)

        # Write back
        return self.write(path, new_content, backup=backup)

    # ═══════════════════════════════════════════════════════════════════════════
    # GLOB
    # ═══════════════════════════════════════════════════════════════════════════

    def glob(self, pattern: str, recursive: bool = True) -> List[str]:
        """
        Find files by glob pattern

        Args:
            pattern: Glob pattern (e.g., "*.py", "**/*.json")
            recursive: If True, use recursive glob

        Returns:
            List of matching file paths
        """
        try:
            if recursive:
                matches = glob_module.glob(pattern, recursive=True)
            else:
                matches = glob_module.glob(pattern)

            return sorted(matches)

        except Exception as e:
            print(f"❌ Glob error: {e}")
            return []

    # ═══════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════════════════════════════════════

    def exists(self, path: str) -> bool:
        """Check if file exists"""
        return Path(path).expanduser().exists()

    def is_file(self, path: str) -> bool:
        """Check if path is a file"""
        return Path(path).expanduser().is_file()

    def is_dir(self, path: str) -> bool:
        """Check if path is a directory"""
        return Path(path).expanduser().is_dir()

    def get_size(self, path: str) -> Optional[int]:
        """Get file size in bytes"""
        try:
            return Path(path).expanduser().stat().st_size
        except:
            return None


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n📁 M.O.L.O.C.H. 3.0 File Tools Test\n")

    files = FileTool()

    # Test write
    print("📝 Testing write...")
    test_file = "/tmp/moloch_test.txt"
    success = files.write(test_file, "Test content\nLine 2\n", backup=False)
    print(f"   {'✅' if success else '❌'} Write: {success}")

    # Test read
    print("\n📖 Testing read...")
    content = files.read(test_file)
    if content:
        print(f"   ✅ Read: {len(content)} bytes")
        print(f"   Content: {content[:50]}...")
    else:
        print("   ❌ Read failed")

    # Test edit
    print("\n✏️ Testing edit...")
    success = files.edit(test_file, "Test", "Modified", backup=False)
    print(f"   {'✅' if success else '❌'} Edit: {success}")

    # Test glob
    print("\n🔍 Testing glob...")
    matches = files.glob("/tmp/*.txt")
    print(f"   ✅ Found {len(matches)} .txt files in /tmp")

    # Cleanup
    try:
        os.remove(test_file)
    except:
        pass

    print()
