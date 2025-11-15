# AvatarForge TODO List

Last updated: 2025-01-15

## 🚨 Critical - Must Do Before Production

### 1. Database Initialization ✅ COMPLETED
- [x] Run database initialization script
- [x] Verify tables created: `uploaded_files`, `generations`
- [x] Create `.env` file from `.env.example`
- [x] Set proper `SECRET_KEY` in `.env`

### 2. Fix Failing Unit Tests ✅ COMPLETED
- [x] Fixed async mock setup in `test_file_service.py`
- [x] Fixed path mocking in `test_delete_file_hard_delete`
- [x] All 78/78 tests passing with 87% code coverage

### 3. Storage Directory Setup ✅ COMPLETED
- [x] Created storage initialization script (`scripts/init_storage.py`)
- [x] Storage directories created automatically
- [x] Proper permissions set

---

## 🔧 High Priority - Core Functionality

### 4. ComfyUI Integration ✅ COMPLETED
- [x] Verified ComfyUI is running on `http://localhost:8188`
- [x] Tested `/health` endpoint - ComfyUI status working
- [x] COMFYUI_URL configured in `.env`
- [x] Tested actual avatar generation end-to-end (successful!)
- [ ] Handle ComfyUI webhook callbacks for status updates (TODO)
- [ ] Implement polling mechanism for generation status (TODO)

### 5. Workflow Builder Enhancement ✅ MOSTLY COMPLETED
- [x] Updated model paths to use `v1-5-pruned-emaonly.safetensors`
- [x] Updated pose-specific workflows to use prompt engineering
- [x] Tested workflow generation with real ComfyUI
- [x] Fixed workflow node ordering bug
- [x] Fixed seed generation (changed from -1 to random)
- [ ] Add error handling for missing models (TODO)
- [ ] Validate workflow JSON structure (TODO)
- [ ] Add support for image-to-image (requires workflow restructuring)

### 6. File Management Improvements ✅ MOSTLY COMPLETED
- [ ] Test file upload with real images (TODO)
- [ ] Test deduplication (upload same file twice) (TODO)
- [ ] Verify file deletion works correctly (TODO - manual testing)
- [x] Implemented automatic cleanup job with APScheduler
- [x] Manual cleanup endpoint: `POST /cleanup/orphaned-files`
- [x] File size limits validation (50MB max)
- [x] MIME type validation (PNG, JPG, WEBP)

---

## 📝 Medium Priority - Nice to Have

### 7. API Enhancements
- [ ] Add pagination to generation listing
- [ ] Add filtering by date range
- [ ] Add search functionality for generations
- [ ] Add bulk operations (delete multiple generations)
- [ ] Add file download statistics
- [ ] Add generation retry endpoint

### 8. Authentication & Security
- [ ] Implement API key authentication
- [ ] Add user management (if multi-user)
- [ ] Rate limiting on uploads
- [ ] CORS configuration for production
- [ ] Input sanitization and validation
- [ ] File upload virus scanning (optional)

### 9. Monitoring & Logging
- [ ] Add structured logging (replace print statements)
- [ ] Add metrics collection (Prometheus/StatsD)
- [ ] Add error tracking (Sentry)
- [ ] Monitor storage usage
- [ ] Monitor generation queue depth
- [ ] Add health check for database

### 10. Documentation
- [ ] Add API usage examples to `API_DOCUMENTATION.md`
- [ ] Create user guide
- [ ] Document deployment process
- [ ] Add architecture diagrams
- [ ] Document error codes and meanings
- [ ] Create troubleshooting guide

---

## 🧪 Testing & Quality

### 11. Test Coverage Improvement
- [ ] Fix 6 failing tests (see Critical #2)
- [ ] Increase coverage to 80%+
  - Current: 46% overall
  - Target: 80%+
- [ ] Add integration tests with real ComfyUI
- [ ] Add end-to-end tests
- [ ] Add performance tests
- [ ] Add load tests (concurrent uploads/generations)

### 12. Code Quality
- [ ] Run linter: `ruff check avatarforge/`
- [ ] Run formatter: `ruff format avatarforge/`
- [ ] Add type hints to all functions
- [ ] Run mypy for type checking
- [ ] Fix all deprecation warnings:
  - `datetime.utcnow()` → `datetime.now(datetime.UTC)`
  - Pydantic `example` → `json_schema_extra`

---

## 🚀 Deployment & Infrastructure

### 13. Production Setup
- [ ] Set up production database (PostgreSQL/MySQL)
- [ ] Configure environment variables
- [ ] Set up reverse proxy (Nginx/Caddy)
- [ ] Configure SSL/TLS certificates
- [ ] Set up systemd service or Docker
- [ ] Configure log rotation
- [ ] Set up backup strategy (database + files)

### 14. Docker Configuration
- [ ] Create Dockerfile
- [ ] Create docker-compose.yml
- [ ] Include ComfyUI in Docker setup
- [ ] Configure volumes for storage
- [ ] Test Docker deployment locally
- [ ] Create production docker-compose

### 15. CI/CD Pipeline
- [ ] Set up GitHub Actions / GitLab CI
- [ ] Run tests on every commit
- [ ] Auto-deploy to staging
- [ ] Manual approval for production
- [ ] Run security scans
- [ ] Generate coverage reports

---

## 💡 Feature Additions

### 16. Advanced Multi-View Avatar Generation System
**Goal:** Implement sophisticated avatar generation with identity consistency across multiple views

#### Phase 1: Enhanced Schema & Prompt Engineering (Quick Win)
- [ ] Create `AdvancedAvatarRequest` schema with rich input structure:
  - `base_image`: Optional input photo for img2img
  - `style`: Style selection (photorealistic, anime, etc.)
  - `model`: AI model selector (qwen3-image-edit, etc.)
  - `views`: List of view angles with descriptions
  - `clothing`: Structured clothing data (base, overlay, accessories)
  - `realism`: Detailed realism settings (lighting, skin, camera)
  - `output_resolution`: Configurable output size
  - `ensure_consistency`: Identity preservation toggle
- [ ] Create supporting schemas:
  - `ViewRequest`: angle + description for each view
  - `ClothingRequest`: base_outfit + overlay_item + accessories list
  - `RealismSettings`: lighting, skin, clothing, camera details
- [ ] Update `build_workflow()` to use enhanced prompt details
- [ ] Add clothing and accessories to prompt construction
- [ ] Add realism modifiers (lighting, skin texture, camera effects)
- [ ] Test multi-view generation via enhanced prompt engineering

#### Phase 2: ComfyUI Advanced Models Setup
- [ ] Research and document required ComfyUI models:
  - IP-Adapter or InstantID for identity preservation
  - ControlNet models for pose control
  - PhotoMaker or similar for face consistency
  - Qwen3-image-edit or equivalent advanced models
- [ ] Install IP-Adapter custom nodes and models
- [ ] Install ControlNet models:
  - OpenPose for pose detection/control
  - Depth for 3D consistency
  - Canny for edge-guided generation
- [ ] Test each model individually with ComfyUI
- [ ] Document model paths and configuration

#### Phase 3: Multi-View Workflow Builder
- [ ] Create `build_advanced_workflow()` function
- [ ] Implement identity extraction from base_image
- [ ] Add IP-Adapter nodes for identity conditioning
- [ ] Add ControlNet nodes for pose control
- [ ] Build view-specific workflow generation
- [ ] Implement multi-workflow orchestration
- [ ] Add consistency verification between views

#### Phase 4: API Integration
- [ ] Add new endpoint: `POST /avatarforge-controller/generate/advanced`
- [ ] Support backward compatibility with existing endpoints
- [ ] Add graceful degradation (use simple workflow if models unavailable)
- [ ] Implement batch processing for multiple views
- [ ] Add progress tracking for multi-view generation
- [ ] Create response schema for multi-view results

#### Phase 5: Testing & Refinement
- [ ] Create test suite for advanced generation
- [ ] Test identity consistency across views
- [ ] Test clothing consistency across angles
- [ ] Test with different realism settings
- [ ] Performance testing (multi-view generation time)
- [ ] Add error handling for missing models

#### Optional Enhancements:
- [ ] Add view angle auto-detection from base_image
- [ ] Implement view interpolation (generate intermediate angles)
- [ ] Add 3D pose estimation for better consistency
- [ ] Support custom ControlNet poses
- [ ] Add style transfer between views
- [ ] Implement background consistency across views

### 17. Advanced File Management
- [ ] Add file versioning
- [ ] Add file tagging/categories
- [ ] Add file search by metadata
- [ ] Add thumbnail generation
- [ ] Add image optimization/compression
- [ ] Add format conversion (PNG→WEBP)

### 17. Generation Features
- [ ] Add batch generation (multiple prompts)
- [ ] Add generation templates
- [ ] Add favorite/bookmark system
- [ ] Add generation sharing (public URLs)
- [ ] Add generation export (ZIP download)
- [ ] Add generation history export (CSV/JSON)

### 18. User Experience
- [ ] Add WebSocket support for real-time status
- [ ] Add email notifications on completion
- [ ] Add webhook support (call URL on completion)
- [ ] Add generation preview/thumbnails
- [ ] Add generation comparison view
- [ ] Add undo/redo for generations

---

## 🐛 Known Issues

### Issues to Fix:
1. ~~**Test failures** - 6 tests failing due to async mocks~~ ✅ FIXED (78/78 passing)
2. ~~**Workflow builder** - Using placeholder model names~~ ✅ FIXED (using v1-5-pruned-emaonly.safetensors)
3. ~~**ComfyUI integration** - Not fully tested~~ ✅ TESTED (successful generation confirmed)
4. ~~**File cleanup** - No automatic cleanup job running~~ ✅ IMPLEMENTED (APScheduler with daily cleanup)
5. **Error messages** - Some could be more descriptive
6. **Validation** - Some edge cases not validated
7. **Image-to-image** - Not yet supported (requires workflow restructuring)
8. **ControlNet models** - None installed (limits pose control to prompt engineering)

---

## 📊 Performance Optimization

### 19. Performance Improvements
- [ ] Add database indexes:
  - `uploaded_files.content_hash` (already indexed)
  - `generations.status`
  - `generations.created_at`
- [ ] Add Redis caching for:
  - File metadata lookups
  - Generation status
  - Frequently accessed data
- [ ] Optimize image loading (lazy loading)
- [ ] Add CDN for static files
- [ ] Implement connection pooling
- [ ] Add database query optimization

### 20. Scalability
- [ ] Move file storage to S3/MinIO
- [ ] Set up load balancer
- [ ] Implement job queue (Celery/RQ)
- [ ] Add horizontal scaling support
- [ ] Database replication (read replicas)
- [ ] Implement sharding strategy (if needed)

---

## 📚 Learning & Exploration

### 21. Research & Evaluate
- [ ] Alternative image storage (S3, Cloudinary)
- [ ] Alternative databases (PostgreSQL, MongoDB)
- [ ] Message queue systems (RabbitMQ, Kafka)
- [ ] Caching solutions (Redis, Memcached)
- [ ] Monitoring tools (Grafana, DataDog)
- [ ] AI model optimization techniques

---

## ✅ Completed

### Core System (Original)
- [x] Database models (UploadedFile, Generation)
- [x] File service with deduplication
- [x] Generation service with tracking
- [x] All 13 API endpoints
- [x] Comprehensive tooltips and documentation
- [x] Configuration system
- [x] Swagger UI integration
- [x] File upload with multipart support
- [x] SHA256 content hashing
- [x] Reference counting
- [x] Soft/hard deletion
- [x] Generation status tracking
- [x] Backward compatibility with base64

### Recent Additions (2025-01-15)
- [x] **All 78 tests passing** (100% pass rate, 87% code coverage)
- [x] **Database initialization** - Tables created and verified
- [x] **Storage directory setup** - Automated init script created
- [x] **Fixed all deprecation warnings** - Updated to Pydantic v2, SQLAlchemy 2.0, datetime.now(timezone.utc)
- [x] **APScheduler integration** - Automatic file cleanup with toggleable scheduler
- [x] **Manual cleanup endpoint** - `POST /cleanup/orphaned-files`
- [x] **ComfyUI integration tested** - Successful end-to-end generation confirmed
- [x] **Workflow builder fixes** - Updated to use actual available models (v1-5-pruned-emaonly.safetensors)
- [x] **Fixed workflow node ordering bug** - CheckpointLoader now correctly positioned
- [x] **Fixed seed generation** - Changed from -1 to valid random positive integer
- [x] **Pose-specific workflows** - Using prompt engineering for different view angles

---

## 🎯 Quick Start When You Return

### Day 1 - Get Running:
```bash
# 1. Initialize database
python -m avatarforge.database.init_db

# 2. Create .env file
cp .env.example .env

# 3. Start ComfyUI (in separate terminal)
# ... (your ComfyUI startup command)

# 4. Start API server
cd backend
uv run python main.py

# 5. Test it works
curl http://localhost:8000/docs
```

### Day 1 - First Tests:
```bash
# 1. Health check
curl http://localhost:8000/avatarforge-controller/health

# 2. Upload a test image
curl -X POST http://localhost:8000/avatarforge-controller/upload/pose_image \
  -F "file=@test_image.png"

# 3. Generate an avatar
curl -X POST http://localhost:8000/avatarforge-controller/generate/avatar \
  -H "Content-Type: application/json" \
  -d '{"prompt": "warrior character", "realism": false}'
```

### Week 1 Priorities:
1. Fix failing tests (#2)
2. Initialize database (#1)
3. Test with real ComfyUI (#4)
4. Update model paths (#5)
5. Test file upload/deduplication (#6)

---

## 📞 Questions to Answer

When you return, consider:
- [ ] Who will use this API? (Single user? Multiple users?)
- [ ] Where will it be deployed? (Local? Cloud? Docker?)
- [ ] What's the expected load? (Users/day, generations/day?)
- [ ] Do you need authentication?
- [ ] Do you need to support multiple ComfyUI instances?
- [ ] What's your backup strategy?

---

## 🎉 What's Already Working

You have a **production-ready foundation**:
- ✅ Full file management with deduplication
- ✅ Complete API with 13 endpoints
- ✅ Database-backed persistence
- ✅ Comprehensive documentation
- ✅ 53 unit tests (8 passing, 6 fixable)
- ✅ Swagger UI for testing
- ✅ Configurable via environment variables
- ✅ Backward compatible with existing code

The system is **80% complete** - just needs testing, ComfyUI integration, and deployment!

---

**Welcome back when you return! Start with the "Day 1" section and you'll be up and running quickly. 🚀**
