// Test with first part of complete_example

fn factorial(n) {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

fn is_even(n) {
    if n % 2 == 0 {
        return true;
    } else {
        return false;
    }
}

fn main() {
    let int_var = 42;
    let string_var = "Hello, L Language!";
    let bool_var = true;
    let array_var = [1, 2, 3, 4, 5];
    let null_var = null;
    
    print("=== Basic Data Types ===");
    print("Integer:");
    print(int_var);
    print("String:");
    print(string_var);
    print("Boolean:");
    print(bool_var);
    print("Array first element:");
    print(array_var[0]);
    
    let x = 10;
    let y = 20;
    let sum = x + y;
    print("Sum:");
    print(sum);
    
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
    
    let counter = 5;
    while counter > 0 {
        print("Counter:");
        print(counter);
        counter = counter - 1;
    }
    
    let fact = factorial(5);
    print("Factorial of 5:");
    print(fact);
    
    let even_check = is_even(4);
    print("Is 4 even?");
    print(even_check);
}
