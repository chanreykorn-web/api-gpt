import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, API-GPT!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="174.16.10.143", port=8000, reload=True)