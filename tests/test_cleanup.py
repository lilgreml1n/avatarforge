"""Unit tests for file cleanup functionality"""
import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

from avatarforge.database.base import Base
from avatarforge.models.uploaded_file import UploadedFile
from avatarforge.services.file_service import FileService
from avatarforge.scheduler import cleanup_orphaned_files_job, start_scheduler, shutdown_scheduler


class TestCleanupOrphanedFiles:
    """Tests for cleanup_orphaned_files method"""

    @pytest.fixture
    def db_session(self, tmp_path):
        """Create a temporary database session"""
        db_path = tmp_path / "test.db"
        db_url = f"sqlite:///{db_path}"
        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        yield session
        session.close()
        engine.dispose()

    @pytest.fixture
    def file_service(self, db_session, tmp_path):
        """Create FileService instance with temporary storage"""
        service = FileService(db_session)
        service.storage_root = tmp_path / "storage"
        service.uploads_dir = service.storage_root / "uploads"
        service.uploads_dir.mkdir(parents=True, exist_ok=True)
        return service

    def create_test_file(self, file_service, file_id: str, days_old: int, reference_count: int = 0):
        """Helper to create a test file with specific age and reference count"""
        # Create physical file
        # storage_path should be relative to uploads_dir (not storage_root)
        storage_subpath = f"pose_image/{file_id}.txt"
        file_path = file_service.uploads_dir / storage_subpath
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("test content")

        # Create database record
        created_at = datetime.now(timezone.utc) - timedelta(days=days_old)
        file_record = UploadedFile(
            file_id=file_id,
            filename=f"{file_id}.txt",
            content_hash=f"hash_{file_id}",
            file_type="pose_image",
            mime_type="text/plain",
            size=100,
            width=512,
            height=512,
            storage_path=storage_subpath,
            reference_count=reference_count,
            is_deleted=False,
            created_at=created_at,
            last_accessed=created_at
        )
        file_service.db.add(file_record)
        file_service.db.commit()

        return file_record

    def test_cleanup_no_orphaned_files(self, file_service):
        """Test cleanup when there are no orphaned files"""
        # Create files with references
        self.create_test_file(file_service, "file1", days_old=40, reference_count=1)
        self.create_test_file(file_service, "file2", days_old=40, reference_count=2)

        files_deleted = file_service.cleanup_orphaned_files(days=30)

        assert files_deleted == 0

    def test_cleanup_orphaned_files_old_enough(self, file_service):
        """Test cleanup deletes orphaned files older than threshold"""
        # Create orphaned files (reference_count=0)
        old_orphan = self.create_test_file(file_service, "old_orphan", days_old=40, reference_count=0)
        old_orphan_id = old_orphan.file_id

        # Create recent orphaned file (should not be deleted)
        recent_orphan = self.create_test_file(file_service, "recent_orphan", days_old=10, reference_count=0)
        recent_orphan_id = recent_orphan.file_id

        files_deleted = file_service.cleanup_orphaned_files(days=30)

        assert files_deleted == 1

        # Verify old orphan is hard deleted from DB
        old_file_check = file_service.db.query(UploadedFile).filter_by(file_id=old_orphan_id).first()
        assert old_file_check is None

        # Verify recent orphan still exists
        recent_file_check = file_service.db.query(UploadedFile).filter_by(file_id=recent_orphan_id).first()
        assert recent_file_check is not None
        assert recent_file_check.is_deleted is False

    def test_cleanup_deletes_physical_files(self, file_service):
        """Test that cleanup deletes physical files from disk"""
        # Create orphaned file
        old_file = self.create_test_file(file_service, "physical_test", days_old=40, reference_count=0)
        file_path = file_service.get_file_path(old_file)

        assert file_path.exists()

        files_deleted = file_service.cleanup_orphaned_files(days=30)

        assert files_deleted == 1
        assert not file_path.exists()

    def test_cleanup_with_missing_physical_file(self, file_service):
        """Test cleanup handles missing physical files gracefully"""
        # Create DB record without physical file
        created_at = datetime.now(timezone.utc) - timedelta(days=40)
        file_record = UploadedFile(
            file_id="missing_file",
            filename="missing.txt",
            content_hash="hash_missing",
            file_type="pose_image",
            mime_type="text/plain",
            size=100,
            width=512,
            height=512,
            storage_path="uploads/missing.txt",
            reference_count=0,
            is_deleted=False,
            created_at=created_at,
            last_accessed=created_at
        )
        file_service.db.add(file_record)
        file_service.db.commit()

        # Should not raise exception
        files_deleted = file_service.cleanup_orphaned_files(days=30)

        assert files_deleted == 1
        # File should be hard deleted from DB
        deleted_file = file_service.db.query(UploadedFile).filter_by(file_id="missing_file").first()
        assert deleted_file is None

    def test_cleanup_multiple_files(self, file_service):
        """Test cleanup with multiple orphaned files"""
        # Create multiple old orphaned files
        for i in range(5):
            self.create_test_file(file_service, f"orphan_{i}", days_old=40, reference_count=0)

        # Create files that should not be deleted
        self.create_test_file(file_service, "has_refs", days_old=40, reference_count=1)
        self.create_test_file(file_service, "too_recent", days_old=10, reference_count=0)

        files_deleted = file_service.cleanup_orphaned_files(days=30)

        assert files_deleted == 5

    def test_cleanup_custom_days_threshold(self, file_service):
        """Test cleanup with custom days threshold"""
        # Create files of varying ages
        self.create_test_file(file_service, "file_60_days", days_old=60, reference_count=0)
        self.create_test_file(file_service, "file_45_days", days_old=45, reference_count=0)
        self.create_test_file(file_service, "file_30_days", days_old=30, reference_count=0)

        # Use 50 day threshold
        files_deleted = file_service.cleanup_orphaned_files(days=50)

        # Only the 60-day-old file should be deleted
        assert files_deleted == 1

    def test_cleanup_already_deleted_files(self, file_service):
        """Test that cleanup ignores files already marked as deleted"""
        # Create orphaned file already marked as deleted
        created_at = datetime.now(timezone.utc) - timedelta(days=40)
        file_record = UploadedFile(
            file_id="already_deleted",
            filename="deleted.txt",
            content_hash="hash_deleted",
            file_type="pose_image",
            mime_type="text/plain",
            size=100,
            width=512,
            height=512,
            storage_path="uploads/deleted.txt",
            reference_count=0,
            is_deleted=True,  # Already deleted
            created_at=created_at,
            last_accessed=created_at
        )
        file_service.db.add(file_record)
        file_service.db.commit()

        files_deleted = file_service.cleanup_orphaned_files(days=30)

        # Should not count already-deleted files
        assert files_deleted == 0


class TestScheduler:
    """Tests for scheduler functionality"""

    def test_scheduler_starts_when_enabled(self):
        """Test that scheduler starts when ENABLE_SCHEDULER is True"""
        import avatarforge.scheduler as scheduler_module

        with patch('avatarforge.scheduler.settings') as mock_settings:
            mock_settings.ENABLE_SCHEDULER = True
            mock_settings.CLEANUP_SCHEDULE_HOUR = 2
            mock_settings.FILE_CLEANUP_DAYS = 30

            with patch('avatarforge.scheduler.BackgroundScheduler') as MockScheduler:
                mock_scheduler_instance = MagicMock()
                MockScheduler.return_value = mock_scheduler_instance

                # Clear any existing scheduler
                scheduler_module.scheduler = None

                start_scheduler()

                # Verify scheduler was created and started
                MockScheduler.assert_called_once()
                mock_scheduler_instance.add_job.assert_called_once()
                mock_scheduler_instance.start.assert_called_once()

    def test_scheduler_disabled_when_setting_false(self):
        """Test that scheduler does not start when ENABLE_SCHEDULER is False"""
        with patch('avatarforge.scheduler.settings') as mock_settings:
            mock_settings.ENABLE_SCHEDULER = False

            with patch('avatarforge.scheduler.BackgroundScheduler') as MockScheduler:
                start_scheduler()

                # Scheduler should not be created
                MockScheduler.assert_not_called()

    def test_scheduler_shutdown(self):
        """Test that scheduler shuts down properly"""
        import avatarforge.scheduler as scheduler_module

        with patch('avatarforge.scheduler.settings') as mock_settings:
            mock_settings.ENABLE_SCHEDULER = True
            mock_settings.CLEANUP_SCHEDULE_HOUR = 2

            with patch('avatarforge.scheduler.BackgroundScheduler') as MockScheduler:
                mock_scheduler_instance = MagicMock()
                MockScheduler.return_value = mock_scheduler_instance

                # Clear any existing scheduler
                scheduler_module.scheduler = None

                start_scheduler()
                shutdown_scheduler()

                # Verify shutdown was called
                mock_scheduler_instance.shutdown.assert_called_once_with(wait=True)

    def test_cleanup_job_executes(self):
        """Test that cleanup job executes successfully"""
        with patch('avatarforge.scheduler.SessionLocal') as MockSessionLocal:
            with patch('avatarforge.scheduler.FileService') as MockFileService:
                mock_db = MagicMock()
                MockSessionLocal.return_value = mock_db

                mock_service = MagicMock()
                mock_service.cleanup_orphaned_files.return_value = 5
                MockFileService.return_value = mock_service

                # Execute the job
                cleanup_orphaned_files_job()

                # Verify service was created and cleanup was called
                MockFileService.assert_called_once_with(mock_db)
                mock_service.cleanup_orphaned_files.assert_called_once()
                mock_db.close.assert_called_once()

    def test_cleanup_job_handles_exceptions(self):
        """Test that cleanup job handles exceptions gracefully"""
        with patch('avatarforge.scheduler.SessionLocal') as MockSessionLocal:
            with patch('avatarforge.scheduler.FileService') as MockFileService:
                mock_db = MagicMock()
                MockSessionLocal.return_value = mock_db

                # Make cleanup raise an exception
                mock_service = MagicMock()
                mock_service.cleanup_orphaned_files.side_effect = Exception("Test error")
                MockFileService.return_value = mock_service

                # Should not raise exception
                cleanup_orphaned_files_job()

                # DB should still be closed
                mock_db.close.assert_called_once()

    def test_scheduler_uses_correct_schedule(self):
        """Test that scheduler uses the configured schedule hour"""
        import avatarforge.scheduler as scheduler_module

        with patch('avatarforge.scheduler.settings') as mock_settings:
            mock_settings.ENABLE_SCHEDULER = True
            mock_settings.CLEANUP_SCHEDULE_HOUR = 3  # 3 AM
            mock_settings.FILE_CLEANUP_DAYS = 30

            with patch('avatarforge.scheduler.BackgroundScheduler') as MockScheduler:
                mock_scheduler_instance = MagicMock()
                MockScheduler.return_value = mock_scheduler_instance

                # Clear any existing scheduler
                scheduler_module.scheduler = None

                start_scheduler()

                # Verify job was added with correct schedule
                call_args = mock_scheduler_instance.add_job.call_args
                trigger = call_args[1]['trigger']

                # CronTrigger should have hour=3, minute=0
                assert trigger.fields[5].expressions[0].first == 3  # hour field
                assert trigger.fields[6].expressions[0].first == 0  # minute field
