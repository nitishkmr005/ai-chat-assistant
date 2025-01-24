# AI Chat Assistant

A modern, ChatGPT-like interface built with Streamlit and Ollama.

## Features

- 🎨 Modern, responsive UI design
- 💬 Real-time message streaming
- ⚡ Fast response times
- 🔄 Context-aware conversations
- 🕒 Message timestamps
- 💫 Smooth animations and transitions

## Requirements

- Python 3.8+
- Ollama with phi4 model installed

## Installation

### 1. Install Ollama

#### For Linux:
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# In a new terminal, pull the phi4 model
ollama pull phi4
```

#### For Linux (Manual Installation):
```bash
# Download the latest release
curl -L https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64 -o ollama

# Make it executable
chmod +x ollama

# Move it to your path
sudo mv ollama /usr/local/bin

# Start Ollama service
ollama serve

# In a new terminal, pull the phi4 model
ollama pull phi4
```

### 2. Install the Application

1. Clone the repository:
```bash
git clone https://github.com/nitishkmr005/ai-chat-assistant.git
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

2. In a new terminal, run the Streamlit app:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Features

- Modern, ChatGPT-like interface
- Real-time message streaming
- Context toggle for conversation memory
- Timestamps for messages
- Responsive design
- Loading indicators
- Clean, minimal UI

## Git commands

git add .
git commit -m "commit message"
git push -u origin main

### Git new repo

git init
git add .
git commit -m "Initial commit: AI Chat Assistant"
git remote add origin https://github.com/YOUR_USERNAME/ai-chat-assistant.git
git push -u origin main

## Troubleshooting

If you encounter any issues:

1. Make sure Ollama service is running:
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it:
ollama serve
```

2. Verify the phi4 model is installed:
```bash
ollama list
```

3. Check Ollama logs:
```bash
journalctl -u ollama
```

## License

MIT 