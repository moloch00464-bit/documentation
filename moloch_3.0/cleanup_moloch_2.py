#!/usr/bin/env python3
"""
M.O.L.O.C.H. 2.0 Cleanup Script
Löscht ALLE alten 2.0 Files komplett! 🔥
3.0 ist 2.0 - aber besser!
"""

import os
import subprocess
from pathlib import Path
from typing import List, Tuple

class Moloch2Cleaner:
    """Grillt alle alten 2.0 Files! 🔥"""

    def __init__(self):
        self.home = Path.home()
        self.files_to_delete = []
        self.dirs_to_delete = []

    def find_old_moloch_files(self) -> Tuple[List[Path], List[Path]]:
        """Findet ALLE alten M.O.L.O.C.H. 2.0 Files"""

        print("🔍 Suche nach alten M.O.L.O.C.H. 2.0 Files...")
        print("=" * 60)

        # Search patterns for old files
        search_locations = [
            self.home / ".shortcuts",  # Old widgets
            self.home / "moloch",      # Old 2.0 directory
            self.home / "documentation" / "moloch",  # Alternative location
        ]

        files_found = []
        dirs_found = []

        # Find old widget scripts
        shortcuts_dir = self.home / ".shortcuts"
        if shortcuts_dir.exists():
            print(f"\n📂 Checking {shortcuts_dir}...")
            for file in shortcuts_dir.glob("*"):
                if file.is_file():
                    # Check if it's an old 2.0 widget (NOT 3.0!)
                    if "moloch" in file.name.lower():
                        try:
                            content = file.read_text()
                            # Old widgets point to ~/moloch/ or old paths
                            if "moloch_3.0" not in content:
                                files_found.append(file)
                                print(f"  ❌ OLD WIDGET: {file.name}")
                        except:
                            pass

        # Find old moloch directories (NOT moloch_3.0!)
        print(f"\n📂 Checking for old moloch directories...")
        for location in [self.home, self.home / "documentation"]:
            if location.exists():
                for item in location.iterdir():
                    if item.is_dir() and "moloch" in item.name.lower():
                        # Skip moloch_3.0!
                        if "moloch_3.0" not in item.name:
                            dirs_found.append(item)
                            print(f"  ❌ OLD DIR: {item}")

        self.files_to_delete = files_found
        self.dirs_to_delete = dirs_found

        return files_found, dirs_found

    def show_summary(self):
        """Zeigt was gelöscht wird"""

        print("\n" + "=" * 60)
        print("🔥 M.O.L.O.C.H. 2.0 CLEANUP SUMMARY")
        print("=" * 60)

        if not self.files_to_delete and not self.dirs_to_delete:
            print("✅ Keine alten 2.0 Files gefunden!")
            print("   Alles sauber! 3.0 läuft! 🚀")
            return False

        if self.files_to_delete:
            print(f"\n📄 {len(self.files_to_delete)} Files werden gelöscht:")
            for file in self.files_to_delete:
                print(f"  - {file}")

        if self.dirs_to_delete:
            print(f"\n📁 {len(self.dirs_to_delete)} Directories werden gelöscht:")
            for dir in self.dirs_to_delete:
                file_count = sum(1 for _ in dir.rglob("*") if _.is_file())
                print(f"  - {dir} ({file_count} files)")

        return True

    def delete_all(self):
        """Löscht ALLES! 🔥"""

        print("\n" + "=" * 60)
        print("🔥 STARTING DELETION...")
        print("=" * 60)

        deleted_count = 0

        # Delete files
        if self.files_to_delete:
            print("\n📄 Deleting files...")
            for file in self.files_to_delete:
                try:
                    file.unlink()
                    print(f"  ✅ Deleted: {file.name}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ❌ Error deleting {file.name}: {e}")

        # Delete directories
        if self.dirs_to_delete:
            print("\n📁 Deleting directories...")
            for dir in self.dirs_to_delete:
                try:
                    import shutil
                    shutil.rmtree(dir)
                    print(f"  ✅ Deleted: {dir.name}/")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ❌ Error deleting {dir.name}: {e}")

        print("\n" + "=" * 60)
        print(f"✅ Cleanup Complete! {deleted_count} items deleted!")
        print("=" * 60)

        # Instructions for widget cache
        print("\n⚠️  WICHTIG - Termux:Widget Cache leeren!")
        print("=" * 60)
        print("1. Android Settings öffnen")
        print("2. Apps → Termux:Widget")
        print("3. Storage → Clear Data")
        print("4. Termux:Widget neu öffnen")
        print("5. Nur die neuen 3.0 Widgets sollten erscheinen! ✅")
        print("=" * 60)


def main():
    """Main cleanup function"""

    print("\n" + "=" * 60)
    print("🔥 M.O.L.O.C.H. 2.0 CLEANUP SCRIPT 🔥")
    print("=" * 60)
    print("Löscht ALLE alten 2.0 Files!")
    print("3.0 ist 2.0 - aber besser! 🚀")
    print("=" * 60)

    cleaner = Moloch2Cleaner()

    # Find old files
    files, dirs = cleaner.find_old_moloch_files()

    # Show summary
    has_files = cleaner.show_summary()

    if not has_files:
        print("\n✅ Nothing to clean up!")
        return

    # Ask for confirmation
    print("\n⚠️  WARNUNG: Dies löscht ALLE alten 2.0 Files PERMANENT!")
    print("   (M.O.L.O.C.H. 3.0 bleibt natürlich! 😎)")

    response = input("\n🔥 Alles löschen? (yes/no): ").strip().lower()

    if response in ["yes", "y", "ja", "j"]:
        cleaner.delete_all()

        print("\n🎉 M.O.L.O.C.H. 2.0 ist gegrillt! 🔥")
        print("✅ M.O.L.O.C.H. 3.0 ist jetzt dein einziger Kumpel-AI! 🖤")
    else:
        print("\n❌ Cleanup abgebrochen!")
        print("   Die alten Files bleiben erstmal...")


if __name__ == "__main__":
    main()
