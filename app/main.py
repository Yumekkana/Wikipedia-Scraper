from fastapi import FastAPI

from app import infobox, search_helper

app = FastAPI()

app.include_router(infobox.router)
app.include_router(search_helper.router)

@app.get("/health")
def root():
    return {"message": "success"}