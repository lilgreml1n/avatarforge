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
    # Use high-quality Realistic Vision V5.1 for photorealistic generation
    if request.realism:
        model_name = "realisticVisionV51_v51VAE.safetensors"  # Professional photorealistic model
    else:
        # For anime/stylized, fall back to SD 1.5 or use same model with different prompting
        model_name = "realisticVisionV51_v51VAE.safetensors"

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


def build_inpaint_workflow(request) -> Dict[str, Any]:
    """
    Build an inpainting workflow to fix specific regions (like eyes)

    Args:
        request: AvatarRequest object with:
            - prompt (str): What to generate in masked area
            - base_image (str): Base64 image to inpaint on
            - mask_image (str): Base64 mask (white = inpaint, black = keep)
            - denoise (float, optional): How much to change (0.5-1.0), default 0.75
            - negative_prompt (str, optional): What to avoid

    Returns:
        Dict containing the ComfyUI inpaint workflow
    """
    import random

    workflow = {
        "prompt": {},
        "client_id": "avatarforge"
    }

    node_id = 1

    # 1. Load base image (from uploaded file)
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "image": request.base_image,
            "upload": "image"
        },
        "class_type": "LoadImage"
    }
    base_image_node = str(node_id)
    node_id += 1

    # 2. Load mask image (from uploaded file)
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "image": request.mask_image,
            "upload": "image"
        },
        "class_type": "LoadImage"
    }
    mask_image_node = str(node_id)
    node_id += 1

    # 2b. Convert image to mask
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "image": [mask_image_node, 0],
            "channel": "red"
        },
        "class_type": "ImageToMask"
    }
    mask_node = str(node_id)
    node_id += 1

    # 3. Checkpoint Loader
    model_name = "realisticVisionV51_v51VAE.safetensors"
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "ckpt_name": model_name
        },
        "class_type": "CheckpointLoaderSimple"
    }
    checkpoint_node = str(node_id)
    node_id += 1

    # 4. Positive prompt (focused on the area to fix)
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "text": request.prompt,
            "clip": [checkpoint_node, 1]
        },
        "class_type": "CLIPTextEncode"
    }
    positive_node = str(node_id)
    node_id += 1

    # 5. Negative prompt
    negative_text = getattr(request, 'negative_prompt', 'blurry, low quality')
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "text": negative_text,
            "clip": [checkpoint_node, 1]
        },
        "class_type": "CLIPTextEncode"
    }
    negative_node = str(node_id)
    node_id += 1

    # 6. VAE Encode the base image
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "pixels": [base_image_node, 0],
            "vae": [checkpoint_node, 2]
        },
        "class_type": "VAEEncode"
    }
    vae_encode_node = str(node_id)
    node_id += 1

    # 7. Set Latent Noise Mask (applies mask to latent)
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "samples": [vae_encode_node, 0],
            "mask": [mask_node, 0]
        },
        "class_type": "SetLatentNoiseMask"
    }
    masked_latent_node = str(node_id)
    node_id += 1

    # 8. KSampler for inpainting
    steps = getattr(request, 'steps', 60)
    cfg = getattr(request, 'cfg', 7.0)
    denoise = getattr(request, 'denoise', 0.75)
    sampler_name = getattr(request, 'sampler_name', 'dpmpp_2m')  # Fixed sampler name
    scheduler = getattr(request, 'scheduler', 'karras')

    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "seed": random.randint(0, 18446744073709551615),
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
            "denoise": denoise,  # Partial denoise for inpainting
            "model": [checkpoint_node, 0],
            "positive": [positive_node, 0],
            "negative": [negative_node, 0],
            "latent_image": [masked_latent_node, 0]
        },
        "class_type": "KSampler"
    }
    sampler_node = str(node_id)
    node_id += 1

    # 9. VAE Decode
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "samples": [sampler_node, 0],
            "vae": [checkpoint_node, 2]
        },
        "class_type": "VAEDecode"
    }
    decode_node = str(node_id)
    node_id += 1

    # 10. Save Image
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "filename_prefix": "inpainted",
            "images": [decode_node, 0]
        },
        "class_type": "SaveImage"
    }

    return workflow


def build_qwen_inpaint_workflow(request) -> Dict[str, Any]:
    """
    Build a Qwen-Image-Edit-2509 inpainting workflow for high-quality edits

    This uses the state-of-the-art Qwen Image Edit model which offers:
    - Superior quality compared to traditional inpainting
    - Better context understanding via vision-language model
    - Precise control over edited regions

    Args:
        request: AvatarRequest object with:
            - prompt (str): Editing instruction (e.g., "fix the eyes to be clear and bright")
            - base_image (str): Filename of base image in ComfyUI input folder
            - mask_image (str, optional): Filename of mask (white=edit, black=keep)
            - negative_prompt (str, optional): What to avoid
            - use_lightning (bool, optional): Use 4-step Lightning LoRA for speed
            - steps (int, optional): Number of sampling steps (default 20, 4 with Lightning)
            - cfg (float, optional): Guidance scale (default 2.0-3.0)

    Returns:
        Dict containing the ComfyUI Qwen inpainting workflow
    """
    import random

    workflow = {
        "prompt": {},
        "client_id": "avatarforge"
    }

    node_id = 1

    # 1. Load base image
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "image": request.base_image,
            "upload": "image"
        },
        "class_type": "LoadImage"
    }
    base_image_node = str(node_id)
    node_id += 1

    # 2. Load Qwen UNET (GGUF)
    model_filename = "Qwen-Image-Edit-2509-Q4_K_M.gguf"  # Q4_K_M quantization
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "unet_name": model_filename
        },
        "class_type": "UnetLoaderGGUF"  # From ComfyUI-GGUF custom node
    }
    unet_node = str(node_id)
    node_id += 1

    # 3. Load Qwen Text Encoder (CLIP)
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "clip_name1": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
            "type": "qwen"
        },
        "class_type": "DualCLIPLoader"
    }
    clip_node = str(node_id)
    node_id += 1

    # 4. Load VAE
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "vae_name": "qwen_image_vae.safetensors"
        },
        "class_type": "VAELoader"
    }
    vae_node = str(node_id)
    node_id += 1

    # 5. Optional: Load Lightning LoRA for 4-step inference
    use_lightning = getattr(request, 'use_lightning', False)
    if use_lightning:
        workflow["prompt"][str(node_id)] = {
            "inputs": {
                "lora_name": "Qwen-Image-Edit-Lightning-4steps-V1.0.safetensors",
                "strength_model": 1.0,
                "model": [unet_node, 0]
            },
            "class_type": "LoraLoaderModelOnly"
        }
        model_node = str(node_id)
        node_id += 1
    else:
        model_node = unet_node

    # 6. Use base image directly (no scaling needed)
    scaled_image_node = base_image_node

    # 7. Encode positive prompt
    prompt_text = request.prompt
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "text": prompt_text,
            "clip": [clip_node, 0]
        },
        "class_type": "CLIPTextEncode"
    }
    positive_node = str(node_id)
    node_id += 1

    # 8. Encode negative prompt
    negative_text = getattr(request, 'negative_prompt', 'blurry, low quality, distorted')
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "text": negative_text,
            "clip": [clip_node, 0]
        },
        "class_type": "CLIPTextEncode"
    }
    negative_node = str(node_id)
    node_id += 1

    # 9. VAE Encode the image
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "pixels": [scaled_image_node, 0],
            "vae": [vae_node, 0]
        },
        "class_type": "VAEEncode"
    }
    latent_node = str(node_id)
    node_id += 1

    # 10. Optional: Apply mask if provided
    if hasattr(request, 'mask_image') and request.mask_image:
        # Load mask
        workflow["prompt"][str(node_id)] = {
            "inputs": {
                "image": request.mask_image,
                "upload": "image"
            },
            "class_type": "LoadImage"
        }
        mask_image_node = str(node_id)
        node_id += 1

        # Convert to mask
        workflow["prompt"][str(node_id)] = {
            "inputs": {
                "image": [mask_image_node, 0],
                "channel": "red"
            },
            "class_type": "ImageToMask"
        }
        mask_node = str(node_id)
        node_id += 1

        # Apply mask to latent
        workflow["prompt"][str(node_id)] = {
            "inputs": {
                "samples": [latent_node, 0],
                "mask": [mask_node, 0]
            },
            "class_type": "SetLatentNoiseMask"
        }
        masked_latent_node = str(node_id)
        node_id += 1
    else:
        masked_latent_node = latent_node

    # 11. KSampler for image editing
    steps = getattr(request, 'steps', 4 if use_lightning else 20)
    cfg = getattr(request, 'cfg', 2.5)

    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "seed": random.randint(0, 18446744073709551615),
            "steps": steps,
            "cfg": cfg,
            "sampler_name": "euler",
            "scheduler": "simple",
            "denoise": 1.0,  # Full denoise for image editing
            "model": [model_node, 0],
            "positive": [positive_node, 0],
            "negative": [negative_node, 0],
            "latent_image": [masked_latent_node, 0]
        },
        "class_type": "KSampler"
    }
    sampler_node = str(node_id)
    node_id += 1

    # 12. VAE Decode
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "samples": [sampler_node, 0],
            "vae": [vae_node, 0]
        },
        "class_type": "VAEDecode"
    }
    decode_node = str(node_id)
    node_id += 1

    # 13. Save Image
    workflow["prompt"][str(node_id)] = {
        "inputs": {
            "filename_prefix": "qwen_inpaint",
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
