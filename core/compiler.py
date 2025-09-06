import os
import subprocess
import sys
from lmnast import start, LumenParseError, LumenSemanticError
import argparse
import config
import shutil
from pathlib import Path

def get_install_dir() -> str:
    """
    Get the directory where the Lumen compiler is installed.
    Works on Windows/Linux/macOS and supports both script and frozen (PyInstaller) modes.
    """
    if getattr(sys, 'frozen', False):  # Running as PyInstaller EXE
        return str(Path(sys.executable).resolve().parent)
    else:  # Running as a Python script
        return str(Path(__file__).resolve().parent)

def in_venv() -> bool:
    # Standard venv detection
    if getattr(sys, "base_prefix", sys.prefix) != sys.prefix:
        return True
    if "VIRTUAL_ENV" in os.environ:
        return True

    # Extra check for WSL/Linux: see if 'activate' exists in parent dirs
    exec_path = Path(sys.executable).resolve()
    for parent in exec_path.parents:
        if (parent / "bin" / "activate").exists():
            return True

    return False

class LumenCompilerError(Exception):
    """Base exception class for Lumen compiler errors"""
    pass

class LumenSyntaxError(LumenCompilerError):
    """Exception raised for syntax errors in Lumen code"""
    def __init__(self, message, line_number=None, token=None):
        self.line_number = line_number
        self.token = token
        if line_number:
            super().__init__(f"Syntax error at line {line_number}: {message}")
        else:
            super().__init__(f"Syntax error: {message}")

class LumenFileError(LumenCompilerError):
    """Exception raised for file-related errors"""
    pass

def setup_argument_parser():
    """Set up and return the argument parser with error handling"""
    parser = argparse.ArgumentParser(
        description="Lumen Programming Language Compiler",
        prog="lumen",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python compiler.py example.lmn           # Parse and validate
  python compiler.py -p example.lmn       # Compile to Python
  python compiler.py -c example.lmn       # Compile to binary
  python compiler.py -d example.lmn       # Debug mode
        """
    )

    parser.add_argument("-c", "--compile", action="store_true",
                        help="Compiles to a Binary executable file.")
    parser.add_argument("-p", "--py", action="store_true", 
                        help="Compiles to a Python file, not binary.")
    parser.add_argument("-d", "--debug", action="store_true", 
                        help="Shows general Debug text.")
    parser.add_argument("file", nargs="?", 
                        help="Lumen source file to compile")
    
    return parser

def validate_file(filename):
    """Validate that the input file exists and has correct extension"""
    if not filename:
        raise LumenFileError("No input file specified")
    
    file_path = Path(filename)
    
    if not file_path.exists():
        raise LumenFileError(f"File '{filename}' not found")
    
    if not file_path.is_file():
        raise LumenFileError(f"'{filename}' is not a regular file")
    
    if file_path.suffix != '.lmn':
        print(f"Warning: File '{filename}' doesn't have .lmn extension")
    
    try:
        with open(filename, 'r') as f:
            # Try to read the file to check if it's accessible
            f.read(1)
    except PermissionError:
        raise LumenFileError(f"Permission denied: Cannot read '{filename}'")
    except UnicodeDecodeError:
        raise LumenFileError(f"File '{filename}' contains invalid characters or is binary")
    
    return file_path

def ensure_output_directory(directory):
    """Ensure the output directory exists"""
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        raise LumenFileError(f"Permission denied: Cannot create directory '{directory}'")
    except OSError as e:
        raise LumenFileError(f"Cannot create directory '{directory}': {e}")

class PythonCodeGenerator:
    def __init__(self):
        self.static_vars = {}
        self.global_vars = {}
        self.functions = {}
        self.libraries = {}
        self.indent_level = 0
        self.labels = {}
        self.gotos = []
    
    def get_indent(self):
        return "    " * self.indent_level
    
    def format_value(self, value, var_type=None):
        """Format a value for Python output with proper type handling"""
        if value is None:
            return "None"

        if var_type == 'bool' and isinstance(value, str):
            if value.lower() in ('true', 'false'):
                return value.capitalize()
        
        # Handle bracket expressions (array/dict access) like variable[index] or variable["key"]
        if isinstance(value, str) and '[' in value and ']' in value:
            # This is already formatted as access expression, return as-is
            return value
        
        # Handle array values
        if var_type == 'ary' and isinstance(value, list):
            formatted_elements = []
            for element in value:
                # Handle quoted strings, numbers, and variables
                if isinstance(element, str):
                    # Check if it's already a quoted string
                    if (element.startswith('"') and element.endswith('"')) or (element.startswith("'") and element.endswith("'")):
                        formatted_elements.append(element)
                    else:
                        # Check if it's a number
                        try:
                            float(element)  # Try to convert to number
                            formatted_elements.append(element)
                        except ValueError:
                            # Check if it's a variable reference
                            if element.isidentifier():
                                formatted_elements.append(element)
                            else:
                                # It's a string that needs quotes
                                formatted_elements.append(f'"{element}"')
                else:
                    formatted_elements.append(str(element))
            return f"[{', '.join(formatted_elements)}]"
        
        # Handle dictionary values
        if var_type == 'dic' and isinstance(value, dict):
            formatted_pairs = []
            for key, val in value.items():
                # Format key (ensure it's quoted if not already)
                if not ((key.startswith('"') and key.endswith('"')) or (key.startswith("'") and key.endswith("'"))):
                    key_str = f'"{key}"'
                else:
                    key_str = key
                
                # Format value
                if isinstance(val, str):
                    # Check if value is already quoted or is a number/variable
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val_str = val
                    else:
                        try:
                            float(val)  # Try to convert to number
                            val_str = val
                        except ValueError:
                            if val.isidentifier():
                                val_str = val  # Variable reference
                            else:
                                val_str = f'"{val}"'  # String literal
                else:
                    val_str = str(val)
                
                formatted_pairs.append(f"{key_str}: {val_str}")
            return f"{{{', '.join(formatted_pairs)}}}"
        
        # Handle regular string values
        if isinstance(value, str):
            # If it's already quoted, return as-is
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                return value
            
            # Try to determine if it's a number
            try:
                float(value)
                return value  # It's a number, return without quotes
            except ValueError:
                # Check if it's a variable reference
                if value.isidentifier():
                    return value
                else:
                    # It's a string literal that needs quotes
                    return f'"{value}"'
        
        return str(value)

    def find_used_static_vars(self, ast):
        """Find static variables used in an AST subtree"""
        used_statics = set()

        if isinstance(ast, (list, tuple)):
            for item in ast:
                if isinstance(item, (list, tuple)):
                    used_statics.update(self.find_used_static_vars(item))
                elif isinstance(item, str) and item in self.static_vars:
                    used_statics.add(item)
        elif isinstance(ast, str) and ast in self.static_vars:
            used_statics.add(ast)

        return used_statics
    
    def collect_labels_and_gotos(self, lmast):
        """First pass: collect all labels and goto statements for validation"""
        def collect_recursive(statements, scope_name="global"):
            for stmt in statements:
                if isinstance(stmt, (list, tuple)) and len(stmt) >= 2:
                    if stmt[0] == "label":
                        label_name = stmt[1]
                        if label_name in self.labels:
                            raise LumenSemanticError(f"Duplicate label '{label_name}'")
                        self.labels[label_name] = scope_name
                    elif stmt[0] == "goto":
                        label_name = stmt[1]
                        self.gotos.append((label_name, scope_name))
                    elif stmt[0] in ("if", "while", "fun") and len(stmt) >= 3:
                        # Recursively check nested statements
                        if stmt[0] == "fun":
                            collect_recursive(stmt[3], f"function_{stmt[1]}")
                        else:
                            collect_recursive(stmt[2], f"{stmt[0]}_{len(self.labels)}")
        
        collect_recursive(lmast)
        
        # Validate that all gotos have corresponding labels
        for goto_label, goto_scope in self.gotos:
            if goto_label not in self.labels:
                raise LumenSemanticError(f"Undefined label '{goto_label}' in goto statement")
            
            # In Lumen, we'll allow cross-scope gotos but warn about them
            label_scope = self.labels[goto_label]
            if label_scope != goto_scope and goto_scope.startswith("function_"):
                # This would be dangerous - jumping out of a function
                raise LumenSemanticError(f"Cannot goto label '{goto_label}' from inside function - "
                                       f"labels inside functions can only be reached from within the same function")

    def compile_to_python(self, lmast):
        """Compile Lumen AST to Python code with library support"""
        if not isinstance(lmast, list):
            raise LumenCompilerError("Invalid AST: Expected list of statements")

        # First, collect and validate labels and gotos
        self.collect_labels_and_gotos(lmast)
        py_code = ""
        
        # Get the Lumen installation directory
        lumen_install_dir = get_install_dir()
        
        # Add library imports at the top - use absolute path to Lumen install
        py_code += "# Library imports\n"
        py_code += "import sys\n"
        py_code += "from pathlib import Path\n\n"
        
        # Add Lumen installation directory to Python path
        py_code += f"# Add Lumen installation directory to path\n"
        py_code += f"lumen_install_dir = Path(r'{lumen_install_dir}')\n"
        py_code += f"sys.path.insert(0, str(lumen_install_dir))\n\n"
        
        # Now import from the Lumen installation directory
        py_code += f"from lmnlib import load_library\n\n"
        
        # Add library loading code
        py_code += "# Load libraries\n"
        py_code += "install_dir = lumen_install_dir\n\n"
        
        # Process library directives first
        for stmt in lmast:
            if isinstance(stmt, (list, tuple)) and len(stmt) >= 2:
                if stmt[0] == "include":
                    lib_name = stmt[1]
                    lib_var = lib_name.lower()
                    self.libraries[lib_var] = lib_name
                    py_code += f"{lib_var} = load_library('{lib_name}', system=True, install_dir=install_dir)\n"
                elif stmt[0] == "import":
                    package_name = stmt[1]
                    pkg_var = package_name.lower()
                    self.libraries[pkg_var] = package_name
                    py_code += f"{pkg_var} = load_library('{package_name}', system=False, install_dir=install_dir)\n"
        
        if self.libraries:
            py_code += "\n"

        # First pass: collect all static and global variables
        for stmt in lmast:
            if isinstance(stmt, (list, tuple)) and len(stmt) >= 2:
                if stmt[0] == "declare" and len(stmt) >= 5 and stmt[4]:  # is_static is True
                    var_type, name, value = stmt[1], stmt[2], stmt[3]
                    self.static_vars[name] = (var_type, value)
                elif stmt[0] == "global":
                    var_type, name, value = stmt[1], stmt[2], stmt[3]
                    self.global_vars[name] = (var_type, value)

        # Add static variables
        if self.static_vars:
            py_code += "# Static constants (immutable)\n"
            for name, (var_type, value) in self.static_vars.items():
                formatted_value = self.format_value(value, var_type)
                py_code += f"{name} = {formatted_value}\n"
            py_code += "\n"

        # Add global variable declarations
        if self.global_vars:
            py_code += "# Global variables\n"
            for name, (var_type, value) in self.global_vars.items():
                if value is not None:
                    formatted_value = self.format_value(value, var_type)
                    py_code += f"{name} = {formatted_value}\n"
                else:
                    py_code += f"{name} = None\n"
            py_code += "\n"

        # Generate goto implementation if needed
        if self.labels or self.gotos:
            py_code += self.generate_goto_implementation(lmast)
        else:
            # No gotos, compile normally
            py_code += self.compile_statements(lmast)

        return py_code

    def generate_goto_implementation(self, lmast):
        """Generate Python code using proper goto state machine"""
        py_code = ""
        
        # First, define all functions (they can't contain gotos)
        for stmt in lmast:
            if isinstance(stmt, (list, tuple)) and len(stmt) >= 2 and stmt[0] == "fun":
                py_code += self.compile_single_statement(stmt)
        
        # Generate main program with goto support
        py_code += "# Main program with goto support\n"
        py_code += "def main_program():\n"
        self.indent_level += 1
        
        # Generate labels and statements mapping
        non_function_statements = []
        label_map = {}
        
        for stmt in lmast:
            if isinstance(stmt, (list, tuple)) and len(stmt) >= 2:
                if stmt[0] == "label":
                    label_map[stmt[1]] = len(non_function_statements)
                elif stmt[0] != "fun":  # Skip function definitions
                    non_function_statements.append(stmt)
        
        py_code += f"{self.get_indent()}pc = 0\n"
        py_code += f"{self.get_indent()}while pc < {len(non_function_statements)}:\n"
        self.indent_level += 1
        
        # Generate statement execution
        for idx, stmt in enumerate(non_function_statements):
            py_code += f"{self.get_indent()}if pc == {idx}:\n"
            self.indent_level += 1
            
            if stmt[0] == "goto":
                label_name = stmt[1]
                if label_name in label_map:
                    py_code += f"{self.get_indent()}pc = {label_map[label_name]}\n"
                    py_code += f"{self.get_indent()}continue\n"
                else:
                    py_code += f"{self.get_indent()}raise RuntimeError(f'Undefined label: {label_name}')\n"
            else:
                # Execute the statement directly
                stmt_code = self.compile_single_statement(stmt).strip()
                if stmt_code:
                    # Remove the indent from the statement and add our own
                    lines = stmt_code.split('\n')
                    for line in lines:
                        if line.strip():
                            py_code += f"{self.get_indent()}{line.strip()}\n"
            
            self.indent_level -= 1
        
        py_code += f"{self.get_indent()}pc += 1\n"
        self.indent_level -= 1  # End while loop
        self.indent_level -= 1  # End function
        
        py_code += "\n# Execute main program\n"
        py_code += "if __name__ == '__main__':\n"
        py_code += "    main_program()\n"
        
        return py_code

    def contains_goto(self, statements):
        """Check if a list of statements contains any goto or label statements"""
        if not isinstance(statements, list):
            return False
            
        for stmt in statements:
            if isinstance(stmt, (list, tuple)) and len(stmt) >= 1:
                if stmt[0] in ("goto", "label"):
                    return True
                # Recursively check nested statements
                elif stmt[0] in ("if", "while") and len(stmt) >= 3:
                    if self.contains_goto(stmt[2]):
                        return True
        return False

    def compile_single_statement(self, stmt):
        """Compile a single statement to Python code with library support"""
        py_code = ""
        
        if not isinstance(stmt, (list, tuple)) or len(stmt) < 2:
            return py_code

        stmt_type = stmt[0]

        # Handle library directives (skip in code generation since they're handled at top)
        if stmt_type in ("include", "import"):
            return py_code

        # Handle library function calls
        elif stmt_type == "lib_call":
            lib_name, func_name, args = stmt[1], stmt[2], stmt[3]
            lib_var = lib_name.lower()
            
            if lib_var not in self.libraries:
                raise LumenSemanticError(f"Library '{lib_name}' not loaded")
            
            args_str = ", ".join(str(arg) for arg in args) if args else ""
            py_code += f"{self.get_indent()}{lib_var}.{func_name}({args_str})\n"

        # Handle library property access
        elif stmt_type == "lib_access":
            lib_name, member_name = stmt[1], stmt[2]
            lib_var = lib_name.lower()
            
            if lib_var not in self.libraries:
                raise LumenSemanticError(f"Library '{lib_name}' not loaded")
            
            # This would typically be used in assignments or expressions
            py_code += f"{self.get_indent()}{lib_var}.{member_name}\n"

        # All your existing statement handling code...
        elif stmt_type == "declare":
            var_type, name, value, is_static = stmt[1], stmt[2], stmt[3], stmt[4]
            if not is_static:  # Regular variables (non-static)
                if self.is_expression(value):
                    py_code += f"{self.get_indent()}{name} = {value}\n"
                else:
                    formatted_value = self.format_value(value, var_type)
                    py_code += f"{self.get_indent()}{name} = {formatted_value}\n"

        elif stmt_type == "assign":
            name, value = stmt[1], stmt[2]
            if self.is_expression(value):
                py_code += f"{self.get_indent()}{name} = {value}\n"
            else:
                formatted_value = self.format_value(value)
                py_code += f"{self.get_indent()}{name} = {formatted_value}\n"

        elif stmt_type == "print":
            if len(stmt) != 2:
                raise LumenSyntaxError("Invalid print statement")
            if not isinstance(stmt[1], list):
                raise LumenSyntaxError("Print arguments must be a list")

            # Process print arguments properly
            args = []
            for arg in stmt[1]:
                if arg == ",":
                    continue  # Skip comma tokens
                
                # Handle library access in print statements
                if "." in arg and not (arg.startswith(('"', "'"))):
                    # Check if it's library access
                    parts = arg.split(".", 1)
                    if len(parts) == 2 and parts[0].lower() in self.libraries:
                        args.append(arg)  # Keep library access as-is
                        continue
                
                if self.is_expression(arg):
                    args.append(arg)  # Keep expressions as-is
                else:
                    args.append(self.format_value(arg))

            py_code += f"{self.get_indent()}print({', '.join(args)})\n"

        elif stmt_type == "inc":
            if len(stmt) != 2:
                raise LumenSyntaxError("Invalid increment statement")
            py_code += f"{self.get_indent()}{stmt[1]} += 1\n"

        elif stmt_type == "dec":
            if len(stmt) != 2:
                raise LumenSyntaxError("Invalid decrement statement")
            py_code += f"{self.get_indent()}{stmt[1]} -= 1\n"

        elif stmt_type == "if":
            if len(stmt) != 3:
                raise LumenSyntaxError("Invalid if statement: expected condition and body")
            py_code += f"{self.get_indent()}if {stmt[1]}:\n"
            self.indent_level += 1
            body_code = self.compile_statements(stmt[2])
            if not body_code.strip():
                py_code += f"{self.get_indent()}pass\n"
            else:
                py_code += body_code
            self.indent_level -= 1

        elif stmt_type == "while":
            if len(stmt) != 3:
                raise LumenSyntaxError("Invalid while statement: expected condition and body")
            
            py_code += f"{self.get_indent()}while {stmt[1]}:\n"
            self.indent_level += 1
            body_code = self.compile_statements(stmt[2])
            if not body_code.strip():
                py_code += f"{self.get_indent()}pass\n"
            else:
                py_code += body_code
            self.indent_level -= 1

        elif stmt_type == "call":
            if len(stmt) != 3:
                raise LumenSyntaxError("Invalid function call format")

            func_name, args = stmt[1], stmt[2]

            # Validate function exists
            if func_name not in self.functions:
                raise LumenSemanticError(f"Undefined function '{func_name}'")

            # Validate argument count
            expected_params = len(self.functions[func_name]['params'])
            provided_args = len(args)

            if expected_params != provided_args:
                raise LumenSemanticError(f"Function '{func_name}' expects {expected_params} arguments, got {provided_args}")

            args_str = ", ".join(args) if args else ""
            py_code += f"{self.get_indent()}{func_name}({args_str})\n"

        elif stmt_type == "return":
            if len(stmt) != 2:
                raise LumenSyntaxError("Invalid return statement")
            if stmt[1] is not None:
                py_code += f"{self.get_indent()}return {stmt[1]}\n"
            else:
                py_code += f"{self.get_indent()}return\n"

        elif stmt_type == "fun":
            if len(stmt) != 4:
                raise LumenSyntaxError("Invalid function definition: expected name, arguments, and body")

            name, params, body = stmt[1], stmt[2], stmt[3]
            self.functions[name] = {'params': params, 'body': body}

            # Check if function contains gotos - not allowed
            if self.contains_goto(body):
                raise LumenSemanticError(f"Function '{name}' contains goto statements - "
                                       f"goto is not supported inside functions")

            # Generate Python function
            params_str = ", ".join(params) if isinstance(params, list) else str(params)
            py_code += f"{self.get_indent()}def {name}({params_str}):\n"

            self.indent_level += 1

            # Add global declaration for global variables used in this function
            global_vars_used = self.find_global_vars_used(body)
            if global_vars_used:
                py_code += f"{self.get_indent()}global {', '.join(global_vars_used)}\n"

            body_code = self.compile_statements(body)
            if not body_code.strip():
                py_code += f"{self.get_indent()}pass\n"
            else:
                py_code += body_code
            self.indent_level -= 1
            py_code += "\n"

        return py_code

    def compile_statements(self, statements):
        """Compile statements normally (without goto state machine)"""
        py_code = ""
        
        for stmt in statements:
            if stmt is None:
                continue

            try:
                if not isinstance(stmt, (list, tuple)) or len(stmt) < 2:
                    continue

                stmt_type = stmt[0]
                
                if stmt_type in ("import", "include"):
                    continue

                if stmt_type == "declare":
                    var_type, name, value, is_static = stmt[1], stmt[2], stmt[3], stmt[4]
                    if not is_static:  # Regular variables (non-static)
                        # Don't format expressions, they need to be evaluated
                        if isinstance(value, str) and not (value.startswith(('"', "'"))) and not value.replace('.','').replace('-','').isdigit() and value.lower() not in ('true', 'false'):
                            py_code += f"{self.get_indent()}{name} = {value}\n"
                        else:
                            formatted_value = self.format_value(value, var_type)
                            py_code += f"{self.get_indent()}{name} = {formatted_value}\n"

                elif stmt_type == "assign":
                    name, value = stmt[1], stmt[2]
                    # Don't format expressions, they need to be evaluated
                    if isinstance(value, str) and not (value.startswith(('"', "'"))) and not value.replace('.','').replace('-','').isdigit() and value.lower() not in ('true', 'false'):
                        py_code += f"{self.get_indent()}{name} = {value}\n"
                    else:
                        formatted_value = self.format_value(value)
                        py_code += f"{self.get_indent()}{name} = {formatted_value}\n"

                elif stmt_type == "print":
                    if len(stmt) != 2:
                        raise LumenSyntaxError("Invalid print statement")
                    if not isinstance(stmt[1], list):
                        raise LumenSyntaxError("Print arguments must be a list")

                    # Process print arguments - don't quote expressions, handle commas properly
                    args = []
                    for arg in stmt[1]:
                        if arg == ",":
                            continue  # Skip comma tokens
                        if isinstance(arg, str) and not (arg.startswith(('"', "'"))) and not arg.replace('.','').replace('-','').isdigit() and arg not in ('True', 'False'):
                            args.append(arg)  # Keep expressions as-is
                        else:
                            args.append(self.format_value(arg))

                    py_code += f"{self.get_indent()}print({', '.join(args)})\n"

                elif stmt_type == "inc":
                    if len(stmt) != 2:
                        raise LumenSyntaxError("Invalid increment statement")
                    py_code += f"{self.get_indent()}{stmt[1]} += 1\n"

                elif stmt_type == "dec":
                    if len(stmt) != 2:
                        raise LumenSyntaxError("Invalid decrement statement")
                    py_code += f"{self.get_indent()}{stmt[1]} -= 1\n"

                elif stmt_type == "while":
                    if len(stmt) != 3:
                        raise LumenSyntaxError("Invalid while statement: expected condition and body")
                    
                    py_code += f"{self.get_indent()}while {stmt[1]}:\n"
                    self.indent_level += 1
                    body_code = self.compile_statements(stmt[2])
                    if not body_code.strip():
                        py_code += f"{self.get_indent()}pass\n"
                    else:
                        py_code += body_code
                    self.indent_level -= 1

                elif stmt_type == "if":
                    if len(stmt) != 3:
                        raise LumenSyntaxError("Invalid if statement: expected condition and body")
                    py_code += f"{self.get_indent()}if {stmt[1]}:\n"
                    self.indent_level += 1
                    body_code = self.compile_statements(stmt[2])
                    if not body_code.strip():
                        py_code += f"{self.get_indent()}pass\n"
                    else:
                        py_code += body_code
                    self.indent_level -= 1

                elif stmt_type == "fun":
                    if len(stmt) != 4:
                        raise LumenSyntaxError("Invalid function definition: expected name, arguments, and body")

                    name, params, body = stmt[1], stmt[2], stmt[3]
                    self.functions[name] = {'params': params, 'body': body}

                    # Generate Python function
                    params_str = ", ".join(params) if isinstance(params, list) else str(params)
                    py_code += f"{self.get_indent()}def {name}({params_str}):\n"

                    self.indent_level += 1

                    # Add global declaration for global variables used in this function
                    global_vars_used = self.find_global_vars_used(body)
                    if global_vars_used:
                        py_code += f"{self.get_indent()}global {', '.join(global_vars_used)}\n"

                    body_code = self.compile_statements(body)
                    if not body_code.strip():
                        py_code += f"{self.get_indent()}pass\n"
                    else:
                        py_code += body_code
                    self.indent_level -= 1
                    py_code += "\n"

                elif stmt_type == "call":
                    if len(stmt) != 3:
                        raise LumenSyntaxError("Invalid function call format")

                    func_name, args = stmt[1], stmt[2]

                    # Validate function exists
                    if func_name not in self.functions:
                        raise LumenSemanticError(f"Undefined function '{func_name}'")

                    # Validate argument count
                    expected_params = len(self.functions[func_name]['params'])
                    provided_args = len(args)

                    if expected_params != provided_args:
                        raise LumenSemanticError(f"Function '{func_name}' expects {expected_params} arguments, got {provided_args}")

                    args_str = ", ".join(args) if args else ""
                    py_code += f"{self.get_indent()}{func_name}({args_str})\n"

                elif stmt_type == "return":
                    if len(stmt) != 2:
                        raise LumenSyntaxError("Invalid return statement")
                    if stmt[1] is not None:
                        py_code += f"{self.get_indent()}return {stmt[1]}\n"
                    else:
                        py_code += f"{self.get_indent()}return\n"

                elif stmt_type in ("label", "goto"):
                    # These are handled by the goto state machine, skip in normal compilation
                    pass

                else:
                    raise LumenSyntaxError(f"Unknown statement type: {stmt_type}")

            except Exception as e:
                if isinstance(e, (LumenSyntaxError, LumenSemanticError)):
                    raise
                else:
                    raise LumenSyntaxError(f"Error processing statement: {str(e)}")

        return py_code

    def is_variable_used(self, ast, var_name):
        """Check if a variable is used in an AST subtree"""
        if isinstance(ast, (list, tuple)):
            for item in ast:
                if self.is_variable_used(item, var_name):
                    return True
        elif isinstance(ast, str):
            return ast == var_name
        return False

    def find_global_vars_used(self, ast):
        """Find global variables used in an AST subtree"""
        used_globals = set()

        if isinstance(ast, (list, tuple)):
            for item in ast:
                if isinstance(item, (list, tuple)):
                    used_globals.update(self.find_global_vars_used(item))
                elif isinstance(item, str) and item in self.global_vars:
                    used_globals.add(item)
        elif isinstance(ast, str) and ast in self.global_vars:
            used_globals.add(ast)

        return used_globals

def compile_to_python(lmast):
    """Main function to compile Lumen AST to Python"""
    generator = PythonCodeGenerator()
    return generator.compile_to_python(lmast)

def write_python_file(py_result, filename, debug=False):
    """Write Python code to file with error handling"""
    pyfilename = filename.replace(".lmn", ".py")
    
    try:
        # Create python directory in the project folder (where the .lmn file is)
        project_dir = Path(config.file).parent
        python_dir = project_dir / "python"
        ensure_output_directory(str(python_dir))
        
        output_path = python_dir / pyfilename
        
        with open(output_path, "w", encoding='utf-8') as out:
            out.write(py_result)
        
        if debug:
            print(f"The resulting Python code:\n{'-'*40}")
            print(py_result)
            print(f"{'-'*40}")
            print(f"File saved to: {output_path.resolve()}")
        
        return output_path
        
    except Exception as e:
        raise LumenFileError(f"Failed to write Python file: {e}")

def compile_to_binary(python_file_path, debug=False):
    """Compile Python file to binary with error handling"""
    try:
        # Get args properly
        parser = setup_argument_parser()
        # Only parse known args to avoid conflicts
        args, _ = parser.parse_known_args()
        
        venv = in_venv()
        if debug:
            print(f"VENV state: {venv}")
        
        nInputs = ["y","n",""]
        inp = ""
        
        install_dir = Path(get_install_dir())
        if os.name == "nt":
            python_exe = os.path.join(install_dir, "python-files-lmn", "python.exe")
        else:
            python_exe = "python3"
        
        if os.name != "nt":
            if not venv:
                print("""\n!WARNING!\n
PYTHON ON LINUX IS WEIRD!
MY BEST RECOMMENDATION IS TO SETUP A
VENV TO AVOID ERRORS!
                """)
                inp = input("CONTINUE? (y/N): ")
                while inp.lower() not in nInputs:
                    inp = input("CONTINUE? (y/N): ")
            else:
                inp = "y"
                
            if inp.lower() == nInputs[0]:  
                if debug:
                    print("Checking PyInstaller...")
                try:
                    subprocess.run([python_exe, "-m", "PyInstaller", "--version"], 
                                 check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    if debug:
                        print("Installing PyInstaller...")
                    subprocess.run([python_exe, "-m", "pip", "install", "PyInstaller"], 
                                 check=True)
            else:
                raise LumenCompilerError("Compilation Cancelled!")
        
        print("Compiling to binary...")
        print("It is normal if the console hangs for a bit...")
        
        # Check if icon exists
        icon_path = install_dir / "icon.ico"
        compile_args = [
            python_exe, "-m", "PyInstaller",
            "--onefile",
            "--hidden-import=lmnast",
            "--hidden-import=config"
        ]
        
        if icon_path.exists():
            compile_args.extend(["--icon", str(icon_path)])
        
        compile_args.append(str(python_file_path))
        
        compile_result = subprocess.run(compile_args, 
                                      capture_output=True, text=True, timeout=300)
        
        if compile_result.returncode != 0:
            raise LumenCompilerError(f"PyInstaller compilation failed: {compile_result.stderr}")

        print("Binary compilation completed successfully")
            
    except subprocess.TimeoutExpired:
        raise LumenCompilerError("Compilation timed out - the process took too long")
    except FileNotFoundError:
        if os.name == "nt":
            raise LumenCompilerError("Bundled Python interpreter not found")
        else:
            raise LumenCompilerError("Python3 not found - please install Python")
    except Exception as e:
        raise LumenCompilerError(f"Unexpected error during binary compilation: {e}")

def main():
    """Main function with comprehensive error handling"""
    args = None
    try:
        # Parse arguments
        parser = setup_argument_parser()
        args = parser.parse_args()
        
        # Validate input
        if not args.file:
            parser.print_help()
            print("\nError: No input file specified")
            sys.exit(1)
        
        # Set debug mode in config
        if args.debug:
            config.set_debug_mode(True)
        
        # Validate file
        file_path = validate_file(args.file)
        config.file = str(file_path)
        
        if args.debug:
            print(f"Processing file: {file_path}")
            print("Validating environment...")
            
            # Check environment
            env_issues = config.validate_environment()
            if env_issues:
                print("Environment issues found:")
                for issue in env_issues:
                    print(f"  - {issue}")
                print()
        
        # Parse Lumen code
        try:
            if args.debug:
                print("Parsing Lumen source code...")
            
            lumen_code = start()
            
            if args.debug:
                print(f"Successfully parsed AST:")
                for i, stmt in enumerate(lumen_code):
                    print(f"  [{i}]: {stmt}")
                print()
            
        except LumenParseError as e:
            print(f"Parse error: {e}")
            sys.exit(1)
        except LumenSemanticError as e:
            print(f"Semantic error: {e}")
            sys.exit(1)
        
        # Compile to Python
        try:
            if args.debug:
                print("Compiling to Python...")
            
            py_result = compile_to_python(lumen_code)
            
            # Write Python file
            py_file = write_python_file(py_result, file_path.name, args.debug)
            
            if not args.py and not args.compile:
                print(f"Successfully compiled to Python: {py_file}")
            
        except (LumenSyntaxError, LumenSemanticError) as e:
            print(f"Compilation error: {e}")
            sys.exit(1)
        
        # Compile to binary if requested
        if args.compile:
            try:
                if args.debug:
                    print("Starting binary compilation...")
                
                compile_to_binary(py_file, args.debug)
                print(f"Successfully compiled to binary")
                
            except LumenCompilerError as e:
                print(f"Binary compilation error: {e}")
                sys.exit(1)
        
    except LumenFileError as e:
        print(f"File error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCompilation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        if args and args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()