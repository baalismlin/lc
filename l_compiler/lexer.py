"""
Lexer Module for L Compiler

This module provides the lexical analysis (tokenization) functionality for the L compiler.
It converts raw source code strings into a stream of tokens for the parser.
"""

import logging

logger = logging.getLogger(__name__)


class Token:
    """
    Represents a single token in the source code.
    
    A token is the smallest unit of meaning in the source code, containing
    information about its type, value, and source location.
    
    Attributes:
        type: Token type string (e.g., 'INT', 'IDENT', 'OP', 'FN', etc.)
        value: The actual value of the token (e.g., variable name, number)
        line: Line number where the token appears (1-indexed)
        col: Column number where the token appears (1-indexed)
    """
    
    def __init__(self, type_, value, line, col):
        """
        Initialize a Token.
        
        Args:
            type_: Token type identifier
            value: Token value
            line: Source line number (1-indexed)
            col: Source column number (1-indexed)
        """
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        """Return string representation of the token."""
        return f"Token({self.type}, {repr(self.value)})"
    
    def __eq__(self, other):
        """Check token equality for testing purposes."""
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and 
                self.value == other.value)


class Lexer:
    """
    Lexical analyzer for the L programming language.
    
    The lexer converts source code strings into a sequence of tokens by:
    1. Scanning through the source character by character
    2. Identifying keywords, identifiers, literals, operators, and symbols
    3. Tracking line and column numbers for error reporting
    4. Skipping whitespace and comments
    
    Supported token types:
    - Keywords: fn, let, if, else, while, return, true, false, null
    - Operators: =, ==, !=, <, <=, >, >=, +, -, *, /, &&, ||, !
    - Symbols: (, ), {, }, [, ], ,, ;
    - Literals: integers, strings
    - Identifiers: variable and function names
    """
    
    KEYWORDS = {
        'fn', 'let', 'if', 'else', 'while', 'return', 'true', 'false', 'null'
    }
    
    SYMBOLS = {
        '(', ')', '{', '}', '[', ']', ',', ';'
    }
    
    OPERATORS = {
        '=', '==', '!=', '<', '<=', '>', '>=', '+', '-', '*', '/', '%', '&&', '||', '!'
    }
    
    def __init__(self, source):
        """
        Initialize the lexer with source code.
        
        Args:
            source: Source code string to tokenize
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
        logger.info(f"Lexer initialized with {len(source)} characters")
    
    def peek(self, n=0):
        """
        Peek at the character at current position + offset without advancing.
        
        Args:
            n: Offset from current position (default: 0)
            
        Returns:
            Character at position or None if out of bounds
        """
        if self.pos + n < len(self.source):
            return self.source[self.pos + n]
        return None
    
    def advance(self, n=1):
        """
        Advance the position by n characters, tracking line and column numbers.
        
        Args:
            n: Number of characters to advance (default: 1)
        """
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
        """Skip whitespace characters (space, tab, carriage return, newline)."""
        while self.peek() and self.peek() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        """
        Skip single-line comments (// to end of line).
        
        Returns:
            True if a comment was skipped, False otherwise
        """
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() and self.peek() != '\n':
                self.advance()
            logger.debug(f"Skipped comment at line {self.line}")
            return True
        return False
    
    def read_number(self):
        """
        Read a sequence of digits as an integer literal.
        
        Returns:
            Integer value of the number
        """
        start = self.pos
        while self.peek() and self.peek().isdigit():
            self.advance()
        value = int(self.source[start:self.pos])
        logger.debug(f"Read number: {value}")
        return value
    
    def read_string(self):
        """
        Read a string literal (enclosed in single or double quotes).
        
        Handles escape sequences (e.g., \\n, \\", etc.)
        
        Returns:
            String value without the enclosing quotes
        """
        quote = self.peek()
        self.advance()  # skip opening quote
        start = self.pos
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()  # skip escape character
            self.advance()
        value = self.source[start:self.pos]
        self.advance()  # skip closing quote
        logger.debug(f"Read string: '{value[:30]}...'")
        return value
    
    def read_identifier(self):
        """
        Read an identifier (alphanumeric characters and underscores).
        
        Returns:
            Identifier string
        """
        start = self.pos
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            self.advance()
        ident = self.source[start:self.pos]
        logger.debug(f"Read identifier: {ident}")
        return ident
    
    def tokenize(self):
        """
        Convert the entire source code into a list of tokens.
        
        This is the main entry point for the lexer. It processes the source
        code character by character, identifying and creating tokens until
        the end of the source is reached.
        
        Returns:
            List of Token objects, ending with an EOF token
            
        Raises:
            SyntaxError: If an unknown character is encountered
        """
        logger.info("Starting tokenization")
        token_count = 0
        
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self.skip_comment():
                continue
            
            ch = self.peek()
            
            # Number literal
            if ch.isdigit():
                value = self.read_number()
                self.tokens.append(Token('INT', value, self.line, self.col))
                token_count += 1
                continue
            
            # String literal
            if ch in '"\'':
                value = self.read_string()
                self.tokens.append(Token('STRING', value, self.line, self.col))
                token_count += 1
                continue
            
            # Identifier or keyword
            if ch.isalpha() or ch == '_':
                ident = self.read_identifier()
                if ident in self.KEYWORDS:
                    self.tokens.append(Token(ident.upper(), ident, self.line, self.col))
                    logger.debug(f"Keyword token: {ident.upper()}")
                else:
                    self.tokens.append(Token('IDENT', ident, self.line, self.col))
                token_count += 1
                continue
            
            # Multi-character operators (==, !=, <=, >=, &&, ||)
            two_char = self.peek() + (self.peek(1) or '')
            if two_char in self.OPERATORS:
                self.tokens.append(Token('OP', two_char, self.line, self.col))
                self.advance(2)
                token_count += 1
                logger.debug(f"Operator token: {two_char}")
                continue
            
            # Single-character operators and symbols
            if ch in self.OPERATORS:
                self.tokens.append(Token('OP', ch, self.line, self.col))
                self.advance()
                token_count += 1
                logger.debug(f"Operator token: {ch}")
                continue
            
            if ch in self.SYMBOLS:
                self.tokens.append(Token('SYMBOL', ch, self.line, self.col))
                self.advance()
                token_count += 1
                logger.debug(f"Symbol token: {ch}")
                continue
            
            error_msg = f"Unknown character '{ch}' at line {self.line}, col {self.col}"
            logger.error(error_msg)
            raise SyntaxError(error_msg)
        
        # Add EOF token
        self.tokens.append(Token('EOF', '', self.line, self.col))
        logger.info(f"Tokenization complete: {token_count + 1} tokens generated")
        return self.tokens
