"""
Parser Module for L Compiler

This module provides the parsing functionality for the L compiler.
It converts a stream of tokens into an Abstract Syntax Tree (AST) using
recursive descent parsing.
"""

import logging
from .ast_nodes import *

logger = logging.getLogger(__name__)


class Parser:
    """
    Recursive descent parser for the L programming language.
    
    The parser builds an Abstract Syntax Tree (AST) from a stream of tokens
    produced by the lexer. It uses a top-down parsing approach with separate
    methods for each grammar rule.
    
    Grammar Overview:
    - Program: One or more function definitions
    - Function: 'fn' name '(' params? ')' '{' body '}'
    - Statements: let, if, while, return, assignment, expression
    - Expressions: Precedence levels from or to primary
    
    The parser tracks the current position in the token stream and provides
    methods for peeking at tokens, advancing, and expecting specific tokens.
    """
    
    def __init__(self, tokens):
        """
        Initialize the parser with a token stream.
        
        Args:
            tokens: List of Token objects from the lexer
        """
        self.tokens = tokens
        self.pos = 0
        logger.info(f"Parser initialized with {len(tokens)} tokens")
    
    def peek(self, n=0):
        """
        Peek at the token at current position + offset without advancing.
        
        Args:
            n: Offset from current position (default: 0)
            
        Returns:
            Token at position or None if out of bounds
        """
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n]
        return None
    
    def advance(self):
        """
        Advance to the next token and return the current token.
        
        Returns:
            Current token before advancing, or None if at EOF
        """
        token = self.peek()
        if token:
            self.pos += 1
        return token
    
    def expect(self, type_, value=None):
        """
        Expect a token of a specific type (and optionally value) at current position.
        
        Advances the position if the expectation is met.
        
        Args:
            type_: Expected token type
            value: Optional expected token value
            
        Returns:
            The expected token
            
        Raises:
            SyntaxError: If the expected token is not found
        """
        token = self.advance()
        if not token or token.type != type_:
            error_msg = f"Expected {type_}, got {token.type if token else 'EOF'}"
            logger.error(error_msg)
            raise SyntaxError(error_msg)
        if value is not None and token.value != value:
            error_msg = f"Expected {value}, got {token.value}"
            logger.error(error_msg)
            raise SyntaxError(error_msg)
        return token
    
    def parse(self):
        """
        Parse the entire token stream into a Program AST node.
        
        This is the main entry point for parsing. It repeatedly parses
        function definitions until EOF is reached.
        
        Returns:
            Program AST node containing all function definitions
        """
        logger.info("Starting parsing")
        functions = []
        while self.peek() and self.peek().type != 'EOF':
            func = self.parse_function()
            functions.append(func)
        program = Program(functions)
        logger.info(f"Parsing complete: {len(functions)} function(s) parsed")
        return program
    
    def parse_function(self):
        """
        Parse a function definition.
        
        Grammar: 'fn' IDENT '(' params? ')' '{' block '}'
        
        Returns:
            Function AST node
        """
        logger.debug("Parsing function")
        self.expect('FN')
        name = self.expect('IDENT').value
        self.expect('SYMBOL', '(')
        
        # Parse parameters
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
        
        logger.debug(f"Parsed function: {name} with {len(params)} parameter(s)")
        return Function(name, params, body)
    
    def parse_block(self):
        """
        Parse a block of statements.
        
        A block is a sequence of statements ending with a closing brace.
        
        Returns:
            List of statement AST nodes
        """
        stmts = []
        while self.peek() and not (self.peek().type == 'SYMBOL' and self.peek().value == '}'):
            stmt = self.parse_stmt()
            stmts.append(stmt)
        logger.debug(f"Parsed block with {len(stmts)} statement(s)")
        return stmts
    
    def parse_stmt(self):
        """
        Parse a single statement.
        
        Handles: let, if, while, return, assignment, expression statements
        
        Returns:
            Statement AST node
            
        Raises:
            SyntaxError: If an unexpected token is encountered
        """
        token = self.peek()
        
        # let statement: let name = expr;
        if token.type == 'LET':
            logger.debug("Parsing let statement")
            self.advance()
            name = self.expect('IDENT').value
            self.expect('OP', '=')
            expr = self.parse_expr()
            self.expect('SYMBOL', ';')
            return LetStmt(name, expr)
        
        # if statement: if cond { then } [else { else }]
        if token.type == 'IF':
            logger.debug("Parsing if statement")
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
        
        # while statement: while cond { body }
        if token.type == 'WHILE':
            logger.debug("Parsing while statement")
            self.advance()
            cond = self.parse_expr()
            self.expect('SYMBOL', '{')
            body = self.parse_block()
            self.expect('SYMBOL', '}')
            return WhileStmt(cond, body)
        
        # return statement: return expr;
        if token.type == 'RETURN':
            logger.debug("Parsing return statement")
            self.advance()
            expr = self.parse_expr()
            self.expect('SYMBOL', ';')
            return ReturnStmt(expr)
        
        # Assignment statement: name = expr;
        if token.type == 'IDENT':
            if self.peek(1) and self.peek(1).type == 'OP' and self.peek(1).value == '=':
                logger.debug("Parsing assignment statement")
                name = self.expect('IDENT').value
                self.expect('OP', '=')
                expr = self.parse_expr()
                self.expect('SYMBOL', ';')
                return AssignStmt(name, expr)
        
        # Expression statement: expr;
        logger.debug("Parsing expression statement")
        expr = self.parse_expr()
        self.expect('SYMBOL', ';')
        return ExprStmt(expr)
    
    def parse_expr(self):
        """
        Parse an expression (starting at lowest precedence: OR).
        
        Returns:
            Expression AST node
        """
        return self.parse_or()
    
    def parse_or(self):
        """
        Parse OR expressions (|| operator).
        
        Precedence level 1 (lowest).
        
        Returns:
            Expression AST node
        """
        left = self.parse_and()
        while self.peek() and self.peek().type == 'OP' and self.peek().value == '||':
            op = self.advance().value
            right = self.parse_and()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_and(self):
        """
        Parse AND expressions (&& operator).
        
        Precedence level 2.
        
        Returns:
            Expression AST node
        """
        left = self.parse_equality()
        while self.peek() and self.peek().type == 'OP' and self.peek().value == '&&':
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_equality(self):
        """
        Parse equality expressions (==, != operators).
        
        Precedence level 3.
        
        Returns:
            Expression AST node
        """
        left = self.parse_comparison()
        while self.peek() and self.peek().type == 'OP' and self.peek().value in ('==', '!='):
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_comparison(self):
        """
        Parse comparison expressions (<, <=, >, >= operators).
        
        Precedence level 4.
        
        Returns:
            Expression AST node
        """
        left = self.parse_additive()
        while self.peek() and self.peek().type == 'OP' and self.peek().value in ('<', '<=', '>', '>='):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_additive(self):
        """
        Parse additive expressions (+, - operators).
        
        Precedence level 5.
        
        Returns:
            Expression AST node
        """
        left = self.parse_multiplicative()
        while self.peek() and self.peek().type == 'OP' and self.peek().value in ('+', '-'):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_multiplicative(self):
        """
        Parse multiplicative expressions (*, /, % operators).
        
        Precedence level 6.
        
        Returns:
            Expression AST node
        """
        left = self.parse_unary()
        while self.peek() and self.peek().type == 'OP' and self.peek().value in ('*', '/', '%'):
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryExpr(op, left, right)
        return left
    
    def parse_unary(self):
        """
        Parse unary expressions (!, - operators).
        
        Precedence level 7.
        
        Returns:
            Expression AST node
        """
        if self.peek() and self.peek().type == 'OP' and self.peek().value in ('!', '-'):
            op = self.advance().value
            expr = self.parse_unary()
            return UnaryExpr(op, expr)
        return self.parse_postfix()
    
    def parse_postfix(self):
        """
        Parse postfix expressions (function calls, indexing).
        
        Precedence level 8.
        
        Returns:
            Expression AST node
        """
        expr = self.parse_primary()
        
        while True:
            # Function call: expr(args)
            if self.peek() and self.peek().type == 'SYMBOL' and self.peek().value == '(':
                self.advance()
                args = []
                if self.peek() and not (self.peek().type == 'SYMBOL' and self.peek().value == ')'):
                    args.append(self.parse_expr())
                    while self.peek() and self.peek().type == 'SYMBOL' and self.peek().value == ',':
                        self.advance()
                        args.append(self.parse_expr())
                self.expect('SYMBOL', ')')
                expr = CallExpr(expr.name if isinstance(expr, VarExpr) else str(expr), args)
            
            # Indexing: expr[index]
            elif self.peek() and self.peek().type == 'SYMBOL' and self.peek().value == '[':
                self.advance()
                index = self.parse_expr()
                self.expect('SYMBOL', ']')
                expr = IndexExpr(expr, index)
            
            else:
                break
        
        return expr
    
    def parse_primary(self):
        """
        Parse primary expressions (literals, identifiers, parenthesized expressions, lists).
        
        Precedence level 9 (highest).
        
        Returns:
            Expression AST node
            
        Raises:
            SyntaxError: If an unexpected token is encountered
        """
        token = self.peek()
        
        # Integer literal
        if token.type == 'INT':
            self.advance()
            return IntExpr(token.value)
        
        # String literal
        if token.type == 'STRING':
            self.advance()
            return StringExpr(token.value)
        
        # Boolean literal: true
        if token.type == 'TRUE':
            self.advance()
            return BoolExpr(True)
        
        # Boolean literal: false
        if token.type == 'FALSE':
            self.advance()
            return BoolExpr(False)
        
        # Null literal
        if token.type == 'NULL':
            self.advance()
            return NullExpr()
        
        # Identifier (variable reference)
        if token.type == 'IDENT':
            self.advance()
            return VarExpr(token.value)
        
        # Parenthesized expression: (expr)
        if token.type == 'SYMBOL' and token.value == '(':
            self.advance()
            expr = self.parse_expr()
            self.expect('SYMBOL', ')')
            return expr
        
        # List literal: [item1, item2, ...]
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
        
        error_msg = f"Unexpected token: {token}"
        logger.error(error_msg)
        raise SyntaxError(error_msg)
