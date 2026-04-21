// Complete example demonstrating all L language features

// Function to calculate factorial
fn factorial(n) {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

// Function to check if a number is even
fn is_even(n) {
    if n % 2 == 0 {
        return true;
    } else {
        return false;
    }
}

// Main function demonstrating all features
fn main() {
    // 1. Basic data types
    let int_var = 42;
    let string_var = "Hello, L Language!";
    let bool_var = true;
    let array_var = [1, 2, 3, 4, 5];
    let null_var = null;
    
    // Console output
    print("=== Basic Data Types ===");
    print("Integer:");
    print(int_var);
    print("String:");
    print(string_var);
    print("Boolean:");
    print(bool_var);
    print("Array first element:");
    print(array_var[0]);
    
    // 2. Variable declaration and assignment
    let x = 10;
    let y = 20;
    let sum = x + y;
    print("Sum:");
    print(sum);
    
    // 3. if, else if, and else
    print("\n=== Conditional Statements ===");
    let number = 15;
    
    if number < 0 {
        print("Negative");
    } else if number == 0 {
        print("Zero");
    } else if number < 10 {
        print("Small positive");
    } else if number < 20 {
        print("Medium positive");
    } else {
        print("Large positive");
    }
    
    // 4. while loop
    print("\n=== While Loop ===");
    let counter = 5;
    while counter > 0 {
        print("Counter:");
        print(counter);
        counter = counter - 1;
    }
    
    // 5. Function calls
    print("\n=== Function Calls ===");
    let fact = factorial(5);
    print("Factorial of 5:");
    print(fact);
    
    let even_check = is_even(4);
    print("Is 4 even?");
    print(even_check);
    
    // 6. String processing functions
    print("\n=== String Processing ===");
    let text = "Hello World";
    
    // Get character at index
    let first_char = char_at(text, 0);
    print("First character:");
    print(first_char);
    
    // Get substring
    let substring = substr(text, 0, 5);
    print("Substring (0-5):");
    print(substring);
    
    // Split lines
    let multiline = "Line1\nLine2\nLine3";
    let lines = split_lines(multiline);
    print("First line:");
    print(lines[0]);
    
    // Join array
    let parts = ["Hello", "World"];
    let joined = join(parts, " ");
    print("Joined:");
    print(joined);
    
    // Character conversion
    let char_code = ord_func("A");
    print("Ordinal of 'A':");
    print(char_code);
    
    let char_from_code = chr_func(65);
    print("Character from 65:");
    print(char_from_code);
    
    // 7. File I/O functions
    print("\n=== File I/O ===");
    let file_content = "This is a test file.";
    write_file("test_output.txt", file_content);
    print("Written to file");
    
    let read_content = read_file("test_output.txt");
    print("Read from file:");
    print(read_content);
    
    // 8. Array operations
    print("\n=== Array Operations ===");
    let numbers = [10, 20, 30];
    print("Original array:");
    print(numbers[0]);
    print(numbers[1]);
    print(numbers[2]);
    
    push(numbers, 40);
    print("After push:");
    print(numbers[0]);
    print(numbers[1]);
    print(numbers[2]);
    print(numbers[3]);
    
    // Array indexing
    let first = numbers[0];
    let last = numbers[3];
    print("First:");
    print(first);
    print("Last:");
    print(last);
    
    // 9. Logical operators
    print("\n=== Logical Operators ===");
    let a = true;
    let b = false;
    
    let and_result = a && b;
    let or_result = a || b;
    let not_result = !a;
    
    print("a && b:");
    print(and_result);
    print("a || b:");
    print(or_result);
    print("!a:");
    print(not_result);
    
    // 10. Comparison operators
    print("\n=== Comparison Operators ===");
    let p = 10;
    let q = 20;
    
    print("10 == 20:");
    print(p == q);
    print("10 != 20:");
    print(p != q);
    print("10 < 20:");
    print(p < q);
    print("10 <= 20:");
    print(p <= q);
    print("10 > 20:");
    print(p > q);
    print("10 >= 20:");
    print(p >= q);
    
    print("\n=== Complete ===");
}
