from agents import Agent, Runner, handoffs, function_tool
from connection import config
import geocoder
import requests
import rich 


@function_tool
def current_location() -> str:
    """Returns the current location."""
    g = geocoder.ip('me')
    return f"\n\nCurrent location is {g.city},{g.country}."


@function_tool
def breaking_news() -> str:
    """Returns the latest breaking news."""
    return "\n\nBreaking news: The weather is sunny with a chance of rain later.\n\n"


Plant_agent = Agent(
    name="Plant Agent",
    instructions="You are a plant biology expert. Answer questions related to plants like photosynthesis."
)


main_agent = Agent(
    name="main_agent",
    instructions="You are a helpful assistant. Use the tools and hand off to the Plant Agent when needed.",
    tools=[current_location, breaking_news],
    handoffs=[Plant_agent]
)


result = Runner.run_sync(
    main_agent,
    """
        1. What is my current location?
        2. Any breaking news?
        3. What is photosynthesis?
    """,
    run_config=config
)


print("=" * 50)
print("\n\nLast Agent Used:", result.last_agent.name if result.last_agent else "Unknown")
rich.print(result.new_items)
print("\n\nFinal Output:", result.final_output)
