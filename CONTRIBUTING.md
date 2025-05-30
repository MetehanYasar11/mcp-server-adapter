# Contributing to MCP Vision Adapter

Thank you for your interest in contributing! This project aims to be a hub for modernizing and connecting classic automation tools, CLIs, and agent-based systems to new LLM/agent environments. Your ideas, code, and feedback are welcome.

## How to Contribute

- **Fork the repository** and create a new branch for your feature or fix.
- **Open a pull request** with a clear description of your changes.
- **Discuss ideas** in GitHub Issues before large changes.
- **Write tests** for new features or bugfixes.
- **Follow code style** (see existing code and `pyproject.toml`).
- **Add documentation** for new features in README or as docstrings.

## Areas to Contribute

- New adapters (CLI, REST, etc.) for different tools/services
- CLI-to-MCP tunnel improvements
- Web UI enhancements
- Example automations (e.g., n8n, Zapier, etc.)
- Integrations with LLMs, OpenAI, or other agent frameworks
- Documentation, tutorials, and usage guides

## Development Setup

1. **Clone the repo:**
   ```sh
   git clone https://github.com/MetehanYasar11/mcp-server-adapter.git
   cd mcp-server-adapter
   ```
2. **Create a virtual environment (recommended):**
   ```sh
   python -m venv .venv
   # or with conda
   conda create -n mcp python=3.10
   conda activate mcp
   ```
3. **Install dependencies:**
   ```sh
   pip install -r yolov8_service/requirements.txt
   pip install -e .
   ```
4. **Run tests:**
   ```sh
   pytest -q
   ```

## Communication

- For questions, ideas, or support, contact [Metehan Yaşar on LinkedIn](https://www.linkedin.com/in/metehan-y-16475a164/)
- Open an issue for bugs, feature requests, or discussions

## Vision

The goal is to create an environment where anyone can define their classic automations as tools for modern LLMs and agents. Let's build a hub for the next generation of automation!
