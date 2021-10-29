mod models;

use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder, HttpRequest, Error};
use actix_web::http::header::{ContentDisposition, DispositionType};
use actix_files as fs;
use log::*;
use log::LevelFilter::Info;
use serde::Serialize;
use simple_logger::SimpleLogger;
use mongodb::{Client, options::ClientOptions, bson::doc, options::FindOptions, Database};
use futures::stream::TryStreamExt;

use models::login;
use crate::models::login::LoginResponse;
use crate::models::student::Student;

struct AppState {
    db: Database,
}

#[post("/api/login")]
async fn login_request(form: web::Json<login::LoginRequest>, state: web::Data<AppState>) -> HttpResponse {
    info!("Login request {:?}", form);

    let collection = state.db.collection::<Student>("test");
    let filter = doc! { "id": form.id };
    let options = FindOptions::builder().sort(doc! { "id": 1 }).build();
    let mut cursor = collection.find(filter, options).await.unwrap();

    let mut response = None;

    while let Some(student) = cursor.try_next().await.unwrap() {
        if student.id == form.id.unwrap() {
            response = Some(login::LoginResponse {
                leaving: false,
                valid: true,
                name: "Test".to_string()
            });
            break;
        }
    };

    HttpResponse::Ok()
        .body(serde_json::to_string::<login::LoginResponse>(&response.unwrap_or(LoginResponse {
            leaving: false,
            valid: false,
            name: "".to_string()
        })).unwrap())
}

async fn get_client() -> Result<Client, mongodb::error::Error> {
    let client_options = ClientOptions::parse("mongodb://localhost:27017").await?;
    let client = Client::with_options(client_options)?;
    Ok(client)
}

#[actix_web::main]
async fn main() -> Result<(), Error> {
    SimpleLogger::new().with_level(Info).init().unwrap();
    trace!("Started logger");

    let client = get_client().await.unwrap();
    let db = client.database("test");

    HttpServer::new(move || {
        App::new()
            .data(AppState { db: db.clone() })
            .service(login_request)
            .service(
                fs::Files::new("/", "./website/build")
                    .use_last_modified(true))
    })
        .bind("127.0.0.1:3030")?
        .run()
        .await?;

    return Ok(())
}