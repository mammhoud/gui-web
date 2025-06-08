
## Usage with FastAPI

Example `main.py` for FastAPI:

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from flaskwebgui import FlaskUI

app = FastAPI()

app.mount("/public", StaticFiles(directory="dist/"))
templates = Jinja2Templates(directory="dist")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("some_page.html", {"request": request})

if __name__ == "__main__":
    FlaskUI(app=app, server="fastapi").run()
```

> FastAPI app will be served by `uvicorn`.

---
