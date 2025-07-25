# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # --- 1. Load Gemini API Key ---
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("GEMINI_API_KEY is missing in .env file!")

# genai.configure(api_key=api_key)
# model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

# # --- 2. Define Agent Class ---
# class Agent:
#     def __init__(self, name, instructions="", handler=None, handoffs=None):
#         self.name = name
#         self.instructions = instructions
#         self.handler = handler
#         self.handoffs = handoffs or []

#     def handle(self, input_data):
#         if self.handler:
#             return self.handler(input_data)
#         return f"⚠️ {self.name} has no handler."

# # --- 3. Poem Type Classifier (Triage Logic) ---
# def triage_poem(poem: str) -> str:
#     """
#     Decide poem type: Lyric, Narrative, or Dramatic.
#     """
#     prompt = f"""
#     You are a poetry classifier. Carefully read the poem below and classify it strictly into ONE of the following types:

#     1. Lyric — expresses emotions, feelings, or personal thoughts.
#     2. Narrative — tells a story with characters or a sequence of events.
#     3. Dramatic — written as a speech, monologue, or dramatic scene, often suitable for performance.

#     Return ONLY the word: Lyric, Narrative, or Dramatic — nothing else.

#     Poem:
#     {poem}
#     """
#     response = model.generate_content(prompt)
#     result = response.text.strip().lower()

#     for keyword in ["lyric", "narrative", "dramatic"]:
#         if keyword in result:
#             return keyword
#     return "unknown"

# # --- 4. Poem Analyzer ---
# def analyze_poem(poem: str, poem_type: str) -> str:
#     """
#     Analyze the poem based on its type.
#     """
#     prompt_map = {
#         "lyric": "Explain the emotions and personal feelings in this lyric poem.",
#         "narrative": "Describe the story, characters, and events in this narrative poem.",
#         "dramatic": "Highlight the theatrical and expressive elements in this dramatic poem."
#     }

#     if poem_type not in prompt_map:
#         return "❌ Unknown poem type."

#     full_prompt = f"{prompt_map[poem_type]}\n\nPoem:\n{poem}"
#     response = model.generate_content(full_prompt)
#     return response.text.strip()

# # --- 5. Analyst Agent Handlers ---
# def lyric_handler(poem): return analyze_poem(poem, "lyric")
# def narrative_handler(poem): return analyze_poem(poem, "narrative")
# def dramatic_handler(poem): return analyze_poem(poem, "dramatic")

# # --- 6. Create Analyst Agents ---
# lyric_agent = Agent(name="Lyric Agent", instructions="Handles lyric poems", handler=lyric_handler)
# narrative_agent = Agent(name="Narrative Agent", instructions="Handles narrative poems", handler=narrative_handler)
# dramatic_agent = Agent(name="Dramatic Agent", instructions="Handles dramatic poems", handler=dramatic_handler)

# # --- 7. Triage Agent Logic ---
# def triage_handler(poem: str):
#     poem_type = triage_poem(poem)
#     print(f"\n📌 Detected Poem Type: {poem_type.capitalize()}")

#     agent_map = {
#         "lyric": lyric_agent,
#         "narrative": narrative_agent,
#         "dramatic": dramatic_agent
#     }

#     selected_agent = agent_map.get(poem_type)

#     if selected_agent:
#         print(f"🔀 Handing off to: {selected_agent.name}\n")
#         return selected_agent.handle(poem)
#     else:
#         return "❌ Could not classify the poem."

# # --- 8. Create Triage Agent ---
# triage_agent = Agent(
#     name="Triage Agent",
#     instructions="Handoff to the appropriate agent based on the type of poem.",
#     handler=triage_handler,
#     handoffs=[lyric_agent, narrative_agent, dramatic_agent]
# )

# # --- 9. Get Multi-line User Input ---
# def get_multiline_input(prompt_msg="📥 Paste your poem (ENTER twice to finish):"):
#     print(prompt_msg)
#     lines = []
#     while True:
#         line = input()
#         if line == "":
#             break
#         lines.append(line)
#     return "\n".join(lines)

# # --- 10. Main Program ---
# if __name__ == "__main__":
#     print("🎉 Welcome to the Poetry Analyzer with Agent Handoff!\n")
#     poem_input = get_multiline_input()

#     print("\n🤖 Triage Agent is analyzing your poem...\n")
#     result = triage_agent.handle(poem_input)

#     print("\n📚 Analysis:\n")
#     print(result)
#     print("\n✅ Done. Thanks for using the Poetry Agent!")
