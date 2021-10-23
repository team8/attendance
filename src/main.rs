use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder, HttpRequest, Error};
use actix_web::http::header::{ContentDisposition, DispositionType};
use actix_files as fs;
use log::*;
use simple_logger::SimpleLogger;

#[post("/api/login")]
async fn login_request(req_body: String) -> impl Responder {
    trace!("Login request {}", req_body);

    HttpResponse::Ok()
}

#[actix_web::main]
async fn main() -> tokio::io::Result<()> {
    SimpleLogger::new().init().unwrap();
    trace!("Started logger");

    HttpServer::new(|| {
        App::new()
            .service(login_request)
            .service(
                fs::Files::new("/", "./website/build")
                    .use_last_modified(true))
    })
        .bind("127.0.0.1:3030")?
        .run()
        .await
}