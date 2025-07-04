import pytest
from video_editor.core.command import Command
from video_editor.strategies.text_strategies import AddTextStrategy, OverlayTextStrategy
from video_editor.strategies.video_strategies import AddVideoStrategy, OverlayVideoStrategy
from video_editor.strategies.audio_strategies import AddAudioStrategy, OverlayAudioStrategy

class TestAddTextStrategy:
    """Unit tests for AddTextStrategy"""
    
    def test_supports_valid_command(self):
        """Test that strategy supports valid text+text add command"""
        strategy = AddTextStrategy()
        command = Command(
            operation="add",
            left_operand={"type": "text", "value": "Hello"},
            right_operand={"type": "text", "value": " World"}
        )
        
        assert strategy.supports(command) is True
    
    def test_does_not_support_wrong_operation(self):
        """Test that strategy doesn't support non-add operations"""
        strategy = AddTextStrategy()
        command = Command(
            operation="overlay",
            left_operand={"type": "text", "value": "Hello"},
            right_operand={"type": "text", "value": " World"}
        )
        
        assert strategy.supports(command) is False
    
    def test_does_not_support_wrong_types(self):
        """Test that strategy doesn't support non-text types"""
        strategy = AddTextStrategy()
        command = Command(
            operation="add",
            left_operand={"type": "video", "path": "/video.mp4"},
            right_operand={"type": "text", "value": " World"}
        )
        
        assert strategy.supports(command) is False
    
    def test_execute_successful(self):
        """Test successful execution of text addition"""
        strategy = AddTextStrategy()
        command = Command(
            operation="add",
            left_operand={"type": "text", "value": "Hello"},
            right_operand={"type": "text", "value": " World"}
        )
        
        result = strategy.execute(command)
        
        assert result is not None
        assert result["type"] == "text"
        assert result["bytes"] == b"Hello World"
        assert result["size"] == 11
        assert "metadata" in result
        assert result["metadata"]["operation"] == "concatenation"
    
    def test_execute_with_empty_values(self):
        """Test execution with empty string values"""
        strategy = AddTextStrategy()
        command = Command(
            operation="add",
            left_operand={"type": "text", "value": ""},
            right_operand={"type": "text", "value": "World"}
        )
        
        result = strategy.execute(command)
        
        assert result is not None
        assert result["bytes"] == b"World"

class TestOverlayTextStrategy:
    """Unit tests for OverlayTextStrategy"""
    
    def test_supports_valid_command(self):
        """Test that strategy supports valid text+video overlay command"""
        strategy = OverlayTextStrategy()
        command = Command(
            operation="overlay",
            left_operand={"type": "text", "value": "WATERMARK"},
            right_operand={"type": "video", "path": "/video.mp4"}
        )
        
        assert strategy.supports(command) is True
    
    def test_does_not_support_wrong_operation(self):
        """Test that strategy doesn't support non-overlay operations"""
        strategy = OverlayTextStrategy()
        command = Command(
            operation="add",
            left_operand={"type": "text", "value": "WATERMARK"},
            right_operand={"type": "video", "path": "/video.mp4"}
        )
        
        assert strategy.supports(command) is False
    
    def test_execute_successful(self):
        """Test successful execution of text overlay"""
        strategy = OverlayTextStrategy()
        command = Command(
            operation="overlay",
            left_operand={"type": "text", "value": "WATERMARK"},
            right_operand={"type": "video", "path": "/test/video.mp4"}
        )
        
        result = strategy.execute(command)
        
        assert result is not None
        assert result["type"] == "video"
        assert b"WATERMARK" in result["bytes"]
        assert "metadata" in result
        assert result["metadata"]["watermark_text"] == "WATERMARK"
        assert result["metadata"]["operation"] == "text_watermark"

class TestAddVideoStrategy:
    """Unit tests for AddVideoStrategy"""
    
    def test_supports_valid_command(self):
        """Test that strategy supports valid video+video add command"""
        strategy = AddVideoStrategy()
        command = Command(
            operation="add",
            left_operand={"type": "video", "path": "/video1.mp4"},
            right_operand={"type": "video", "path": "/video2.mp4"}
        )
        
        assert strategy.supports(command) is True
    
    def test_execute_successful(self):
        """Test successful execution of video concatenation"""
        strategy = AddVideoStrategy()
        command = Command(
            operation="add",
            left_operand={"type": "video", "path": "/video1.mp4"},
            right_operand={"type": "video", "path": "/video2.mp4"}
        )
        
        result = strategy.execute(command)
        
        assert result is not None
        assert result["type"] == "video"
        assert "metadata" in result
        assert result["metadata"]["operation"] == "video_concatenation"

class TestOverlayVideoStrategy:
    """Unit tests for OverlayVideoStrategy"""
    
    def test_supports_valid_command(self):
        """Test that strategy supports valid video+audio overlay command"""
        strategy = OverlayVideoStrategy()
        command = Command(
            operation="overlay",
            left_operand={"type": "video", "path": "/video.mp4"},
            right_operand={"type": "audio", "path": "/audio.mp3"}
        )
        
        assert strategy.supports(command) is True
    
    def test_execute_successful(self):
        """Test successful execution of video-audio overlay"""
        strategy = OverlayVideoStrategy()
        command = Command(
            operation="overlay",
            left_operand={"type": "video", "path": "/video.mp4"},
            right_operand={"type": "audio", "path": "/audio.mp3"}
        )
        
        result = strategy.execute(command)
        
        assert result is not None
        assert result["type"] == "video"
        assert "metadata" in result
        assert result["metadata"]["operation"] == "audio_overlay"

class TestAddAudioStrategy:
    """Unit tests for AddAudioStrategy"""
    
    def test_supports_valid_command(self):
        """Test that strategy supports valid audio+audio add command"""
        strategy = AddAudioStrategy()
        command = Command(
            operation="add",
            left_operand={"type": "audio", "path": "/audio1.mp3"},
            right_operand={"type": "audio", "path": "/audio2.mp3"}
        )
        
        assert strategy.supports(command) is True
    
    def test_execute_successful(self):
        """Test successful execution of audio concatenation"""
        strategy = AddAudioStrategy()
        command = Command(
            operation="add",
            left_operand={"type": "audio", "path": "/audio1.mp3"},
            right_operand={"type": "audio", "path": "/audio2.mp3"}
        )
        
        result = strategy.execute(command)
        
        assert result is not None
        assert result["type"] == "audio"
        assert "metadata" in result
        assert result["metadata"]["operation"] == "audio_concatenation"

class TestOverlayAudioStrategy:
    """Unit tests for OverlayAudioStrategy"""
    
    def test_supports_valid_command(self):
        """Test that strategy supports valid audio+audio overlay command"""
        strategy = OverlayAudioStrategy()
        command = Command(
            operation="overlay",
            left_operand={"type": "audio", "path": "/audio1.mp3"},
            right_operand={"type": "audio", "path": "/audio2.mp3"}
        )
        
        assert strategy.supports(command) is True
    
    def test_execute_successful(self):
        """Test successful execution of audio mixing"""
        strategy = OverlayAudioStrategy()
        command = Command(
            operation="overlay",
            left_operand={"type": "audio", "path": "/audio1.mp3"},
            right_operand={"type": "audio", "path": "/audio2.mp3"}
        )
        
        result = strategy.execute(command)
        
        assert result is not None
        assert result["type"] == "audio"
        assert "metadata" in result
        assert result["metadata"]["operation"] == "audio_mixing"

class TestBaseStrategyResult:
    """Test the base strategy result creation method"""
    
    def test_create_result_with_metadata(self):
        """Test creating result with metadata"""
        strategy = AddTextStrategy()
        metadata = {"test": "value"}
        
        result = strategy._create_result("text", b"test data", metadata)
        
        assert result["type"] == "text"
        assert result["bytes"] == b"test data"
        assert result["size"] == 9
        assert result["metadata"] == metadata
    
    def test_create_result_without_metadata(self):
        """Test creating result without metadata"""
        strategy = AddTextStrategy()
        
        result = strategy._create_result("text", b"test data")
        
        assert result["type"] == "text"
        assert result["bytes"] == b"test data"
        assert result["size"] == 9
        assert "metadata" not in result