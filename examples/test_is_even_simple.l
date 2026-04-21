fn is_even(n) {
    if n < 2 {
        return true;
    } else {
        return false;
    }
}

fn main() {
    let even_check = is_even(4);
    print(even_check);
}
