#!/bin/bash
################################################################################
# ComfyUI Restart Script
################################################################################
#
# This script safely restarts ComfyUI to load new custom nodes like GGUF
#
################################################################################

echo "================================================================================"
echo "🔄 RESTARTING COMFYUI"
echo "================================================================================"
echo ""

# Find ComfyUI process
COMFYUI_PID=$(pgrep -f "python.*main.py.*8188")

if [ -z "$COMFYUI_PID" ]; then
    echo "⚠️  ComfyUI not running"
else
    echo "📍 Found ComfyUI process: $COMFYUI_PID"
    echo "🛑 Stopping ComfyUI..."

    # Try graceful shutdown first
    kill $COMFYUI_PID

    # Wait up to 10 seconds
    for i in {1..10}; do
        if ! ps -p $COMFYUI_PID > /dev/null 2>&1; then
            echo "✅ ComfyUI stopped gracefully"
            break
        fi
        sleep 1
    done

    # Force kill if still running
    if ps -p $COMFYUI_PID > /dev/null 2>&1; then
        echo "⚠️  Forcing shutdown..."
        kill -9 $COMFYUI_PID
        sleep 2
    fi
fi

echo ""
echo "🚀 Starting ComfyUI..."
echo ""

cd /home/raven/Documents/ComfyUI

# Start ComfyUI in background
nohup python main.py --listen 0.0.0.0 --port 8188 > /tmp/comfyui.log 2>&1 &
NEW_PID=$!

echo "✅ ComfyUI started with PID: $NEW_PID"
echo ""
echo "⏳ Waiting for ComfyUI to load (10 seconds)..."
sleep 10

echo ""
echo "📊 Checking status..."
if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "✅ ComfyUI is running!"
    echo ""
    echo "📝 Logs: /tmp/comfyui.log"
    echo "🌐 URL: http://192.168.100.133:8188"
    echo ""
    echo "🔍 Checking for GGUF node..."
    if grep -q "GGUF\|gguf" /tmp/comfyui.log 2>/dev/null; then
        echo "✅ GGUF custom node detected in logs!"
    else
        echo "⚠️  GGUF not yet in logs (may still be loading)"
    fi
else
    echo "❌ ComfyUI failed to start"
    echo "📝 Check logs: tail -50 /tmp/comfyui.log"
fi

echo ""
echo "================================================================================"
echo "🎉 RESTART COMPLETE!"
echo "================================================================================"
echo ""
echo "Next steps:"
echo "  1. Test Qwen workflow:"
echo "     cd /home/raven/Documents/git/avatarforge/tests"
echo "     python3 qwen_fitness_influencer.py"
echo ""
echo "================================================================================"
echo ""
