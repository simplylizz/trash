use std::fs::read_to_string;


fn main() {
    let mut valid_game_ids = Vec::new();

    for line in read_to_string("input.txt").unwrap().lines() {
        let string = line.to_string();
        let parts = string.split_once(": ").unwrap();

        let game_id_str = parts.0.to_string().trim_start_matches("Game ").to_string();
        let game_id = game_id_str.parse::<u32>().unwrap();

        let red = 12;
        let green = 13;
        let blue = 14;

        let mut is_valid = true;

        parts.1.split("; ").for_each(|game| {
            game.split(", ").for_each(|cubes| {
                // e.g.: 5 green
                let cube_parts = cubes.split_once(" ").unwrap();
                let cube_count = cube_parts.0.parse::<u32>().unwrap();
                match cube_parts.1 {
                    "red" => {
                        if cube_count > red {
                            is_valid = false;
                        }
                    },
                    "green" => {
                        if cube_count > green {
                            is_valid = false;
                        }
                    },
                    "blue" => {
                        if cube_count > blue {
                            is_valid = false;
                        }
                    },
                    _ => {
                        println!("Invalid color: {}", cube_parts.1);
                    }
                }
            });
        });

        if is_valid {
            valid_game_ids.push(game_id);
        }
    }
    println!("{:?}", valid_game_ids);
    println!("Sum: {}", valid_game_ids.iter().sum::<u32>());
}
