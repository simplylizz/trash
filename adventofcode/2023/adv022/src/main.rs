use std::fs::read_to_string;


fn main() {
    let mut sum = 0;

    for line in read_to_string("input.txt").unwrap().lines() {
        let string = line.to_string();
        let parts = string.split_once(": ").unwrap();

        // hashmap color -> count
        let mut colors_map = std::collections::HashMap::new();

        parts.1.split("; ").for_each(|game| {
            game.split(", ").for_each(|cubes| {
                // e.g.: 5 green
                let cube_parts = cubes.split_once(" ").unwrap();
                let cube_count = cube_parts.0.parse::<u32>().unwrap();
                match colors_map.get_mut(cube_parts.1) {
                    Some(count) => {
                        if *count < cube_count {
                            *count = cube_count;
                        }
                    },
                    None => { colors_map.insert(cube_parts.1, cube_count); }
                }
            });
        });

        // multiply all counts
        let sub_sum = colors_map.values().fold(1, |acc, x| acc * x);
        sum += sub_sum;

    }
    println!("{:?}", sum);
}
