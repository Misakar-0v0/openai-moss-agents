try:
    import rich
except ImportError:
    raise ImportError(f'Please install Rich with `pip install "openai-moss-agents[console]"` or `pip install rich`')

from agents import Agent, Runner
from openai.types.responses.response_stream_event import (
    ResponseFunctionCallArgumentsDoneEvent
)
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown


async def run_console_agent(agent: Agent) -> None:
    console = Console()
    console.print(Panel(
        Markdown(agent.instructions),
        title=f"Agent {agent.name} Instructions",
    ))
    console.print(Panel(
        "print /quit to quit",
        title="help"
    ))
    while True:
        prompt = Prompt.ask("<<<")
        if prompt == "/quit":
            break
        console.print("\n")

        response = Runner.run_streamed(agent, prompt)
        console.print("AI >>>: \n")

        async for event in response.stream_events():
            if hasattr(event, "data") and hasattr(event.data, "delta"):
                console.print(event.data.delta, end="")
            elif isinstance(event, ResponseFunctionCallArgumentsDoneEvent):
                console.print("\n")
                console.print(Panel(
                    Markdown(event.arguments),
                    title=event.name,
                ))
            elif isinstance(event, ResponseFunctionCallArgumentsDoneEvent):
                console.print("\n")
                console.print(Panel(
                    Markdown(event.arguments),
                    title=event.item_id,
                ))

        console.print("\n")
        console.print(Panel(
            Markdown(response.final_output),
            title="AI",
        ))
