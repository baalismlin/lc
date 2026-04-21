"""
AST Node Definitions for L Compiler

This module defines all Abstract Syntax Tree (AST) node classes used in the
parsing and code generation phases of the L compiler.

Each node represents a specific construct in the L language, such as
functions, statements, and expressions.
"""

import logging

logger = logging.getLogger(__name__)


class ASTNode:
    """
    Base class for all AST nodes.
    
    All specific AST node types inherit from this class, providing a common
    interface for the parser and code generator.
    """
    pass


class Program(ASTNode):
    """
    Represents the entire program, containing a list of function definitions.
    
    Attributes:
        functions: List of Function nodes representing all top-level functions
    """
    
    def __init__(self, functions):
        """
        Initialize a Program node.
        
        Args:
            functions: List of Function nodes
        """
        self.functions = functions
        logger.debug(f"Created Program node with {len(functions)} function(s)")
    
    def __repr__(self):
        return f"Program(functions={len(self.functions)})"


class Function(ASTNode):
    """
    Represents a function definition in the L language.
    
    Attributes:
        name: Function name (str)
        params: List of parameter names (list of str)
        body: List of statements in the function body
    """
    
    def __init__(self, name, params, body):
        """
        Initialize a Function node.
        
        Args:
            name: Function name
            params: List of parameter names
            body: List of statement nodes
        """
        self.name = name
        self.params = params
        self.body = body
        logger.debug(f"Created Function node: {name}({', '.join(params)})")
    
    def __repr__(self):
        return f"Function(name={self.name}, params={self.params})"


class LetStmt(ASTNode):
    """
    Represents a variable declaration statement.
    
    Attributes:
        name: Variable name (str)
        expr: Expression node representing the initial value
    """
    
    def __init__(self, name, expr):
        """
        Initialize a LetStmt node.
        
        Args:
            name: Variable name
            expr: Initial value expression
        """
        self.name = name
        self.expr = expr
        logger.debug(f"Created LetStmt node: let {name}")
    
    def __repr__(self):
        return f"LetStmt(name={self.name})"


class AssignStmt(ASTNode):
    """
    Represents a variable assignment statement.
    
    Attributes:
        name: Variable name (str)
        expr: Expression node representing the assigned value
    """
    
    def __init__(self, name, expr):
        """
        Initialize an AssignStmt node.
        
        Args:
            name: Variable name
            expr: Assigned value expression
        """
        self.name = name
        self.expr = expr
        logger.debug(f"Created AssignStmt node: {name} = ...")
    
    def __repr__(self):
        return f"AssignStmt(name={self.name})"


class IfStmt(ASTNode):
    """
    Represents an if-else conditional statement.
    
    Attributes:
        cond: Condition expression node
        then_body: List of statements for the then branch
        else_body: List of statements for the else branch (may be empty)
    """
    
    def __init__(self, cond, then_body, else_body):
        """
        Initialize an IfStmt node.
        
        Args:
            cond: Condition expression
            then_body: List of statements for then branch
            else_body: List of statements for else branch
        """
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body
        logger.debug(f"Created IfStmt node with else_body={len(else_body)>0}")
    
    def __repr__(self):
        return f"IfStmt(else_body={len(self.else_body) > 0})"


class WhileStmt(ASTNode):
    """
    Represents a while loop statement.
    
    Attributes:
        cond: Loop condition expression node
        body: List of statements in the loop body
    """
    
    def __init__(self, cond, body):
        """
        Initialize a WhileStmt node.
        
        Args:
            cond: Loop condition expression
            body: List of statements in loop body
        """
        self.cond = cond
        self.body = body
        logger.debug(f"Created WhileStmt node")
    
    def __repr__(self):
        return f"WhileStmt(body={len(self.body)} statements)"


class ReturnStmt(ASTNode):
    """
    Represents a return statement.
    
    Attributes:
        expr: Expression node representing the return value (may be None)
    """
    
    def __init__(self, expr):
        """
        Initialize a ReturnStmt node.
        
        Args:
            expr: Return value expression
        """
        self.expr = expr
        logger.debug(f"Created ReturnStmt node")
    
    def __repr__(self):
        return f"ReturnStmt"


class ExprStmt(ASTNode):
    """
    Represents an expression statement (an expression used as a statement).
    
    Attributes:
        expr: Expression node
    """
    
    def __init__(self, expr):
        """
        Initialize an ExprStmt node.
        
        Args:
            expr: Expression node
        """
        self.expr = expr
        logger.debug(f"Created ExprStmt node")
    
    def __repr__(self):
        return f"ExprStmt"


class CallExpr(ASTNode):
    """
    Represents a function call expression.
    
    Attributes:
        name: Function name (str)
        args: List of argument expression nodes
    """
    
    def __init__(self, name, args):
        """
        Initialize a CallExpr node.
        
        Args:
            name: Function name
            args: List of argument expressions
        """
        self.name = name
        self.args = args
        logger.debug(f"Created CallExpr node: {name}({len(args)} args)")
    
    def __repr__(self):
        return f"CallExpr(name={self.name}, args={len(self.args)})"


class BinaryExpr(ASTNode):
    """
    Represents a binary operation expression.
    
    Attributes:
        op: Operator string (e.g., '+', '-', '&&', '||', etc.)
        left: Left operand expression node
        right: Right operand expression node
    """
    
    def __init__(self, op, left, right):
        """
        Initialize a BinaryExpr node.
        
        Args:
            op: Binary operator
            left: Left operand
            right: Right operand
        """
        self.op = op
        self.left = left
        self.right = right
        logger.debug(f"Created BinaryExpr node: {op}")
    
    def __repr__(self):
        return f"BinaryExpr(op={self.op})"


class UnaryExpr(ASTNode):
    """
    Represents a unary operation expression.
    
    Attributes:
        op: Operator string (e.g., '!', '-')
        expr: Operand expression node
    """
    
    def __init__(self, op, expr):
        """
        Initialize a UnaryExpr node.
        
        Args:
            op: Unary operator
            expr: Operand expression
        """
        self.op = op
        self.expr = expr
        logger.debug(f"Created UnaryExpr node: {op}")
    
    def __repr__(self):
        return f"UnaryExpr(op={self.op})"


class VarExpr(ASTNode):
    """
    Represents a variable reference expression.
    
    Attributes:
        name: Variable name (str)
    """
    
    def __init__(self, name):
        """
        Initialize a VarExpr node.
        
        Args:
            name: Variable name
        """
        self.name = name
        logger.debug(f"Created VarExpr node: {name}")
    
    def __repr__(self):
        return f"VarExpr(name={self.name})"


class StringExpr(ASTNode):
    """
    Represents a string literal expression.
    
    Attributes:
        value: String value
    """
    
    def __init__(self, value):
        """
        Initialize a StringExpr node.
        
        Args:
            value: String literal value
        """
        self.value = value
        logger.debug(f"Created StringExpr node: '{value[:20]}...'")
    
    def __repr__(self):
        return f"StringExpr(len={len(self.value)})"


class IntExpr(ASTNode):
    """
    Represents an integer literal expression.
    
    Attributes:
        value: Integer value
    """
    
    def __init__(self, value):
        """
        Initialize an IntExpr node.
        
        Args:
            value: Integer literal value
        """
        self.value = value
        logger.debug(f"Created IntExpr node: {value}")
    
    def __repr__(self):
        return f"IntExpr(value={self.value})"


class BoolExpr(ASTNode):
    """
    Represents a boolean literal expression.
    
    Attributes:
        value: Boolean value (True or False)
    """
    
    def __init__(self, value):
        """
        Initialize a BoolExpr node.
        
        Args:
            value: Boolean literal value
        """
        self.value = value
        logger.debug(f"Created BoolExpr node: {value}")
    
    def __repr__(self):
        return f"BoolExpr(value={self.value})"


class NullExpr(ASTNode):
    """
    Represents a null literal expression.
    """
    
    def __init__(self):
        """Initialize a NullExpr node."""
        logger.debug(f"Created NullExpr node")
    
    def __repr__(self):
        return f"NullExpr"


class ListExpr(ASTNode):
    """
    Represents a list literal expression.
    
    Attributes:
        items: List of item expression nodes
    """
    
    def __init__(self, items):
        """
        Initialize a ListExpr node.
        
        Args:
            items: List of item expressions
        """
        self.items = items
        logger.debug(f"Created ListExpr node with {len(items)} items")
    
    def __repr__(self):
        return f"ListExpr(items={len(self.items)})"


class IndexExpr(ASTNode):
    """
    Represents an index expression (array/list indexing).
    
    Attributes:
        base: Base expression (the list being indexed)
        index: Index expression
    """
    
    def __init__(self, base, index):
        """
        Initialize an IndexExpr node.
        
        Args:
            base: Base expression
            index: Index expression
        """
        self.base = base
        self.index = index
        logger.debug(f"Created IndexExpr node")
    
    def __repr__(self):
        return f"IndexExpr"
