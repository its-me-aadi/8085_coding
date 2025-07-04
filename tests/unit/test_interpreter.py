import pytest
from video_editor.core.interpreter import Interpreter
from video_editor.core.command import Command

class TestInterpreter:
    """Unit tests for the Interpreter class"""
    
    def test_valid_text_add_request(self, interpreter, sample_text_add_request):
        """Test interpreting a valid text addition request"""
        command = interpreter.interpret(sample_text_add_request)
        
        assert command is not None
        assert isinstance(command, Command)
        assert command.operation == "add"
        assert command.left_operand == {"type": "text", "value": "Hello"}
        assert command.right_operand == {"type": "text", "value": " World"}
    
    def test_valid_overlay_request(self, interpreter, sample_text_overlay_request):
        """Test interpreting a valid overlay request"""
        command = interpreter.interpret(sample_text_overlay_request)
        
        assert command is not None
        assert command.operation == "overlay"
        assert command.get_left_type() == "text"
        assert command.get_right_type() == "video"
    
    def test_missing_required_field(self, interpreter, invalid_request_missing_field):
        """Test request missing required field"""
        command = interpreter.interpret(invalid_request_missing_field)
        assert command is None
    
    def test_invalid_operation(self, interpreter, invalid_request_bad_operation):
        """Test request with invalid operation"""
        command = interpreter.interpret(invalid_request_bad_operation)
        assert command is None
    
    def test_missing_operation_field(self, interpreter):
        """Test request missing operation field"""
        request = {
            "left": {"type": "text", "value": "Hello"},
            "right": {"type": "text", "value": " World"}
        }
        command = interpreter.interpret(request)
        assert command is None
    
    def test_missing_left_field(self, interpreter):
        """Test request missing left field"""
        request = {
            "operation": "add",
            "right": {"type": "text", "value": " World"}
        }
        command = interpreter.interpret(request)
        assert command is None
    
    def test_invalid_operand_structure(self, interpreter):
        """Test request with invalid operand structure"""
        request = {
            "operation": "add",
            "left": "not_a_dict",  # Should be a dictionary
            "right": {"type": "text", "value": " World"}
        }
        command = interpreter.interpret(request)
        assert command is None
    
    def test_missing_type_in_operand(self, interpreter):
        """Test operand missing type field"""
        request = {
            "operation": "add",
            "left": {"value": "Hello"},  # Missing "type"
            "right": {"type": "text", "value": " World"}
        }
        command = interpreter.interpret(request)
        assert command is None
    
    def test_all_valid_operations(self, interpreter):
        """Test all valid operations are accepted"""
        valid_operations = ["add", "overlay", "merge", "concat"]
        
        for operation in valid_operations:
            request = {
                "operation": operation,
                "left": {"type": "text", "value": "Hello"},
                "right": {"type": "text", "value": " World"}
            }
            command = interpreter.interpret(request)
            assert command is not None
            assert command.operation == operation
    
    def test_validation_with_valid_request(self, interpreter, sample_text_add_request):
        """Test private validation method with valid request"""
        is_valid = interpreter._validate_request(sample_text_add_request)
        assert is_valid is True
    
    def test_validation_with_invalid_request(self, interpreter, invalid_request_missing_field):
        """Test private validation method with invalid request"""
        is_valid = interpreter._validate_request(invalid_request_missing_field)
        assert is_valid is False
    
    def test_exception_handling(self, interpreter):
        """Test exception handling in interpret method"""
        # Pass None to trigger an exception
        command = interpreter.interpret(None)
        assert command is None
    
    def test_empty_request(self, interpreter):
        """Test completely empty request"""
        command = interpreter.interpret({})
        assert command is None