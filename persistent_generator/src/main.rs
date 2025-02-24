use std::{collections::HashSet, io::Write};

mod gen_2d;
mod gen_3d;
mod types;

fn main() {
    let files = std::fs::read_dir("hundreds-2d")
        .unwrap()
        .map(|a| a.unwrap().path().display().to_string())
        .collect::<HashSet<_>>();
    let max_hundred = 50;
    for a in 0..max_hundred {
        for b in 0..max_hundred {
            for c in 0..max_hundred {
                for l in 0..max_hundred {
                    let name = format!("hundreds-2d-{a}-{b}-{c}-{l}.json");
                    if files.contains(&name) {
                        continue;
                    }

                    let a = a * 100;
                    let b = b * 100;
                    let c = c * 100;
                    let l = l * 100;

                    let task = types::TwoDimensionalTask {
                        a_range: (a, a + 100),
                        b_range: (b, b + 100),
                        c_range: (c, c + 100),
                        l_range: (l, l + 100),
                    };

                    let job = types::Job {
                        task: types::Task::TwoDimensional(task),
                        result: None,
                    };

                    let job_string = serde_json::to_string(&job).unwrap();
                    let mut file = std::fs::File::create(&name).unwrap();
                    file.write_all(job_string.as_bytes()).unwrap();
                }
            }
        }
    }
}
