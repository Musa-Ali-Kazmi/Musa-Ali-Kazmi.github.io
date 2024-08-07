from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    name: str
    content: str

messages: List[Message] = []

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/message")
async def message_page(request: Request):
    return templates.TemplateResponse("message.html", {"request": request, "messages": messages})

@app.post("/message")
async def add_message(request: Request, name: str = Form(...), content: str = Form(...)):
    messages.append(Message(name=name, content=content))
    return templates.TemplateResponse("message.html", {"request": request, "messages": messages})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




