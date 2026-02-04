"""Main FastAPI application"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import prices, sentiment, recommendations
from app.models.database import init_db

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Halan Invest - Fund Orchestrator",
    description="Monitor & analyze investment funds with real-time price tracking and sentiment analysis",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import asyncio
from app.orchestrator import start_continuous_monitoring

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database and start background tasks"""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")
    
    # Start background monitoring loop
    logger.info("Starting background monitoring...")
    asyncio.create_task(start_continuous_monitoring())


# Include routers
app.include_router(prices.router)
app.include_router(sentiment.router)
app.include_router(recommendations.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Halan Invest - Fund Orchestrator API",
        "version": "1.0.0",
        "endpoints": {
            "prices": "/api/prices",
            "sentiment": "/api/sentiment",
            "recommendations": "/api/recommendations",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "halan-invest-api"}


@app.get("/api/system/status")
async def system_status():
    """Detailed system status endpoint"""
    from app.services.monitoring import system_monitor
    return system_monitor.get_system_status()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
