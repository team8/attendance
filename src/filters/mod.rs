use warp::Filter;
use crate::handlers;

pub fn filters() -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
    logins()
        .or(website())
}

pub fn logins() -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
    println!("Stuff");
    warp::path!("api" / "posts")
        .and(warp::post())
        .and_then(handlers::debug)
}

pub fn website() -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
    warp::fs::dir("website/build")
}