# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial implementation of Flask chatbot application

## [2026-10-17] - Version 1.1.0

### Fixed
- Removed unnecessary proxy environment variable unsetting code that was redundant with `httpx.Client(trust_env=False)`
- Added startup validation for required `UF_API_KEY` environment variable
- Implemented comprehensive request validation for `/chat` endpoint:
  - Content-Type validation (must be application/json)
  - Required field validation ("message" must exist)
  - Input validation (message must be non-empty string)
- Added conversation history limits to prevent unbounded session growth:
  - Maximum 21 messages (1 system message + 10 exchanges)
  - History trimming preserves system message and most recent conversations
- Enhanced error handling for OpenAI API calls:
  - Try/except block around API calls
  - Error logging (using print for development)
  - Generic error responses to avoid leaking internal details
- Made model name configurable via `OPENAI_MODEL` environment variable
- Added input sanitization (whitespace stripping on user messages)

### Changed
- Improved code organization and documentation
- Updated application to be more robust and production-ready

### Removed
- Manual proxy environment variable cleanup loop (4 lines)

## [2026-10-16] - Version 1.0.0

### Added
- Initial Flask chatbot application
- Basic chat functionality with OpenAI API
- Session-based conversation history
- Simple HTML interface
- Session reset functionality
- Gunicorn configuration for production deployment