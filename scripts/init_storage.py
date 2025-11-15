#!/usr/bin/env python3
"""
Initialize storage directory structure for AvatarForge

This script creates the base storage directories. Subdirectories will be
created automatically as files are uploaded using hash-based structure:
  storage/uploads/{file_type}/{hash[:2]}/{hash[2:4]}/{hash}.ext
"""
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from avatarforge.core.config import settings


def init_storage():
    """Initialize storage directory structure"""

    storage_root = Path(settings.STORAGE_PATH if hasattr(settings, 'STORAGE_PATH') else "./storage")

    directories = [
        storage_root / "uploads",
        storage_root / "outputs",
    ]

    print("🗂️  Initializing AvatarForge storage directories...")
    print(f"   Storage root: {storage_root.absolute()}")
    print()

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        # Set permissions (rwxr-xr-x)
        directory.chmod(0o755)
        print(f"   ✓ Created: {directory.relative_to(storage_root.parent)}")

    print()
    print("✅ Storage initialization complete!")
    print()
    print("📁 Directory Structure:")
    print("   storage/")
    print("   ├── uploads/     # Uploaded files (hash-based subdirs created automatically)")
    print("   │   ├── pose_image/")
    print("   │   │   └── {hash[:2]}/{hash[2:4]}/{hash}.ext")
    print("   │   └── reference_image/")
    print("   │       └── {hash[:2]}/{hash[2:4]}/{hash}.ext")
    print("   └── outputs/     # Generated avatar outputs")
    print()
    print("💡 Subdirectories will be created automatically as files are uploaded.")
    print()

    # Create a .gitignore in storage to prevent committing files
    gitignore_path = storage_root / ".gitignore"
    gitignore_content = """# Ignore all files in storage
*
!.gitignore
"""
    gitignore_path.write_text(gitignore_content)
    print(f"   ✓ Created .gitignore in storage directory")
    print()


if __name__ == "__main__":
    try:
        init_storage()
    except Exception as e:
        print(f"❌ Error initializing storage: {e}", file=sys.stderr)
        sys.exit(1)
