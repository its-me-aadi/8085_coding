import pytest
import time
from unittest.mock import patch
from video_editor import process_video_request

class TestAPIIntegration:
    """Integration tests for the main API entry point"""
    
    def test_text_addition_end_to_end(self, sample_text_add_request):
        """Test complete text addition workflow"""
        result = process_video_request(sample_text_add_request)
        
        assert result is not None
        assert result["type"] == "text"
        assert result["bytes"] == b"Hello World"
        assert result["size"] == 11
        assert "metadata" in result
        assert result["metadata"]["operation"] == "concatenation"
        assert result["metadata"]["original_left"] == "Hello"
        assert result["metadata"]["original_right"] == " World"
    
    def test_text_watermark_end_to_end(self, sample_text_overlay_request):
        """Test complete text watermark workflow"""
        result = process_video_request(sample_text_overlay_request)
        
        assert result is not None
        assert result["type"] == "video"
        assert result["size"] > 0
        assert "metadata" in result
        assert result["metadata"]["operation"] == "text_watermark"
        assert result["metadata"]["watermark_text"] == "WATERMARK"
        assert result["metadata"]["original_video"] == "/path/to/video.mp4"
    
    def test_video_audio_overlay_end_to_end(self, sample_video_audio_overlay_request):
        """Test complete video-audio overlay workflow"""
        result = process_video_request(sample_video_audio_overlay_request)
        
        assert result is not None
        assert result["type"] == "video"
        assert result["size"] > 0
        assert "metadata" in result
        assert result["metadata"]["operation"] == "audio_overlay"
        assert result["metadata"]["video_source"] == "/path/to/video.mp4"
        assert result["metadata"]["audio_source"] == "/path/to/audio.mp3"
    
    def test_invalid_request_end_to_end(self, invalid_request_missing_field):
        """Test invalid request handling end-to-end"""
        result = process_video_request(invalid_request_missing_field)
        assert result is None
    
    def test_unsupported_operation_end_to_end(self):
        """Test unsupported operation handling end-to-end"""
        request = {
            "operation": "add",
            "left": {"type": "video", "path": "/video.mp4"},
            "right": {"type": "text", "value": "Hello"}
        }
        
        result = process_video_request(request)
        assert result is None
    
    def test_all_supported_text_operations(self):
        """Test all supported text operations"""
        # Text concatenation
        request = {
            "operation": "add",
            "left": {"type": "text", "value": "Part1"},
            "right": {"type": "text", "value": "Part2"}
        }
        result = process_video_request(request)
        assert result is not None
        assert result["bytes"] == b"Part1Part2"
        
        # Text watermark
        request = {
            "operation": "overlay",
            "left": {"type": "text", "value": "COPYRIGHT"},
            "right": {"type": "video", "path": "/sample.mp4"}
        }
        result = process_video_request(request)
        assert result is not None
        assert result["type"] == "video"
    
    def test_all_supported_video_operations(self):
        """Test all supported video operations"""
        # Video concatenation
        request = {
            "operation": "add",
            "left": {"type": "video", "path": "/video1.mp4"},
            "right": {"type": "video", "path": "/video2.mp4"}
        }
        result = process_video_request(request)
        assert result is not None
        assert result["type"] == "video"
        assert result["metadata"]["operation"] == "video_concatenation"
        
        # Video-audio overlay
        request = {
            "operation": "overlay",
            "left": {"type": "video", "path": "/video.mp4"},
            "right": {"type": "audio", "path": "/audio.mp3"}
        }
        result = process_video_request(request)
        assert result is not None
        assert result["type"] == "video"
        assert result["metadata"]["operation"] == "audio_overlay"
    
    def test_all_supported_audio_operations(self):
        """Test all supported audio operations"""
        # Audio concatenation
        request = {
            "operation": "add",
            "left": {"type": "audio", "path": "/audio1.mp3"},
            "right": {"type": "audio", "path": "/audio2.mp3"}
        }
        result = process_video_request(request)
        assert result is not None
        assert result["type"] == "audio"
        assert result["metadata"]["operation"] == "audio_concatenation"
        
        # Audio mixing
        request = {
            "operation": "overlay",
            "left": {"type": "audio", "path": "/base.mp3"},
            "right": {"type": "audio", "path": "/overlay.mp3"}
        }
        result = process_video_request(request)
        assert result is not None
        assert result["type"] == "audio"
        assert result["metadata"]["operation"] == "audio_mixing"
    
    def test_performance_timing(self, sample_text_add_request):
        """Test that performance timing is recorded"""
        start_time = time.time()
        result = process_video_request(sample_text_add_request)
        end_time = time.time()
        
        assert result is not None
        # Processing should be fast for our mock implementation
        assert (end_time - start_time) < 1.0  # Less than 1 second
    
    def test_empty_text_values(self):
        """Test handling of empty text values"""
        request = {
            "operation": "add",
            "left": {"type": "text", "value": ""},
            "right": {"type": "text", "value": "OnlyRight"}
        }
        
        result = process_video_request(request)
        assert result is not None
        assert result["bytes"] == b"OnlyRight"
    
    def test_special_characters_in_text(self):
        """Test handling of special characters in text"""
        request = {
            "operation": "add",
            "left": {"type": "text", "value": "Hello 🌍"},
            "right": {"type": "text", "value": " & Special chars: !@#$%"}
        }
        
        result = process_video_request(request)
        assert result is not None
        expected = "Hello 🌍 & Special chars: !@#$%".encode('utf-8')
        assert result["bytes"] == expected
    
    @patch('video_editor.core.interpreter.Interpreter.interpret')
    def test_interpreter_failure_handling(self, mock_interpret, sample_text_add_request):
        """Test handling when interpreter fails"""
        mock_interpret.return_value = None
        
        result = process_video_request(sample_text_add_request)
        assert result is None
    
    @patch('video_editor.core.processor.Processor.process_command')
    def test_processor_failure_handling(self, mock_process, sample_text_add_request):
        """Test handling when processor fails"""
        mock_process.return_value = None
        
        result = process_video_request(sample_text_add_request)
        assert result is None
    
    def test_exception_handling_in_main_function(self):
        """Test exception handling in main process_video_request function"""
        # Pass invalid input type to trigger exception
        result = process_video_request("not_a_dict")
        assert result is None
    
    def test_multiple_requests_independence(self):
        """Test that multiple requests don't interfere with each other"""
        request1 = {
            "operation": "add",
            "left": {"type": "text", "value": "First"},
            "right": {"type": "text", "value": "Request"}
        }
        
        request2 = {
            "operation": "add",
            "left": {"type": "text", "value": "Second"},
            "right": {"type": "text", "value": "Request"}
        }
        
        result1 = process_video_request(request1)
        result2 = process_video_request(request2)
        
        assert result1 is not None
        assert result2 is not None
        assert result1["bytes"] == b"FirstRequest"
        assert result2["bytes"] == b"SecondRequest"
        
        # Results should be independent
        assert result1 != result2