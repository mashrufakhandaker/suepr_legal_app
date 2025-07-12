# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.services.ai_case.ai_case_route import router as ai_case_router
from app.services.doc_upload.doc_upload_route import router as doc_upload_router
from app.services.doc_generate.doc_generate_route import router as doc_generate_router


app = FastAPI(
    title=settings.APP_NAME,
    description="SUEPR Legal AI - Comprehensive Legal Assistant API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directories
os.makedirs("uploads/temp", exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(ai_case_router, prefix="/api/ai", tags=["AI Case Services"])
app.include_router(doc_upload_router, prefix="/api/upload", tags=["Document Upload"])
app.include_router(doc_generate_router, prefix="/api/doc-generate", tags=["Document Generation"])

@app.get("/")
async def root():
    return {"message": "SUEPR Legal AI API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "suepr-legal-ai"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
