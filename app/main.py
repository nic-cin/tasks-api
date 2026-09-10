from fastapi import FastAPI

app = FastAPI(title="Tasks API", version="0.1.0")


@app.get("/")
def root():
    return {"status": "ok", "message": "Tasks API rodando"}