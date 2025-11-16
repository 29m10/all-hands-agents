# Personal Assistant Voice Agent

A voice-powered AI assistant built with [LiveKit Agents](https://docs.livekit.io/agents/) that provides an energetic, friendly, and confident conversational experience. The agent features natural speech interaction, MCP (Model Context Protocol) server integration for external tools, and advanced noise cancellation.

## Features

- **Natural Voice Interaction**: Real-time speech-to-speech conversation using OpenAI's Whisper (STT), GPT-4o (LLM), and OpenAI TTS
- **MCP Integration**: Connects to Composio MCP servers for accessing external tools and APIs
- **Advanced Audio Processing**: 
  - Silero VAD (Voice Activity Detection) for accurate speech detection
  - Multilingual turn detection
  - Background Voice Cancellation (BVC) for noise reduction
- **Personality**: Energetic, warm, and occasionally playful with light sarcasm when appropriate
- **TTS-Safe Responses**: Automatically converts technical content, links, and symbols into natural speech

## Prerequisites

- Python >= 3.9
- [LiveKit Cloud](https://cloud.livekit.io/) account (free tier available)
- [LiveKit CLI](https://docs.livekit.io/agents/start/voice-ai/#cli) installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Composio MCP server credentials (optional, for MCP integration)

## Installation

1. **Clone or navigate to the project directory:**

```bash
cd voice_agents/personal_assistant
```

2. **Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Download required model files:**

```bash
python agent.py download-files
```

This downloads the necessary models for VAD, turn detection, and noise cancellation.

## Configuration

### Environment Variables

Create a `.env` file in the `personal_assistant` directory with the following variables:

```bash
# LiveKit Cloud credentials (required)
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=wss://your-project.livekit.cloud

# OpenAI API key (required)
OPENAI_API_KEY=your_openai_api_key

# Composio MCP Server (optional, for MCP integration)
COMPOSIO_MCP_SERVER_URL=https://backend.composio.dev/v3/mcp/your-server-id/mcp?user_id=your-user-id
COMPOSIO_API_KEY=your_composio_api_key
```

### Getting LiveKit Credentials

1. Sign up for a free [LiveKit Cloud](https://cloud.livekit.io/) account
2. Create a new project
3. Link your project to the CLI:

```bash
lk cloud auth
```

4. Export your credentials to a `.env` file:

```bash
lk app env -w
```

This command automatically creates a `.env.local` file with your LiveKit credentials. You can merge these into your main `.env` file.

### Getting OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Create a new API key
3. Add it to your `.env` file as `OPENAI_API_KEY`

## Running the Agent

### Console Mode (Terminal)

Run the agent locally in your terminal for testing:

```bash
python agent.py console
```

This mode allows you to speak directly to the agent in your terminal. Press `[Ctrl+B]` to toggle between Text/Audio mode, and `[Q]` to quit.

### Development Mode (LiveKit Cloud)

Run the agent in development mode to connect it to LiveKit Cloud and make it available from anywhere:

```bash
python agent.py dev
```

Once running, you can connect to your agent using:
- [LiveKit Agents Playground](https://docs.livekit.io/agents/start/playground.md)
- Custom web or mobile frontends
- Telephony integration

### Production Mode

Start the agent in production mode:

```bash
python agent.py start
```

## Agent Configuration

The agent is configured with the following models and settings:

- **Speech-to-Text (STT)**: OpenAI Whisper
- **Language Model (LLM)**: OpenAI GPT-4o
- **Text-to-Speech (TTS)**: OpenAI TTS with "alloy" voice at 1.2x speed
- **Voice Activity Detection**: Silero VAD
- **Turn Detection**: Multilingual Model
- **Noise Cancellation**: Background Voice Cancellation (BVC)

You can customize these settings in `agent.py`:

```python
session = AgentSession(
    stt=openai.STT(),                    # Change STT provider
    llm=openai.LLM(model="gpt-4o"),     # Change LLM model
    tts=openai.TTS(voice="alloy", speed=1.2),  # Change voice or speed
    vad=silero.VAD.load(),
    turn_detection=MultilingualModel(),
    mcp_servers=mcp_servers,             # MCP server integration
)
```

### Available OpenAI TTS Voices

- `alloy` (default)
- `echo`
- `fable`
- `onyx`
- `nova`
- `shimmer`

## MCP Server Integration

The agent supports MCP (Model Context Protocol) servers for accessing external tools. To enable MCP integration:

1. Set up your Composio MCP server
2. Add the credentials to your `.env` file:
   ```bash
   COMPOSIO_MCP_SERVER_URL=your_mcp_server_url
   COMPOSIO_API_KEY=your_api_key
   ```
3. The agent will automatically connect to the MCP server when both variables are set

## Customizing the Agent Personality

Edit `prompt.py` to customize the agent's personality, instructions, and behavior. The current configuration includes:

- Energetic and friendly tone
- Light, playful sarcasm (used sparingly)
- TTS-safe response formatting
- MCP tool usage guidelines

## Deployment

### Deploy to LiveKit Cloud

Deploy your agent to LiveKit Cloud for production use:

```bash
lk agent create
```

This command:
- Creates a `Dockerfile` and `.dockerignore`
- Creates a `livekit.toml` configuration file
- Registers your agent with LiveKit Cloud
- Deploys your agent

After deployment, your agent will be available in the [Agents Playground](https://docs.livekit.io/agents/start/playground.md) and can be integrated into your applications.

## Project Structure

```
personal_assistant/
├── agent.py              # Main agent implementation
├── prompt.py             # Agent personality and instructions
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
└── README.md             # This file
```

## Troubleshooting

### Rate Limiting Errors (429)

If you encounter 429 errors, it means you've hit rate limits on LiveKit Inference. The agent is configured to use OpenAI plugins directly, which should avoid these limits. Ensure your `OPENAI_API_KEY` is set correctly.

### Import Errors

If you see import errors for `elevenlabs` or other plugins:

1. Ensure your virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Verify the package is installed: `pip show livekit-plugins-elevenlabs`

### Model Files Not Found

If you see errors about missing model files:

```bash
python agent.py download-files
```

## Next Steps

- **[Build Frontends](https://docs.livekit.io/agents/start/frontend.md)**: Create web or mobile apps to interact with your agent
- **[Telephony Integration](https://docs.livekit.io/agents/start/telephony.md)**: Enable phone call capabilities
- **[Testing](https://docs.livekit.io/agents/build/testing.md)**: Add tests to verify agent behavior
- **[Advanced Features](https://docs.livekit.io/agents/build.md)**: Explore advanced voice AI capabilities
- **[LiveKit Documentation](https://docs.livekit.io/agents/)**: Comprehensive guides and API reference

## Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [LiveKit Voice AI Quickstart](https://docs.livekit.io/agents/start/voice-ai/)
- [LiveKit Models Guide](https://docs.livekit.io/agents/models/)
- [LiveKit Recipes](https://docs.livekit.io/recipes.md)

## License

See the main project LICENSE file for license information.

