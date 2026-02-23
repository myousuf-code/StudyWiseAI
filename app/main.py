"""
StudyWiseAI FastAPI Application
Main application entry point
"""
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

from app.core.config import settings
from app.core.database import create_tables
from app.api import auth, study_plans, ai_assistant, progress, reminders

# Create FastAPI instance
app = FastAPI(
    title="StudyWiseAI API",
    description="AI-powered learning platform with personalized study plans and smart features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    create_tables()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS + ["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176"],  # Add Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(study_plans.router, prefix="/api/study-plans", tags=["Study Plans"])
app.include_router(ai_assistant.router, prefix="/api/ai", tags=["AI Assistant"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress Tracking"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["Reminders"])

# Check if React build exists
react_build_path = Path(__file__).parent.parent / "frontend-react" / "dist"
use_react = react_build_path.exists()

if use_react:
    # Serve React build
    app.mount("/assets", StaticFiles(directory=str(react_build_path / "assets")), name="react-assets")
    
    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        """Serve React app for all non-API routes"""
        if full_path.startswith("api/"):
            # Let API routes handle themselves
            return
        
        # Try to serve the file if it exists
        file_path = react_build_path / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Otherwise serve index.html (for React Router)
        return FileResponse(react_build_path / "index.html")
else:
    # Fallback to old frontend during development
    app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
    templates = Jinja2Templates(directory="frontend/templates")
    
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Home page route"""
        return templates.TemplateResponse("index_bulletproof.html", {"request": request})

    @app.get("/full", response_class=HTMLResponse)
    async def full_page(request: Request):
        """Full version page for comparison"""
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/test", response_class=HTMLResponse)
    async def test_page(request: Request):
        """Test page for debugging"""
        return templates.TemplateResponse("test.html", {"request": request})

    @app.get("/progressive", response_class=HTMLResponse)
    async def progressive_test(request: Request):
        """Progressive test page to identify issues"""
        return templates.TemplateResponse("progressive_test.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "StudyWiseAI API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )