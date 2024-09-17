# Social Swarm: AI-Powered Twitter Content Generator

Social Swarm is an innovative project that leverages AI agents to generate engaging Twitter content based on user-provided topics. This project aims to streamline social media content creation by utilizing advanced language models and a suite of specialized agents.

## Technologies Used

- Python 3.10
- Next.js 14
- TypeScript
- Tailwind CSS
- Modal
- OpenAI API
- Together API
- Perplexity AI API
- Composio API

## Project Goals

The main objective of Social Swarm is to create a system that can:

1. Accept a topic from the user
2. Utilize multiple AI agents to gather relevant information
3. Generate engaging tweets based on the collected data
4. Perform a groundedness check to ensure the quality of the generated content
5. Provide an easy-to-use web interface for interacting with the system

## Setup Instructions

To set up the project locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/sailingsf/ai_agent_hackathon.git
   cd social-swarm
   ```

2. Set up the backend:
   ```
   cd agents
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the `agents` directory and add the following variables:
   ```
   TOGETHER_API_KEY=your_together_api_key
   OPENAI_LOCAL_API_KEY=your_openai_api_key
   PERPLEXITY_API_KEY=your_perplexity_api_key
   COMPOSIO_API_KEY=your_composio_api_key
   UPSTAGE_API_KEY=your_upstage_api_key
   ```

4. Set up the frontend:
   ```
   cd ../ui
   npm install
   ```

5. Run the backend:
   ```
   cd ../agents
   modal deploy main.py
   ```

6. Run the frontend:
   ```
   cd ../ui
   npm run dev
   ```

7. Open your browser and navigate to `http://localhost:3000` to use the application.

## Project Structure

The project is divided into two main parts:

1. Backend (agents):
   - Contains the AI agents and tools for generating content
   - Implements the Modal serverless functions for API endpoints
   - Handles integration with various AI services

2. Frontend (ui):
   - Next.js application for the user interface
   - Allows users to input topics and view generated tweets

Key files and directories:

```
agents/
├── main.py                 # Main Modal app and API endpoints
├── run_agents.py           # Orchestrates the AI agents
├── agent_class.py          # Defines the Agent class
├── tools/                  # Contains various tools used by agents
└── requirements.txt        # Python dependencies

ui/
├── app/                    # Next.js app directory
│   ├── page.tsx            # Main page component
│   └── types/types.ts      # TypeScript type definitions
├── package.json            # Node.js dependencies
└── tailwind.config.ts      # Tailwind CSS configuration
```

## Usage

1. Start the application and navigate to the web interface.
2. Enter a topic in the input field.
3. Click "Get started" to generate tweets.
4. View the generated tweets and their associated information.

## Contributing

Contributions to Social Swarm are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.