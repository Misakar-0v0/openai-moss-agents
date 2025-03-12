import asyncio

from agents import Runner, Agent
from openai_moss_agents.moss_tool import MOSSProtocolTool
from openai_moss_agents.example_moss_libs import math_lib


async def main():
    tool = MOSSProtocolTool()

    instruction = tool.with_instruction("assistant for human")

    moss_agent = Agent(
        name="moss_agent",
        instructions=instruction,
        model="gpt-4o",
        tools=[tool.as_agent_tool()]
    )

    normal_agent = Agent(
        name="normal_agent",
        instructions="you are a helpful assistant",
        model="gpt-4o",
        tools=[],
    )

    result = await Runner.run(moss_agent, "How many letters r are there in the content: \"strawberry strawberry\"? use moss tool")
    print("moss_agent: ", result.final_output)

    result = await Runner.run(normal_agent, "How many letters r are there in the content: \"strawberry strawberry\"?")
    print("normal_agent: ", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())