from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Command:
    """
    Represents a processed command from the interpreter.
    """
    operation: str
    left_operand: Dict[str, Any]
    right_operand: Dict[str, Any]
    
    def get_operation_type(self) -> str:
        """Get the operation type (add, overlay, etc.)"""
        return self.operation
    
    def get_left_type(self) -> str:
        """Get the type of the left operand"""
        return self.left_operand.get("type", "")
    
    def get_right_type(self) -> str:
        """Get the type of the right operand"""
        return self.right_operand.get("type", "")
    
    def get_strategy_key(self) -> str:
        """
        Generate a strategy key based on operation and operand types.
        
        Returns:
            String in format: "operation_lefttype_righttype"
        """
        return f"{self.operation}_{self.get_left_type()}_{self.get_right_type()}"
    
    def __str__(self) -> str:
        return f"Command({self.operation}: {self.get_left_type()} + {self.get_right_type()})"