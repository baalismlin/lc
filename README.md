# L Language Self-Hosting Compiler

A self-hosting compiler for the L programming language. The project demonstrates bootstrapping by implementing a compiler in Python (lc1.py), then implementing the same compiler in L itself (lc2.l), and finally using lc2.py to compile itself.

## Project Structure

```
lc/
├── lc1.py              # First compiler written in Python
├── examples/           # Example L programs
│   ├── hello.l
│   ├── while.l
│   ├── file.l
│   ├── iftest.l
│   └── booltest.l
├── selfhost/           # Self-hosting compiler
│   └── lc2.l          # Compiler written in L
└── out/               # Generated Python files
```

## L Language Features

L is a minimal, dynamically-typed language designed for self-hosting.

### Types
- `int` - Integer values
- `string` - UTF-8 strings
- `bool` - Boolean values (true/false)
- `list` - Lists (created with `[]`, modified with `push`)
- `null` - Null value

### Syntax

#### Variables
```l
let name = "hello";
name = "world";  // Reassignment allowed
```

#### Functions
```l
fn add(a, b) {
    return a + b;
}

fn main() {
    print(add(1, 2));
}
```

#### Conditionals
```l
if x > 0 {
    print("positive");
} else {
    print("non-positive");
}
```

#### Loops
```l
while i < 10 {
    print(i);
    i = i + 1;
}
```

#### String Operations
- `len(s)` - String length
- `substr(s, start, count)` - Substring
- `char_at(s, i)` - Character at index
- `ord(s)` - Character to ASCII code
- `chr(n)` - ASCII code to character
- `str(x)` - Convert to string
- `int(x)` - Convert to integer
- `split_lines(s)` - Split by newlines
- `join(list, sep)` - Join with separator

#### File I/O
- `read_file(path)` - Read file contents
- `write_file(path, text)` - Write text to file

#### Console Output
- `print(x)` - Print to console

#### Lists
```l
let xs = [];
push(xs, 42);
print(xs[0]);  // 42
print(len(xs)); // 1
```

## Usage

### Compile an L program with lc1.py

```bash
python lc1.py examples/hello.l out/hello.py
python out/hello.py
```

### Bootstrap the self-hosting compiler

```bash
# Step 1: Compile lc2.l with lc1.py
python lc1.py selfhost/lc2.l out/lc2.py

# Step 2: Use lc2.py to compile itself
python out/lc2.py selfhost/lc2.l out/lc2_self.py

# Step 3: Compare the results
fc /b out/lc2.py out/lc2_self.py
```

If self-hosting is successful, lc2.py and lc2_self.py should be identical.

## Self-Hosting Status

- [x] lc1.py implemented (Python compiler)
- [x] lc2.l implemented (L compiler)
- [x] lc1.py can compile lc2.l
- [ ] lc2.py can compile lc2.l
- [ ] lc2.py == lc2_self.py (exact match)

## Development

### Running examples

```bash
python lc1.py examples/hello.l out/hello.py
python out/hello.py

python lc1.py examples/while.l out/while.py
python out/while.py
```

### Testing

The `examples/` directory contains test programs:
- `hello.l` - Basic print
- `while.l` - While loop
- `file.l` - File reading
- `iftest.l` - If statement
- `booltest.l` - Boolean expressions

## License

MIT License
