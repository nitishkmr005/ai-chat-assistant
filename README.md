# Ollama Model Explorer

A modern chat interface for exploring and testing different open-source LLMs through Ollama. Built with Flask, this application provides a seamless way to interact with various open-source language models like DeepSeek, Phi-4, OpenHermes, and Qwen.

## Features

- 🤖 Test multiple open-source LLMs in one interface
- 🔄 Easy model switching without restart
- 🌡️ Real-time temperature adjustment for model responses
- 💬 Real-time message streaming
- 🎨 Code syntax highlighting with line numbers
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
  - new-model-name

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
ollama pull new-model-name
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

## Adding New Models

### 1. Download New Model
```bash
# Pull new model from Ollama
ollama pull new-model-name
```

### 2. Update Model Selection in HTML
In `app/templates/chat.html`, add the new model to the dropdown:
```html
<select id="model-select">
    <option value="deepseek-r1:7b">DeepSeek</option>
    <option value="phi4">Phi-4</option>
    <option value="openhermes">OpenHermes</option>
    <option value="qwen2.5:32b">Qwen2</option>
    <option value="new-model-name">New Model Display Name</option>
</select>
```

### 3. Update README
In the Requirements section, add your new model to the list:
```markdown
- One of these models installed:
  - deepseek-r1:7b
  - phi4
  - openhermes
  - qwen2.5:32b
  - new-model-name
```

### 4. Default Model (Optional)
If you want to change the default model, update in `app/routes.py`:
```python
@main.route('/chat', methods=['GET', 'POST'])
def chat():
    # Change default model here
    model = request.args.get('model', 'new-model-name') if request.method == 'GET' \
        else request.json.get('model', 'new-model-name')
```

### Model Compatibility Notes
- Ensure model supports text generation API
- Check model's required parameters (some might need specific temperature ranges)
- Test model's response format compatibility
- Verify model's performance with code generation if needed

### Testing New Model
1. Pull the model using Ollama
2. Add to dropdown in HTML
3. Test with various prompts
4. Verify code highlighting works
5. Check response streaming
6. Test temperature sensitivity

No other code changes are typically needed as the app is designed to work with any Ollama-compatible model. 