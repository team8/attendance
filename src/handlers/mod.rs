use std::convert::Infallible;
use warp::http::StatusCode;

pub async fn debug() -> Result<impl warp::Reply, Infallible> {
    Ok(warp::reply::reply())
}