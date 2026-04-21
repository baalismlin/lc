"""
Code Generator Module for L Compiler

This module provides the code generation functionality for the L compiler.
It converts an Abstract Syntax Tree (AST) into executable Python code.
"""

import logging
from .ast_nodes import *

logger = logging.getLogger(__name__)


class CodeGenerator:
    """
    Code generator that transforms L AST into Python source code.
    
    The code generator traverses the AST and emits Python code line by line,
    handling:
    - Function definitions
    - Variable declarations and assignments
    - Control flow (if, while)
    - Expressions (binary, unary, function calls, indexing)
    - Literals (integers, strings, booleans, null, lists)
    - Runtime library functions
    """
    
    def __init__(self):
        """Initialize the code generator."""
        self.indent = 0
        self.lines = []
        logger.info("CodeGenerator initialized")
    
    def emit(self, line=''):
        """
        Emit a line of code with proper indentation.
        
        Args:
            line: Code line to emit (empty string for blank line)
        """
        if line:
            self.lines.append('    ' * self.indent + line)
        else:
            self.lines.append('')
    
    def indent_push(self):
        """Increase indentation level by one."""
        self.indent += 1
    
    def indent_pop(self):
        """Decrease indentation level by one."""
        self.indent -= 1
    
    def escape_string(self, s):
        """
        Escape special characters in a string literal for Python.
        
        Args:
            s: String to escape
            
        Returns:
            Escaped string
        """
        return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
    
    def generate(self, program):
        """
        Generate Python code from a Program AST node.
        
        This is the main entry point for code generation. It emits:
        1. Runtime library functions
        2. All function definitions
        3. Main entry point
        
        Args:
            program: Program AST node
            
        Returns:
            Complete Python source code as a string
        """
        logger.info("Starting code generation")
        self.emit_runtime()
        self.emit()
        
        for func in program.functions:
            self.generate_function(func)
        
        self.emit()
        self.emit('if __name__ == "__main__":')
        self.indent_push()
        self.emit('main()')
        self.indent_pop()
        
        code = '\n'.join(self.lines)
        logger.info(f"Code generation complete: {len(self.lines)} lines generated")
        return code
    
    def emit_runtime(self):
        """Emit the runtime library functions required by L programs."""
        logger.debug("Emitting runtime library")
        self.emit('# Runtime functions')
        
        # Console output
        self.emit('def print(s):')
        self.indent_push()
        self.emit('print(s)')
        self.indent_pop()
        self.emit()
        
        # File I/O functions
        self.emit('def read_file(path):')
        self.indent_push()
        self.emit('with open(path, "r", encoding="utf-8") as f:')
        self.indent_push()
        self.emit('return f.read()')
        self.indent_pop()
        self.indent_pop()
        self.emit()
        
        self.emit('def write_file(path, text):')
        self.indent_push()
        self.emit('with open(path, "w", encoding="utf-8", newline="") as f:')
        self.indent_push()
        self.emit('f.write(text)')
        self.indent_pop()
        self.indent_pop()
        self.emit()
        
        # List operations
        self.emit('def push(xs, v):')
        self.indent_push()
        self.emit('xs.append(v)')
        self.indent_pop()
        self.emit()
        
        # String operations
        self.emit('def char_at(s, i):')
        self.indent_push()
        self.emit('if i < len(s):')
        self.indent_push()
        self.emit('return s[i]')
        self.indent_pop()
        self.emit('else:')
        self.indent_push()
        self.emit('return ""')
        self.indent_pop()
        self.indent_pop()
        self.emit()
        
        self.emit('def substr(s, start, count):')
        self.indent_push()
        self.emit('return s[start:start+count]')
        self.indent_pop()
        self.emit()
        
        self.emit('def split_lines(s):')
        self.indent_push()
        self.emit('return s.splitlines()')
        self.indent_pop()
        self.emit()
        
        self.emit('def join(xs, sep):')
        self.indent_push()
        self.emit('return sep.join(xs)')
        self.indent_pop()
        self.emit()
        
        # Character conversion functions
        self.emit('def ord_func(s):')
        self.indent_push()
        self.emit('return ord(s)')
        self.indent_pop()
        self.emit()
        
        self.emit('def chr_func(n):')
        self.indent_push()
        self.emit('return chr(n)')
        self.indent_pop()
        self.emit()
        
        # String utility
        self.emit('def unescape_newlines(s):')
        self.indent_push()
        self.emit('return s.replace("\\\\n", "\\n")')
        self.indent_pop()
        self.emit()
    
    def generate_function(self, func):
        """
        Generate Python code for a function definition.
        
        Args:
            func: Function AST node
        """
        logger.debug(f"Generating function: {func.name}")
        params = ', '.join(func.params)
        self.emit(f'def {func.name}({params}):')
        self.indent_push()
        for stmt in func.body:
            self.generate_stmt(stmt)
        self.indent_pop()
        self.emit()
    
    def generate_stmt(self, stmt):
        """
        Generate Python code for a statement.
        
        Args:
            stmt: Statement AST node
        """
        if isinstance(stmt, LetStmt):
            expr = self.generate_expr(stmt.expr)
            self.emit(f'{stmt.name} = {expr}')
            logger.debug(f"Generated let statement: {stmt.name}")
        
        elif isinstance(stmt, AssignStmt):
            expr = self.generate_expr(stmt.expr)
            self.emit(f'{stmt.name} = {expr}')
            logger.debug(f"Generated assignment: {stmt.name}")
        
        elif isinstance(stmt, IfStmt):
            cond = self.generate_expr(stmt.cond)
            self.emit(f'if {cond}:')
            self.indent_push()
            for s in stmt.then_body:
                self.generate_stmt(s)
            self.indent_pop()
            if stmt.else_body:
                self.emit('else:')
                self.indent_push()
                for s in stmt.else_body:
                    self.generate_stmt(s)
                self.indent_pop()
            logger.debug("Generated if statement")
        
        elif isinstance(stmt, WhileStmt):
            cond = self.generate_expr(stmt.cond)
            self.emit(f'while {cond}:')
            self.indent_push()
            for s in stmt.body:
                self.generate_stmt(s)
            self.indent_pop()
            logger.debug("Generated while statement")
        
        elif isinstance(stmt, ReturnStmt):
            expr = self.generate_expr(stmt.expr)
            self.emit(f'return {expr}')
            logger.debug("Generated return statement")
        
        elif isinstance(stmt, ExprStmt):
            expr = self.generate_expr(stmt.expr)
            self.emit(f'{expr}')
            logger.debug("Generated expression statement")
    
    def generate_expr(self, expr):
        """
        Generate Python code for an expression.
        
        Args:
            expr: Expression AST node
            
        Returns:
            Python expression string
        """
        if isinstance(expr, VarExpr):
            return expr.name
        
        elif isinstance(expr, StringExpr):
            return f'"{self.escape_string(expr.value)}"'
        
        elif isinstance(expr, IntExpr):
            return str(expr.value)
        
        elif isinstance(expr, BoolExpr):
            return 'True' if expr.value else 'False'
        
        elif isinstance(expr, NullExpr):
            return 'None'
        
        elif isinstance(expr, BinaryExpr):
            left = self.generate_expr(expr.left)
            right = self.generate_expr(expr.right)
            op = expr.op
            # Map L operators to Python
            if op == '&&':
                op = 'and'
            elif op == '||':
                op = 'or'
            return f'({left} {op} {right})'
        
        elif isinstance(expr, UnaryExpr):
            e = self.generate_expr(expr.expr)
            if expr.op == '!':
                return f'(not {e})'
            return f'{expr.op}{e}'
        
        elif isinstance(expr, CallExpr):
            args = ', '.join(self.generate_expr(a) for a in expr.args)
            # Handle built-in function name mapping
            name = expr.name
            if name == 'ord':
                name = 'ord_func'
            elif name == 'chr':
                name = 'chr_func'
            return f'{name}({args})'
        
        elif isinstance(expr, ListExpr):
            items = ', '.join(self.generate_expr(i) for i in expr.items)
            return f'[{items}]'
        
        elif isinstance(expr, IndexExpr):
            base = self.generate_expr(expr.base)
            index = self.generate_expr(expr.index)
            return f'{base}[{index}]'
        
        return str(expr)
