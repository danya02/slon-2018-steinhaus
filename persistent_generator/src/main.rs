use std::{collections::HashSet, io::Write};

use chrono::Timelike;

mod gen_2d;
mod gen_3d;
mod types;

fn main() {
    let files = std::fs::read_dir("hundreds-2d")
        .unwrap()
        .map(|a| {
            a.unwrap()
                .path()
                .file_name()
                .unwrap()
                .to_string_lossy()
                .to_string()
        })
        .collect::<HashSet<_>>();
    println!("file: {:?}", files.iter().next());
    let max_hundred = 10;
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
                    let mut file = std::fs::File::create(format!("hundreds-2d/{}", name)).unwrap();
                    file.write_all(job_string.as_bytes()).unwrap();
                }
            }
        }
    }

    let files = std::fs::read_dir("hundreds-2d")
        .unwrap()
        .map(|a| a.unwrap().path().display().to_string())
        .collect::<HashSet<_>>();

    for file in files {
        loop {
            let now = chrono::Utc::now().with_timezone(&chrono_tz::Europe::Moscow);
            let hour = now.time().hour();
            println!("hour: {}", hour);
            let working_hours = 6..=21;
            if working_hours.contains(&hour) {
                println!("Current hour is inside working hours, so not running");
                println!("Try again in 15 minutes");
                std::thread::sleep(std::time::Duration::from_secs(15 * 60));
                continue;
            }
            break;
        }

        println!("{}", file);
        let start = std::time::Instant::now();
        let text = std::fs::read_to_string(&file).unwrap();
        let mut job: types::Job = serde_json::from_str(&text).unwrap();
        if job.result.is_some() {
            println!("Job already has result, skipping");
            continue;
        }
        let result = match job.task {
            types::Task::TwoDimensional(task) => gen_2d::run(task),
            types::Task::ThreeDimensional(task) => gen_3d::run(task),
        };
        job.result = Some(result);

        let job_string = serde_json::to_string(&job).unwrap();
        let mut file = std::fs::File::create(&file).unwrap();
        file.write_all(job_string.as_bytes()).unwrap();

        let end = std::time::Instant::now();
        let duration = end - start;
        println!("Took {:.4} seconds", duration.as_secs_f64());
        println!("Found {} results", job.result.unwrap().len());
    }
}
