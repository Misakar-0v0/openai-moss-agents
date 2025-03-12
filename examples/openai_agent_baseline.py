import asyncio

from agents import Runner, Agent
from openai_moss_agents.moss_tool import MOSSProtocolTool
from openai_moss_agents.example_moss_libs import math_lib
from openai_moss_agents.rich_console import run_console_agent


async def main():
    tool = MOSSProtocolTool(
        modulename=math_lib.__name__,
    )

    instruction = tool.with_instruction("assistant for human")
    print(instruction)

    agent = Agent(
        name="jojo",
        instructions=instruction,
        model="gpt-4",
        tools=[tool.as_agent_tool()]
    )

    await run_console_agent(agent)


if __name__ == "__main__":
    asyncio.run(main())
