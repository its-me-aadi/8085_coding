from typing import Optional
from video_editor.core.command import Command
from video_editor.strategies.base_strategy import BaseStrategy
from video_editor.strategies.text_strategies import AddTextStrategy, OverlayTextStrategy
from video_editor.strategies.video_strategies import AddVideoStrategy, OverlayVideoStrategy
from video_editor.strategies.audio_strategies import AddAudioStrategy, OverlayAudioStrategy
from video_editor.utils.logger import logger

class StrategyFactory:
    """
    Factory class to create and manage strategies for different operation-media type combinations.
    """
    
    def __init__(self):
        # Register all available strategies
        self.strategies = [
            # Text strategies
            AddTextStrategy(),
            OverlayTextStrategy(),
            
            # Video strategies  
            AddVideoStrategy(),
            OverlayVideoStrategy(),
            
            # Audio strategies
            AddAudioStrategy(),
            OverlayAudioStrategy(),
        ]
    
    def get_strategy(self, command: Command) -> Optional[BaseStrategy]:
        """
        Get the appropriate strategy for a command.
        
        Args:
            command: The command to find a strategy for
            
        Returns:
            Strategy instance or None if no strategy found
        """
        logger.debug(f"Finding strategy for: {command.get_strategy_key()}")
        
        # Find the first strategy that supports this command
        for strategy in self.strategies:
            if strategy.supports(command):
                logger.debug(f"Found strategy: {strategy.__class__.__name__}")
                return strategy
        
        logger.warning(f"No strategy found for command: {command.get_strategy_key()}")
        return None
    
    def register_strategy(self, strategy: BaseStrategy):
        """
        Register a new strategy.
        
        Args:
            strategy: The strategy to register
        """
        self.strategies.append(strategy)
        logger.info(f"Registered strategy: {strategy.__class__.__name__}")
    
    def list_supported_operations(self) -> list:
        """
        Get a list of all supported operation-media type combinations.
        
        Returns:
            List of supported combinations
        """
        supported = []
        # This would need to be implemented based on each strategy's supports method
        # For now, return a basic list
        return [
            "add_text_text",
            "overlay_text_video", 
            "overlay_video_audio",
            "add_video_video",
            "add_audio_audio",
        ]