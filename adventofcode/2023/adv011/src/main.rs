use std::fs::read_to_string;

fn main() {
    let mut sum = 0;

    for line in read_to_string("input.txt").unwrap().lines() {
        let string = line.to_string();
        let mut first = -1;
        let mut second = -1;

        for c in string.chars() {
            // test if c is a number
            if c.is_digit(10) {
                // if first is -1, set first to c
                if first == -1 {
                    first = c.to_digit(10).unwrap() as i32;
                    second = first;
                } else {
                    second = c.to_digit(10).unwrap() as i32;
                }
            }
        }

        if first > 0 {
            sum += first * 10 + second;
        }
    }
    println!("{}", sum);
}
