import uvicorn


def main():
    uvicorn.run("server.routes.app:app", host="127.0.0.1", port=10001, reload=True)
