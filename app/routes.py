from flask import Blueprint, render_template, jsonify, request, Response
import requests
import json
import markdown
import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer

main = Blueprint('main', __name__)

def format_message(content):
    """Format message with markdown and code highlighting"""
    # Unescape HTML entities before processing
    content = content.replace('&quot;', '"')
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = content.replace('&amp;', '&')
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        content,
        extensions=['fenced_code', 'tables', 'nl2br', 'sane_lists']
    )

    # Process code blocks
    def replace_code_block(match):
        language = match.group(1) or 'text'
        code = match.group(2).strip()
        
        # Unescape HTML entities in code blocks
        code = code.replace('&quot;', '"')
        code = code.replace('&lt;', '<')
        code = code.replace('&gt;', '>')
        code = code.replace('&amp;', '&')
        
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            lexer = TextLexer()
        
        formatter = HtmlFormatter(
            linenos='table',
            cssclass='highlight',
            style='monokai',
            noclasses=False
        )
        
        highlighted = highlight(code, lexer, formatter)
        
        return f'''
        <div class="code-block">
            <div class="code-header">
                <span class="language-tag">{language}</span>
                <button class="copy-button" onclick="copyCode(this)">
                    Copy code
                </button>
            </div>
            {highlighted}
        </div>
        '''

    # Replace code blocks with highlighted versions
    html_content = re.sub(
        r'<pre><code class="language-(\w+)">(.*?)</code></pre>',
        replace_code_block,
        html_content,
        flags=re.DOTALL
    )

    return html_content

@main.route('/')
def index():
    return render_template('chat.html')

@main.route('/chat', methods=['GET', 'POST'])
def chat():
    message = request.args.get('message') if request.method == 'GET' else request.json.get('message')
    model = request.args.get('model', 'deepseek-r1:7b') if request.method == 'GET' else request.json.get('model', 'deepseek-r1:7b')
    temperature = float(request.args.get('temperature', 0.7)) if request.method == 'GET' else float(request.json.get('temperature', 0.7))

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': message,
                'stream': True,
                'temperature': temperature
            },
            stream=True
        )

        def generate():
            # Send response header for SSE
            yield "data: {}\n\n"
            
            current_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        current_response += chunk['response']
                        formatted_response = format_message(current_response)
                        yield f"data: {json.dumps({'text': formatted_response})}\n\n"

        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        return jsonify({'error': str(e)}), 500 