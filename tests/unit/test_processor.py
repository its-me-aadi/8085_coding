import pytest
from unittest.mock import Mock, patch
from video_editor.core.processor import Processor
from video_editor.core.command import Command

class TestProcessor:
    """Unit tests for the Processor class"""
    
    def test_processor_initialization(self):
        """Test processor initializes correctly"""
        processor = Processor()
        assert processor.strategy_factory is not None
    
    def test_process_command_successful(self, processor, sample_command):
        """Test successful command processing"""
        result = processor.process_command(sample_command)
        
        assert result is not None
        assert result["type"] == "text"
        assert result["bytes"] == b"Hello World"
        assert "metadata" in result
    
    def test_process_command_unsupported(self, processor, unsupported_command):
        """Test processing unsupported command"""
        result = processor.process_command(unsupported_command)
        assert result is None
    
    @patch('video_editor.strategies.strategy_factory.StrategyFactory.get_strategy')
    def test_process_command_no_strategy_found(self, mock_get_strategy, processor, sample_command):
        """Test when no strategy is found for command"""
        mock_get_strategy.return_value = None
        
        result = processor.process_command(sample_command)
        assert result is None
    
    @patch('video_editor.strategies.strategy_factory.StrategyFactory.get_strategy')
    def test_process_command_strategy_execution_fails(self, mock_get_strategy, processor, sample_command):
        """Test when strategy execution fails"""
        mock_strategy = Mock()
        mock_strategy.execute.return_value = None  # Simulate failure
        mock_get_strategy.return_value = mock_strategy
        
        result = processor.process_command(sample_command)
        assert result is None
    
    @patch('video_editor.strategies.strategy_factory.StrategyFactory.get_strategy')
    def test_process_command_exception_handling(self, mock_get_strategy, processor, sample_command):
        """Test exception handling in process_command"""
        mock_get_strategy.side_effect = Exception("Test exception")
        
        result = processor.process_command(sample_command)
        assert result is None
    
    def test_process_command_overlay_operation(self, processor):
        """Test processing overlay operation"""
        command = Command(
            operation="overlay",
            left_operand={"type": "text", "value": "WATERMARK"},
            right_operand={"type": "video", "path": "/video.mp4"}
        )
        
        result = processor.process_command(command)
        
        assert result is not None
        assert result["type"] == "video"
        assert "metadata" in result
        assert result["metadata"]["operation"] == "text_watermark"
    
    def test_process_command_video_audio_overlay(self, processor):
        """Test processing video-audio overlay"""
        command = Command(
            operation="overlay",
            left_operand={"type": "video", "path": "/video.mp4"},
            right_operand={"type": "audio", "path": "/audio.mp3"}
        )
        
        result = processor.process_command(command)
        
        assert result is not None
        assert result["type"] == "video"
        assert "metadata" in result
        assert result["metadata"]["operation"] == "audio_overlay"