import re
import os
import config
from pathlib import Path

class LumenParseError(Exception):
    """Base exception for parsing errors"""
    pass

class LumenTokenizeError(LumenParseError):
    """Exception raised during tokenization"""
    pass

class LumenSyntaxError(LumenParseError):
    """Exception raised for syntax errors"""
    def __init__(self, message, line_number=None, token=None, position=None):
        self.line_number = line_number
        self.token = token
        self.position = position
        
        error_msg = message
        if line_number:
            error_msg = f"Line {line_number}: {message}"
        if token:
            error_msg += f" (near '{token}')"
        if position is not None:
            error_msg += f" at position {position}"
            
        super().__init__(error_msg)

class LumenSemanticError(LumenParseError):
    """Exception raised for semantic errors (type mismatches, undefined variables, etc.)"""
    pass

# ------------------ Expression Parser ------------------
class ExpressionParser:
    """Handles parsing and evaluation of arithmetic expressions"""
    
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.operators = {
            '!': {'precedence': 7, 'associativity': 'right'},
            'not': {'precedence': 7, 'associativity': 'right'},
            '||': {'precedence': 1, 'associativity': 'left'},
            'or': {'precedence': 1, 'associativity': 'left'},
            '&&': {'precedence': 2, 'associativity': 'left'},
            'and': {'precedence': 2, 'associativity': 'left'},
            '==': {'precedence': 3, 'associativity': 'left'},
            '!=': {'precedence': 3, 'associativity': 'left'},
            '<': {'precedence': 4, 'associativity': 'left'},
            '>': {'precedence': 4, 'associativity': 'left'},
            '<=': {'precedence': 4, 'associativity': 'left'},
            '>=': {'precedence': 4, 'associativity': 'left'},
            '+': {'precedence': 5, 'associativity': 'left'},
            '-': {'precedence': 5, 'associativity': 'left'},
            '*': {'precedence': 6, 'associativity': 'left'},
            '/': {'precedence': 6, 'associativity': 'left'},
            '%': {'precedence': 6, 'associativity': 'left'},
        }
    
    def is_operator(self, token):
        """Check if token is an operator"""
        return token in self.operators
    
    def is_operand(self, token):
        """Check if token is an operand (number, string, variable)"""
        if isinstance(token, str):
            # Check if it's a number
            try:
                float(token)
                return True
            except ValueError:
                pass
            
            # Check if it's a string literal
            if (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
                return True
            
            # Check if it's a variable name
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token):
                return True
        
        return False
    
    def parse_expression(self, tokens):
        """Parse expression tokens into a single expression string using shunting yard algorithm"""
        if not tokens:
            return None

        # If it's just a single token, return it
        if len(tokens) == 1:
            return tokens[0]

        # Convert infix to postfix and then back to a Python expression
        output = []
        operator_stack = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if self.is_operand(token):
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop operators until we find opening parenthesis
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Remove the '('
                else:
                    raise LumenSyntaxError("Mismatched parentheses in expression")
            elif self.is_operator(token):
                # Handle unary operators (right associative)
                if token == '!' or token == 'not':
                    # Just push unary operators onto the stack
                    operator_stack.append(token)
                else:
                    # Pop operators with higher or equal precedence
                    while (operator_stack and 
                           operator_stack[-1] != '(' and
                           operator_stack[-1] in self.operators and
                           self.operators[operator_stack[-1]]['precedence'] >= self.operators[token]['precedence']):
                        output.append(operator_stack.pop())
                    operator_stack.append(token)
            else:
                # Unknown token - might be part of a more complex expression
                output.append(token)

            i += 1

        # Pop remaining operators
        while operator_stack:
            if operator_stack[-1] in ('(', ')'):
                raise LumenSyntaxError("Mismatched parentheses in expression")
            output.append(operator_stack.pop())

        # Convert postfix back to infix Python expression
        return self.postfix_to_python(output)
    
    def parse_function_call_expression(self, tokens):
        """Parse function call within an expression"""
        func_name = tokens[0]
        if tokens[1] != '(':
            raise LumenSyntaxError(f"Expected '(' after function name '{func_name}'")
        
        # Find matching parenthesis
        paren_count = 0
        end_paren = -1
        for i in range(1, len(tokens)):
            if tokens[i] == '(':
                paren_count += 1
            elif tokens[i] == ')':
                paren_count -= 1
                if paren_count == 0:
                    end_paren = i
                    break

        if end_paren == -1:
            raise LumenSyntaxError("Unmatched parenthesis in function call")
        
        # Parse arguments
        arg_tokens = tokens[2:end_paren]
        args = []
        if arg_tokens:
            current_arg = []
            for token in arg_tokens:
                if token == ',':
                    if current_arg:
                        arg_expr = self.parse_expression(current_arg)
                        args.append(arg_expr)
                        current_arg = []
                else:
                    current_arg.append(token)
            if current_arg:
                arg_expr = self.parse_expression(current_arg)
                args.append(arg_expr)
        
        # Return function call as expression
        args_str = ', '.join(args) if args else ''
        return f"{func_name}({args_str})"
    
    def postfix_to_python(self, postfix):
        """Convert postfix notation to Python expression"""
        if not postfix:
            return None

        if len(postfix) == 1:
            return postfix[0]

        stack = []
        for token in postfix:
            if self.is_operator(token):
                # Handle unary operators (like !)
                if ((token == '!') or (token == 'not')) and len(stack) >= 1:
                    operand = stack.pop()
                    expr = f"(not {operand})"
                    stack.append(expr)
                # Handle binary operators
                elif len(stack) >= 2:
                    right = stack.pop()
                    left = stack.pop()

                    # Convert logical operators to Python equivalents
                    if token == '&&' or token == 'and':
                        expr = f"({left} and {right})"
                    elif token == '||' or token == 'or':
                        expr = f"({left} or {right})"
                    else:
                        expr = f"({left} {token} {right})"

                    stack.append(expr)
                else:
                    raise LumenSyntaxError(f"Invalid expression: not enough operands for operator '{token}'")
            else:
                stack.append(token)

        if len(stack) != 1:
            raise LumenSyntaxError("Invalid expression: malformed")

        return stack[0]

# ------------------ Symbol Table for Type Checking ------------------
class Symbol:
    def __init__(self, name, var_type, value=None, is_static=False, scope='global'):
        self.name = name
        self.var_type = var_type  # 'int', 'str', 'var'
        self.value = value
        self.is_static = is_static
        self.scope = scope

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.functions = {}
        self.scope_stack = ['global']
        self.static_vars = {}
        self.global_vars = {}
    
    def enter_scope(self, scope_name):
        self.scope_stack.append(scope_name)
    
    def exit_scope(self):
        if len(self.scope_stack) > 1:
            scope = self.scope_stack.pop()
            # Remove local variables from this scope
            to_remove = [name for name, symbol in self.symbols.items() 
                        if symbol.scope == scope]
            for name in to_remove:
                del self.symbols[name]
    
    def current_scope(self):
        return self.scope_stack[-1]
    
    def declare_variable(self, name, var_type, value=None, is_static=False):
        # For global variables, always use global scope
        if name in self.global_vars:
            scope = 'global'
            full_name = name
        else:
            scope = self.current_scope()
            full_name = f"{scope}.{name}" if scope != 'global' else name
        
        if is_static:
            if name in self.static_vars:
                raise LumenSemanticError(f"Static variable '{name}' already declared")
            self.static_vars[name] = Symbol(name, var_type, value, True, 'static')
            return
        
        if full_name in self.symbols:
            raise LumenSemanticError(f"Variable '{name}' already declared in current scope")
        
        self.symbols[full_name] = Symbol(name, var_type, value, False, scope)
    
    def assign_variable(self, name, value):
        """Assign a value to a variable, checking function parameters first"""
        scope = self.current_scope()
        full_name = f"{scope}.{name}" if scope != 'global' else name

        # Check static variables first - they cannot be reassigned
        if name in self.static_vars:
            raise LumenSemanticError(f"Cannot reassign static variable '{name}'")

        # Check if it's a function parameter
        is_parameter = False
        if scope != 'global' and name in self.get_function_parameters(scope):
            is_parameter = True
            # For parameters, we need to create the variable in the local scope
            if full_name not in self.symbols:
                self.declare_variable(name, 'var', value)
            else:
                symbol = self.symbols[full_name]

        # Check local scope first, then global
        if full_name in self.symbols:
            symbol = self.symbols[full_name]
        elif name in self.symbols:  # Check global scope
            symbol = self.symbols[name]
        elif is_parameter:
            # If it's a parameter but not yet in symbols, declare it
            self.declare_variable(name, 'var', value)
            return
        else:
            raise LumenSemanticError(f"Undefined variable '{name}'")

        if not self.check_type_compatibility(symbol.var_type, value):
            raise LumenSemanticError(f"Type mismatch: Cannot assign {self.infer_type(value)} to {symbol.var_type} variable '{name}'")

    def is_function_parameter(self, name):
        """Check if a variable is a function parameter in the current scope"""
        scope = self.current_scope()
        if scope != 'global' and name in self.get_function_parameters(scope):
            return True
        return False
    
    def get_variable(self, name):
        """Get a variable from the symbol table, checking function parameters first"""
        # Check static variables first
        if name in self.static_vars:
            return self.static_vars[name]

        # Check current scope (function parameters and local variables)
        scope = self.current_scope()
        full_name = f"{scope}.{name}" if scope != 'global' else name

        # Check local scope first
        if full_name in self.symbols:
            return self.symbols[full_name]

        # Check if it's a function parameter (parameters are stored with function scope)
        if scope != 'global' and name in self.get_function_parameters(scope):
            # Create a temporary symbol for the parameter
            return Symbol(name, 'var', None, False, scope)

        # Check global variables
        if name in self.global_vars:
            scope = 'global'
            full_name = name

        # Check global scope
        if full_name in self.symbols:
            return self.symbols[full_name]
        elif name in self.symbols:  # Check global scope
            return self.symbols[name]
        else:
            raise LumenSemanticError(f"Undefined variable '{name}'")

    def get_function_parameters(self, function_name):
        """Get the parameters of a function"""
        if function_name in self.functions:
            return self.functions[function_name]['params']
        return []
    
    def declare_function(self, name, params, body_ast):
        if name in self.functions:
            raise LumenSemanticError(f"Function '{name}' already declared")
        self.functions[name] = {'params': params, 'body': body_ast}
    
    def get_function(self, name):
        if name not in self.functions:
            raise LumenSemanticError(f"Undefined function '{name}'")
        return self.functions[name]
    
    def check_type_compatibility(self, declared_type, value):
        """Check if a value is compatible with the declared type"""
        if declared_type == 'var':
            return True  # var can hold anything
        
        # Handle array and dictionary types
        if declared_type == 'ary':
            return isinstance(value, list) or (isinstance(value, str) and value.startswith('['))
        
        if declared_type == 'dic':
            return isinstance(value, dict) or (isinstance(value, str) and value.startswith('{'))
        
        inferred_type = self.infer_type(value)
        return declared_type == inferred_type
    
    def infer_type(self, value):
        """Infer the type of a value"""
        if isinstance(value, str):
            # Check if it's a string literal
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                return 'str'
            # Check if it's an array literal
            if value.startswith('[') and value.endswith(']'):
                return 'ary'
            # Check if it's a dict literal
            if value.startswith('{') and value.endswith('}'):
                return 'dic'
            elif value.lower() in ("true", "false"):
                return 'bool'
            # Check if it's a number
            try:
                int(value)
                return 'int'
            except ValueError:
                try:
                    float(value)
                    return 'float'  # We might want to add float support later
                except ValueError:
                    return 'var'  # Unknown type, treat as var
        elif isinstance(value, list):
            return 'ary'
        elif isinstance(value, dict):
            return 'dic'
        return 'var'

# Global symbol table and expression parser
symbol_table = SymbolTable()
expression_parser = ExpressionParser(symbol_table)

# ------------------ Enhanced Tokenizer ------------------
def tokenize_lumen_file(file_path):
    """Tokenize Lumen source file with enhanced expression support"""
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise LumenTokenizeError(f"File '{file_path}' not found")
        
        if not file_path.is_file():
            raise LumenTokenizeError(f"'{file_path}' is not a regular file")
        
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                code = f.read()
        except UnicodeDecodeError as e:
            raise LumenTokenizeError(f"Cannot read file '{file_path}': {e}")
        except PermissionError:
            raise LumenTokenizeError(f"Permission denied reading '{file_path}'")
        
        if not code.strip():
            raise LumenTokenizeError("File is empty or contains only whitespace")
        
        # Remove comments before tokenization
        code = remove_comments(code)
        
        pattern = r'(\".*?\"|\'.*?\'|\w+:|\+\+|--|==|!=|<=|>=|&&|\|\||[{}()\[\];,:=<>+\-*/%!]|[^\s{}()\[\];,:=<>+\-*/%!]+)'
        
        try:
            tokens = re.findall(pattern, code)
        except re.error as e:
            raise LumenTokenizeError(f"Regular expression error: {e}")
        
        if not tokens:
            raise LumenTokenizeError("No valid tokens found in file")

        # Process tokens to handle attached operators and combine multi-character operators
        final_tokens = []
        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Handle multi-character operators that might be separated
            if i + 1 < len(tokens):
                combined = token + tokens[i + 1]
                if combined in ['==', '!=', '<=', '>=', '&&', '||', '++', '--']:
                    final_tokens.append(combined)
                    i += 2
                    continue
                # Also check for && and || as separate tokens
                elif token == '&' and tokens[i + 1] == '&':
                    final_tokens.append('&&')
                    i += 2
                    continue
                elif token == '|' and tokens[i + 1] == '|':
                    final_tokens.append('||')
                    i += 2
                    continue
                
            # Separate trailing ++ or -- from identifiers
            if token.endswith("++") and len(token) > 2:
                final_tokens.append(token[:-2])
                final_tokens.append("++")
            elif token.endswith("--") and len(token) > 2:
                final_tokens.append(token[:-2])
                final_tokens.append("--")
            else:
                final_tokens.append(token)

            i += 1
        
        return final_tokens
        
    except LumenTokenizeError:
        raise
    except Exception as e:
        raise LumenTokenizeError(f"Unexpected error during tokenization: {e}")

def remove_comments(code):
    """Remove both single-line (//) and multi-line (/* */) comments"""
    # Remove multi-line comments first
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove single-line comments
    lines = code.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Find // comments but ignore those inside strings
        in_string = False
        string_char = None
        cleaned_line = []
        i = 0
        
        while i < len(line):
            char = line[i]
            
            if char in ('"', "'") and not in_string:
                in_string = True
                string_char = char
                cleaned_line.append(char)
            elif char == string_char and in_string:
                in_string = False
                string_char = None
                cleaned_line.append(char)
            elif char == '/' and i + 1 < len(line) and line[i+1] == '/' and not in_string:
                # Found // comment outside of string, skip rest of line
                break
            else:
                cleaned_line.append(char)
            
            i += 1
        
        cleaned_lines.append(''.join(cleaned_line))
    
    return '\n'.join(cleaned_lines)

# ------------------ Enhanced Parser ------------------
def find_matching_brace(tokens, start_index):
    """Find the matching } for the { at start_index with error handling"""
    if start_index >= len(tokens):
        raise LumenSyntaxError(f"Index {start_index} out of range", position=start_index)
    
    if tokens[start_index] != "{":
        raise LumenSyntaxError(f"Expected '{{' but found '{tokens[start_index]}'", 
                             token=tokens[start_index], position=start_index)
    
    depth = 0
    for i in range(start_index, len(tokens)):
        if tokens[i] == "{":
            depth += 1
        elif tokens[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    
    raise LumenSyntaxError("Unmatched opening brace '{'", 
                         token="{", position=start_index)

def find_matching_bracket(tokens, start_index):
    """Find the matching ] for the [ at start_index with error handling"""
    if start_index >= len(tokens):
        raise LumenSyntaxError(f"Index {start_index} out of range", position=start_index)
    
    if tokens[start_index] != "[":
        raise LumenSyntaxError(f"Expected '[' but found '{tokens[start_index]}'", 
                             token=tokens[start_index], position=start_index)
    
    depth = 0
    for i in range(start_index, len(tokens)):
        if tokens[i] == "[":
            depth += 1
        elif tokens[i] == "]":
            depth -= 1
            if depth == 0:
                return i
    
    raise LumenSyntaxError("Unmatched opening bracket '['", 
                         token="[", position=start_index)

def find_matching_paren(tokens, start_index):
    """Find the matching ) for the ( at start_index with error handling"""
    if start_index >= len(tokens):
        raise LumenSyntaxError(f"Index {start_index} out of range", position=start_index)
    
    if tokens[start_index] != "(":
        raise LumenSyntaxError(f"Expected '(' but found '{tokens[start_index]}'", 
                             token=tokens[start_index], position=start_index)
    
    depth = 0
    for i in range(start_index, len(tokens)):
        if tokens[i] == "(":
            depth += 1
        elif tokens[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    
    raise LumenSyntaxError("Unmatched opening parenthesis '('", 
                         token="(", position=start_index)

def validate_identifier(name, position=None):
    """Validate that a string is a valid identifier"""
    if not name:
        raise LumenSyntaxError("Empty identifier", position=position)
    
    if not isinstance(name, str):
        raise LumenSyntaxError(f"Identifier must be string, got {type(name)}", position=position)
    
    # Basic identifier validation
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
        raise LumenSyntaxError(f"Invalid identifier '{name}': must start with letter or underscore", 
                             token=name, position=position)
    
    # Check for reserved Python keywords
    python_keywords = {
        'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
        'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
        'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
    }
    
    if name in python_keywords:
        raise LumenSyntaxError(f"'{name}' is a reserved Python keyword", token=name, position=position)

def parse_value_expression(tokens, start_index):
    """Parse a value expression (can be literal, variable, function call, or arithmetic expression)"""
    if start_index >= len(tokens):
        raise LumenSyntaxError("Expected value expression", position=start_index)
    
    # Find the end of the expression (until semicolon or specific terminators)
    end_index = start_index
    paren_depth = 0
    bracket_depth = 0
    
    while end_index < len(tokens):
        token = tokens[end_index]
        
        if token == '(':
            paren_depth += 1
        elif token == ')':
            paren_depth -= 1
        elif token == '[':
            bracket_depth += 1
        elif token == ']':
            bracket_depth -= 1
        elif token == ';' and paren_depth == 0 and bracket_depth == 0:
            break
        elif token in ['{', '}'] and paren_depth == 0 and bracket_depth == 0:
            break
        
        end_index += 1
    
    if end_index == start_index:
        raise LumenSyntaxError("Empty value expression", position=start_index)
    
    value_tokens = tokens[start_index:end_index]
    
    # Use expression parser to handle the tokens
    try:
        expression = expression_parser.parse_expression(value_tokens)
        return expression, end_index
    except Exception as e:
        # If expression parsing fails, treat as simple concatenation
        return ' '.join(value_tokens), end_index

def parse_label(tokens, start_index):
    """Parse a label definition: labelName:"""
    if start_index >= len(tokens):
        raise LumenSyntaxError("Unexpected end of tokens when parsing label")
    
    label_token = tokens[start_index]
    if not label_token.endswith(':'):
        raise LumenSyntaxError(f"Expected label with ':', got '{label_token}'")
    
    label_name = label_token[:-1]  # Remove the trailing colon
    validate_identifier(label_name, start_index)
    
    return ("label", label_name), start_index + 1

def parse_goto(tokens, start_index):
    """Parse a goto statement: goto labelName;"""
    if start_index >= len(tokens):
        raise LumenSyntaxError("Unexpected end of tokens when parsing goto")
    
    if tokens[start_index] != "goto":
        raise LumenSyntaxError(f"Expected 'goto', got '{tokens[start_index]}'")
    
    if start_index + 1 >= len(tokens):
        raise LumenSyntaxError("Expected label name after 'goto'")
    
    label_name = tokens[start_index + 1]
    validate_identifier(label_name, start_index + 1)
    
    # Check for semicolon
    if start_index + 2 >= len(tokens) or tokens[start_index + 2] != ";":
        raise LumenSyntaxError(f"Expected ';' after goto statement", 
                             position=start_index + 2)
    
    return ("goto", label_name), start_index + 3

def parse_array_literal(tokens, start_index):
    """Parse array literal: [element1, element2, element3]"""
    if start_index >= len(tokens) or tokens[start_index] != "[":
        raise LumenSyntaxError("Expected '[' at start of array literal")
    
    try:
        bracket_end = find_matching_bracket(tokens, start_index)
    except LumenSyntaxError as e:
        raise LumenSyntaxError(f"Error in array literal: {e}")
    
    # Parse array elements
    element_tokens = tokens[start_index + 1:bracket_end]
    elements = []
    
    if element_tokens:
        current_element = []
        for token in element_tokens:
            if token == ",":
                if current_element:
                    elem_expr = expression_parser.parse_expression(current_element)
                    elements.append(elem_expr)
                    current_element = []
            else:
                current_element.append(token)
        
        # Add the last element
        if current_element:
            elem_expr = expression_parser.parse_expression(current_element)
            elements.append(elem_expr)
    
    return elements, bracket_end + 1

def parse_dict_literal(tokens, start_index):
    """Parse dictionary literal: {"key1":"value1"; "key2":"value2";}"""
    if start_index >= len(tokens) or tokens[start_index] != "{":
        raise LumenSyntaxError("Expected '{' at start of dictionary literal")
    
    try:
        brace_end = find_matching_brace(tokens, start_index)
    except LumenSyntaxError as e:
        raise LumenSyntaxError(f"Error in dictionary literal: {e}")
    
    # Parse dictionary key-value pairs
    content_tokens = tokens[start_index + 1:brace_end]
    pairs = {}
    
    if content_tokens:
        current_key = None
        current_value = []
        i = 0
        
        while i < len(content_tokens):
            token = content_tokens[i]
            
            if token == ":":
                if current_key is None:
                    raise LumenSyntaxError(f"Unexpected ':' without key in dictionary", 
                                         token=token, position=start_index + 1 + i)
                
                i += 1
                while i < len(content_tokens) and content_tokens[i] != ";":
                    current_value.append(content_tokens[i])
                    i += 1
                
                if not current_value:
                    raise LumenSyntaxError(f"Missing value after ':' for key '{current_key}'", 
                                         token=token, position=start_index + 1 + i)
                
                # Parse value expression
                value = expression_parser.parse_expression(current_value)
                if i >= len(content_tokens) or content_tokens[i] != ";":
                    raise LumenSyntaxError(f"Expected ';' after dictionary value for key '{current_key}'", 
                                         token=content_tokens[i] if i < len(content_tokens) else "EOF",
                                         position=start_index + 1 + i)
                
                pairs[current_key] = value
                current_key = None
                current_value = []
                i += 1
                
            elif token == ";":
                raise LumenSyntaxError(f"Unexpected ';' without key:value pair", 
                                     token=token, position=start_index + 1 + i)
            else:
                if current_key is not None:
                    raise LumenSyntaxError(f"Expected ':' after key '{current_key}', found '{token}'", 
                                         token=token, position=start_index + 1 + i)
                
                current_key = token
                i += 1
        
        if current_key is not None:
            raise LumenSyntaxError(f"Incomplete key:value pair for key '{current_key}'", 
                                 token=current_key, position=start_index + 1 + len(content_tokens) - 1)
    
    return pairs, brace_end + 1

def parse_function_call(tokens, start_index):
    """Parse function call: functionName(arg1, arg2, ...)"""
    func_name = tokens[start_index]
    validate_identifier(func_name, start_index)
    
    if start_index + 1 >= len(tokens) or tokens[start_index + 1] != "(":
        raise LumenSyntaxError(f"Expected '(' after function name '{func_name}'")
    
    try:
        paren_end = find_matching_paren(tokens, start_index + 1)
    except LumenSyntaxError as e:
        raise LumenSyntaxError(f"Error in function call '{func_name}': {e}")
    
    # Parse arguments with expression support
    arg_tokens = tokens[start_index + 2:paren_end]
    args = []
    if arg_tokens:
        current_arg = []
        for token in arg_tokens:
            if token == ",":
                if current_arg:
                    arg_expr = expression_parser.parse_expression(current_arg)
                    args.append(arg_expr)
                    current_arg = []
            else:
                current_arg.append(token)
        if current_arg:
            arg_expr = expression_parser.parse_expression(current_arg)
            args.append(arg_expr)
    
    return ("call", func_name, args), paren_end + 1

def parse_tokens(tokens):
    """Enhanced parser with expression and function call support"""
    if not tokens:
        return []
    
    if not isinstance(tokens, list):
        raise LumenSyntaxError("Tokens must be a list")
    
    ast = []
    i = 0
    
    try:
        while i < len(tokens):
            if i >= len(tokens):
                break
                
            t = tokens[i]

            # Skip empty tokens
            if not t.strip():
                i += 1
                continue

            # Function call (identifier followed by parentheses)
            if (i + 1 < len(tokens) and tokens[i + 1] == "(" and 
                t not in ("if", "while", "fun", "print") and
                not t.startswith("print")):
                
                call_ast, next_i = parse_function_call(tokens, i)
                
                # Expect semicolon after function call
                if next_i < len(tokens) and tokens[next_i] == ";":
                    next_i += 1
                else:
                    raise LumenSyntaxError(f"Expected ';' after function call", position=next_i)
                
                ast.append(call_ast)
                i = next_i
                continue

            # Increment / Decrement (postfix: x++, x--)
            if i + 1 < len(tokens) and tokens[i+1] in ("++", "--"):
                validate_identifier(t, i)
                # Don't check if variable exists here - defer to compilation phase
                # This allows function parameters to work
                ast.append(("inc" if tokens[i+1] == "++" else "dec", t))
                i += 2
                continue

            elif t == "global":
                if i + 1 >= len(tokens):
                    raise LumenSyntaxError("Expected variable name after 'global'", position=i)

                # Get variable type and name: global int counter 5;
                if i + 3 >= len(tokens):
                    raise LumenSyntaxError("Incomplete global declaration", position=i)

                var_type = tokens[i+1]
                name = tokens[i+2]

                if var_type not in ("int", "str", "var", "ary", "dic", "bool"):
                    raise LumenSyntaxError(f"Invalid type '{var_type}' for global variable", 
                                         token=var_type, position=i+1)

                validate_identifier(name, i+2)

                # Parse the value expression
                value_expr, end_index = parse_value_expression(tokens, i + 3)

                if end_index >= len(tokens) or tokens[end_index] != ";":
                    raise LumenSyntaxError(f"Missing semicolon after global declaration '{name}'", 
                                         position=end_index)

                # Store global variable information
                symbol_table.global_vars[name] = (var_type, value_expr)
                symbol_table.declare_variable(name, var_type, value_expr, False)

                ast.append(("global", var_type, name, value_expr))
                i = end_index + 1

            elif t.endswith(':'):
                label_ast, next_i = parse_label(tokens, i)
                ast.append(label_ast)
                i = next_i
            
            # Goto statement
            elif t == "goto":
                goto_ast, next_i = parse_goto(tokens, i)
                ast.append(goto_ast)
                i = next_i

            # Variable declaration with enhanced expression support
            elif t in ("int", "str", "var", "static", "ary", "dic", "bool"):
                is_static = False
                var_type = t
                
                if t == "static":
                    is_static = True
                    i += 1
                    if i >= len(tokens):
                        raise LumenSyntaxError("Expected type after 'static'", position=i-1)
                    if tokens[i] not in ("int", "str", "var", "ary", "dic"):
                        raise LumenSyntaxError(f"Invalid type '{tokens[i]}' after 'static'", 
                                             token=tokens[i], position=i)
                    var_type = tokens[i]
                            
                if i + 1 >= len(tokens):
                    raise LumenSyntaxError(f"Expected variable name after '{var_type}'", position=i)
                
                name = tokens[i+1]
                validate_identifier(name, i+1)
                
                # Handle array declaration: ary name[1,2,3];
                if var_type == "ary" and i + 2 < len(tokens) and tokens[i+2] == "[":
                    elements, next_i = parse_array_literal(tokens, i + 2)

                    # Expect semicolon
                    if next_i >= len(tokens) or tokens[next_i] != ";":
                        raise LumenSyntaxError(f"Expected ';' after array declaration", position=next_i)

                    # Declare variable in symbol table
                    symbol_table.declare_variable(name, var_type, elements, is_static)

                    ast.append(("declare", var_type, name, elements, is_static))
                    i = next_i + 1
                
                # Handle dictionary declaration: dic name{"key":"value"};
                elif var_type == "dic" and i + 2 < len(tokens) and tokens[i+2] == "{":
                    pairs, next_i = parse_dict_literal(tokens, i + 2)
                    
                    # Expect semicolon AFTER the closing brace
                    if next_i >= len(tokens) or tokens[next_i] != ";":
                        raise LumenSyntaxError(f"Expected ';' after dictionary declaration", 
                                             position=next_i, token=tokens[next_i] if next_i < len(tokens) else "EOF")
                    
                    # Declare variable in symbol table
                    symbol_table.declare_variable(name, var_type, pairs, is_static)
                    
                    ast.append(("declare", var_type, name, pairs, is_static))
                    i = next_i + 1
                
                # Handle regular variable declaration with expression support
                else:
                    # Parse the value expression
                    value_expr, end_index = parse_value_expression(tokens, i + 2)

                    if end_index >= len(tokens) or tokens[end_index] != ";":
                        raise LumenSyntaxError(f"Missing semicolon after variable declaration '{name}'", 
                                             token=name, position=i+1)

                    if value_expr is None:
                        raise LumenSyntaxError(f"Variable '{name}' declared without value", 
                                             token=name, position=i+1)

                    # Declare variable in symbol table
                    symbol_table.declare_variable(name, var_type, value_expr, is_static)

                    ast.append(("declare", var_type, name, value_expr, is_static))
                    i = end_index + 1

            # Print statement
            elif t.startswith("print"):
                args = []
                if len(t) > 5:  # print has content attached
                    args.append(t[6:])
                
                i += 1
                while i < len(tokens) and tokens[i] != ";":
                    # Check for array/dictionary access: variable[ ... ]
                    if (i + 1 < len(tokens) and tokens[i+1] == "[" and
                        tokens[i] not in ('if', 'while', 'fun', 'print', 'return', 'int', 'str', 'var', 'static', 'ary', 'dic')):
                        
                        variable_name = tokens[i]
                        bracket_start = i + 1
                        
                        try:
                            bracket_end = find_matching_bracket(tokens, bracket_start)
                        except LumenSyntaxError as e:
                            raise LumenSyntaxError(f"Error in array/dict access: {e}")
                        
                        # Extract inner content and parse as expression
                        inner_tokens = tokens[bracket_start + 1:bracket_end]
                        inner_content = expression_parser.parse_expression(inner_tokens) if inner_tokens else ""
                        
                        # Create combined access expression
                        access_expr = f"{variable_name}[{inner_content}]"
                        args.append(access_expr)
                        
                        i = bracket_end + 1
                    else:
                        args.append(tokens[i])
                        i += 1
                
                if i >= len(tokens):
                    raise LumenSyntaxError("Missing semicolon after print statement", position=i-1)
                
                if not args:
                    raise LumenSyntaxError("Print statement cannot be empty")
                
                ast.append(("print", args))
                i += 1  # Move past the semicolon

            # If/While statement
            elif t in ("if", "while"):
                # Find condition inside parentheses
                paren_start = i + 1
                if paren_start >= len(tokens):
                    raise LumenSyntaxError(f"Expected '(' after '{t}'", token=t, position=i)

                if tokens[paren_start] != "(":
                    raise LumenSyntaxError(f"Expected '(' after '{t}', found '{tokens[paren_start]}'", 
                                         token=tokens[paren_start], position=paren_start)

                try:
                    paren_end = find_matching_paren(tokens, paren_start)
                except LumenSyntaxError as e:
                    raise LumenSyntaxError(f"Error in {t} condition: {e}")

                condition_tokens = tokens[paren_start+1:paren_end]
                if not condition_tokens:
                    raise LumenSyntaxError(f"Empty condition in {t} statement", position=paren_start)

                # Parse condition as expression
                condition = expression_parser.parse_expression(condition_tokens)

                # Parse body inside braces
                brace_start = paren_end + 1
                if brace_start >= len(tokens):
                    raise LumenSyntaxError(f"Expected '{{' after {t} condition", position=paren_end)

                if tokens[brace_start] != "{":
                    raise LumenSyntaxError(f"Expected '{{' after {t} condition, found '{tokens[brace_start]}'", 
                                         token=tokens[brace_start], position=brace_start)

                try:
                    body_end = find_matching_brace(tokens, brace_start)
                except LumenSyntaxError as e:
                    raise LumenSyntaxError(f"Error in {t} body: {e}")

                body_tokens = tokens[brace_start+1:body_end]

                # Enter new scope for control blocks
                symbol_table.enter_scope(f"{t}_{len(ast)}")
                try:
                    body_ast = parse_tokens(body_tokens)
                finally:
                    symbol_table.exit_scope()

                # Check for required semicolon after closing brace
                next_token_index = body_end + 1
                if next_token_index >= len(tokens) or tokens[next_token_index] != ";":
                    raise LumenSyntaxError(f"Expected ';' after {t} block", 
                                         position=body_end, token=tokens[body_end] if body_end < len(tokens) else "EOF")

                ast.append((t, condition, body_ast))
                i = next_token_index + 1  # Skip the semicolon

            # Function definition
            elif t == "fun":
                if i + 1 >= len(tokens):
                    raise LumenSyntaxError("Expected function name after 'fun'", position=i)

                name = tokens[i+1]
                validate_identifier(name, i+1)

                args_start = i + 2
                if args_start >= len(tokens) or tokens[args_start] != "(":
                    raise LumenSyntaxError(f"Expected '(' after function name '{name}'", 
                                         token=name, position=i+1)

                # Find closing parenthesis
                try:
                    args_end = find_matching_paren(tokens, args_start)
                except LumenSyntaxError as e:
                    raise LumenSyntaxError(f"Error in function '{name}' parameters: {e}")

                # Parse arguments
                arg_tokens = tokens[args_start+1:args_end]
                params = []
                if arg_tokens:
                    current_param = ""
                    for token in arg_tokens:
                        if token == ",":
                            if current_param.strip():
                                param_name = current_param.strip()
                                validate_identifier(param_name)
                                params.append(param_name)
                                current_param = ""
                        else:
                            current_param += token + " "

                    if current_param.strip():
                        param_name = current_param.strip()
                        validate_identifier(param_name)
                        params.append(param_name)

                # Parse function body
                body_start = args_end + 1
                if body_start >= len(tokens):
                    raise LumenSyntaxError(f"Expected '{{' after function '{name}' parameters", position=args_end)

                if tokens[body_start] != "{":
                    raise LumenSyntaxError(f"Expected '{{' after function '{name}' parameters, found '{tokens[body_start]}'", 
                                         token=tokens[body_start], position=body_start)

                try:
                    body_end = find_matching_brace(tokens, body_start)
                except LumenSyntaxError as e:
                    raise LumenSyntaxError(f"Error in function '{name}' body: {e}")

                body_tokens = tokens[body_start+1:body_end]

                # Enter function scope and declare parameters
                symbol_table.enter_scope(name)
                try:
                    # Declare parameters as variables in function scope
                    for param in params:
                        symbol_table.declare_variable(param, 'var', None)  # Parameters are untyped

                    body_ast = parse_tokens(body_tokens)

                    # Declare function in global scope
                    symbol_table.declare_function(name, params, body_ast)

                finally:
                    symbol_table.exit_scope()

                # Check for required semicolon after function definition
                next_token_index = body_end + 1
                if next_token_index >= len(tokens) or tokens[next_token_index] != ";":
                    raise LumenSyntaxError(f"Expected ';' after function definition", 
                                         position=body_end, token=tokens[body_end] if body_end < len(tokens) else "EOF")

                ast.append(("fun", name, params, body_ast))
                i = next_token_index + 1  # Skip the semicolon

            # Return statement with expression support
            elif t.startswith("return"):
                if symbol_table.current_scope() == 'global':
                    raise LumenSyntaxError("Return statement outside of function")

                if len(t) > 6:  # return has value attached
                    value = t[6:].strip()
                    if not value:
                        raise LumenSyntaxError("Invalid return statement format", token=t, position=i)

                    # Check for semicolon
                    if i + 1 >= len(tokens) or tokens[i+1] != ";":
                        raise LumenSyntaxError(f"Expected ';' after return statement", 
                                             position=i+1, token=tokens[i+1] if i+1 < len(tokens) else "EOF")

                    ast.append(("return", value))
                    i += 2  # Skip return and semicolon
                else:  # return followed by separate tokens
                    if i + 1 < len(tokens) and tokens[i+1] != ";":
                        # Parse return value as expression
                        value_expr, end_index = parse_value_expression(tokens, i + 1)

                        # Check for semicolon after value
                        if end_index >= len(tokens) or tokens[end_index] != ";":
                            raise LumenSyntaxError(f"Expected ';' after return value", 
                                                 position=end_index, token=tokens[end_index] if end_index < len(tokens) else "EOF")

                        ast.append(("return", value_expr))
                        i = end_index + 1  # Skip past semicolon
                    else:
                        # Check for semicolon
                        if i + 1 >= len(tokens) or tokens[i+1] != ";":
                            raise LumenSyntaxError(f"Expected ';' after return statement", 
                                                 position=i+1, token=tokens[i+1] if i+1 < len(tokens) else "EOF")

                        ast.append(("return", None))
                        i += 2  # Skip return and semicolon

            # Enhanced variable assignment with expression support
            elif (re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*', t) and 
                  i + 1 < len(tokens) and 
                  (tokens[i+1] in ("=", "[") or 
                   (tokens[i+1] not in ("++", "--", "(") and
                    not tokens[i+1].startswith(("int", "str", "var", "static", "if", "while", "fun", "return", "print"))))):

                name = t
                validate_identifier(name, i)

                # Handle bracket expressions in assignments: variable[index] = value;
                if i + 1 < len(tokens) and tokens[i+1] == "[":
                    try:
                        bracket_end = find_matching_bracket(tokens, i + 1)
                    except LumenSyntaxError as e:
                        raise LumenSyntaxError(f"Error in array/dict assignment: {e}")

                    # Extract index/key and parse as expression
                    inner_tokens = tokens[i + 2:bracket_end]
                    index_expr = expression_parser.parse_expression(inner_tokens) if inner_tokens else ""

                    # Check for assignment operator after bracket
                    if bracket_end + 1 >= len(tokens):
                        raise LumenSyntaxError(f"Expected '=' or ';' after bracket expression", 
                                             position=bracket_end + 1)

                    if bracket_end + 1 < len(tokens) and tokens[bracket_end + 1] == "=":
                        # This is assignment: variable[index] = value;
                        value_expr, end_index = parse_value_expression(tokens, bracket_end + 2)

                        if end_index >= len(tokens) or tokens[end_index] != ";":
                            raise LumenSyntaxError(f"Expected ';' after assignment", 
                                                 position=end_index)

                        access_expr = f"{name}[{index_expr}]"

                        # Validate assignment
                        symbol_table.assign_variable(name, value_expr)

                        ast.append(("assign", access_expr, value_expr))
                        i = end_index + 1  # skip past semicolon
                    else:
                        # This is just access: variable[index];
                        if bracket_end + 1 >= len(tokens) or tokens[bracket_end + 1] != ";":
                            raise LumenSyntaxError(f"Expected ';' after expression", 
                                                 position=bracket_end + 1)
                        
                        access_expr = f"{name}[{index_expr}]"
                        ast.append(("expr", access_expr))
                        i = bracket_end + 2  # skip past semicolon
                else:
                    # Handle regular assignment with expression support
                    if i + 1 < len(tokens) and tokens[i+1] == "=":
                        # Explicit assignment: var = expression;
                        value_expr, end_index = parse_value_expression(tokens, i + 2)
                        
                        if end_index >= len(tokens) or tokens[end_index] != ";":
                            raise LumenSyntaxError(f"Expected ';' after assignment to '{name}'", 
                                                 position=end_index)
                        
                        next_i = end_index + 1
                    else:
                        # Implicit assignment: var expression;
                        value_expr, end_index = parse_value_expression(tokens, i + 1)
                        
                        if end_index >= len(tokens) or tokens[end_index] != ";":
                            raise LumenSyntaxError(f"Expected ';' after assignment to '{name}'", 
                                                 position=end_index)
                        
                        next_i = end_index + 1

                    if not value_expr:
                        raise LumenSyntaxError(f"Empty value in assignment to '{name}'", 
                                             token=name, position=i)

                    # Validate assignment
                    symbol_table.assign_variable(name, value_expr)

                    ast.append(("assign", name, value_expr))
                    i = next_i

            # Handle unexpected tokens
            elif t == ";":
                # Empty statement, skip
                i += 1
            elif t in ("{", "}"):
                raise LumenSyntaxError(f"Unexpected brace '{t}'", token=t, position=i)
            elif t in ("(", ")"):
                raise LumenSyntaxError(f"Unexpected parenthesis '{t}'", token=t, position=i)
            else:
                # Try to provide helpful error messages for common mistakes
                if i + 1 < len(tokens) and tokens[i+1] == "(":
                    raise LumenSyntaxError(f"Unknown function '{t}' or missing 'fun' keyword", token=t, position=i)
                else:
                    raise LumenSyntaxError(f"Unexpected token '{t}'", token=t, position=i)

    except LumenSyntaxError:
        raise
    except LumenSemanticError:
        raise
    except Exception as e:
        raise LumenSyntaxError(f"Unexpected error during parsing: {e}")

    return ast

# ------------------ Entry ------------------
def parse_lumen_file(file_path):
    """Parse a Lumen file with comprehensive error handling"""
    try:
        # Reset symbol table for new file
        global symbol_table, expression_parser
        symbol_table = SymbolTable()
        expression_parser = ExpressionParser(symbol_table)
        
        tokens = tokenize_lumen_file(file_path)
        ast = parse_tokens(tokens)
        return ast
    except LumenParseError:
        raise
    except Exception as e:
        raise LumenParseError(f"Unexpected error parsing file '{file_path}': {e}")

def start():
    """Entry point for parsing with error handling"""
    try:
        if not config.file:
            raise LumenParseError("No file specified in config")
        
        filename = config.file
        
        if not filename:
            raise LumenParseError("Empty filename in config")
        
        lumen_ast = parse_lumen_file(filename)
        return lumen_ast
        
    except LumenParseError:
        raise
    except Exception as e:
        raise LumenParseError(f"Unexpected error in start(): {e}")

# ------------------ Test Function ------------------
def test_parser():
    """Test the enhanced parser with expression examples"""
    try:
        test_cases = [
            # Basic expressions
            ("int x 5 + 3; print x;", "Arithmetic in declaration"),
            ("int a 1; int b 2; int c a + b; print c;", "Variable arithmetic"),
            ("fun add(a, b) { return a + b; } int result add(1, 2); print result;", "Function with return"),
            
            # Your original example
            ("fun add(a, b) { int result a + b; return result; } int numa 1; int numb 1; int resultc add(numa, numb); print resultc;", "Original example"),
            
            # Complex expressions
            ("int x 2 * 3 + 4; print x;", "Precedence test"),
            ("int a 5; int b a * 2 + 3; print b;", "Mixed variables and literals"),
        ]
        
        for test_code, description in test_cases:
            print(f"\n--- Testing: {description} ---")
            print(f"Code: {test_code}")
            
            test_filename = "test_temp.lmn"
            
            try:
                # Write test file
                with open(test_filename, "w") as f:
                    f.write(test_code)
                
                # Set config
                config.file = test_filename
                
                # Parse
                ast = start()
                print(f"✓ Success: {ast}")
                
            except (LumenParseError, LumenSemanticError) as e:
                print(f"✗ Error: {e}")
            except Exception as e:
                print(f"✗ Unexpected Error: {e}")
            
            finally:
                # Cleanup
                try:
                    os.remove(test_filename)
                except:
                    pass
                    
    except Exception as e:
        print(f"Test Error: {e}")
        return None

if __name__ == "__main__":
    print("Running Enhanced Lumen AST Parser Tests...")
    test_parser()