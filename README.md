# AI Chat Assistant

A modern, ChatGPT-like interface built with Flask and Ollama, featuring real-time streaming responses and code syntax highlighting.

## Features

- 🎨 Modern, Claude-inspired UI design
- 💬 Real-time message streaming
- ⚡ Fast response times
- 🔄 Model selection (deepseek, phi4, openhermes, qwen)
- 🌡️ Temperature control
- 📝 Markdown support
- 🎨 Code syntax highlighting
- 💫 Smooth animations and transitions

## Requirements

- Python 3.8+
- Flask
- Ollama with required models installed

## Installation

### 1. Install Ollama

#### For Linux:
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

### 2. Install Required Models
```bash
# Pull the models
ollama pull deepseek-r1:7b
ollama pull phi4
ollama pull openhermes2.5-mistral
ollama pull qwen2:32b
```

### 3. Install the Application

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-chat-assistant.git
cd ai-chat-assistant
```

2. Create a virtual environment and activate it:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. Install the requirements:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure Ollama service is running:
```bash
ollama serve
```

2. Run the Flask app:
```bash
python run.py
```

The app will be available at `http://localhost:5000`

## Features

### UI Features
- Clean, modern interface inspired by Claude
- Real-time message streaming
- Code syntax highlighting with language detection
- Markdown formatting support
- Temperature control slider
- Model selection dropdown
- Responsive design

### Technical Features
- Server-Sent Events (SSE) for streaming
- Markdown parsing and rendering
- Code syntax highlighting using Pygments
- Real-time temperature adjustment
- Multiple model support
- Error handling and recovery

## Project Structure
```
ai-chat-assistant/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── base.html
│       └── chat.html
├── config.py
├── requirements.txt
└── run.py
```

## Troubleshooting

1. Make sure Ollama service is running:
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it:
ollama serve
```

2. Verify the models are installed:
```bash
ollama list
```

3. Check Flask app logs for errors:
```bash
python run.py
```

4. If you see CORS errors, make sure you're accessing the correct URL

## License

MIT 