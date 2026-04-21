"""
CLI Module for L Compiler

This module provides the command-line interface for the L compiler.
It handles file I/O and orchestrates the compilation pipeline.
"""

import sys
import logging
from pathlib import Path
from .lexer import Lexer
from .parser import Parser
from .codegen import CodeGenerator

logger = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    """
    Configure logging for the compiler.
    
    Args:
        level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.info("Logging configured")


def compile_file(input_path, output_path):
    """
    Compile an L source file to Python.
    
    This function orchestrates the entire compilation pipeline:
    1. Read the L source file
    2. Lexical analysis (tokenization)
    3. Parsing (AST construction)
    4. Code generation (Python output)
    5. Write the compiled Python file
    
    Args:
        input_path: Path to the input .l file
        output_path: Path to the output .py file
        
    Raises:
        FileNotFoundError: If input file does not exist
        SyntaxError: If there are syntax errors in the source
        IOError: If there are issues reading/writing files
    """
    logger.info(f"Starting compilation: {input_path} -> {output_path}")
    
    # Read input file
    input_file = Path(input_path)
    if not input_file.exists():
        error_msg = f"Input file not found: {input_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    logger.info(f"Reading input file: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    logger.info(f"Read {len(source)} characters from input file")
    
    # Lexical analysis
    logger.info("Phase 1: Lexical analysis")
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    logger.info(f"Tokenization complete: {len(tokens)} tokens generated")
    
    # Parsing
    logger.info("Phase 2: Parsing")
    parser = Parser(tokens)
    ast = parser.parse()
    logger.info(f"Parsing complete: AST with {len(ast.functions)} function(s)")
    
    # Code generation
    logger.info("Phase 3: Code generation")
    codegen = CodeGenerator()
    python_code = codegen.generate(ast)
    logger.info(f"Code generation complete: {len(python_code)} characters generated")
    
    # Write output file
    output_file = Path(output_path)
    logger.info(f"Writing output file: {output_path}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    logger.info(f"Compilation successful: {input_path} -> {output_path}")
    print(f'Compiled {input_path} -> {output_path}')


def main():
    """
    Main entry point for the CLI.
    
    Parses command-line arguments and invokes the compiler.
    
    Usage:
        python -m l_compiler.cli <input.l> <output.py>
    
    Exits with code 1 on error.
    """
    # Setup logging
    setup_logging()
    
    # Parse arguments
    if len(sys.argv) != 3:
        print('Usage: python -m l_compiler.cli <input.l> <output.py>')
        logger.error("Invalid number of arguments")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        compile_file(input_path, output_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        logger.error(f"Syntax error: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"I/O error: {e}")
        logger.error(f"I/O error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
