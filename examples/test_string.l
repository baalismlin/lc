// Test string processing functions

fn main() {
    let text = "Hello World";
    let first_char = char_at(text, 0);
    print(first_char);
    
    let substring = substr(text, 0, 5);
    print(substring);
}
