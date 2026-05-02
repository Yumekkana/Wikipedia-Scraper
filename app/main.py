from fastapi import FastAPI

from app import infobox

app = FastAPI()

app.include_router(infobox.router)

@app.get("/health")
def root():
    return {"message": "success"}