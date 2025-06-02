# EasyChat
EasyChat is a clean and user-friendly AI chat application built with Python Tkinter, designed to interact with OpenAI GPT models.

## Features

- Clean and modern user interface
- Multi-language support (English/Chinese)
- Customizable API settings (OpenAI API)
- Adjustable font sizes
- Chat history export
- Smart message grouping with timestamps
- Keyboard shortcuts support
- Request rate limiting protection
- Intuitive settings management

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/EasyChat.git
cd EasyChat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python EASYCHAT_V1.py
```

## Usage Guide

### Initial Setup
1. Open the settings (⚙) and configure your OpenAI API key
2. Select your preferred language and font sizes
3. Click "Test Connection" to verify your API settings

### Basic Operations
- **Send Message**: Click Send button or press Ctrl+Enter
- **New Line**: Press Enter
- **Context Menu**: Right-click for copy/paste/select all options
- **Clear Chat**: Click the clear button (🗑)
- **Export Chat**: Click the export button (📁)

### Settings Configuration
- API Settings:
  - API Key
  - API URL
  - Model Selection (e.g., gpt-3.5-turbo, gpt-4)
- Interface Settings:
  - Language Selection
  - Chat Font Size
  - Input Font Size

## Configuration

The application automatically creates `easychat_config.ini` which stores:
- API configurations
- Interface language preference
- Font size settings

## Interface Preview

images/screenshot.png


### Key Components
- **UI Framework**: Python Tkinter
- **API Integration**: OpenAI GPT API
- **Configuration**: ConfigParser
- **Image Handling**: PIL (Pillow)

### Architecture
- Clean separation of UI and business logic
- Event-driven message handling
- Threaded API calls for responsive UI
- Configurable settings management

### Version 1.0.0
- Initial release
- Core chat functionality
- Multi-language support
- Font size customization
- Chat export feature
- Modern UI design
- Rate limiting implementation

