import pytest
from video_editor.strategies.strategy_factory import StrategyFactory
from video_editor.strategies.base_strategy import BaseStrategy
from video_editor.strategies.text_strategies import AddTextStrategy, OverlayTextStrategy
from video_editor.strategies.video_strategies import AddVideoStrategy, OverlayVideoStrategy
from video_editor.strategies.audio_strategies import AddAudioStrategy, OverlayAudioStrategy
from video_editor.core.command import Command
from typing import Dict, Any, Optional

class TestStrategyFactory:
    """Unit tests for the StrategyFactory class"""
    
    def test_factory_initialization(self):
        """Test factory initializes with all expected strategies"""
        factory = StrategyFactory()
        
        # Check that strategies are registered
        assert len(factory.strategies) > 0
        
        # Check for specific strategy types
        strategy_types = [type(s).__name__ for s in factory.strategies]
        expected_types = [
            'AddTextStrategy', 'OverlayTextStrategy',
            'AddVideoStrategy', 'OverlayVideoStrategy',
            'AddAudioStrategy', 'OverlayAudioStrategy'
        ]
        
        for expected_type in expected_types:
            assert expected_type in strategy_types
    
    def test_get_strategy_text_add(self):
        """Test getting strategy for text addition"""
        factory = StrategyFactory()
        command = Command(
            operation="add",
            left_operand={"type": "text", "value": "Hello"},
            right_operand={"type": "text", "value": " World"}
        )
        
        strategy = factory.get_strategy(command)
        
        assert strategy is not None
        assert isinstance(strategy, AddTextStrategy)
    
    def test_get_strategy_text_overlay(self):
        """Test getting strategy for text overlay"""
        factory = StrategyFactory()
        command = Command(
            operation="overlay",
            left_operand={"type": "text", "value": "WATERMARK"},
            right_operand={"type": "video", "path": "/video.mp4"}
        )
        
        strategy = factory.get_strategy(command)
        
        assert strategy is not None
        assert isinstance(strategy, OverlayTextStrategy)
    
    def test_get_strategy_video_audio_overlay(self):
        """Test getting strategy for video-audio overlay"""
        factory = StrategyFactory()
        command = Command(
            operation="overlay",
            left_operand={"type": "video", "path": "/video.mp4"},
            right_operand={"type": "audio", "path": "/audio.mp3"}
        )
        
        strategy = factory.get_strategy(command)
        
        assert strategy is not None
        assert isinstance(strategy, OverlayVideoStrategy)
    
    def test_get_strategy_video_add(self):
        """Test getting strategy for video concatenation"""
        factory = StrategyFactory()
        command = Command(
            operation="add",
            left_operand={"type": "video", "path": "/video1.mp4"},
            right_operand={"type": "video", "path": "/video2.mp4"}
        )
        
        strategy = factory.get_strategy(command)
        
        assert strategy is not None
        assert isinstance(strategy, AddVideoStrategy)
    
    def test_get_strategy_audio_add(self):
        """Test getting strategy for audio concatenation"""
        factory = StrategyFactory()
        command = Command(
            operation="add",
            left_operand={"type": "audio", "path": "/audio1.mp3"},
            right_operand={"type": "audio", "path": "/audio2.mp3"}
        )
        
        strategy = factory.get_strategy(command)
        
        assert strategy is not None
        assert isinstance(strategy, AddAudioStrategy)
    
    def test_get_strategy_audio_overlay(self):
        """Test getting strategy for audio mixing"""
        factory = StrategyFactory()
        command = Command(
            operation="overlay",
            left_operand={"type": "audio", "path": "/audio1.mp3"},
            right_operand={"type": "audio", "path": "/audio2.mp3"}
        )
        
        strategy = factory.get_strategy(command)
        
        assert strategy is not None
        assert isinstance(strategy, OverlayAudioStrategy)
    
    def test_get_strategy_unsupported_combination(self):
        """Test getting strategy for unsupported combination"""
        factory = StrategyFactory()
        command = Command(
            operation="add",
            left_operand={"type": "video", "path": "/video.mp4"},
            right_operand={"type": "text", "value": "Hello"}
        )
        
        strategy = factory.get_strategy(command)
        assert strategy is None
    
    def test_get_strategy_invalid_operation(self):
        """Test getting strategy for invalid operation"""
        factory = StrategyFactory()
        command = Command(
            operation="invalid_operation",
            left_operand={"type": "text", "value": "Hello"},
            right_operand={"type": "text", "value": " World"}
        )
        
        strategy = factory.get_strategy(command)
        assert strategy is None
    
    def test_register_strategy(self):
        """Test registering a new strategy"""
        factory = StrategyFactory()
        initial_count = len(factory.strategies)
        
        # Create a mock strategy
        class MockStrategy(BaseStrategy):
            def supports(self, command: Command) -> bool:
                return command.operation == "mock"
            
            def execute(self, command: Command) -> Optional[Dict[str, Any]]:
                return {"type": "mock", "bytes": b"mock_data", "size": 9}
        
        mock_strategy = MockStrategy()
        factory.register_strategy(mock_strategy)
        
        assert len(factory.strategies) == initial_count + 1
        assert mock_strategy in factory.strategies
    
    def test_list_supported_operations(self):
        """Test listing supported operations"""
        factory = StrategyFactory()
        supported = factory.list_supported_operations()
        
        assert isinstance(supported, list)
        assert len(supported) > 0
        
        # Check for some expected combinations
        expected_operations = [
            "add_text_text",
            "overlay_text_video",
            "overlay_video_audio"
        ]
        
        for expected in expected_operations:
            assert expected in supported
    
    def test_strategy_selection_priority(self):
        """Test that the first matching strategy is selected"""
        factory = StrategyFactory()
        command = Command(
            operation="add",
            left_operand={"type": "text", "value": "Hello"},
            right_operand={"type": "text", "value": " World"}
        )
        
        # Get strategy twice to ensure consistency
        strategy1 = factory.get_strategy(command)
        strategy2 = factory.get_strategy(command)
        
        assert strategy1 is not None
        assert strategy2 is not None
        assert type(strategy1) == type(strategy2)
        assert isinstance(strategy1, AddTextStrategy)