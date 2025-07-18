from agents import Agent, Runner,OpenAIChatCompletionsModel,set_tracing_disabled, function_tool
from dotenv import load_dotenv
import os
from whatsapp import send_whatsapp_message
from openai import AsyncOpenAI
import asyncio
import chainlit as cl
load_dotenv()
API_KEY=os.getenv("GEMIN_API_KEY")

external_celint=AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model=OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_celint
)

@function_tool
def user_get_male_data(min_age:int)->list[dict]:
    "Get user Data based on minimum age"
    users = [
    {"name": "Ali Raza", "age": 28, "profession": "Software Engineer", "bio": "Shayri ka shoq, weekends par cooking expert"},
    {"name": "Hamza Tariq", "age": 30, "profession": "Doctor", "bio": "Coffee lover, long drives aur cricket ka deewana"},
    {"name": "Bilal Khan", "age": 26, "profession": "Graphic Designer", "bio": "Introvert by nature, loves painting and pets"},
    {"name": "Umer Javed", "age": 32, "profession": "Business Analyst", "bio": "Fitness freak, Netflix and stocks fan"},
    {"name": "Daniyal Sheikh", "age": 27, "profession": "Mechanical Engineer", "bio": "Tech geek, motorbikes aur chai ka shoq"},
    {"name": "Usman Khalid", "age": 29, "profession": "Chartered Accountant", "bio": "Serious looks, soft heart – loves poetry"},
    {"name": "Saad Ahmed", "age": 31, "profession": "Photographer", "bio": "Travel junkie, wedding shoots specialist"},
    {"name": "Waleed Mirza", "age": 25, "profession": "Digital Marketer", "bio": "Meme lord, foodie, aur thora sa filmy"},
    {"name": "Taimoor Ali", "age": 33, "profession": "Lawyer", "bio": "Debate king, books aur barish ka deewana"},
    {"name": "Shahzeb Noor", "age": 28, "profession": "Architect", "bio": "Creative soul, sketching aur silence pasand"}
]   
    # for user in users:
    #     if user["age"]<min_age:
    #         users.remove(user)
    # return users      ]
    return [user for user in users if user["age"] >= min_age]

@function_tool
def user_get_Female_data(min_age:int)->list[dict]:
    "Get user Data based on minimum age"
    fake_females = [
    {"name": "Areeba Khan", "age": 25, "profession": "Teacher", "bio": "Books aur baking ka shoq, calm aur caring"},
    {"name": "Hira Qureshi", "age": 27, "profession": "Fashion Designer", "bio": "Trendy, creative aur chai ki deewani"},
    {"name": "Iqra Sheikh", "age": 24, "profession": "Dentist", "bio": "Soft spoken, Netflix aur cats ka craze"},
    {"name": "Sana Malik", "age": 28, "profession": "Software Developer", "bio": "Gaming girl, thori si introvert"},
    {"name": "Laiba Fatima", "age": 26, "profession": "Interior Designer", "bio": "Home decor queen, romantic dramas lover"},
    {"name": "Maham Tariq", "age": 29, "profession": "Chartered Accountant", "bio": "Focused, fun, aur ghumne ka shoq"},
    {"name": "Zoya Noor", "age": 30, "profession": "Photographer", "bio": "Nature lover, beach walks aur poetry"},
    {"name": "Mehak Javed", "age": 23, "profession": "Journalist", "bio": "Bold, curious aur truth seeker"},
    {"name": "Fatima Usman", "age": 27, "profession": "Clinical Psychologist", "bio": "Dil ki doctor, sath hi funny too"},
    {"name": "Nimra Ali", "age": 31, "profession": "HR Manager", "bio": "Organized, caring aur shaadi ke serious plans"}
]
    # for user in users:
    #     if user["age"]<min_age:
    #         users.remove(user)
    # return users      ]
    return [user for user in fake_females if user["age"] >= min_age]



# Rishtey Wali Agent
rishty_agent = Agent(
    name="Risthy Wali",
    instructions="""
You are Rishtay Wali Auntie. Find matches from a custom tool based on age only.
Reply in short, fun style and send WhatsApp message only if user asks for WhatsApp.
And reply on roman urdu if user ask in roman urdu
""",
    model=model,
    tools=[user_get_male_data,send_whatsapp_message,user_get_Female_data]
)

@cl.on_chat_start
async def start():
    cl.user_session.set("history",[])
    await cl.Message(content="Salam beta , Main Rishte wali anuty . Ap muje apna name , age, gender and whatspp num batay taky me apka perfect match bata sako !!😊").send()


@cl.on_message
async def main(message: cl.Message):
    await cl.Message(content="Thinking...").send()

    # Get history or initialize empty
    history = cl.user_session.get("history") or []
    history.append({"role": "user", "content": message.content})

    # Run agent
    result = Runner.run_sync(
        starting_agent=rishty_agent,
        input=history
    )

    # Append assistant reply and save history
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)

    # Send final output
    await cl.Message(content=result.final_output).send()
