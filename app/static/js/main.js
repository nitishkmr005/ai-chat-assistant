// Move copyCode function outside DOMContentLoaded
function copyCode(button) {
    const codeBlock = button.closest('.code-block');
    const code = codeBlock.querySelector('code').innerText;
    
    navigator.clipboard.writeText(code).then(() => {
        const originalText = button.innerText;
        button.innerText = 'Copied!';
        button.style.backgroundColor = '#30A46C';
        button.style.borderColor = '#30A46C';
        button.style.color = '#fff';
        
        setTimeout(() => {
            button.innerText = originalText;
            button.style.backgroundColor = '';
            button.style.borderColor = '';
            button.style.color = '';
        }, 2000);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const modelSelect = document.getElementById('model-select');
    const temperatureInput = document.getElementById('temperature');
    const temperatureValue = document.getElementById('temperature-value');

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });

    // Update temperature value display
    temperatureInput.addEventListener('input', function() {
        temperatureValue.textContent = this.value;
    });

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
        messageDiv.innerHTML = `
            <div class="avatar">${isUser ? '👤' : '🤖'}</div>
            <div class="message-content">${content}</div>
        `;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, true);
        userInput.value = '';
        userInput.style.height = 'auto';

        // Create streaming response
        const response = new EventSource(`/chat?message=${encodeURIComponent(message)}&model=${modelSelect.value}&temperature=${temperatureInput.value}`);
        
        let currentMessage = document.createElement('div');
        currentMessage.className = 'message assistant';
        currentMessage.innerHTML = `
            <div class="avatar">🤖</div>
            <div class="message-content"></div>
        `;
        messagesContainer.appendChild(currentMessage);

        let messageContent = currentMessage.querySelector('.message-content');
        
        response.onmessage = function(e) {
            if (e.data) {
                try {
                    const data = JSON.parse(e.data);
                    if (data.text) {
                        messageContent.innerHTML = data.text;
                        messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    }
                } catch (error) {
                    console.log('Received initial connection message');
                }
            }
        };

        response.onerror = function() {
            response.close();
        };
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}); 