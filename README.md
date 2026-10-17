# Flask Chatbot Application

A simple Flask-based chatbot application that interacts with the OpenAI API (via the University of Florida's AI endpoint) to provide conversational responses.

## Features

- Conversational AI with context retention
- Session-based conversation history
- Configurable model via environment variables
- RESTful API endpoints for chat and session reset
- Error handling and input validation
- Conversation history limits to prevent excessive storage usage

## Requirements

- Python 3.8+
- Flask
- Flask-Session
- OpenAI Python client
- HTTPX

See `requirements.txt` for specific versions.

## Installation

1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set required environment variables:
   - `UF_API_KEY`: Your University of Florida AI API key
   - `SECRET_KEY`: Flask secret key (defaults to "dev-secret-key" for development)
   - Optional: `OPENAI_MODEL` (defaults to "gpt-oss-120b")

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `UF_API_KEY` | University of Florida AI API key (required) | - |
| `SECRET_KEY` | Flask secret key for session signing | "dev-secret-key" |
| `OPENAI_MODEL` | Model name to use with the OpenAI API | "gpt-oss-120b" |

## Usage

1. Set the required environment variables (especially `UF_API_KEY`)
2. Run the application:
   - Development: `python app.py`
   - Production: Use Gunicorn or another WSGI server (see `gunicorn_config.py` and `flask_app.service` for examples)
3. Access the web interface at `http://localhost:8081` (or configured port)
4. API endpoints:
   - `GET /`: Serves the main HTML interface
   - `POST /chat`: Send a message to the chatbot
     - Request body: `{"message": "your message here"}`
     - Response: `{"response": "bot's response"}`
   - `POST /reset`: Reset the conversation session

## Project Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Main HTML interface
├── static/             # Static assets (CSS, JS, images)
├── flask_session/      # Server-side session storage
├── gunicorn_config.py  # Gunicorn configuration
├── flask_app.service   # Systemd service file (example)
└── nginx_custom.conf   # Nginx configuration (example)
```

## Improvements in Latest Version

See `IMPROVEMENTS_SUMMARY.md` for a detailed list of recent improvements, including:
- Removal of unnecessary proxy environment variable handling
- Added startup validation for required API key
- Implemented request validation and error handling
- Added conversation history limits
- Made model name configurable
- Enhanced input sanitization

## License

This project is proprietary and intended for internal use.

## Contact

For questions or support, please contact the maintainers.
