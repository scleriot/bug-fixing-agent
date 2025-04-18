# Code Engine for Bug Fixing

A Python-based agent that helps non-technical users fix bugs and make changes to codebases through natural language requests.

This POC was created as part of the [Dust](https://dust.tt/) AI Agents Hackathon in Paris.

## Features

- Uses LLM to analyze and fix code issues
- Git integration for pulling, committing, and pushing changes
- File management capabilities (read/write)
- REST API for integration with other applications

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   MODEL_ID=your_model_name
   API_KEY=your_api_key
   CODEBASE_PATH=/path/to/codebase
   ```

## Usage

### As a command-line tool:
```
python agent.py "fix the button click handler in main.js"
```

### As an API server:
```
python api.py
```

Then send POST requests to `/api/run` with JSON body:
```json
{
  "query": "fix the button click handler in main.js",
  "context": "additional context about the application"
}
```

## Technical Details

- Built with smolagents from HuggingFace
- Uses LiteLLM for model access
- Git operations handled through subprocess, relying on a user being authenticated on the system

## Next steps

In order to improve the agent's capabilities for medium and large code base, we would need to have some kind of codebase embedding and RAG.
