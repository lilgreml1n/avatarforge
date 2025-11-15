"""
Background task scheduler for automated maintenance tasks
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from .core.config import settings
from .database.session import SessionLocal
from .services.file_service import FileService

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler: BackgroundScheduler | None = None


def cleanup_orphaned_files_job():
    """
    Background job to cleanup orphaned files.
    Runs in a separate database session.
    """
    db: Session = SessionLocal()
    try:
        file_service = FileService(db)
        files_deleted = file_service.cleanup_orphaned_files(days=settings.FILE_CLEANUP_DAYS)
        logger.info(
            f"Scheduled cleanup completed: deleted {files_deleted} orphaned file(s) "
            f"older than {settings.FILE_CLEANUP_DAYS} days"
        )
    except Exception as e:
        logger.error(f"Error during scheduled cleanup: {e}", exc_info=True)
    finally:
        db.close()


def start_scheduler():
    """
    Start the background scheduler if ENABLE_SCHEDULER is True.
    Called on application startup.
    """
    global scheduler

    if not settings.ENABLE_SCHEDULER:
        logger.info("Scheduler disabled via ENABLE_SCHEDULER setting")
        return

    if scheduler is not None:
        logger.warning("Scheduler already started")
        return

    scheduler = BackgroundScheduler()

    # Schedule daily cleanup at configured hour (default: 2 AM)
    trigger = CronTrigger(hour=settings.CLEANUP_SCHEDULE_HOUR, minute=0)
    scheduler.add_job(
        cleanup_orphaned_files_job,
        trigger=trigger,
        id="cleanup_orphaned_files",
        name="Cleanup orphaned files",
        replace_existing=True
    )

    scheduler.start()
    logger.info(
        f"Scheduler started. Daily cleanup scheduled at {settings.CLEANUP_SCHEDULE_HOUR}:00 "
        f"(will delete files older than {settings.FILE_CLEANUP_DAYS} days)"
    )


def shutdown_scheduler():
    """
    Shutdown the background scheduler.
    Called on application shutdown.
    """
    global scheduler

    if scheduler is not None:
        scheduler.shutdown(wait=True)
        scheduler = None
        logger.info("Scheduler shutdown complete")
