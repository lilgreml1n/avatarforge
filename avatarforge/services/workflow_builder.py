"""
ComfyUI Workflow Builder for AvatarForge
Builds ComfyUI workflow JSON from avatar generation requests

API Usage Examples:
==================

1. Basic Avatar Generation (Anime Style):
   POST /avatarforge-controller/generate/avatar
   {
       "prompt": "female warrior, blue armor, long white hair",
       "realism": false
   }

2. Realistic Avatar with Clothing:
   POST /avatarforge-controller/generate/avatar
   {
       "prompt": "male business professional, confident expression",
       "clothing": "grey suit, blue tie, dress shoes",
       "realism": true
   }

3. Avatar with Pose Reference Image:
   POST /avatarforge-controller/generate/avatar
   {
       "prompt": "cyberpunk hacker, neon colors",
       "pose_image": "data:image/png;base64,iVBORw0KGgoAAAANS...",
       "clothing": "hoodie, tactical vest",
       "realism": false
   }

4. Generate Specific Pose View:
   POST /avatarforge-controller/generate_pose?pose=front
   {
       "prompt": "elegant elf archer, green cloak",
       "realism": false
   }
   Available poses: front, back, side, quarter

5. Generate All Pose Views:
   POST /avatarforge-controller/generate_all_poses
   {
       "prompt": "warrior knight, silver armor",
       "clothing": "full plate armor, red cape",
       "realism": false
   }

Supported Parameters:
====================
- prompt: (required) Detailed description of the avatar
  Examples: "female mage with purple robes", "muscular warrior with sword"

- pose_image: (optional) Base64 encoded image for pose control
  Format: "data:image/png;base64,..." or file path

- clothing: (optional) Specific clothing/outfit details
  Examples: "leather jacket, jeans", "medieval armor, cape"

- realism: (optional, default=false) Rendering style toggle
  false = anime/stylized, true = photorealistic

- reference_image: (optional) Base64 image for style matching

- style: (optional) Art style modifier
  Options: "cel-shaded", "watercolor", "oil painting", "pixel art", "comic book"
"""
from typing import Any, Dict

def build_workflow(request) -> Dict[str, Any]:
    """
    Build a ComfyUI workflow from an AvatarRequest

    Args:
        request: AvatarRequest object with the following attributes:
            - prompt (str): Detailed avatar description
            - pose_image (str, optional): Base64 image or path for pose reference
            - clothing (str, optional): Specific clothing details
            - realism (bool): True for realistic, False for anime style
            - reference_image (str, optional): Base64 reference image
            - style (str, optional): Art style modifier

    Returns:
        Dict containing the ComfyUI workflow JSON structure

    Example:
        >>> request = AvatarRequest(
        ...     prompt="female warrior, blue armor",
        ...     clothing="full plate armor, cape",
        ...     realism=False
        ... )
        >>> workflow = build_workflow(request)
    """
    # Base workflow structure for ComfyUI
    workflow = {
        "prompt": {},
        "client_id": "avatarforge"
    }

    # Node counter for unique IDs
    node_id = 1

    # 1. Text Prompt Node (CLIPTextEncode)
    # Build enhanced prompt with clothing and style
    enhanced_prompt = request.prompt

    if hasattr(request, 'clothing') and request.clothing:
        enhanced_prompt = f"{enhanced_prompt}, wearing {request.clothing}"

    if hasattr(request, 'style') and request.style:
        enhanced_prompt = f"{enhanced_prompt}, {request.style} art style"

    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "text": enhanced_prompt,
            "clip": ["4", 1]  # Reference to CLIP model loader (will be node 4)
        },
        "class_type": "CLIPTextEncode"
    }
    positive_prompt_node = str(node_id)
    node_id += 1

    # 2. Negative Prompt Node
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "text": "nsfw, nude, bad quality, blurry, distorted",
            "clip": ["4", 1]  # Reference to CLIP model loader (will be node 4)
        },
        "class_type": "CLIPTextEncode"
    }
    negative_prompt_node = str(node_id)
    node_id += 1

    # 3. Empty Latent Image (or pose/reference image if provided)
    reference_image_input = None

    # Check for pose_image first, then reference_image
    input_image = None
    if hasattr(request, 'pose_image') and request.pose_image:
        input_image = request.pose_image
    elif hasattr(request, 'reference_image') and request.reference_image:
        input_image = request.reference_image

    # Note: Image loading with VAE encoding requires checkpoint to be loaded first
    # For now, we'll always use EmptyLatentImage for text-to-image generation
    # TODO: Restructure workflow to support image-to-image with proper node ordering

    # Empty latent image (text-to-image generation)
    # Support custom resolution if provided
    width = getattr(request, 'width', 512)
    height = getattr(request, 'height', 512)

    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "width": width,
            "height": height,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage"
    }
    latent_node = str(node_id)
    node_id += 1

    # 4. Checkpoint Loader (model selector based on realism)
    # Note: Using v1-5-pruned-emaonly.safetensors as default model
    # TODO: Add realistic_model.safetensors and anime_model.safetensors to ComfyUI models directory
    model_name = "v1-5-pruned-emaonly.safetensors"  # Use available model for now
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "ckpt_name": model_name
        },
        "class_type": "CheckpointLoaderSimple"
    }
    checkpoint_node = str(node_id)
    node_id += 1

    # 5. KSampler (main generation node)
    import random
    # Support custom quality parameters
    steps = getattr(request, 'steps', 20)
    cfg = getattr(request, 'cfg', 7.0)
    sampler_name = getattr(request, 'sampler_name', 'euler')

    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "seed": random.randint(0, 18446744073709551615),  # Random seed
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler_name,
            "scheduler": "normal",
            "denoise": 1.0,
            "model": [checkpoint_node, 0],  # From checkpoint loader
            "positive": [positive_prompt_node, 0],
            "negative": [negative_prompt_node, 0],
            "latent_image": [latent_node, 0]
        },
        "class_type": "KSampler"
    }
    sampler_node = str(node_id)
    node_id += 1

    # 6. VAE Decode
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "samples": [sampler_node, 0],
            "vae": [checkpoint_node, 2]  # VAE from checkpoint loader
        },
        "class_type": "VAEDecode"
    }
    decode_node = str(node_id)
    node_id += 1

    # 7. Save Image
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "filename_prefix": "avatarforge",
            "images": [decode_node, 0]
        },
        "class_type": "SaveImage"
    }

    return workflow


def build_pose_workflow(pose_type: str, request) -> Dict[str, Any]:
    """
    Build a workflow for a specific pose type
    Args:
        pose_type: Type of pose ('front', 'back', 'side', 'quarter')
        request: AvatarRequest object
    Returns:
        Dict containing the pose-specific ComfyUI workflow
    """
    # Get base workflow
    workflow = build_workflow(request)
    
    # Add pose-specific logic
    # Note: Using same model for all poses - control via prompt engineering
    # TODO: Add pose-specific ControlNet models when available
    positive_prompt_node = "1"

    if pose_type == 'front':
        # Front pose - standard proportions, full body view
        workflow["prompt"][positive_prompt_node]["inputs"]["text"] = f"front view, full body shot, {request.prompt}, standing straight, facing camera"

    elif pose_type == 'back':
        # Back pose - emphasize back features, different lighting
        workflow["prompt"][positive_prompt_node]["inputs"]["text"] = f"back view, rear view, {request.prompt}, showing back, facing away from camera"

    elif pose_type == 'side':
        # Side pose - emphasize profile, narrow width
        workflow["prompt"][positive_prompt_node]["inputs"]["text"] = f"side view, profile shot, {request.prompt}, 90 degree angle, side profile"

    elif pose_type == 'quarter':
        # Quarter pose - 3/4 view, partial features
        workflow["prompt"][positive_prompt_node]["inputs"]["text"] = f"3/4 view, three quarter angle, {request.prompt}, slightly turned"
    
    # Adjust image dimensions based on pose
    if pose_type in ['side', 'quarter']:
        # Side and quarter views might need different aspect ratios
        empty_latent_node = "6"  # The EmptyLatentImage node
        if empty_latent_node in workflow["prompt"]:
            workflow["prompt"][empty_latent_node]["inputs"]["width"] = 448
            workflow["prompt"][empty_latent_node]["inputs"]["height"] = 640

    return workflow


def build_all_poses_workflow(request) -> Dict[str, Any]:
    """
    Build a workflow for all poses (front, back, side, quarter)
    Args:
        request: AvatarRequest object
    Returns:
        Dict containing workflows for all poses
    """
    poses = ['front', 'back', 'side', 'quarter']
    all_workflows = {}

    for pose in poses:
        all_workflows[pose] = build_pose_workflow(pose, request)

    return {
        "poses": poses,
        "workflows": all_workflows,
        "request": {
            "prompt": request.prompt,
            "clothing": request.clothing,
            "realism": request.realism
        }
    }
