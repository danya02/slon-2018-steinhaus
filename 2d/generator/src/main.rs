use atomic_counter::AtomicCounter;
use rayon::iter::{ParallelBridge, ParallelIterator};
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, Write};
use std::io::{BufWriter, stdin};

fn evk(a: i64, b: i64, n: i64) -> i64 {
    let a = if a == 0 { n } else { a };
    let b = if b == 0 { n } else { b };

    // Euclidean GCD
    num::integer::gcd(a, b)
}

fn check_items(
    a: i64,
    n: i64,
    counter: &atomic_counter::RelaxedCounter,
    thread_count: usize,
) -> Vec<[i64; 4]> {
    let thread_idx = a;
    println!("[{thread_idx}] running!");
    let start = std::time::Instant::now();
    let mut output = vec![];
    let h_b = if a % 7 != 0 { 7 } else { 1 };

    for b in (0..=n).step_by(h_b) {
        if b % 8 == 0 || (h_b == 1 && b % 7 == 0) {
            continue;
        }

        let h_c = if a % 5 == 0 || b % 5 == 0 { 1 } else { 5 };

        for c in (0..=n).step_by(h_c) {
            if c % 7 == 0 || c % 8 == 0 || (h_c == 1 && c % 5 == 0) {
                continue;
            }

            let h_l = if a % 3 != 0 && b % 3 != 0 && c % 3 != 0 {
                3
            } else {
                1
            };

            for l in (0..=n).step_by(h_l) {
                // Store the current values in the array
                let mut current_values = [a, b, c, l];

                // Sort the last entry
                current_values.sort();

                // Print the current values
                let [a, b, c, l] = current_values;
                if evk(evk(evk(a, b, n), c, n), l, n) == 1 {
                    if (a.pow(4) + b.pow(4) + c.pow(4) + l.pow(4))
                        == (a.pow(2) * l.pow(2)
                            + a.pow(2) * b.pow(2)
                            + b.pow(2) * l.pow(2)
                            + a.pow(2) * c.pow(2)
                            + b.pow(2) * c.pow(2)
                            + c.pow(2) * l.pow(2))
                    {
                        println!("[{thread_idx}] !!!  {} {} {} {}", a, b, c, l);
                        output.push(current_values);
                    }
                }
            }
        }
    }

    let old_counter = counter.inc();
    println!(
        "[{thread_idx}] Finished in {:.2}s \t\t Produced {} items.\t\t{} remaining...",
        start.elapsed().as_secs_f32(),
        output.len(),
        thread_count - old_counter
    );

    output
}

fn main() -> io::Result<()> {
    let mut n = String::new();

    // Prompt for the maximum number of iterations
    println!("Max number of iterations:");
    stdin().read_line(&mut n)?;
    let n: i64 = n.trim().parse().expect("Please enter a valid number");

    let counter = atomic_counter::RelaxedCounter::new(0);
    let thread_count = n as usize / 8;

    let items = (8..=n)
        .step_by(8)
        .par_bridge()
        .map(|a| check_items(a, n, &counter, thread_count))
        .flat_map(|a| a)
        .collect_vec_list();

    println!("Finished calculation, finalizing...");

    let mut f = BufWriter::new(File::create("steinhaus-input")?);
    let mut stored = HashSet::new();
    for mut item in items.into_iter().flat_map(|a| a) {
        item.sort();
        if stored.contains(&item) {
            continue;
        }
        write!(f, "{} {} {} {}\n", item[0], item[1], item[2], item[3])?;
        stored.insert(item);
    }

    Ok(())
}
