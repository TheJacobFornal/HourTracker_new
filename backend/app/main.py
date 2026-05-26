from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import projects, activities, teams, users, time_logs


def create_app() -> FastAPI:
    app = FastAPI(title="HourTrack API", version="4.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://10.1.69.100",
            "http://hourtracker.pemes.net",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(projects.router)
    app.include_router(activities.router)
    app.include_router(teams.router)
    app.include_router(users.router)
    app.include_router(time_logs.router)

    @app.get("/health")
    def health():
        return {"status": "ok1"}

    print("API is working on host")
    return app


app = create_app()
