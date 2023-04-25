from fastapi import *
from fastapi.templating import Jinja2Templates
from util import *
app = FastAPI()

@app.get("/")
def root(request : Request):
    background_udp_streamer()
    return Jinja2Templates(directory=".").TemplateResponse("index.html", context={"request": request})

@app.get("/stop")
def stop_ep():
    stop()
    return {"message": "Stopping"}

@app.get("/rtn")
def rtn_ep():
    if is_stopped:
        return {"message": "Stopped", "data": '404 Not Found'}
    
    return {"message": "Returning", "data": f'{per_sock()}'}