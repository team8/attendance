use warp::Filter;

#[tokio::main]
async fn main() {
    // GET /hello/warp => 200 OK with body "Hello, warp!"
    let page = warp::get()
        .and(warp::path::end())
        .and(warp::fs::file("./website/public/index.html"));
        // .and(warp::fs::file("./Cargo.toml"));

    warp::serve(page)
        .run(([127, 0, 0, 1], 3030))
        .await;
}