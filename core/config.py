"""
Configuration module for Lumen compiler
"""

import os
import sys
from pathlib import Path

# Global configuration variables
file = None
debug_mode = False

def set_debug_mode(enabled: bool):
    """Enable or disable debug mode"""
    global debug_mode
    debug_mode = enabled

def get_debug_mode() -> bool:
    """Get current debug mode state"""
    return debug_mode

def validate_environment():
    """Validate the compiler environment and return any issues found"""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 7):
        issues.append(f"Python 3.7+ required, found {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check if we can write to current directory
    try:
        test_file = Path("test_write_permissions.tmp")
        test_file.write_text("test")
        test_file.unlink()
    except (PermissionError, OSError):
        issues.append("Cannot write to current directory")
    
    # Check if required modules are available
    required_modules = ['pathlib', 'subprocess', 'argparse']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            issues.append(f"Required module '{module}' not available")
    
    return issues

def get_output_directory():
    """Get the default output directory for compiled files"""
    return Path.cwd() / "output"

def get_libs_directory():
    """Get the directory where library files are stored"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_dir = Path(sys.executable).parent
    else:
        # Running as script
        base_dir = Path(__file__).parent
    
    return base_dir / "libs"

def setup_directories():
    """Setup required directories"""
    directories = [
        get_output_directory(),
        get_libs_directory(),
        Path.cwd() / "python",  # For Python output
        Path.cwd() / "dist",    # For binary output
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            if get_debug_mode():
                print(f"Warning: Cannot create directory {directory}")

# Initialize directories on import
setup_directories()