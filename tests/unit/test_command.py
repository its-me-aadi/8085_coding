import pytest
from video_editor.core.command import Command

class TestCommand:
    """Unit tests for the Command class"""
    
    def test_command_creation(self):
        """Test creating a Command object"""
        command = Command(
            operation="add",
            left_operand={"type": "text", "value": "Hello"},
            right_operand={"type": "text", "value": " World"}
        )
        
        assert command.operation == "add"
        assert command.left_operand == {"type": "text", "value": "Hello"}
        assert command.right_operand == {"type": "text", "value": " World"}
    
    def test_get_operation_type(self, sample_command):
        """Test getting operation type"""
        assert sample_command.get_operation_type() == "add"
    
    def test_get_left_type(self, sample_command):
        """Test getting left operand type"""
        assert sample_command.get_left_type() == "text"
    
    def test_get_right_type(self, sample_command):
        """Test getting right operand type"""
        assert sample_command.get_right_type() == "text"
    
    def test_get_strategy_key(self, sample_command):
        """Test generating strategy key"""
        expected_key = "add_text_text"
        assert sample_command.get_strategy_key() == expected_key
    
    def test_get_strategy_key_video_audio(self):
        """Test strategy key for video-audio combination"""
        command = Command(
            operation="overlay",
            left_operand={"type": "video", "path": "/video.mp4"},
            right_operand={"type": "audio", "path": "/audio.mp3"}
        )
        
        expected_key = "overlay_video_audio"
        assert command.get_strategy_key() == expected_key
    
    def test_string_representation(self, sample_command):
        """Test string representation of command"""
        expected_str = "Command(add: text + text)"
        assert str(sample_command) == expected_str
    
    def test_missing_type_in_operand(self):
        """Test behavior when operand is missing type field"""
        command = Command(
            operation="add",
            left_operand={"value": "Hello"},  # Missing "type"
            right_operand={"type": "text", "value": " World"}
        )
        
        assert command.get_left_type() == ""
        assert command.get_right_type() == "text"
        assert command.get_strategy_key() == "add__text"
    
    def test_empty_operands(self):
        """Test behavior with empty operands"""
        command = Command(
            operation="test",
            left_operand={},
            right_operand={}
        )
        
        assert command.get_left_type() == ""
        assert command.get_right_type() == ""
        assert command.get_strategy_key() == "test__"