from fastapi import FastAPI

app = FastAPI(title="LoopIndustrial API")

@app.get("/")
def home():
    return {
        "message": "LoopIndustrial online"
    }