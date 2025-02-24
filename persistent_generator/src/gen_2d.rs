use rayon::iter::{ParallelBridge, ParallelIterator};

use crate::types::TwoDimensionalTask;

fn test(a: u64, b: u64, c: u64, l: u64) -> bool {
    let asq = a * a;
    let bsq = b * b;
    let csq = c * c;
    let lsq = l * l;
    // if (a.pow(4) + b.pow(4) + c.pow(4) + l.pow(4))
    // == (a.pow(2) * l.pow(2)
    //     + a.pow(2) * b.pow(2)
    //     + b.pow(2) * l.pow(2)
    //     + a.pow(2) * c.pow(2)
    //     + b.pow(2) * c.pow(2)
    //     + c.pow(2) * l.pow(2))

    asq * asq + bsq * bsq + csq * csq + lsq * lsq
        == asq * lsq + asq * bsq + bsq * lsq + asq * csq + bsq * csq + csq * lsq
}

pub fn run(task: TwoDimensionalTask) -> Vec<String> {
    let a = task.a_range.0..=task.a_range.1;
    let b = task.b_range.0..=task.b_range.1;
    let c = task.c_range.0..=task.c_range.1;
    let l = task.l_range.0..=task.l_range.1;

    let all_nums = itertools::iproduct!(a, b, c, l).par_bridge();

    let results = all_nums
        .filter(|v| test(v.0, v.1, v.2, v.3))
        .map(|v| format!("{} {} {} {}", v.0, v.1, v.2, v.3))
        .collect_vec_list();

    let mut output = vec![];

    for item in results {
        output.extend(item);
    }
    output
}
