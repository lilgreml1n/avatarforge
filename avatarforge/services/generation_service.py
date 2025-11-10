"""
Generation service for managing avatar generation workflows

Handles creation, tracking, and execution of ComfyUI workflows
"""
import uuid
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.generation import Generation
from ..models.uploaded_file import UploadedFile
from ..services.file_service import FileService
from ..services.workflow_builder import build_workflow, build_pose_workflow, build_all_poses_workflow


class GenerationService:
    """Service for managing avatar generation"""

    def __init__(self, db: Session, comfyui_url: str = "http://localhost:8188"):
        self.db = db
        self.comfyui_url = comfyui_url
        self.file_service = FileService(db)

    def create_generation(
        self,
        prompt: str,
        clothing: Optional[str] = None,
        style: Optional[str] = None,
        realism: bool = False,
        pose_type: Optional[str] = None,
        pose_file_id: Optional[str] = None,
        reference_file_id: Optional[str] = None,
        pose_image: Optional[str] = None,  # Legacy base64 support
        reference_image: Optional[str] = None,  # Legacy base64 support
    ) -> Generation:
        """
        Create a new generation request

        Args:
            prompt: Text description of avatar
            clothing: Optional clothing description
            style: Optional art style
            realism: True for realistic, False for anime
            pose_type: Optional pose type ('front', 'back', 'side', 'quarter', 'all')
            pose_file_id: ID of uploaded pose image
            reference_file_id: ID of uploaded reference image
            pose_image: Legacy base64 pose image
            reference_image: Legacy base64 reference image

        Returns:
            Generation: Created generation record
        """
        generation_id = str(uuid.uuid4())

        # Validate file IDs and increment references
        if pose_file_id:
            pose_file = self.file_service.get_file_by_id(pose_file_id)
            if not pose_file:
                raise HTTPException(status_code=404, detail=f"Pose file not found: {pose_file_id}")
            self.file_service.increment_reference(pose_file_id)

        if reference_file_id:
            ref_file = self.file_service.get_file_by_id(reference_file_id)
            if not ref_file:
                raise HTTPException(status_code=404, detail=f"Reference file not found: {reference_file_id}")
            self.file_service.increment_reference(reference_file_id)

        # Create generation record
        generation = Generation(
            generation_id=generation_id,
            prompt=prompt,
            clothing=clothing,
            style=style,
            realism=1 if realism else 0,
            pose_type=pose_type,
            pose_file_id=pose_file_id,
            reference_file_id=reference_file_id,
            status="queued"
        )

        self.db.add(generation)
        self.db.commit()
        self.db.refresh(generation)

        return generation

    def build_workflow_for_generation(self, generation: Generation) -> Dict[str, Any]:
        """
        Build ComfyUI workflow for a generation

        Args:
            generation: Generation record

        Returns:
            Dict: ComfyUI workflow JSON
        """
        # Create a request-like object for workflow builder
        class WorkflowRequest:
            def __init__(self, gen: Generation, file_service: FileService):
                self.prompt = gen.prompt
                self.clothing = gen.clothing
                self.style = gen.style
                self.realism = bool(gen.realism)

                # Handle pose image - prioritize file_id over legacy base64
                self.pose_image = None
                if gen.pose_file_id:
                    pose_file = file_service.get_file_by_id(gen.pose_file_id)
                    if pose_file:
                        self.pose_image = str(file_service.get_file_path(pose_file))

                # Handle reference image
                self.reference_image = None
                if gen.reference_file_id:
                    ref_file = file_service.get_file_by_id(gen.reference_file_id)
                    if ref_file:
                        self.reference_image = str(file_service.get_file_path(ref_file))

        request = WorkflowRequest(generation, self.file_service)

        # Build appropriate workflow based on pose_type
        if generation.pose_type == "all":
            workflow = build_all_poses_workflow(request)
        elif generation.pose_type in ["front", "back", "side", "quarter"]:
            workflow = build_pose_workflow(generation.pose_type, request)
        else:
            workflow = build_workflow(request)

        return workflow

    def execute_generation(self, generation_id: str) -> Generation:
        """
        Execute a generation by sending workflow to ComfyUI

        Args:
            generation_id: ID of generation to execute

        Returns:
            Generation: Updated generation record

        Raises:
            HTTPException: If generation not found or execution fails
        """
        generation = self.get_generation(generation_id)
        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")

        if generation.status != "queued":
            raise HTTPException(status_code=400, detail=f"Generation already {generation.status}")

        try:
            # Build workflow
            workflow = self.build_workflow_for_generation(generation)

            # Update status
            generation.status = "processing"
            generation.started_at = datetime.utcnow()
            generation.workflow = workflow
            self.db.commit()

            # Send to ComfyUI
            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json=workflow,
                timeout=30
            )
            response.raise_for_status()

            comfyui_response = response.json()

            # Store ComfyUI prompt ID for tracking
            if "prompt_id" in comfyui_response:
                generation.comfyui_prompt_id = comfyui_response["prompt_id"]
                self.db.commit()

            return generation

        except requests.exceptions.RequestException as e:
            generation.status = "failed"
            generation.error_message = f"ComfyUI request failed: {str(e)}"
            generation.completed_at = datetime.utcnow()
            self.db.commit()
            raise HTTPException(status_code=500, detail=generation.error_message)

        except Exception as e:
            generation.status = "failed"
            generation.error_message = f"Generation failed: {str(e)}"
            generation.completed_at = datetime.utcnow()
            self.db.commit()
            raise HTTPException(status_code=500, detail=generation.error_message)

    def get_generation(self, generation_id: str) -> Optional[Generation]:
        """Get generation by ID"""
        return self.db.query(Generation).filter(
            Generation.generation_id == generation_id
        ).first()

    def list_generations(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[Generation]:
        """
        List generations with optional filtering

        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            status: Filter by status

        Returns:
            List of Generation records
        """
        query = self.db.query(Generation).order_by(Generation.created_at.desc())

        if status:
            query = query.filter(Generation.status == status)

        return query.limit(limit).offset(offset).all()

    def update_generation_status(
        self,
        generation_id: str,
        status: str,
        output_files: Optional[List[Dict[str, Any]]] = None,
        error_message: Optional[str] = None
    ) -> Generation:
        """
        Update generation status (typically called by webhook/polling)

        Args:
            generation_id: Generation ID
            status: New status
            output_files: Optional output file information
            error_message: Optional error message

        Returns:
            Updated generation record
        """
        generation = self.get_generation(generation_id)
        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")

        generation.status = status

        if status in ["completed", "failed"]:
            generation.completed_at = datetime.utcnow()

        if output_files:
            generation.output_files = output_files

        if error_message:
            generation.error_message = error_message

        self.db.commit()
        self.db.refresh(generation)

        return generation

    def delete_generation(self, generation_id: str) -> bool:
        """
        Delete a generation and decrement file references

        Args:
            generation_id: Generation ID to delete

        Returns:
            bool: True if deleted
        """
        generation = self.get_generation(generation_id)
        if not generation:
            return False

        # Decrement file references
        if generation.pose_file_id:
            self.file_service.decrement_reference(generation.pose_file_id)

        if generation.reference_file_id:
            self.file_service.decrement_reference(generation.reference_file_id)

        self.db.delete(generation)
        self.db.commit()

        return True

    def check_comfyui_health(self) -> Dict[str, Any]:
        """Check if ComfyUI is available"""
        try:
            response = requests.get(f"{self.comfyui_url}/system_stats", timeout=5)
            response.raise_for_status()
            return {
                "status": "healthy",
                "url": self.comfyui_url,
                "stats": response.json()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "url": self.comfyui_url,
                "error": str(e)
            }
