# AI Chat Assistant

A modern, Claude-inspired chat interface built with Flask and Ollama, featuring real-time streaming responses and code syntax highlighting.

## Features

- 🎨 Modern, clean UI design
- 💬 Real-time message streaming
- 🎨 Code syntax highlighting with line numbers
- 🌡️ Temperature control
- 🤖 Multiple model support
- 📋 Code copy functionality
- 💫 Smooth animations

## Requirements

- Python 3.8+
- Flask
- Ollama
- One of these models installed:
  - deepseek-r1:7b
  - phi4
  - openhermes2.5-mistral
  - qwen2:32b

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-chat-assistant.git
cd ai-chat-assistant
```

### 2. Install Ollama

#### For macOS:
```bash
# Using Homebrew
brew install ollama

# Start Ollama service
ollama serve
```

#### For Linux:
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

#### For Windows:
Download and install from [Ollama's official website](https://ollama.ai/download)

### 3. Install Required Models

```bash
# Install the models you want to use
ollama pull deepseek-r1:7b
ollama pull phi4
ollama pull openhermes
ollama pull qwen2.5:32b
```

### 4. Set Up Python Environment

```bash
# Create virtual environment
python -m venv fresh_env

# Activate virtual environment
source fresh_env/bin/activate  # On Unix/Mac
# or
fresh_env\Scripts\activate     # On Windows

# Install requirements
pip install -r requirements.txt
```

## Running the Application

1. Make sure Ollama is running:
```bash
ollama serve
```

2. In a new terminal, activate the virtual environment:
```bash
source fresh_env/bin/activate  # On Unix/Mac
# or
fresh_env\Scripts\activate     # On Windows
```

3. Run the Flask app:
```bash
python run.py
```

4. Open your browser and go to:
```
http://localhost:5000
```

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

## Usage

1. Select your preferred model from the dropdown
2. Adjust temperature if needed (higher = more creative, lower = more focused)
3. Type your message and press Enter or click Send
4. For code blocks:
   - Syntax highlighting is automatic
   - Click "Copy code" to copy code snippets
   - Line numbers are included for reference

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```bash
   # Check if Ollama is running
   ps aux | grep ollama
   # Start if not running
   ollama serve
   ```

2. **Model Not Found**
   ```bash
   # List installed models
   ollama list
   # Pull missing model
   ollama pull model_name
   ```

3. **Flask App Issues**
   ```bash
   # Make sure you're in virtual environment
   source fresh_env/bin/activate
   # Verify installations
   pip list
   ```

4. **Port Already in Use**
   ```bash
   # Find and kill process using port 5000
   lsof -i :5000
   kill -9 PID
   ```

### Logs

- Check Ollama logs:
  ```bash
  journalctl -u ollama
  ```
- Check Flask logs in terminal where you run the app

## License

MIT 

## Data Privacy & Security

### Local Processing
- All chat processing is done **locally** on your machine
- No data is sent to external servers or cloud services
- Ollama runs completely offline once models are downloaded
- Chat history is stored only in browser session (cleared on browser close)

### Data Flow
1. User input stays within your local network
2. Messages are processed by Ollama locally
3. No data logging or persistence by default
4. No external API calls or tracking

### Model Storage
- Models are downloaded once and stored locally at:
  - Linux: `~/.ollama/models`
  - macOS: `~/.ollama/models`
  - Windows: `C:\Users\username\.ollama\models`

### Network Usage
- Internet connection needed only for:
  - Initial model downloads
  - Updating Ollama software
- No internet required for chat functionality

### Security Considerations
- All processing happens on localhost (127.0.0.1)
- Default port 11434 for Ollama
- Flask runs on localhost:5000
- No external authentication required
- Recommended to run behind firewall

### Data Isolation
- No cloud sync
- No telemetry
- No usage tracking
- No data sharing between sessions

### Best Practices
1. Run behind firewall
2. Don't expose ports to public internet
3. Keep Ollama and models updated
4. Review model licenses for usage terms
5. Clear browser data to remove chat history

This application prioritizes privacy by keeping all processing local and avoiding any external data transmission beyond initial model downloads. 