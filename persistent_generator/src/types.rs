use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct Job {
    pub task: Task,
    pub result: Option<Vec<String>>,
}

#[derive(Serialize, Deserialize)]
pub enum Task {
    TwoDimensional(TwoDimensionalTask),
    ThreeDimensional(ThreeDimensionalTask),
}

#[derive(Serialize, Deserialize)]
pub struct TwoDimensionalTask {
    pub a_range: (u64, u64),
    pub b_range: (u64, u64),
    pub c_range: (u64, u64),
    pub l_range: (u64, u64),
}

#[derive(Serialize, Deserialize)]
pub struct ThreeDimensionalTask {
    pub a_range: (u64, u64),
    pub b_range: (u64, u64),
    pub c_range: (u64, u64),
    pub d_range: (u64, u64),
    pub l_range: (u64, u64),
}
