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
}
