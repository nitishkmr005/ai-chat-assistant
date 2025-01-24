import streamlit as st
import json
import requests
from datetime import datetime

st.set_page_config(layout="wide", page_title="AI Assistant", page_icon="🤖")

def add_custom_css():
    st.markdown(
        """
        <style>
        /* Page Background with subtle gradient */
        .stApp {
            background: linear-gradient(160deg, #1a1a2e 0%, #16213e 100%) !important;
        }
        
        /* Header */
        .stApp header {
            background-color: transparent !important;
            border-bottom: none !important;
        }
        
        /* Hide default title */
        h1 {
            display: none !important;
        }
        
        /* Chat Interface Styling */
        .chat-message {
            display: flex;
            padding: 1.5rem 4rem;
            margin: 0;
            gap: 1.5rem;
            width: 100%;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            transition: background-color 0.3s ease;
        }

        .chat-message:hover {
            background-color: rgba(255,255,255,0.02);
        }

        .chat-message.user {
            background-color: rgba(52,53,65,0.9);
        }

        .chat-message.assistant {
            background-color: rgba(68,70,84,0.9);
        }

        .chat-message .avatar {
            width: 35px;
            height: 35px;
            border-radius: 0.375rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            flex-shrink: 0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            transition: transform 0.2s ease;
        }

        .chat-message:hover .avatar {
            transform: scale(1.05);
        }

        .chat-message .message {
            flex-grow: 1;
            line-height: 1.6;
            color: #ECECF1;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
            font-size: 1rem;
        }

        .timestamp {
            font-size: 0.75rem;
            color: rgba(255,255,255,0.5);
            margin-top: 0.5rem;
        }

        /* Input Container with glass effect */
        .chat-input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 2rem 1rem;
            background: linear-gradient(180deg, rgba(26,26,46,0), rgba(26,26,46,0.9) 40%);
            display: flex;
            justify-content: center;
            z-index: 100;
            backdrop-filter: blur(10px);
        }

        /* Modern Input Field */
        .stTextInput {
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
        }

        .stTextInput input {
            background-color: rgba(64,65,79,0.9) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 1rem !important;
            padding: 1rem 1.5rem !important;
            color: white !important;
            font-size: 1rem !important;
            line-height: 1.5 !important;
            height: auto !important;
            max-height: 200px !important;
            overflow-y: auto !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        }

        .stTextInput input:hover {
            border-color: rgba(255,255,255,0.2) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        }

        .stTextInput input:focus {
            border-color: #10A37F !important;
            box-shadow: 0 0 0 2px rgba(16,163,127,0.2) !important;
            transform: translateY(-1px);
        }

        /* Hide Streamlit Elements */
        #MainMenu, footer, .stDeployButton {
            display: none !important;
        }

        /* Messages Container */
        .main-container {
            max-width: 100%;
            padding-bottom: 120px;
            margin-top: 1rem;
        }

        /* Modern Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(86,88,105,0.5);
            border-radius: 3px;
            transition: background 0.3s ease;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(103,105,128,0.8);
        }

        /* Welcome Message with animation */
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: calc(100vh - 200px);
            color: #ECECF1;
            text-align: center;
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .welcome-title {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            color: #ECECF1;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        .welcome-subtitle {
            font-size: 1.1rem;
            color: #8E8EA0;
            max-width: 600px;
            line-height: 1.6;
        }

        /* Loading indicator */
        .loading-indicator {
            display: inline-block;
            margin-left: 5px;
        }

        .loading-indicator span {
            display: inline-block;
            width: 4px;
            height: 4px;
            background-color: rgba(255,255,255,0.7);
            border-radius: 50%;
            margin: 0 2px;
            animation: bounce 1.4s infinite ease-in-out;
        }

        .loading-indicator span:nth-child(1) { animation-delay: 0s; }
        .loading-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .loading-indicator span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

        /* Context Toggle */
        .context-toggle {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
            background: rgba(255,255,255,0.1);
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .context-toggle:hover {
            background: rgba(255,255,255,0.15);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def get_llm_response(prompt, include_history=False):
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
                'model': 'phi4',
                'prompt': prompt,
                'stream': True
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

def chat_interface():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'is_typing' not in st.session_state:
        st.session_state.is_typing = False
    if 'include_history' not in st.session_state:
        st.session_state.include_history = True

    # Welcome message when no chat history
    if not st.session_state.chat_history:
        st.markdown(
            """
            <div class="welcome-container">
                <div class="welcome-title">AI Assistant</div>
                <div class="welcome-subtitle">
                    Welcome! I'm here to help you with any questions or tasks you have. 
                    Feel free to start a conversation and I'll assist you to the best of my abilities.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Display chat messages
    with st.container():
        # Add context toggle in the header
        st.markdown(
            """
            <style>
            .context-toggle {
                position: fixed;
                top: 1rem;
                right: 1rem;
                z-index: 1000;
                background: rgba(255,255,255,0.1);
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.1);
            }
            .context-toggle:hover {
                background: rgba(255,255,255,0.15);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns([6,1])
        with col2:
            st.markdown(
                f"""
                <div class="context-toggle">
                    <span style="color: #ECECF1; font-size: 0.9rem;">Context</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.toggle("Include context", key="include_history", value=True)

        # Rest of the chat interface
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            role = msg["role"]
            content = msg["content"]
            timestamp = msg.get("timestamp", "")
            st.markdown(
                f"""
                <div class="chat-message {role}">
                    <div class="avatar">{'👤' if role == 'user' else '🤖'}</div>
                    <div class="message">
                        {content}
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Add placeholder for streaming response
        if 'placeholder' not in st.session_state:
            st.session_state.placeholder = st.empty()
        
        # Show typing indicator
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
        
        st.markdown('</div>', unsafe_allow_html=True)

    def handle_input():
        if st.session_state.chat_input and st.session_state.chat_input.strip():
            user_message = st.session_state.chat_input.strip()
            st.session_state.chat_history.append({
                "role": "user", 
                "content": user_message,
                "timestamp": get_timestamp()
            })
            st.session_state.chat_input = ""
            st.session_state.is_typing = True
            
            # Stream the response with context if enabled
            full_response = ""
            for response_chunk in get_llm_response(user_message, st.session_state.include_history):
                full_response += response_chunk
                # Update placeholder with current response
                st.session_state.placeholder.markdown(
                    f"""
                    <div class="chat-message assistant">
                        <div class="avatar">🤖</div>
                        <div class="message">{full_response}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Add complete response to chat history
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": full_response,
                "timestamp": get_timestamp()
            })
            st.session_state.is_typing = False
            st.session_state.placeholder.empty()
            st.rerun()

    # Input field at the bottom
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    st.text_input(
        "",
        placeholder="Type your message here... (Press Enter to send)",
        key="chat_input",
        on_change=handle_input,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.title("AI Assistant")
    add_custom_css()
    chat_interface()

if __name__ == "__main__":
    main()