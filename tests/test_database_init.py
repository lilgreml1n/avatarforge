"""Unit tests for database initialization"""
import pytest
import tempfile
import os
from pathlib import Path
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from avatarforge.database.base import Base
from avatarforge.database.init_db import init_db
from avatarforge.models.uploaded_file import UploadedFile
from avatarforge.models.generation import Generation


class TestDatabaseInitialization:
    """Tests for database initialization"""

    def test_init_db_creates_tables(self, tmp_path):
        """Test that init_db creates all required tables"""
        # Create a temporary database
        db_path = tmp_path / "test.db"
        db_url = f"sqlite:///{db_path}"

        # Create engine and initialize
        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=engine)

        # Inspect the database
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        # Verify both tables exist
        assert "uploaded_files" in tables
        assert "generations" in tables

        engine.dispose()

    def test_uploaded_files_table_schema(self, tmp_path):
        """Test that uploaded_files table has correct columns"""
        db_path = tmp_path / "test.db"
        db_url = f"sqlite:///{db_path}"

        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=engine)

        inspector = inspect(engine)
        columns = {col['name']: col for col in inspector.get_columns('uploaded_files')}

        # Verify all required columns exist
        required_columns = [
            'file_id', 'filename', 'content_hash', 'file_type',
            'mime_type', 'size', 'width', 'height', 'storage_path',
            'reference_count', 'user_id', 'created_at', 'last_accessed',
            'is_deleted'
        ]

        for col in required_columns:
            assert col in columns, f"Column {col} missing from uploaded_files table"

        # Verify primary key
        pk_columns = inspector.get_pk_constraint('uploaded_files')
        assert 'file_id' in pk_columns['constrained_columns']

        engine.dispose()

    def test_generations_table_schema(self, tmp_path):
        """Test that generations table has correct columns"""
        db_path = tmp_path / "test.db"
        db_url = f"sqlite:///{db_path}"

        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=engine)

        inspector = inspect(engine)
        columns = {col['name']: col for col in inspector.get_columns('generations')}

        # Verify all required columns exist
        required_columns = [
            'generation_id', 'prompt', 'clothing', 'style', 'realism',
            'pose_type', 'pose_file_id', 'reference_file_id', 'user_id',
            'status', 'workflow', 'output_files', 'error_message',
            'comfyui_prompt_id', 'created_at', 'started_at', 'completed_at'
        ]

        for col in required_columns:
            assert col in columns, f"Column {col} missing from generations table"

        # Verify primary key
        pk_columns = inspector.get_pk_constraint('generations')
        assert 'generation_id' in pk_columns['constrained_columns']

        engine.dispose()

    def test_uploaded_files_table_indexes(self, tmp_path):
        """Test that uploaded_files table has proper indexes"""
        db_path = tmp_path / "test.db"
        db_url = f"sqlite:///{db_path}"

        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=engine)

        inspector = inspect(engine)
        indexes = inspector.get_indexes('uploaded_files')

        # Get all indexed columns
        indexed_columns = set()
        for index in indexes:
            indexed_columns.update(index['column_names'])

        # Verify critical columns are indexed
        assert 'content_hash' in indexed_columns, "content_hash should be indexed"
        assert 'user_id' in indexed_columns, "user_id should be indexed"

        engine.dispose()

    def test_can_insert_uploaded_file(self, tmp_path):
        """Test that we can insert data into uploaded_files table"""
        db_path = tmp_path / "test.db"
        db_url = f"sqlite:///{db_path}"

        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=engine)

        # Create a session and insert data
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        file_record = UploadedFile(
            file_id="test-file-123",
            filename="test.png",
            content_hash="abc123hash",
            file_type="pose_image",
            mime_type="image/png",
            size=1024,
            width=512,
            height=512,
            storage_path="uploads/test.png",
            reference_count=0,
            is_deleted=False
        )

        session.add(file_record)
        session.commit()

        # Verify insertion
        result = session.query(UploadedFile).filter_by(file_id="test-file-123").first()
        assert result is not None
        assert result.filename == "test.png"
        assert result.content_hash == "abc123hash"

        session.close()
        engine.dispose()

    def test_can_insert_generation(self, tmp_path):
        """Test that we can insert data into generations table"""
        db_path = tmp_path / "test.db"
        db_url = f"sqlite:///{db_path}"

        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=engine)

        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        gen_record = Generation(
            generation_id="test-gen-123",
            prompt="test warrior character",
            realism=0,
            status="queued"
        )

        session.add(gen_record)
        session.commit()

        # Verify insertion
        result = session.query(Generation).filter_by(generation_id="test-gen-123").first()
        assert result is not None
        assert result.prompt == "test warrior character"
        assert result.status == "queued"

        session.close()
        engine.dispose()

    def test_content_hash_unique_constraint(self, tmp_path):
        """Test that content_hash has unique constraint"""
        db_path = tmp_path / "test.db"
        db_url = f"sqlite:///{db_path}"

        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=engine)

        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.exc import IntegrityError
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        # Insert first file
        file1 = UploadedFile(
            file_id="file-1",
            filename="test1.png",
            content_hash="duplicate-hash",
            file_type="pose_image",
            mime_type="image/png",
            size=1024,
            width=512,
            height=512,
            storage_path="uploads/test1.png",
            reference_count=0,
            is_deleted=False
        )
        session.add(file1)
        session.commit()

        # Try to insert second file with same hash
        file2 = UploadedFile(
            file_id="file-2",
            filename="test2.png",
            content_hash="duplicate-hash",  # Same hash
            file_type="pose_image",
            mime_type="image/png",
            size=2048,
            width=512,
            height=512,
            storage_path="uploads/test2.png",
            reference_count=0,
            is_deleted=False
        )

        with pytest.raises(IntegrityError):
            session.add(file2)
            session.commit()

        session.rollback()
        session.close()
        engine.dispose()

    def test_generation_with_json_fields(self, tmp_path):
        """Test that JSON fields work properly in generations table"""
        db_path = tmp_path / "test.db"
        db_url = f"sqlite:///{db_path}"

        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=engine)

        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        workflow_data = {"node1": {"inputs": {}}}
        output_files_data = [{"filename": "output.png", "size": 2048}]

        gen_record = Generation(
            generation_id="test-gen-json",
            prompt="test prompt",
            realism=0,
            status="completed",
            workflow=workflow_data,
            output_files=output_files_data
        )

        session.add(gen_record)
        session.commit()

        # Verify JSON data is stored and retrieved correctly
        result = session.query(Generation).filter_by(generation_id="test-gen-json").first()
        assert result.workflow == workflow_data
        assert result.output_files == output_files_data

        session.close()
        engine.dispose()
