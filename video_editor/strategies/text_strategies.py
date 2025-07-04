from typing import Dict, Any, Optional
from video_editor.core.command import Command
from video_editor.strategies.base_strategy import BaseStrategy
from video_editor.utils.logger import logger

class AddTextStrategy(BaseStrategy):
    """
    Strategy for adding text to text (concatenation).
    """
    
    def supports(self, command: Command) -> bool:
        return (command.get_operation_type() == "add" and 
                command.get_left_type() == "text" and 
                command.get_right_type() == "text")
    
    def execute(self, command: Command) -> Optional[Dict[str, Any]]:
        try:
            logger.info("Executing text addition (concatenation)")
            
            left_value = command.left_operand.get("value", "")
            right_value = command.right_operand.get("value", "")
            
            # Simple text concatenation
            result_text = left_value + right_value
            
            # Convert to bytes
            result_bytes = result_text.encode('utf-8')
            
            logger.debug(f"Text concatenation result: '{result_text}'")
            
            return self._create_result(
                media_type="text",
                data=result_bytes,
                metadata={
                    "original_left": left_value,
                    "original_right": right_value,
                    "operation": "concatenation"
                }
            )
            
        except Exception as e:
            logger.error(f"Error in text addition: {e}")
            return None

class OverlayTextStrategy(BaseStrategy):
    """
    Strategy for overlaying text on video (watermark).
    """
    
    def supports(self, command: Command) -> bool:
        return (command.get_operation_type() == "overlay" and 
                command.get_left_type() == "text" and 
                command.get_right_type() == "video")
    
    def execute(self, command: Command) -> Optional[Dict[str, Any]]:
        try:
            logger.info("Executing text overlay on video (watermark)")
            
            text_value = command.left_operand.get("value", "")
            video_path = command.right_operand.get("path", "")
            
            # For now, simulate watermark creation
            # In a real implementation, this would use FFmpeg or similar
            logger.debug(f"Adding watermark '{text_value}' to video: {video_path}")
            
            # Simulate processing and return mock result
            result_data = f"WATERMARKED_VIDEO_DATA_WITH_TEXT_{text_value}".encode('utf-8')
            
            return self._create_result(
                media_type="video",
                data=result_data,
                metadata={
                    "watermark_text": text_value,
                    "original_video": video_path,
                    "operation": "text_watermark"
                }
            )
            
        except Exception as e:
            logger.error(f"Error in text overlay: {e}")
            return None