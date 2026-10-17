from flask import Flask, render_template, request, jsonify, session
import os
import httpx
from openai import OpenAI
from flask_session import Session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# Configure server-side session storage
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(os.path.dirname(__file__), 'flask_session')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
Session(app)

# Check for required API key
if "UF_API_KEY" not in os.environ:
    raise RuntimeError("UF_API_KEY environment variable is not set")

# Create HTTP client that ignores proxy environment variables
http_client = httpx.Client(trust_env=False)

# Initialize OpenAI client with UF API
client = OpenAI(
    base_url="https://api.ai.it.ufl.edu",
    api_key=os.environ["UF_API_KEY"],
    http_client=http_client
)

# Maximum conversation history length (system message + 10 exchanges = 21 messages)
MAX_HISTORY_MESSAGES = 21

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Initialize conversation history if not present
    if 'messages' not in session:
        session['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Validate request
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    if "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400
    
    user_message = data["message"]
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({"error": "Message must be a non-empty string"}), 400
    
    # Add user message to history
    session['messages'].append({"role": "user", "content": user_message.strip()})
    
    # Trim history if it exceeds maximum length
    if len(session['messages']) > MAX_HISTORY_MESSAGES:
        # Keep system message and the most recent messages
        system_msg = session['messages'][0]  # System message should be first
        recent_messages = session['messages'][-(MAX_HISTORY_MESSAGES-1):]
        session['messages'] = [system_msg] + recent_messages
    
    try:
        # Create chat completion with configurable model
        model_name = os.environ.get("OPENAI_MODEL", "gpt-oss-120b")
        response = client.chat.completions.create(
            model=model_name,
            messages=session['messages']
        )
        
        bot_response = response.choices[0].message.content
        session['messages'].append({"role": "assistant", "content": bot_response})
        
        return jsonify({"response": bot_response})
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"OpenAI API error: {e}")
        return jsonify({"error": "Failed to generate response"}), 500

@app.route("/reset", methods=["POST"])
def reset_session():
    # Clear the session and reinitialize with system message
    session.clear()
    session['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify({"status": "success", "message": "Session reset"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
