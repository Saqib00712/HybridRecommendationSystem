from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/user/dashboard", response_class=HTMLResponse)
async def user_dashboard(request: Request):
    return templates.TemplateResponse("user/dashboard.html", {"request": request})


@router.get("/products", response_class=HTMLResponse)
async def products_page(request: Request):
    return templates.TemplateResponse("user/products.html", {"request": request})


@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


@router.get("/admin/products", response_class=HTMLResponse)
async def admin_products_page(request: Request):
    return templates.TemplateResponse("admin/products.html", {"request": request})