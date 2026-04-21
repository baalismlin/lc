"""
L Compiler - A compiler for the L language to Python

This package provides a complete compiler implementation for the L programming language,
compiling L source code to executable Python code.

Components:
- Lexer: Tokenizes L source code
- Parser: Builds an Abstract Syntax Tree (AST) from tokens
- Code Generator: Transforms AST into Python code
"""

__version__ = "1.0.0"
__author__ = "L Compiler Team"

from .lexer import Lexer, Token
from .parser import Parser
from .codegen import CodeGenerator
from .ast_nodes import *
from .cli import compile_file

__all__ = [
    "Lexer",
    "Token",
    "Parser",
    "CodeGenerator",
    "compile_file",
]
