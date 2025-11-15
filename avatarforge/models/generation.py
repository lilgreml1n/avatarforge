"""Database model for avatar generation tracking"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from sqlalchemy.sql import func
from ..database.base import Base


class Generation(Base):
    """
    Tracks avatar generation requests and their status

    Attributes:
        generation_id: Unique identifier (UUID)
        prompt: Text prompt used for generation
        clothing: Optional clothing description
        style: Optional art style modifier
        realism: Boolean flag for realistic vs anime style
        pose_type: Type of pose ('front', 'back', 'side', 'quarter', 'all', None)
        pose_file_id: Reference to uploaded pose image
        reference_file_id: Reference to uploaded reference image
        user_id: User who requested the generation (nullable for backward compatibility)
        status: Current status ('queued', 'processing', 'completed', 'failed')
        workflow: ComfyUI workflow JSON
        output_files: JSON array of output file information
        error_message: Error details if status is 'failed'
        comfyui_prompt_id: ComfyUI's prompt ID for tracking
        created_at: Request timestamp
        started_at: Processing start timestamp
        completed_at: Processing completion timestamp
    """
    __tablename__ = "generations"

    generation_id = Column(String, primary_key=True)
    prompt = Column(Text, nullable=False)
    clothing = Column(String, nullable=True)
    style = Column(String, nullable=True)
    realism = Column(Integer, default=0)  # SQLite doesn't have boolean, use 0/1
    pose_type = Column(String, nullable=True)
    pose_file_id = Column(String, nullable=True)
    reference_file_id = Column(String, nullable=True)
    user_id = Column(String, nullable=True, index=True)  # User who requested the generation
    status = Column(String, default="queued")  # queued, processing, completed, failed
    workflow = Column(JSON, nullable=True)
    output_files = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    comfyui_prompt_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Generation(id={self.generation_id}, status={self.status}, prompt={self.prompt[:30]}...)>"
