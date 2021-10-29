use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Student {
    pub(crate) id: u32,
    pub(crate) name: String,
    pub(crate) total_time: f64,
    pub(crate) valid_time: f64,
}