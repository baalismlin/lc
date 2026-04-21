#!/usr/bin/env python3
"""
L Compiler - First Version (lc1.py)
Compiles L language to Python
"""

import sys
import re

# ============== LEXER ==============

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    KEYWORDS = {
        'fn', 'let', 'if', 'else', 'while', 'return', 'true', 'false', 'null'
    }
    
    SYMBOLS = {
        '(', ')', '{', '}', '[', ']', ',', ';'
    }
    
    OPERATORS = {
        '=', '==', '!=', '<', '<=', '>', '>=', '+', '-', '*', '/', '&&', '||', '!'
    }
    
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
    
    def peek(self, n=0):
        if self.pos + n < len(self.source):
            return self.source[self.pos + n]
        return None
    
    def advance(self, n=1):
        for _ in range(n):
            if self.pos < len(self.source):
                ch = self.source[self.pos]
                self.pos += 1
                if ch == '\n':
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
    
    def skip_whitespace(self):
        while self.peek() and self.peek() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() and self.peek() != '\n':
                self.advance()
            return True
        return False
    
    def read_number(self):
        start = self.pos
        while self.peek() and self.peek().isdigit():
            self.advance()
        return int(self.source[start:self.pos])
    
    def read_string(self):
        quote = self.peek()
        self.advance()  # skip opening quote
        start = self.pos
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()
            self.advance()
        value = self.source[start:self.pos]
        self.advance()  # skip closing quote
        return value
    
    def read_identifier(self):
        start = self.pos
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            self.advance()
        return self.source[start:self.pos]
    
    def tokenize(self):
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self.skip_comment():
                continue
            
            ch = self.peek()
            
            # Number
            if ch.isdigit():
                value = self.read_number()
                self.tokens.append(Token('INT', value, self.line, self.col))
                continue
            
            # String
            if ch in '"\'':
                value = self.read_string()
                self.tokens.append(Token('STRING', value, self.line, self.col))
                continue
            
            # Identifier or keyword
            if ch.isalpha() or ch == '_':
                ident = self.read_identifier()
                if ident in self.KEYWORDS:
                    self.tokens.append(Token(ident.upper(), ident, self.line, self.col))
                else:
                    self.tokens.append(Token('IDENT', ident, self.line, self.col))
                continue
            
            # Multi-character operators
            two_char = self.peek() + (self.peek(1) or '')
            if two_char in self.OPERATORS:
                self.tokens.append(Token('OP', two_char, self.line, self.col))
                self.advance(2)
                continue
            
            # Single-character operators and symbols
            if ch in self.OPERATORS:
                self.tokens.append(Token('OP', ch, self.line, self.col))
                self.advance()
                continue
            
            if ch in self.SYMBOLS:
                self.tokens.append(Token('SYMBOL', ch, self.line, self.col))
                self.advance()
                continue
            
            raise SyntaxError(f"Unknown character '{ch}' at line {self.line}, col {self.col}")
        
        self.tokens.append(Token('EOF', '', self.line, self.col))
        return self.tokens

# ============== PARSER ==============

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, functions):
        self.functions = functions

class Function(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class LetStmt(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class AssignStmt(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class IfStmt(ASTNode):
    def __init__(self, cond, then_body, else_body):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

class WhileStmt(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class ReturnStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class ExprStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class CallExpr(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class BinaryExpr(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnaryExpr(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class VarExpr(ASTNode):
    def __init__(self, name):
        self.name = name

class StringExpr(ASTNode):
    def __init__(self, value):
        self.value = value

class IntExpr(ASTNode):
    def __init__(self, value):
        self.value = value

class BoolExpr(ASTNode):
    def __init__(self, value):
        self.value = value

class NullExpr(ASTNode):
    pass

class ListExpr(ASTNode):
    def __init__(self, items):
        self.items = items

class IndexExpr(ASTNode):
    def __init__(self, base, index):
        self.base = base
        self.index = index

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self, n=0):
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n]
        return None
    
    def advance(self):
        token = self.peek()
        if token:
            self.pos += 1
        return token
    
    def expect(self, type_, value=None):
        token = self.advance()
        if not token or token.type != type_:
            raise SyntaxError(f"Expected {type_}, got {token.type if token else 'EOF'}")
        if value is not None and token.value != value:
            raise SyntaxError(f"Expected {value}, got {token.value}")
        return token
    
    def parse(self):
        functions = []
        while self.peek() and self.peek().type != 'EOF':
            functions.append(self.parse_function())
        return Program(functions)
    
    def parse_function(self):
        self.expect('FN')
        name = self.expect('IDENT').value
        self.expect('SYMBOL', '(')
        params = []
        if self.peek() and self.peek().type == 'IDENT':
            params.append(self.expect('IDENT').value)
            while self.peek() and self.peek().type == 'SYMBOL' and self.peek().value == ',':
                self.advance()
                params.append(self.expect('IDENT').value)
        self.expect('SYMBOL', ')')
        self.expect('SYMBOL', '{')
        body = self.parse_block()
        self.expect('SYMBOL', '}')
        return Function(name, params, body)
    
    def parse_block(self):
        stmts = []
        while self.peek() and self.peek().type != 'SYMBOL' or self.peek().value != '}':
            stmts.append(self.parse_stmt())
        return stmts
    
    def parse_stmt(self):
        token = self.peek()
        
        if token.type == 'LET':
            self.advance()
            name = self.expect('IDENT').value
            self.expect('OP', '=')
            expr = self.parse_expr()
            self.expect('SYMBOL', ';')
            return LetStmt(name, expr)
        
        if token.type == 'IF':
            self.advance()
            cond = self.parse_expr()
            self.expect('SYMBOL', '{')
            then_body = self.parse_block()
            self.expect('SYMBOL', '}')
            else_body = []
            if self.peek() and self.peek().type == 'ELSE':
                self.advance()
                # Check for else if
                if self.peek() and self.peek().type == 'IF':
                    else_body = [self.parse_stmt()]
                else:
                    self.expect('SYMBOL', '{')
                    else_body = self.parse_block()
                    self.expect('SYMBOL', '}')
            return IfStmt(cond, then_body, else_body)
        
        if token.type == 'WHILE':
            self.advance()
            cond = self.parse_expr()
            self.expect('SYMBOL', '{')
            body = self.parse_block()
            self.expect('SYMBOL', '}')
            return WhileStmt(cond, body)
        
        if token.type == 'RETURN':
            self.advance()
            expr = self.parse_expr()
            self.expect('SYMBOL', ';')
            return ReturnStmt(expr)
        
        # Assignment or expression statement
        if token.type == 'IDENT':
            # Check if it's an assignment
            if self.peek(1) and self.peek(1).type == 'OP' and self.peek(1).value == '=':
                name = self.expect('IDENT').value
                self.expect('OP', '=')
                expr = self.parse_expr()
                self.expect('SYMBOL', ';')
                return AssignStmt(name, expr)
        
        # Expression statement
        expr = self.parse_expr()
        self.expect('SYMBOL', ';')
        return ExprStmt(expr)
    
    def parse_expr(self):
        return self.parse_or()
    
    def parse_or(self):
        left = self.parse_and()
        while self.peek() and self.peek().type == 'OP' and self.peek().value == '||':
            op = self.advance().value
            right = self.parse_and()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_and(self):
        left = self.parse_equality()
        while self.peek() and self.peek().type == 'OP' and self.peek().value == '&&':
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_equality(self):
        left = self.parse_comparison()
        while self.peek() and self.peek().type == 'OP' and self.peek().value in ('==', '!='):
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_comparison(self):
        left = self.parse_additive()
        while self.peek() and self.peek().type == 'OP' and self.peek().value in ('<', '<=', '>', '>='):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.peek() and self.peek().type == 'OP' and self.peek().value in ('+', '-'):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.peek() and self.peek().type == 'OP' and self.peek().value in ('*', '/'):
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_unary(self):
        if self.peek() and self.peek().type == 'OP' and self.peek().value in ('!', '-'):
            op = self.advance().value
            expr = self.parse_unary()
            return UnaryExpr(op, expr)
        return self.parse_postfix()
    
    def parse_postfix(self):
        expr = self.parse_primary()
        
        while True:
            # Function call
            if self.peek() and self.peek().type == 'SYMBOL' and self.peek().value == '(':
                self.advance()
                args = []
                if self.peek() and self.peek().type != 'SYMBOL' and self.peek().value != ')':
                    args.append(self.parse_expr())
                    while self.peek() and self.peek().type == 'SYMBOL' and self.peek().value == ',':
                        self.advance()
                        args.append(self.parse_expr())
                self.expect('SYMBOL', ')')
                expr = CallExpr(expr.name if isinstance(expr, VarExpr) else str(expr), args)
            
            # Index
            elif self.peek() and self.peek().type == 'SYMBOL' and self.peek().value == '[':
                self.advance()
                index = self.parse_expr()
                self.expect('SYMBOL', ']')
                expr = IndexExpr(expr, index)
            
            else:
                break
        
        return expr
    
    def parse_primary(self):
        token = self.peek()
        
        if token.type == 'INT':
            self.advance()
            return IntExpr(token.value)
        
        if token.type == 'STRING':
            self.advance()
            return StringExpr(token.value)
        
        if token.type == 'TRUE':
            self.advance()
            return BoolExpr(True)
        
        if token.type == 'FALSE':
            self.advance()
            return BoolExpr(False)
        
        if token.type == 'NULL':
            self.advance()
            return NullExpr()
        
        if token.type == 'IDENT':
            self.advance()
            return VarExpr(token.value)
        
        if token.type == 'SYMBOL' and token.value == '(':
            self.advance()
            expr = self.parse_expr()
            self.expect('SYMBOL', ')')
            return expr
        
        if token.type == 'SYMBOL' and token.value == '[':
            self.advance()
            items = []
            if not (self.peek() and self.peek().type == 'SYMBOL' and self.peek().value == ']'):
                items.append(self.parse_expr())
                while self.peek() and self.peek().type == 'SYMBOL' and self.peek().value == ',':
                    self.advance()
                    items.append(self.parse_expr())
            self.expect('SYMBOL', ']')
            return ListExpr(items)
        
        raise SyntaxError(f"Unexpected token: {token}")

# ============== CODE GENERATOR ==============

class CodeGenerator:
    def __init__(self):
        self.indent = 0
        self.lines = []
    
    def emit(self, line=''):
        if line:
            self.lines.append('    ' * self.indent + line)
        else:
            self.lines.append('')
    
    def indent_push(self):
        self.indent += 1
    
    def indent_pop(self):
        self.indent -= 1
    
    def escape_string(self, s):
        return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
    
    def generate(self, program):
        self.emit_runtime()
        self.emit()
        for func in program.functions:
            self.generate_function(func)
        self.emit()
        self.emit('if __name__ == "__main__":')
        self.indent_push()
        self.emit('main()')
        self.indent_pop()
        return '\n'.join(self.lines)
    
    def emit_runtime(self):
        self.emit('# Runtime functions')
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
        self.emit('def push(xs, v):')
        self.indent_push()
        self.emit('xs.append(v)')
        self.indent_pop()
        self.emit()
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
        self.emit('def unescape_newlines(s):')
        self.indent_push()
        self.emit('return s.replace("\\\\n", "\\n")')
        self.indent_pop()
        self.emit()
    
    def generate_function(self, func):
        params = ', '.join(func.params)
        self.emit(f'def {func.name}({params}):')
        self.indent_push()
        for stmt in func.body:
            self.generate_stmt(stmt)
        self.indent_pop()
        self.emit()
    
    def generate_stmt(self, stmt):
        if isinstance(stmt, LetStmt):
            expr = self.generate_expr(stmt.expr)
            self.emit(f'{stmt.name} = {expr}')
        
        elif isinstance(stmt, AssignStmt):
            expr = self.generate_expr(stmt.expr)
            self.emit(f'{stmt.name} = {expr}')
        
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
        
        elif isinstance(stmt, WhileStmt):
            cond = self.generate_expr(stmt.cond)
            self.emit(f'while {cond}:')
            self.indent_push()
            for s in stmt.body:
                self.generate_stmt(s)
            self.indent_pop()
        
        elif isinstance(stmt, ReturnStmt):
            expr = self.generate_expr(stmt.expr)
            self.emit(f'return {expr}')
        
        elif isinstance(stmt, ExprStmt):
            expr = self.generate_expr(stmt.expr)
            self.emit(f'{expr}')
    
    def generate_expr(self, expr):
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

# ============== MAIN DRIVER ==============

def compile_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    codegen = CodeGenerator()
    python_code = codegen.generate(ast)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    print(f'Compiled {input_path} -> {output_path}')

def main():
    if len(sys.argv) != 3:
        print('Usage: python lc1.py <input.l> <output.py>')
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    compile_file(input_path, output_path)

if __name__ == '__main__':
    main()
