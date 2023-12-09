use std::fs::read_to_string;

struct Counter {
    counter: [Number; 20],
}

struct Number {
    number_repr: String,
    value: i32,
    current_index: usize,
}

impl Number {
    fn new(number_repr: String, value: i32) -> Number {
        Number {
            number_repr,
            value,
            current_index: 0,
        }
    }

    fn count_char(&mut self, c: u8) -> Option<i32> {
        if self.number_repr.as_bytes()[self.current_index] == c {
            self.current_index += 1;
            if self.number_repr.len() == self.current_index {
                self.current_index = 0;
                return Some(self.value);
            }
            return None;
        }

        if self.number_repr.as_bytes()[0] == c {
            self.current_index = 1;
        } else {
            self.current_index = 0;
        }

        return None;
    }
}

impl Counter {
    fn new() -> Counter {
        Counter {
            counter: [
                Number::new("0".to_string(), 0),
                Number::new("1".to_string(), 1),
                Number::new("2".to_string(), 2),
                Number::new("3".to_string(), 3),
                Number::new("4".to_string(), 4),
                Number::new("5".to_string(), 5),
                Number::new("6".to_string(), 6),
                Number::new("7".to_string(), 7),
                Number::new("8".to_string(), 8),
                Number::new("9".to_string(), 9),
                Number::new("zero".to_string(), 0),
                Number::new("one".to_string(), 1),
                Number::new("two".to_string(), 2),
                Number::new("three".to_string(), 3),
                Number::new("four".to_string(), 4),
                Number::new("five".to_string(), 5),
                Number::new("six".to_string(), 6),
                Number::new("seven".to_string(), 7),
                Number::new("eight".to_string(), 8),
                Number::new("nine".to_string(), 9),
            ],
        }
    }

    fn count_char(&mut self, c: u8) -> Option<i32> {
        let mut result: Option<i32> = None;
        for number in self.counter.iter_mut() {
            match number.count_char(c) {
                Some(value) => {
                    result = Some(value);
                }
                None => {}
            }
        }
        return result;
    }
}

fn main() {
    let mut sum: i32 = 0;

    for line in read_to_string("input.txt").unwrap().lines() {
        let string = line.to_string();
        let mut counter = Counter::new();
        let mut first = -1;
        let mut second = -1;

        for c in string.as_bytes() {
            match counter.count_char(*c) {
                Some(value) => {
                    if first == -1 {
                        first = value;
                    }
                    second = value;
                }
                None => {}
            }
        }

        if first > 0 {
            sum += first * 10 + second;
        }
    }
    println!("{}", sum);
}
