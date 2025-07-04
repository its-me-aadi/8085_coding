from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from video_editor.core.command import Command

class BaseStrategy(ABC):
    """
    Abstract base class for all media manipulation strategies.
    """
    
    @abstractmethod
    def execute(self, command: Command) -> Optional[Dict[str, Any]]:
        """
        Execute the strategy with the given command.
        
        Args:
            command: The command to execute
            
        Returns:
            Dictionary with result data or None on failure
        """
        pass
    
    @abstractmethod
    def supports(self, command: Command) -> bool:
        """
        Check if this strategy supports the given command.
        
        Args:
            command: The command to check
            
        Returns:
            True if supported, False otherwise
        """
        pass
    
    def _create_result(self, media_type: str, data: bytes, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a standardized result dictionary.
        
        Args:
            media_type: Type of the resulting media (video, audio, image, text)
            data: The binary data of the result
            metadata: Optional metadata about the result
            
        Returns:
            Standardized result dictionary
        """
        result = {
            "type": media_type,
            "bytes": data,
            "size": len(data) if data else 0
        }
        
        if metadata:
            result["metadata"] = metadata
            
        return result