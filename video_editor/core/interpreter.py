from typing import Dict, Any, Optional
from video_editor.core.command import Command
from video_editor.utils.logger import logger

class Interpreter:
    """
    Interprets JSON requests and converts them into Command objects.
    """
    
    def interpret(self, request: Dict[str, Any]) -> Optional[Command]:
        """
        Interpret a JSON request and return a Command object.
        
        Args:
            request: Dictionary containing the request data
            
        Returns:
            Command object or None if invalid
        """
        try:
            # Validate required fields
            if not self._validate_request(request):
                return None
            
            operation = request.get("operation")
            left = request.get("left")
            right = request.get("right")
            
            logger.debug(f"Interpreting operation: {operation}")
            
            # Create command object
            command = Command(
                operation=operation,
                left_operand=left,
                right_operand=right
            )
            
            logger.info(f"Successfully interpreted {operation} operation")
            return command
            
        except Exception as e:
            logger.error(f"Error interpreting request: {e}")
            return None
    
    def _validate_request(self, request: Dict[str, Any]) -> bool:
        """
        Validate the request structure.
        
        Args:
            request: The request dictionary
            
        Returns:
            True if valid, False otherwise
        """
        # Check for required fields
        required_fields = ["operation", "left", "right"]
        for field in required_fields:
            if field not in request:
                logger.error(f"Missing required field: {field}")
                return False
        
        # Validate operation type
        valid_operations = ["add", "overlay", "merge", "concat"]
        if request["operation"] not in valid_operations:
            logger.error(f"Invalid operation: {request['operation']}")
            return False
        
        # Validate operand structure
        for operand_name in ["left", "right"]:
            operand = request[operand_name]
            if not isinstance(operand, dict):
                logger.error(f"Invalid {operand_name} operand: must be a dictionary")
                return False
            
            if "type" not in operand:
                logger.error(f"Missing 'type' in {operand_name} operand")
                return False
        
        return True