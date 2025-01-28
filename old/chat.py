import streamlit as st
# Set page config first, before any other Streamlit commands
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import json
import requests
from datetime import datetime
import time
import pyperclip
from io import BytesIO
import base64
import markdown
import pygments
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
import re

def add_custom_css():
    pygments_css = HtmlFormatter().get_style_defs('.highlight')
    
    st.markdown(
        f"""
        <style>
        /* Base Theme */
        .stApp {{
            background-color: #2C3338 !important;
            font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }}

        /* Top Navigation */
        .top-nav {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: #2C3338;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            padding: 0 20px;
            z-index: 1000;
        }}

        .model-info {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #E6E6E6;
        }}

        /* Main Chat Container */
        .main-container {{
            max-width: 1000px;
            margin: 60px auto 100px auto;
            padding: 0;
            height: calc(100vh - 160px);
        }}

        /* Message Styling */
        .chat-message {{
            padding: 20px 32px;
            background: transparent;
            transition: background-color 0.3s ease;
        }}

        .chat-message:hover {{
            background: rgba(255,255,255,0.02);
        }}

        .chat-message.user {{
            background: #343541;
        }}

        .chat-message.assistant {{
            background: #2C3338;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}

        /* Message Content */
        .message {{
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            gap: 24px;
            color: #ECECF1;
            font-size: 16px;
            line-height: 1.6;
        }}

        /* Avatar */
        .avatar {{
            width: 36px;
            height: 36px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
            background: #444654;
        }}

        .chat-message.user .avatar {{
            background: #444654;
        }}

        /* Message Text */
        .message-content {{
            flex-grow: 1;
            overflow-x: auto;
            color: #ECECF1;
        }}

        .message-content p {{
            margin-bottom: 16px;
        }}

        /* Code Blocks */
        .code-block {{
            background: #444654;
            border-radius: 6px;
            padding: 16px;
            margin: 16px 0;
            position: relative;
        }}

        .code-block pre {{
            margin: 0;
            padding: 8px 0;
            overflow-x: auto;
        }}

        .code-block code {{
            font-family: 'Söhne Mono', Monaco, Andale Mono, Ubuntu Mono, monospace;
            font-size: 14px;
            line-height: 1.5;
            color: #ECECF1;
        }}

        /* Input Area */
        .chat-input-container {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(180deg, rgba(44,51,56,0) 0%, #2C3338 50%);
            padding: 24px;
        }}

        .input-wrapper {{
            max-width: 800px;
            margin: 0 auto;
            position: relative;
        }}

        .stTextInput input {{
            background: #40414F !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 12px !important;
            padding: 16px !important;
            color: #ECECF1 !important;
            font-size: 16px !important;
            line-height: 1.5 !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
        }}

        .stTextInput input:focus {{
            border-color: #9B9BA7 !important;
            box-shadow: 0 0 0 2px rgba(155,155,167,0.2) !important;
        }}

        /* Actions */
        .message-actions {{
            margin-top: 8px;
            display: flex;
            gap: 8px;
            opacity: 0;
            transition: opacity 0.2s ease;
        }}

        .chat-message:hover .message-actions {{
            opacity: 1;
        }}

        .action-button {{
            background: transparent;
            border: 1px solid rgba(255,255,255,0.2);
            padding: 4px 8px;
            border-radius: 4px;
            color: #9B9BA7;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .action-button:hover {{
            background: rgba(155,155,167,0.1);
            color: #ECECF1;
        }}

        /* Hide Streamlit Components */
        #MainMenu, footer, .stDeployButton {{
            display: none !important;
        }}

        {pygments_css}
        </style>
        """,
        unsafe_allow_html=True
    )

def detect_code(text):
    """Detect and format code blocks in the text"""
    code_pattern = r'```(\w+)?\n(.*?)\n```'
    
    def format_code(match):
        language = match.group(1) or ''
        code = match.group(2)
        return f'<div class="code-block"><div class="language-tag">{language}</div><pre><code>{code}</code></pre></div>'
    
    return re.sub(code_pattern, format_code, text, flags=re.DOTALL)

def copy_to_clipboard(text):
    pyperclip.copy(text)

def export_chat_history():
    """Export chat history as JSON"""
    if st.session_state.chat_history:
        chat_json = json.dumps(st.session_state.chat_history, indent=2)
        b64 = base64.b64encode(chat_json.encode()).decode()
        href = f'<a href="data:application/json;base64,{b64}" download="chat_history.json">Download Chat History</a>'
        return href
    return ""

def get_llm_response(prompt, include_history=False, temperature=0.7):
    try:
        # Build context from history if enabled
        if include_history and 'chat_history' in st.session_state:
            context = ""
            last_messages = st.session_state.chat_history[-5:] if len(st.session_state.chat_history) > 5 else st.session_state.chat_history
            for msg in last_messages:
                context += f"{msg['role'].title()}: {msg['content']}\n"
            prompt = f"Previous conversation:\n{context}\nUser: {prompt}\nAssistant:"

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': st.session_state.get('selected_model', 'deepseek-r1:7b'),
                'prompt': prompt,
                'stream': True,
                'temperature': temperature
            },
            stream=True
        )
        
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        yield chunk['response']
        else:
            yield f"Error: Unable to get response from Ollama (Status code: {response.status_code})"
    except Exception as e:
        yield f"Error generating response: {str(e)}"

def get_timestamp():
    return datetime.now().strftime("%I:%M %p")

def format_message_content(content, is_streaming=False):
    """Format message content with enhanced markdown and code highlighting"""
    # For plain text responses, just return the content
    if not any(marker in content for marker in ['```', '#', '*', '|', '>']):
        return content

    # Convert markdown to HTML
    html_content = markdown.markdown(
        content,
        extensions=['fenced_code', 'tables', 'nl2br', 'sane_lists']
    )

    # Process code blocks with syntax highlighting
    def replace_code_block(match):
        language = match.group(1) or 'text'
        code = match.group(2)
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            lexer = TextLexer()
        
        highlighted = highlight(code, lexer, HtmlFormatter())
        return f'''
        <div class="code-block">
            <div class="language-tag">{language}</div>
            {highlighted}
        </div>
        '''

    # Replace code blocks with highlighted versions
    if '```' in content:
        html_content = re.sub(
            r'<pre><code class="language-(\w+)">(.*?)</code></pre>',
            replace_code_block,
            html_content,
            flags=re.DOTALL
        )

    return html_content

def chat_interface():
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'is_typing' not in st.session_state:
        st.session_state.is_typing = False
    if 'include_history' not in st.session_state:
        st.session_state.include_history = True
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = 'deepseek-r1:7b'
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 0.7

    # Create a placeholder for streaming at the bottom of messages
    messages_container = st.container()
    if 'placeholder' not in st.session_state:
        st.session_state.placeholder = st.empty()

    # Model selector with specific models
    models = [
        'deepseek-r1:7b',
        'phi4',
        'openhermes2.5-mistral',
        'qwen2:32b'
    ]
    
    # Add model descriptions for tooltip
    model_descriptions = {
        'deepseek-r1:7b': 'DeepSeek R1 7B - Good for general tasks and coding',
        'phi4': 'Phi-4 - Microsoft\'s latest model, good for reasoning',
        'openhermes': 'OpenHermes 2.5 - Based on Mistral, great for chat',
        'qwen2.5-coder:32b': 'Qwen2 Coder 32B - Specialized for coding tasks'
    }

    # Model selector and temperature in header
    st.markdown('<div class="model-selector-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2,4,2])
    with col1:
        st.selectbox(
            "Model",
            models,
            key='selected_model',
            help="\n".join(f"{k}: {v}" for k, v in model_descriptions.items())
        )
    with col3:
        st.markdown('<div class="temperature-container">', unsafe_allow_html=True)
        st.slider("Temperature", 0.0, 1.0, 0.7, 0.1, key='temperature')
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Top navigation
    st.markdown(
        f"""
        <div class="top-nav">
            <div class="model-info">
                <span>🤖</span>
                <span>{st.session_state.selected_model}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display existing messages
    with messages_container:
        for msg in st.session_state.chat_history:
            role = msg["role"]
            content = format_message_content(msg["content"])
            timestamp = msg.get("timestamp", "")
            
            message_html = f"""
            <div class="chat-message {role}">
                <div class="message">
                    <div class="avatar">{'👤' if role == 'user' else '🤖'}</div>
                    <div class="message-content">
                        {content}
                        <div class="timestamp">{timestamp}</div>
                        <div class="message-actions">
                            <button class="action-button" onclick="navigator.clipboard.writeText(`{msg['content']}`)">Copy</button>
                            {'<button class="action-button" onclick="regenerateResponse()">Regenerate</button>' if role == 'assistant' else ''}
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(message_html, unsafe_allow_html=True)

    # Export chat history button
    if st.session_state.chat_history:
        st.markdown(export_chat_history(), unsafe_allow_html=True)

    # Show typing indicator if needed
    if st.session_state.is_typing:
        st.markdown(
            """
            <div class="chat-message assistant">
                <div class="avatar">🤖</div>
                <div class="message">
                    Typing
                    <div class="loading-indicator">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    def handle_input():
        if st.session_state.chat_input and st.session_state.chat_input.strip():
            user_message = st.session_state.chat_input.strip()
            st.session_state.chat_history.append({
                "role": "user", 
                "content": user_message,
                "timestamp": get_timestamp()
            })
            st.session_state.chat_input = ""

            # Stream the response
            full_response = ""
            placeholder = st.empty()

            for response_chunk in get_llm_response(
                user_message, 
                st.session_state.include_history,
                st.session_state.temperature
            ):
                full_response += response_chunk
                formatted_response = format_message_content(full_response, is_streaming=True)
                placeholder.markdown(
                    f"""
                    <div class="chat-message assistant">
                        <div class="message">
                            <div class="avatar">🤖</div>
                            <div class="message-content">
                                {formatted_response}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                time.sleep(0.01)
            
            # Add complete response to chat history
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": full_response,
                "timestamp": get_timestamp()
            })
            
            placeholder.empty()
            st.rerun()

    # Input field at the bottom
    st.markdown(
        """
        <div class="chat-input-container">
            <div class="input-wrapper">
        """, 
        unsafe_allow_html=True
    )
    st.text_input(
        "",
        placeholder="Message AI Assistant...",
        key="chat_input",
        on_change=handle_input,
        label_visibility="collapsed"
    )
    st.markdown('</div></div>', unsafe_allow_html=True)

def main():
    add_custom_css()
    
    # Create a centered container
    with st.container():
        chat_interface()

if __name__ == "__main__":
    main()