from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.analyzer import AnalysisError, analyze_site


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Ontology AIO URL Diagnostic Prototype")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": None, "error": None, "url": ""},
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, url: str = Form("")) -> HTMLResponse:
    try:
        result = analyze_site(url)
        error = None
    except AnalysisError as exc:
        result = None
        error = str(exc)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": result, "error": error, "url": url},
    )
