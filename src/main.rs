mod models;

use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder, HttpRequest, Error};
use actix_web::http::header::{ContentDisposition, DispositionType};
use actix_files as fs;
use log::*;
use serde::Serialize;
use simple_logger::SimpleLogger;

use models::login;

#[post("/api/login")]
async fn login_request(form: web::Json<login::LoginRequest>) -> HttpResponse {
    trace!("Login request {:?}", form);

    let response = login::LoginResponse {
        leaving: false,
        valid: true,
        name: "Test".to_string()
    };

    HttpResponse::Ok()
        .body(serde_json::to_string::<login::LoginResponse>(&response).unwrap())
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