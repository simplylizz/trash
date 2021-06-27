
fn main() {
    let initial_sum: f64 = 7000.0;
    let rate: f64 = 0.02 / 100.0;
    let reinvest_periods: [u16; 5] = [7, 30, 90, 180, 365];
    let invest_periods: [u16; 7] = [30, 90, 180, 365, 2*365, 3*365, 5*365];

    println!("Investment sum: ${}", initial_sum);
    println!("Investment rate: {:.2}% / day", rate * 100.0);
    println!("Investment periods (days): 30, 90, 180, 365, 3*365, 5*365");
    println!("Reinvestment periods (days): 1, 7, 30, 90, 180, 365");

    let mut bodies = vec![initial_sum; reinvest_periods.len()];
    let mut acc_percent = vec![0.0; reinvest_periods.len()];

    // print header
    println!("---");
    println!("   date   |                           reinvest periods");
    print!("          ");
    for period in reinvest_periods {
        print!("| {:^20} ", period);
    }
    println!();

    let mut current_period_index = 0;
    for day in 1..invest_periods.last().unwrap()+1 {
        for reinvest_period_index in 0..reinvest_periods.len() {
            if day % reinvest_periods[reinvest_period_index] == 0 {
                bodies[reinvest_period_index] += acc_percent[reinvest_period_index];
                acc_percent[reinvest_period_index] = 0.0;
            }
            acc_percent[reinvest_period_index] += bodies[reinvest_period_index] * rate
        }

        if day == invest_periods[current_period_index] {
            current_period_index += 1;
            if day < 365 {
                print!("{:4} days", day);
            } else {
                let year = day as f64 / 365.0;
                print!("{:3} years", year);
            }
            for i in 0..reinvest_periods.len() {
                print!(
                    " | {:10} ({:^7.1})",
                    (bodies[i]+ acc_percent[i]) as u32,
                    (bodies[i] + acc_percent[i]) / initial_sum * 100. - 100.,
                );
            }
            println!();
        }
    }
}
