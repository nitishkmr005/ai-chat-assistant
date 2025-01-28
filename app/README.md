# AI Chat Assistant - Code Explanation

## How the Code Works

### 1. Project Structure
```
app/
├── __init__.py          # Flask app initialization
├── routes.py            # Main logic and API endpoints
├── static/             
│   ├── css/            # Styling
│   │   └── style.css
│   └── js/             # Frontend functionality
│       └── main.js
└── templates/          # HTML templates
    ├── base.html
    └── chat.html
```

### 2. Core Components

#### `__init__.py`
```python
# Creates and configures the Flask application
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.routes import main
    app.register_blueprint(main)
    return app
```

#### `routes.py`
The main logic handler:
1. Handles web routes (`/` and `/chat`)
2. Processes messages
3. Communicates with Ollama
4. Formats responses

Key functions:
```python
@main.route('/')
def index():
    # Renders the chat interface
    return render_template('chat.html')

@main.route('/chat')
def chat():
    # 1. Gets user message
    # 2. Sends to Ollama
    # 3. Streams response back
```

#### `chat.html`
The user interface:
1. Message input area
2. Model selection dropdown
3. Temperature control
4. Chat history display

### 3. Data Flow

1. **User Input → Server**
   ```javascript
   // main.js
   async function sendMessage() {
       // 1. Get user message
       // 2. Send to server via EventSource
       // 3. Display response in real-time
   }
   ```

2. **Server → Ollama**
   ```python
   # routes.py
   response = requests.post(
       'http://localhost:11434/api/generate',
       json={
           'model': model,
           'prompt': message,
           'stream': True
       }
   )
   ```

3. **Ollama → User**
   ```python
   def generate():
       # Stream responses back to user
       # Format code blocks
       # Handle markdown
   ```

### 4. Key Features Explained

#### Real-time Streaming
- Uses Server-Sent Events (SSE)
- Updates message as AI generates it
- No page reloads needed

#### Code Highlighting
```python
def format_message(content):
    # 1. Detects code blocks
    # 2. Adds syntax highlighting
    # 3. Adds copy buttons
    # 4. Adds line numbers
```

#### Temperature Control
- Affects AI response randomness
- 0.0 = More focused
- 1.0 = More creative

### 5. Frontend Components

#### CSS Structure
```css
/* Key sections in style.css */
.chat-container    /* Main chat area */
.message          /* Individual messages */
.code-block       /* Code formatting */
.input-container  /* User input area */
```

#### JavaScript Functions
```javascript
// Main functions in main.js
sendMessage()      // Handles message sending
addMessage()       // Adds messages to chat
copyCode()         // Handles code copying
```

### 6. How to Modify

#### Adding Features
1. Add route in `routes.py`
2. Add UI in `chat.html`
3. Add styling in `style.css`
4. Add functionality in `main.js`

#### Changing Models
1. Update model list in `chat.html`
2. Update default in `routes.py`

### 7. Error Handling

```python
try:
    # Main logic
except Exception as e:
    # Returns error to user
    return jsonify({'error': str(e)})
```

### 8. Development Tips

1. Check Flask logs for backend issues
2. Use browser console for frontend debugging
3. Test with different message types
4. Verify Ollama connection

### 9. Common Customizations

1. Change default model
2. Adjust temperature range
3. Modify UI styling
4. Add new message types
5. Customize code highlighting

This documentation should help beginners understand the codebase structure and flow. Each component's purpose is explained with relevant code examples. 