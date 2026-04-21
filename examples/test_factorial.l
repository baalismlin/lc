// Test factorial function

fn factorial(n) {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

fn main() {
    let fact = factorial(5);
    print(fact);
}
