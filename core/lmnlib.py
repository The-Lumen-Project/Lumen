# lmnlib.py
import os
from pathlib import Path

class LumenLibrary:
    def __init__(self, name, functions=None, constants=None):
        self.name = name
        self.functions = functions or {}
        self.constants = constants or {}

    def __getattr__(self, item):
        # Access functions or constants
        if item in self.functions:
            return self.functions[item]
        if item in self.constants:
            return self.constants[item]
        raise AttributeError(f"Library '{self.name}' has no attribute '{item}'")

def load_library(lib_name: str, system=True, install_dir=None):
    """
    Load a library by name.
    - system=True → load from install_dir/libs
    - system=False → load from install_dir/packages
    """
    if not lib_name.isupper():
        raise ValueError(f"Library name must be ALL CAPS: got '{lib_name}'")

    if install_dir is None:
        install_dir = Path(__file__).parent

    folder = "libs" if system else "packages"
    lib_path = Path(install_dir) / folder / f"{lib_name}.lmnh"

    if not lib_path.exists():
        raise FileNotFoundError(f"Library '{lib_name}' not found at {lib_path}")

    functions = {}
    constants = {}
    info = {}  # Store library metadata

    # Pre-import common modules that libraries use
    context = {
        'math': __import__('math'),
        'sys': __import__('sys'),
        'os': __import__('os'),
        'random': __import__('random'),
        'datetime': __import__('datetime'),
        're': __import__('re'),
        'platform': __import__('platform'),
        'json': __import__('json'),
        'string': __import__('string'),
        'requests': __import__('requests'),
    }

    current_section = None
    with open(lib_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):  # skip empty lines and comments
                continue
            
            # Handle INFO section
            if line.startswith("[INFO]"):
                current_section = "INFO"
                continue
            elif current_section == "INFO" and "=" in line:
                key, val = map(str.strip, line.split("=", 1))
                info[key] = val
                continue
                
            # Handle IMPORTS section (skip since we pre-import)
            if line.startswith("[IMPORTS]"):
                current_section = None
                continue
                
            # Section headers
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1].upper()
                continue

            # Constants
            if current_section == "CONSTANTS" and "=" in line:
                key, val = map(str.strip, line.split("=", 1))
                try:
                    constants[key] = eval(val, context)
                except Exception as e:
                    #print(f"Warning: Could not evaluate constant {key}={val}: {e}")
                    constants[key] = val

            # Functions
            elif current_section == "FUNCTIONS" and "=" in line:
                key, val = map(str.strip, line.split("=", 1))
                
                # Handle function definition with parameters in parentheses
                if "(" in key and ")" in key:
                    # Extract function name and parameters
                    func_name = key.split("(")[0].strip()
                    params_str = key.split("(")[1].split(")")[0].strip()
                    params = [p.strip() for p in params_str.split(",")] if params_str else []
                    
                    # Create the function with access to pre-imported modules
                    if params:
                        # Build a lambda function with the correct number of parameters
                        param_names = ", ".join(params)
                        lambda_expr = f"lambda {param_names}: {val}"
                        try:
                            functions[func_name] = eval(lambda_expr, context)
                        except Exception as e:
                            print(f"Warning: Could not create function {func_name}: {e}")
                    else:
                        # No parameters
                        try:
                            functions[func_name] = eval(f"lambda: {val}", context)
                        except Exception as e:
                            print(f"Warning: Could not create function {func_name}: {e}")
                else:
                    # Simple function definition without parameters in name
                    def make_func(template):
                        def func(*args):
                            # Format the template with arguments
                            formatted = template.format(*args)
                            try:
                                return eval(formatted, context)
                            except Exception as e:
                                print(f"Error evaluating {formatted}: {e}")
                                return None
                        return func
                    
                    functions[key] = make_func(val)

    # Create the library with metadata as constants
    for key, value in info.items():
        constants[key] = value

    return LumenLibrary(lib_name, functions=functions, constants=constants)

# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    install_dir = Path(__file__).parent
