"""System Monitoring Service - Tracks application health and metrics"""
import logging
import psutil
import os
import platform
from datetime import datetime
from typing import Dict
from sqlalchemy.sql import text
from app.models.database import SessionLocal

logger = logging.getLogger(__name__)

class SystemMonitor:
    """Monitor system resources and application health"""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.start_time = datetime.now()

    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        return {
            "status": "healthy", # You might change this based on checks
            "timestamp": datetime.now().isoformat(),
            "environment": self._get_environment_info(),
            "resources": self._get_resource_usage(),
            "database": self._check_database_health(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }

    def _get_environment_info(self) -> Dict:
        """Get host environment details"""
        return {
            "os": platform.system(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
        }

    def _get_resource_usage(self) -> Dict:
        """Get CPU and Memory usage"""
        try:
            # System-wide metrics
            sys_cpu = psutil.cpu_percent(interval=None)
            sys_mem = psutil.virtual_memory()

            # Process-specific metrics
            proc_mem = self.process.memory_info()
            
            return {
                "cpu_percent": sys_cpu,
                "memory_total_mb": round(sys_mem.total / (1024 * 1024), 2),
                "memory_available_mb": round(sys_mem.available / (1024 * 1024), 2),
                "process_memory_mb": round(proc_mem.rss / (1024 * 1024), 2),
            }
        except Exception as e:
            logger.error(f"Error getting resource usage: {e}")
            return {"error": str(e)}

    def _check_database_health(self) -> Dict:
        """Check database connectivity"""
        db = SessionLocal()
        try:
            # Simple query to check connection
            db.execute(text("SELECT 1"))
            return {"status": "connected", "latency_ms": 0} # Could measure latency
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {"status": "disconnected", "error": str(e)}
        finally:
            db.close()

# Global monitor instance
system_monitor = SystemMonitor()
