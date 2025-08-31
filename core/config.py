# config.py
import sys
from pathlib import Path

# Global configuration
file = None
debug_mode = False
verbose_errors = False

# Error handling configuration
class ErrorConfig:
    """Configuration for error handling behavior"""
    MAX_ERROR_DISPLAY = 10  # Maximum number of errors to display before stopping
    SHOW_STACK_TRACE = False  # Whether to show full stack traces
    EXIT_ON_FIRST_ERROR = False  # Whether to exit immediately on first error
    ERROR_LOG_FILE = None  # Optional file to log errors to

# Error tracking
class ErrorTracker:
    """Track and manage compilation errors"""
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def add_error(self, error):
        """Add an error to the tracker"""
        self.errors.append(error)
        if ErrorConfig.EXIT_ON_FIRST_ERROR:
            self.print_errors()
            sys.exit(1)
        elif len(self.errors) >= ErrorConfig.MAX_ERROR_DISPLAY:
            self.print_errors()
            print(f"Too many errors ({len(self.errors)}). Stopping compilation.")
            sys.exit(1)
    
    def add_warning(self, warning):
        """Add a warning to the tracker"""
        self.warnings.append(warning)
    
    def has_errors(self):
        """Check if there are any errors"""
        return len(self.errors) > 0
    
    def print_errors(self):
        """Print all accumulated errors and warnings"""
        if self.warnings:
            print("Warnings:")
            for warning in self.warnings:
                print(f"  Warning: {warning}")
            print()
        
        if self.errors:
            print("Errors:")
            for error in self.errors:
                print(f"  Error: {error}")
            print(f"\nCompilation failed with {len(self.errors)} error(s)")
            
            if ErrorConfig.ERROR_LOG_FILE:
                try:
                    with open(ErrorConfig.ERROR_LOG_FILE, 'a') as f:
                        f.write(f"\n=== Compilation Errors for {file} ===\n")
                        for error in self.errors:
                            f.write(f"Error: {error}\n")
                        for warning in self.warnings:
                            f.write(f"Warning: {warning}\n")
                        f.write("=" * 50 + "\n")
                except Exception as e:
                    print(f"Warning: Could not write to error log: {e}")
    
    def clear(self):
        """Clear all errors and warnings"""
        self.errors.clear()
        self.warnings.clear()

# Global error tracker instance
error_tracker = ErrorTracker()

def set_debug_mode(debug):
    """Set global debug mode"""
    global debug_mode, verbose_errors
    debug_mode = debug
    verbose_errors = debug
    if debug:
        ErrorConfig.SHOW_STACK_TRACE = True

def get_file_info():
    """Get information about the current file being processed"""
    if not file:
        return {"file": None, "exists": False, "size": 0}
    
    try:
        file_path = Path(file)
        return {
            "file": str(file_path),
            "exists": file_path.exists(),
            "size": file_path.stat().st_size if file_path.exists() else 0,
            "absolute_path": str(file_path.resolve()) if file_path.exists() else None
        }
    except Exception:
        return {"file": str(file), "exists": False, "size": 0}

def validate_environment():
    """Validate that the environment is set up correctly for compilation"""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 6):
        issues.append("Python 3.6 or higher is required")
    
    # Check required modules
    required_modules = ['re', 'os', 'subprocess', 'pathlib', 'argparse']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            issues.append(f"Required module '{module}' not available")
    
    # Check write permissions for output directories
    output_dirs = ['python', 'dist', 'build']
    for dir_name in output_dirs:
        try:
            test_dir = Path(dir_name)
            test_dir.mkdir(exist_ok=True)
            # Try to write a test file
            test_file = test_dir / ".test_permissions"
            test_file.write_text("test")
            test_file.unlink()  # Delete test file
        except Exception as e:
            issues.append(f"Cannot write to '{dir_name}' directory: {e}")
    
    return issues

# Initialize error tracker
def reset_error_state():
    """Reset the global error state"""
    global error_tracker
    error_tracker.clear()

# Utility functions for error reporting
def format_file_location(line=None, column=None):
    """Format file location information for error messages"""
    location_parts = []
    if file:
        location_parts.append(str(Path(file).name))
    if line is not None:
        location_parts.append(f"line {line}")
    if column is not None:
        location_parts.append(f"column {column}")
    
    return ":".join(location_parts) if location_parts else "unknown location"