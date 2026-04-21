fn main() {
    let in_path = "selfhost/lc2.l";
    let out_path = "out/lc2_self.py";
    compile_file(in_path, out_path);
}

fn compile_file(in_path, out_path) {
    print("Reading: " + in_path);
    let src = read_file(in_path);
    print("Source length: " + str(len_func(src)));
    print("First 50 chars: " + substr(src, 0, 50));
    let tokens = lex(src);
    print("Token count: " + str(len_func(tokens)));
    let ast = parse_program(tokens);
    print("AST generated");
    let py = gen_program(ast);
    print("Python length: " + str(len_func(py)));
    write_file(out_path, py);
    print("Written: " + out_path);
}

fn lex(src) {
    let tokens = [];
    let i = 0;
    let len = 0;
    len = len_func(src);
    while i < len {
        let ch = char_at(src, i);
        
        if ch == " " || ch == "\t" || ch == "\r" || ch == "\n" {
            i = i + 1;
        } else if ch == "/" && char_at(src, i + 1) == "/" {
            while i < len && char_at(src, i) != "\n" {
                i = i + 1;
            }
        } else if is_digit(ch) {
            let start = i;
            while i < len && is_digit(char_at(src, i)) {
                i = i + 1;
            }
            let s = substr(src, start, i - start);
            push(tokens, ["INT", s]);
        } else if ch == "\"" || ch == "'" {
            let quote = ch;
            i = i + 1;
            let start = i;
            while i < len && char_at(src, i) != quote {
                if char_at(src, i) == "\\" {
                    i = i + 1;
                }
                i = i + 1;
            }
            let s = substr(src, start, i - start);
            push(tokens, ["STRING", s]);
            i = i + 1;
        } else if is_alpha(ch) || ch == "_" {
            let start = i;
            while i < len && (is_alpha_num(char_at(src, i)) || char_at(src, i) == "_") {
                i = i + 1;
            }
            let s = substr(src, start, i - start);
            let kw = is_keyword(s);
            if kw {
                push(tokens, [s, s]);
            } else {
                push(tokens, ["IDENT", s]);
            }
        } else if is_two_char_op(src, i) {
            let s = substr(src, i, 2);
            push(tokens, ["OP", s]);
            i = i + 2;
        } else if is_one_char_op(ch) {
            push(tokens, ["OP", ch]);
            i = i + 1;
        } else if is_symbol(ch) {
            push(tokens, ["SYMBOL", ch]);
            i = i + 1;
        } else {
            print("Unknown char: " + ch);
            i = i + 1;
        }
    }
    push(tokens, ["EOF", ""]);
    return tokens;
}

fn is_digit(ch) {
    return ch == "0" || ch == "1" || ch == "2" || ch == "3" || ch == "4" || ch == "5" || ch == "6" || ch == "7" || ch == "8" || ch == "9";
}

fn is_alpha(ch) {
    let c = ord_func(ch);
    return (c >= 65 && c <= 90) || (c >= 97 && c <= 122);
}

fn is_alpha_num(ch) {
    return is_digit(ch) || is_alpha(ch);
}

fn is_keyword(s) {
    return s == "fn" || s == "let" || s == "if" || s == "else" || s == "while" || s == "return" || s == "true" || s == "false" || s == "null";
}

fn is_two_char_op(src, i) {
    let s = substr(src, i, 2);
    return s == "==" || s == "!=" || s == "<=" || s == ">=" || s == "&&" || s == "||";
}

fn is_one_char_op(ch) {
    return ch == "=" || ch == "<" || ch == ">" || ch == "+" || ch == "-" || ch == "*" || ch == "/" || ch == "!";
}

fn is_symbol(ch) {
    return ch == "(" || ch == ")" || ch == "{" || ch == "}" || ch == "[" || ch == "]" || ch == "," || ch == ";";
}

fn char_at(s, i) {
    return s[i];
}

fn len_func(s) {
    return len(s);
}

fn parse_program(tokens) {
    let funcs = [];
    let pos = 0;
    while peek(tokens, pos) != "EOF" {
        let result = parse_function(tokens, pos);
        let node = get_item(result, 0);
        pos = get_item(result, 1);
        push(funcs, node);
    }
    return ["program", funcs];
}

fn peek(tokens, pos) {
    if pos < len_func(tokens) {
        let t = get_item(tokens, pos);
        return get_item(t, 0);
    }
    return "EOF";
}

fn peek_val(tokens, pos) {
    if pos < len_func(tokens) {
        let t = get_item(tokens, pos);
        return get_item(t, 1);
    }
    return "";
}

fn parse_function(tokens, pos) {
    expect(tokens, pos, "fn");
    pos = pos + 1;
    let name = peek_val(tokens, pos);
    pos = pos + 1;
    expect(tokens, pos, "SYMBOL");
    expect_val(tokens, pos, "(");
    pos = pos + 1;
    let params = [];
    if peek(tokens, pos) == "IDENT" {
        push(params, peek_val(tokens, pos));
        pos = pos + 1;
        while peek(tokens, pos) == "SYMBOL" && peek_val(tokens, pos) == "," {
            pos = pos + 1;
            push(params, peek_val(tokens, pos));
            pos = pos + 1;
        }
    }
    expect(tokens, pos, "SYMBOL");
    expect_val(tokens, pos, ")");
    pos = pos + 1;
    expect(tokens, pos, "SYMBOL");
    expect_val(tokens, pos, "{");
    pos = pos + 1;
    let result = parse_block(tokens, pos);
    let body = get_item(result, 0);
    pos = get_item(result, 1);
    expect(tokens, pos, "SYMBOL");
    expect_val(tokens, pos, "}");
    pos = pos + 1;
    return [["fn", name, params, body], pos];
}

fn parse_block(tokens, pos) {
    let stmts = [];
    let is_end = 0;
    is_end = peek(tokens, pos) == "SYMBOL" && peek_val(tokens, pos) == "}";
    while is_end == 0 {
        let result = parse_stmt(tokens, pos);
        push(stmts, get_item(result, 0));
        pos = get_item(result, 1);
        is_end = peek(tokens, pos) == "SYMBOL" && peek_val(tokens, pos) == "}";
    }
    return [stmts, pos];
}

fn parse_stmt(tokens, pos) {
    let t = peek(tokens, pos);
    
    if t == "LET" {
        pos = pos + 1;
        let name = peek_val(tokens, pos);
        pos = pos + 1;
        expect(tokens, pos, "OP");
        expect_val(tokens, pos, "=");
        pos = pos + 1;
        let result = parse_expr(tokens, pos);
        let expr = get_item(result, 0);
        pos = get_item(result, 1);
        expect(tokens, pos, "SYMBOL");
        expect_val(tokens, pos, ";");
        pos = pos + 1;
        return [["let", name, expr], pos];
    }
    
    if t == "IF" {
        pos = pos + 1;
        let result = parse_expr(tokens, pos);
        let cond = get_item(result, 0);
        pos = get_item(result, 1);
        expect(tokens, pos, "SYMBOL");
        expect_val(tokens, pos, "{");
        pos = pos + 1;
        let result2 = parse_block(tokens, pos);
        let then_body = get_item(result2, 0);
        pos = get_item(result2, 1);
        expect(tokens, pos, "SYMBOL");
        expect_val(tokens, pos, "}");
        pos = pos + 1;
        let else_body = [];
        if peek(tokens, pos) == "ELSE" {
            pos = pos + 1;
            expect(tokens, pos, "SYMBOL");
            expect_val(tokens, pos, "{");
            pos = pos + 1;
            let result3 = parse_block(tokens, pos);
            else_body = get_item(result3, 0);
            pos = get_item(result3, 1);
            expect(tokens, pos, "SYMBOL");
            expect_val(tokens, pos, "}");
            pos = pos + 1;
        }
        return [["if", cond, then_body, else_body], pos];
    }
    
    if t == "WHILE" {
        pos = pos + 1;
        let result = parse_expr(tokens, pos);
        let cond = get_item(result, 0);
        pos = get_item(result, 1);
        expect(tokens, pos, "SYMBOL");
        expect_val(tokens, pos, "{");
        pos = pos + 1;
        let result2 = parse_block(tokens, pos);
        let body = get_item(result2, 0);
        pos = get_item(result2, 1);
        expect(tokens, pos, "SYMBOL");
        expect_val(tokens, pos, "}");
        pos = pos + 1;
        return [["while", cond, body], pos];
    }
    
    if t == "RETURN" {
        pos = pos + 1;
        let result = parse_expr(tokens, pos);
        let expr = get_item(result, 0);
        pos = get_item(result, 1);
        expect(tokens, pos, "SYMBOL");
        expect_val(tokens, pos, ";");
        pos = pos + 1;
        return [["return", expr], pos];
    }
    
    if t == "IDENT" {
        if peek(tokens, pos + 1) == "OP" && peek_val(tokens, pos + 1) == "=" {
            let name = peek_val(tokens, pos);
            pos = pos + 2;
            let result = parse_expr(tokens, pos);
            let expr = get_item(result, 0);
            pos = get_item(result, 1);
            expect(tokens, pos, "SYMBOL");
            expect_val(tokens, pos, ";");
            pos = pos + 1;
            return [["assign", name, expr], pos];
        }
    }
    
    let result = parse_expr(tokens, pos);
    let expr = get_item(result, 0);
    pos = get_item(result, 1);
    expect(tokens, pos, "SYMBOL");
    expect_val(tokens, pos, ";");
    pos = pos + 1;
    return [["expr", expr], pos];
}

fn parse_expr(tokens, pos) {
    return parse_or(tokens, pos);
}

fn parse_or(tokens, pos) {
    let result = parse_and(tokens, pos);
    let left = get_item(result, 0);
    pos = get_item(result, 1);
    while peek(tokens, pos) == "OP" && peek_val(tokens, pos) == "||" {
        let op = peek_val(tokens, pos);
        pos = pos + 1;
        let result2 = parse_and(tokens, pos);
        let right = get_item(result2, 0);
        pos = get_item(result2, 1);
        left = ["binop", op, left, right];
    }
    return [left, pos];
}

fn parse_and(tokens, pos) {
    let result = parse_equality(tokens, pos);
    let left = get_item(result, 0);
    pos = get_item(result, 1);
    while peek(tokens, pos) == "OP" && peek_val(tokens, pos) == "&&" {
        let op = peek_val(tokens, pos);
        pos = pos + 1;
        let result2 = parse_equality(tokens, pos);
        let right = get_item(result2, 0);
        pos = get_item(result2, 1);
        left = ["binop", op, left, right];
    }
    return [left, pos];
}

fn parse_equality(tokens, pos) {
    let result = parse_comparison(tokens, pos);
    let left = get_item(result, 0);
    pos = get_item(result, 1);
    while peek(tokens, pos) == "OP" && (peek_val(tokens, pos) == "==" || peek_val(tokens, pos) == "!=") {
        let op = peek_val(tokens, pos);
        pos = pos + 1;
        let result2 = parse_comparison(tokens, pos);
        let right = get_item(result2, 0);
        pos = get_item(result2, 1);
        left = ["binop", op, left, right];
    }
    return [left, pos];
}

fn parse_comparison(tokens, pos) {
    let result = parse_additive(tokens, pos);
    let left = get_item(result, 0);
    pos = get_item(result, 1);
    while peek(tokens, pos) == "OP" && (peek_val(tokens, pos) == "<" || peek_val(tokens, pos) == "<=" || peek_val(tokens, pos) == ">" || peek_val(tokens, pos) == ">=") {
        let op = peek_val(tokens, pos);
        pos = pos + 1;
        let result2 = parse_additive(tokens, pos);
        let right = get_item(result2, 0);
        pos = get_item(result2, 1);
        left = ["binop", op, left, right];
    }
    return [left, pos];
}

fn parse_additive(tokens, pos) {
    let result = parse_multiplicative(tokens, pos);
    let left = get_item(result, 0);
    pos = get_item(result, 1);
    while peek(tokens, pos) == "OP" && (peek_val(tokens, pos) == "+" || peek_val(tokens, pos) == "-") {
        let op = peek_val(tokens, pos);
        pos = pos + 1;
        let result2 = parse_multiplicative(tokens, pos);
        let right = get_item(result2, 0);
        pos = get_item(result2, 1);
        left = ["binop", op, left, right];
    }
    return [left, pos];
}

fn parse_multiplicative(tokens, pos) {
    let result = parse_unary(tokens, pos);
    let left = get_item(result, 0);
    pos = get_item(result, 1);
    while peek(tokens, pos) == "OP" && (peek_val(tokens, pos) == "*" || peek_val(tokens, pos) == "/") {
        let op = peek_val(tokens, pos);
        pos = pos + 1;
        let result2 = parse_unary(tokens, pos);
        let right = get_item(result2, 0);
        pos = get_item(result2, 1);
        left = ["binop", op, left, right];
    }
    return [left, pos];
}

fn parse_unary(tokens, pos) {
    if peek(tokens, pos) == "OP" && (peek_val(tokens, pos) == "!" || peek_val(tokens, pos) == "-") {
        let op = peek_val(tokens, pos);
        pos = pos + 1;
        let result = parse_unary(tokens, pos);
        let expr = get_item(result, 0);
        pos = get_item(result, 1);
        return [["unary", op, expr], pos];
    }
    return parse_postfix(tokens, pos);
}

fn parse_postfix(tokens, pos) {
    let result = parse_primary(tokens, pos);
    let expr = get_item(result, 0);
    pos = get_item(result, 1);
    
    while true {
        if peek(tokens, pos) == "SYMBOL" && peek_val(tokens, pos) == "(" {
            pos = pos + 1;
            let args = [];
            if peek(tokens, pos) != "SYMBOL" || peek_val(tokens, pos) != ")" {
                let result2 = parse_expr(tokens, pos);
                push(args, get_item(result2, 0));
                pos = get_item(result2, 1);
                while peek(tokens, pos) == "SYMBOL" && peek_val(tokens, pos) == "," {
                    pos = pos + 1;
                    let result3 = parse_expr(tokens, pos);
                    push(args, get_item(result3, 0));
                    pos = get_item(result3, 1);
                }
            }
            expect(tokens, pos, "SYMBOL");
            expect_val(tokens, pos, ")");
            pos = pos + 1;
            let name = get_item(expr, 1);
            expr = ["call", name, args];
        } else if peek(tokens, pos) == "SYMBOL" && peek_val(tokens, pos) == "[" {
            pos = pos + 1;
            let result2 = parse_expr(tokens, pos);
            let index = get_item(result2, 0);
            pos = get_item(result2, 1);
            expect(tokens, pos, "SYMBOL");
            expect_val(tokens, pos, "]");
            pos = pos + 1;
            expr = ["index", expr, index];
        } else {
            break;
        }
    }
    
    return [expr, pos];
}

fn parse_primary(tokens, pos) {
    let t = peek(tokens, pos);
    
    if t == "INT" {
        let val = peek_val(tokens, pos);
        pos = pos + 1;
        return [["int", val], pos];
    }
    
    if t == "STRING" {
        let val = peek_val(tokens, pos);
        pos = pos + 1;
        return [["string", val], pos];
    }
    
    if t == "TRUE" {
        pos = pos + 1;
        return [["bool", "true"], pos];
    }
    
    if t == "FALSE" {
        pos = pos + 1;
        return [["bool", "false"], pos];
    }
    
    if t == "NULL" {
        pos = pos + 1;
        return [["null", ""], pos];
    }
    
    if t == "IDENT" {
        let val = peek_val(tokens, pos);
        pos = pos + 1;
        return [["var", val], pos];
    }
    
    if t == "SYMBOL" && peek_val(tokens, pos) == "(" {
        pos = pos + 1;
        let result = parse_expr(tokens, pos);
        let expr = get_item(result, 0);
        pos = get_item(result, 1);
        expect(tokens, pos, "SYMBOL");
        expect_val(tokens, pos, ")");
        pos = pos + 1;
        return [expr, pos];
    }
    
    if t == "SYMBOL" && peek_val(tokens, pos) == "[" {
        pos = pos + 1;
        let items = [];
        if peek(tokens, pos) != "SYMBOL" || peek_val(tokens, pos) != "]" {
            let result = parse_expr(tokens, pos);
            push(items, get_item(result, 0));
            pos = get_item(result, 1);
            while peek(tokens, pos) == "SYMBOL" && peek_val(tokens, pos) == "," {
                pos = pos + 1;
                let result2 = parse_expr(tokens, pos);
                push(items, get_item(result2, 0));
                pos = get_item(result2, 1);
            }
        }
        expect(tokens, pos, "SYMBOL");
        expect_val(tokens, pos, "]");
        pos = pos + 1;
        return [["list", items], pos];
    }
    
    return [["null", ""], pos];
}

fn expect(tokens, pos, type) {
    if peek(tokens, pos) != type {
        print("Expected " + type);
    }
}

fn expect_val(tokens, pos, val) {
    if peek_val(tokens, pos) != val {
        print("Expected " + val);
    }
}

fn get_item(lst, i) {
    return lst[i];
}

fn gen_program(ast) {
    let lines = [];
    emit_runtime(lines);
    push(lines, "");
    let funcs = get_item(ast, 1);
    let i = 0;
    while i < len_func(funcs) {
        gen_function(lines, get_item(funcs, i));
        i = i + 1;
    }
    let s = join(lines, "\n");
    return unescape_newlines(s);
}

fn emit_runtime(lines) {
    push(lines, "# Runtime functions");
    push(lines, "def read_file(path):");
    push(lines, "    with open(path, \"r\", encoding=\"utf-8\") as f:");
    push(lines, "        return f.read()");
    push(lines, "");
    push(lines, "def write_file(path, text):");
    push(lines, "    with open(path, \"w\", encoding=\"utf-8\") as f:");
    push(lines, "        f.write(text)");
    push(lines, "");
    push(lines, "def push(xs, v):");
    push(lines, "    xs.append(v)");
    push(lines, "");
    push(lines, "def char_at(s, i):");
    push(lines, "    try:");
    push(lines, "        return s[i]");
    push(lines, "    except IndexError:");
    push(lines, "        return \"\"");
    push(lines, "");
    push(lines, "def substr(s, start, count):");
    push(lines, "    return s[start:start+count]");
    push(lines, "");
    push(lines, "def split_lines(s):");
    push(lines, "    return s.splitlines()");
    push(lines, "");
    push(lines, "def join(xs, sep):");
    push(lines, "    return sep.join(xs)");
    push(lines, "");
    push(lines, "def ord_func(s):");
    push(lines, "    return ord(s)");
    push(lines, "");
    push(lines, "def chr_func(n):");
    push(lines, "    return chr(n)");
    push(lines, "");
    push(lines, "def unescape_newlines(s):");
    push(lines, "    return s.replace(\"\\\\n\", \"\\n\")");
}

fn gen_function(lines, func) {
    let name = get_item(func, 1);
    let params = get_item(func, 2);
    let body = get_item(func, 3);
    let ps = join(params, ", ");
    push(lines, "def " + name + "(" + ps + "):");
    let i = 0;
    while i < len_func(body) {
        gen_stmt(lines, get_item(body, i), 1);
        i = i + 1;
    }
    push(lines, "");
}

fn gen_stmt(lines, stmt, indent) {
    let kind = get_item(stmt, 0);
    
    if kind == "let" {
        let name = get_item(stmt, 1);
        let expr = gen_expr(get_item(stmt, 2));
        push(lines, indent_str(indent) + name + " = " + expr);
    } else if kind == "assign" {
        let name = get_item(stmt, 1);
        let expr = gen_expr(get_item(stmt, 2));
        push(lines, indent_str(indent) + name + " = " + expr);
    } else if kind == "if" {
        let cond = gen_expr(get_item(stmt, 1));
        let then_body = get_item(stmt, 2);
        let else_body = get_item(stmt, 3);
        push(lines, indent_str(indent) + "if " + cond + ":");
        let i = 0;
        while i < len_func(then_body) {
            gen_stmt(lines, get_item(then_body, i), indent + 1);
            i = i + 1;
        }
        if len_func(else_body) > 0 {
            push(lines, indent_str(indent) + "else:");
            let j = 0;
            while j < len_func(else_body) {
                gen_stmt(lines, get_item(else_body, j), indent + 1);
                j = j + 1;
            }
        }
    } else if kind == "while" {
        let cond = gen_expr(get_item(stmt, 1));
        let body = get_item(stmt, 2);
        push(lines, indent_str(indent) + "while " + cond + ":");
        let i = 0;
        while i < len_func(body) {
            gen_stmt(lines, get_item(body, i), indent + 1);
            i = i + 1;
        }
    } else if kind == "return" {
        let expr = gen_expr(get_item(stmt, 1));
        push(lines, indent_str(indent) + "return " + expr);
    } else if kind == "expr" {
        let expr = gen_expr(get_item(stmt, 1));
        push(lines, indent_str(indent) + expr);
    }
}

fn gen_expr(expr) {
    let kind = get_item(expr, 0);
    
    if kind == "var" {
        return get_item(expr, 1);
    } else if kind == "string" {
        return "\"" + escape_str(get_item(expr, 1)) + "\"";
    } else if kind == "int" {
        return get_item(expr, 1);
    } else if kind == "bool" {
        let val = get_item(expr, 1);
        if val == "true" {
            return "True";
        } else {
            return "False";
        }
    } else if kind == "null" {
        return "None";
    } else if kind == "binop" {
        let op = get_item(expr, 1);
        let left = gen_expr(get_item(expr, 2));
        let right = gen_expr(get_item(expr, 3));
        if op == "&&" {
            op = "and";
        } else if op == "||" {
            op = "or";
        }
        return "(" + left + " " + op + " " + right + ")";
    } else if kind == "unary" {
        let op = get_item(expr, 1);
        let e = gen_expr(get_item(expr, 2));
        if op == "!" {
            return "(not " + e + ")";
        } else {
            return op + e;
        }
    } else if kind == "call" {
        let name = get_item(expr, 1);
        let args = get_item(expr, 2);
        let arg_strs = [];
        let i = 0;
        while i < len_func(args) {
            push(arg_strs, gen_expr(get_item(args, i)));
            i = i + 1;
        }
        let arg_str = join(arg_strs, ", ");
        if name == "ord" {
            name = "ord_func";
        } else if name == "chr" {
            name = "chr_func";
        }
        return name + "(" + arg_str + ")";
    } else if kind == "list" {
        let items = get_item(expr, 1);
        let item_strs = [];
        let i = 0;
        while i < len_func(items) {
            push(item_strs, gen_expr(get_item(items, i)));
            i = i + 1;
        }
        return "[" + join(item_strs, ", ") + "]";
    } else if kind == "index" {
        let base = gen_expr(get_item(expr, 1));
        let idx = gen_expr(get_item(expr, 2));
        return base + "[" + idx + "]";
    }
    return "";
}

fn indent_str(n) {
    let s = "";
    let i = 0;
    while i < n {
        s = s + "    ";
        i = i + 1;
    }
    return s;
}

fn escape_str(s) {
    let result = "";
    let i = 0;
    let len = len_func(s);
    while i < len {
        let ch = char_at(s, i);
        if ch == "\\" {
            result = result + "\\\\";
        } else if ch == "\"" {
            result = result + "\\\"";
        } else if ch == "\n" {
            result = result + "\\n";
        } else if ch == "\t" {
            result = result + "\\t";
        } else {
            result = result + ch;
        }
        i = i + 1;
    }
    return result;
}
