import pytest
from typing import Dict, Any
from video_editor.core.command import Command
from video_editor.core.interpreter import Interpreter
from video_editor.core.processor import Processor

@pytest.fixture
def sample_text_add_request() -> Dict[str, Any]:
    """Sample request for text addition"""
    return {
        "operation": "add",
        "left": {"type": "text", "value": "Hello"},
        "right": {"type": "text", "value": " World"}
    }

@pytest.fixture
def sample_text_overlay_request() -> Dict[str, Any]:
    """Sample request for text overlay on video"""
    return {
        "operation": "overlay",
        "left": {"type": "text", "value": "WATERMARK"},
        "right": {"type": "video", "path": "/path/to/video.mp4"}
    }

@pytest.fixture
def sample_video_audio_overlay_request() -> Dict[str, Any]:
    """Sample request for video-audio overlay"""
    return {
        "operation": "overlay",
        "left": {"type": "video", "path": "/path/to/video.mp4"},
        "right": {"type": "audio", "path": "/path/to/audio.mp3"}
    }

@pytest.fixture
def invalid_request_missing_field() -> Dict[str, Any]:
    """Invalid request missing required field"""
    return {
        "operation": "add",
        "left": {"type": "text", "value": "Hello"}
        # Missing "right" field
    }

@pytest.fixture
def invalid_request_bad_operation() -> Dict[str, Any]:
    """Invalid request with unsupported operation"""
    return {
        "operation": "invalid_op",
        "left": {"type": "text", "value": "Hello"},
        "right": {"type": "text", "value": " World"}
    }

@pytest.fixture
def sample_command() -> Command:
    """Sample command object"""
    return Command(
        operation="add",
        left_operand={"type": "text", "value": "Hello"},
        right_operand={"type": "text", "value": " World"}
    )

@pytest.fixture
def interpreter() -> Interpreter:
    """Interpreter instance"""
    return Interpreter()

@pytest.fixture
def processor() -> Processor:
    """Processor instance"""
    return Processor()

@pytest.fixture
def unsupported_command() -> Command:
    """Command with unsupported operation combination"""
    return Command(
        operation="add",
        left_operand={"type": "video", "path": "/video.mp4"},
        right_operand={"type": "text", "value": "Hello"}
    )