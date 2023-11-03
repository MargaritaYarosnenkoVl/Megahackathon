from fastapi import FastAPI

app = FastAPI(
    title="This is ХОРОШО!"
)


@app.get("/")
def hello():
    return "Hello world"
