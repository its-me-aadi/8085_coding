from typing import Dict, Any, Optional
from video_editor.core.command import Command
from video_editor.strategies.strategy_factory import StrategyFactory
from video_editor.utils.logger import logger

class Processor:
    """
    Processes commands by selecting and executing appropriate strategies.
    """
    
    def __init__(self):
        self.strategy_factory = StrategyFactory()
    
    def process_command(self, command: Command) -> Optional[Dict[str, Any]]:
        """
        Process a command using the appropriate strategy.
        
        Args:
            command: The command to process
            
        Returns:
            Dictionary with processed result or None on failure
        """
        try:
            logger.info(f"Processing command: {command}")
            
            # Get the appropriate strategy
            strategy = self.strategy_factory.get_strategy(command)
            
            if strategy is None:
                logger.error(f"No strategy found for command: {command.get_strategy_key()}")
                return None
            
            logger.debug(f"Using strategy: {strategy.__class__.__name__}")
            
            # Execute the strategy
            result = strategy.execute(command)
            
            if result is None:
                logger.error("Strategy execution failed")
                return None
            
            logger.info("Command processed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            return None