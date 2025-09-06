# Run this to see exact filenames
from pathlib import Path

libs_dir = Path("core/libs")
if libs_dir.exists():
    print("Library files found:")
    for file in libs_dir.glob("*"):
        print(f"  - {file.name} (extension: {file.suffix})")
else:
    print("libs directory does not exist!")