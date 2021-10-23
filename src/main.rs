mod filters;
mod handlers;

use warp::*;

#[tokio::main]
async fn main() {
    let api = filters::filters();

    warp::serve(api)
        .run(([127, 0, 0, 1], 3030))
        .await;
}