import os
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, mcp
from livekit.plugins import noise_cancellation, silero, openai, elevenlabs
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from prompt import VOICE_AGENT_SYSTEM_PROMPT

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=VOICE_AGENT_SYSTEM_PROMPT,
        )


async def entrypoint(ctx: agents.JobContext):
    composio_server_url = os.getenv("COMPOSIO_MCP_SERVER_URL")
    composio_api_key = os.getenv("COMPOSIO_API_KEY")
    
    mcp_servers = []
    if composio_server_url and composio_api_key:
        mcp_servers.append(
            mcp.MCPServerHTTP(
                url=composio_server_url,
                headers={
                    "x-api-key": composio_api_key,
                }
            )
        )
    
    session = AgentSession(
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o"),
        tts=openai.TTS(voice="alloy", speed=1.2),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
        mcp_servers=mcp_servers,
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    # await session.generate_reply(
    #     instructions="Greet the user and offer your assistance."
    # )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))