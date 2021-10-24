use serde::{Serialize, Deserialize};

#[derive(Deserialize, Copy, Clone, Debug)]
pub struct LoginRequest {
    id: Option<usize>,
}

#[derive(Serialize, Clone)]
pub struct LoginResponse {
    pub(crate) leaving: bool,
    pub(crate) valid: bool,
    pub(crate) name: String,
}