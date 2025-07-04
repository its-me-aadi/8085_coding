# Media Manipulator Service

A flexible media processing service that interprets JSON requests and processes them using a strategy pattern based on operation types and media combinations.

## Features

- **Strategy-based processing**: Different strategies for different media type combinations
- **Extensible architecture**: Easy to add new operations and media types
- **Comprehensive logging**: Detailed logging for debugging and monitoring
- **Type safety**: Full type hints throughout the codebase
- **Error handling**: Robust error handling and validation

## Supported Operations

### Add Operations
- **Text + Text**: Concatenates two text strings
- **Video + Video**: Concatenates two video files
- **Audio + Audio**: Concatenates two audio files

### Overlay Operations
- **Text + Video**: Adds text watermark to video
- **Video + Audio**: Adds audio track to video
- **Audio + Audio**: Mixes two audio tracks

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic API

```python
from video_editor import process_video_request

# Example: Text concatenation
request = {
    "operation": "add",
    "left": {"type": "text", "value": "Hello"},
    "right": {"type": "text", "value": " World"}
}

result = process_video_request(request)
if result:
    print(f"Result: {result['bytes'].decode('utf-8')}")
```

### Request Format

All requests must follow this structure:

```json
{
    "operation": "add|overlay|merge|concat",
    "left": {
        "type": "text|video|audio|image",
        "value": "string_value",  // for text
        "path": "/path/to/file"   // for media files
    },
    "right": {
        "type": "text|video|audio|image", 
        "value": "string_value",  // for text
        "path": "/path/to/file"   // for media files
    }
}
```

### Response Format

Successful responses return:

```json
{
    "type": "text|video|audio|image",
    "bytes": "binary_data",
    "size": 1234,
    "metadata": {
        "operation": "operation_type",
        // ... additional metadata
    }
}
```

Failed requests return `None`.

## Examples

### 1. Text Concatenation

```python
request = {
    "operation": "add",
    "left": {"type": "text", "value": "Hello"},
    "right": {"type": "text", "value": " World"}
}
# Result: "Hello World"
```

### 2. Video Watermark

```python
request = {
    "operation": "overlay",
    "left": {"type": "text", "value": "© 2024 My Company"},
    "right": {"type": "video", "path": "/path/to/video.mp4"}
}
# Result: Video with text watermark
```

### 3. Video with Audio

```python
request = {
    "operation": "overlay",
    "left": {"type": "video", "path": "/path/to/video.mp4"},
    "right": {"type": "audio", "path": "/path/to/audio.mp3"}
}
# Result: Video with added audio track
```

## Architecture

The service follows a clean architecture pattern:

```
video_editor/
├── __init__.py                 # Main API entry point
├── core/
│   ├── interpreter.py          # Request interpretation
│   ├── processor.py            # Command processing
│   └── command.py              # Command data structure
├── strategies/
│   ├── base_strategy.py        # Abstract strategy base
│   ├── strategy_factory.py     # Strategy selection
│   ├── text_strategies.py      # Text processing strategies
│   ├── video_strategies.py     # Video processing strategies
│   └── audio_strategies.py     # Audio processing strategies
└── utils/
    └── logger.py               # Logging utilities
```

### Key Components

1. **Interpreter**: Validates and parses JSON requests into Command objects
2. **Processor**: Orchestrates strategy selection and execution
3. **Strategy Factory**: Selects appropriate strategies based on command type
4. **Strategies**: Implement specific media processing logic
5. **Logger**: Provides comprehensive logging throughout the pipeline

## Adding New Strategies

To add support for new operations or media types:

1. **Create a new strategy class**:

```python
from video_editor.strategies.base_strategy import BaseStrategy

class MyNewStrategy(BaseStrategy):
    def supports(self, command: Command) -> bool:
        return (command.get_operation_type() == "my_operation" and 
                command.get_left_type() == "my_media_type")
    
    def execute(self, command: Command) -> Optional[Dict[str, Any]]:
        # Implement your processing logic
        pass
```

2. **Register the strategy**:

```python
# In strategy_factory.py
from .my_strategies import MyNewStrategy

class StrategyFactory:
    def __init__(self):
        self.strategies = [
            # ... existing strategies
            MyNewStrategy(),
        ]
```

## Logging

The service provides detailed logging at different levels:

- **DEBUG**: Detailed execution information
- **INFO**: General operation status
- **WARNING**: Non-critical issues
- **ERROR**: Processing failures
- **SUCCESS**: Successful completion with timing

## Testing

Run the demo script to test all functionality:

```bash
python3 demo.py
```

## Future Enhancements

- **Real media processing**: Integrate with FFmpeg, OpenCV, or similar libraries
- **Asynchronous processing**: Support for long-running operations
- **File I/O**: Direct file input/output support
- **Batch processing**: Multiple operations in a single request
- **Validation**: Advanced media format validation
- **Performance monitoring**: Detailed performance metrics

## Dependencies

Currently minimal dependencies for the core service. For actual media processing, you would add:

- `ffmpeg-python` for video/audio processing
- `opencv-python` for image/video manipulation
- `pillow` for image processing
- `moviepy` for video editing

## License

[Add your license information here]