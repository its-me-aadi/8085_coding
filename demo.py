#!/usr/bin/env python3
"""
Demonstration script for the media-manipulator service.
Shows how to use different operations and media types.
"""

from video_editor import process_video_request

def test_text_addition():
    """Test text + text addition (concatenation)"""
    print("\n=== Testing Text Addition ===")
    request = {
        "operation": "add",
        "left": {"type": "text", "value": "Hello"},
        "right": {"type": "text", "value": " World"}
    }
    
    result = process_video_request(request)
    if result:
        print(f"Result type: {result['type']}")
        print(f"Result text: {result['bytes'].decode('utf-8')}")
        print(f"Metadata: {result.get('metadata', {})}")
    else:
        print("Processing failed")

def test_text_watermark():
    """Test text overlay on video (watermark)"""
    print("\n=== Testing Text Watermark on Video ===")
    request = {
        "operation": "overlay",
        "left": {"type": "text", "value": "WATERMARK"},
        "right": {"type": "video", "path": "/path/to/video.mp4"}
    }
    
    result = process_video_request(request)
    if result:
        print(f"Result type: {result['type']}")
        print(f"Result size: {result['size']} bytes")
        print(f"Metadata: {result.get('metadata', {})}")
    else:
        print("Processing failed")

def test_video_audio_overlay():
    """Test video + audio overlay"""
    print("\n=== Testing Video + Audio Overlay ===")
    request = {
        "operation": "overlay",
        "left": {"type": "video", "path": "/path/to/video.mp4"},
        "right": {"type": "audio", "path": "/path/to/audio.mp3"}
    }
    
    result = process_video_request(request)
    if result:
        print(f"Result type: {result['type']}")
        print(f"Result size: {result['size']} bytes")
        print(f"Metadata: {result.get('metadata', {})}")
    else:
        print("Processing failed")

def test_unsupported_operation():
    """Test an unsupported operation combination"""
    print("\n=== Testing Unsupported Operation ===")
    request = {
        "operation": "add",
        "left": {"type": "video", "path": "/path/to/video.mp4"},
        "right": {"type": "text", "value": "Hello"}
    }
    
    result = process_video_request(request)
    if result:
        print(f"Unexpected success: {result}")
    else:
        print("Processing failed as expected for unsupported combination")

def test_invalid_request():
    """Test an invalid request structure"""
    print("\n=== Testing Invalid Request ===")
    request = {
        "operation": "add",
        "left": {"type": "text"}  # Missing "value" or "path"
        # Missing "right" entirely
    }
    
    result = process_video_request(request)
    if result:
        print(f"Unexpected success: {result}")
    else:
        print("Processing failed as expected for invalid request")

if __name__ == "__main__":
    print("Media Manipulator Service Demo")
    print("===============================")
    
    # Run all tests
    test_text_addition()
    test_text_watermark()
    test_video_audio_overlay()
    test_unsupported_operation()
    test_invalid_request()
    
    print("\n=== Demo Complete ===")