from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
templates = Jinja2Templates(directory="admin_panel/templates")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Salam@123")

@app.get("/admin", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/admin", response_class=HTMLResponse)
async def admin_login_post(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        return templates.TemplateResponse("dashboard.html", {"request": request})
    return RedirectResponse("/admin", status_code=303)
