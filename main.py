import uvicorn
from decouple import config

host = config("HOST")
port = int(config("PORT"))
reload_server = config("RELOAD")

if __name__ == "__main__":
    uvicorn.run("app:app", host=host, port=port, reload=reload_server)