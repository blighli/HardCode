import threading
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .utils import assets_path

app = FastAPI()
web_path =assets_path.get("assets/web")
app.mount("/", StaticFiles(directory=web_path), name="static")

@app.get("/hello")
async def read_root(): 
    return {"Hello": "World"}

class FastAPIServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.config = uvicorn.Config(
            app = app,
            host = "0.0.0.0",
            port = 8000,
            log_level = "info"
        )
        self.running = False
        self.server = uvicorn.Server(config=self.config)

    def run(self):
        self.running = True
        self.server.run()

    def stop(self):
        if self.running:
            self.server.should_exit = True
            self.running = False
            