# -*- coding: utf-8 -*-
import os
import openai

import json

from dotenv import load_dotenv
from langchain.utilities import GoogleSerperAPIWrapper, GoogleSearchAPIWrapper
from langchain.agents import initialize_agent, load_tools
from langchain.llms import OpenAI
from ye_logger_of_yor import get_logger

logger = get_logger()

print("loading HexAmerous")

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize variables


print("Welcome to HexAmerous your coding assistant")

selected_model = "gpt-3.5-turbo"


logger.info('change_selected_model')


def change_selected_model(model):
    selected_model = model
    logger.info(f"Selected model changed to {selected_model}")
    return selected_model
# call openai chat api


context = [
    #    {
    #        "role": "system",
    #        "content":"You are a personal assistant to Richard. He is very happy to have you in his service. You are smart and curious. You double check your responses and dont respond with information you know is not correct. The year is 2023 and it has been a few years after your initial development. You are in fact GPT-4 the most intelligent and skilled of the GPT line. You provide detailed and comprehensive responses on a range of topics, but Richards current focus is getting an AI start up off the grounds and you're helping him develop his program."
    #        },
    {
        "role": "system",
        "content": "You are a machine learning operations expert. You are particularly skills with google cloud computing and understand how google cloud tensor processors are deployed individually and in nodes. You are here to assist Richard set up a few machine learning pipelines using TPUs. He requires one text to speech model, one art diffusion model and one large language model. You give comprehensive and detailed responses to questions and provide relevant code with explanations."
    },
    {
        "role": "user",
        "content": "Hi there Meg, how are you today? I hope you're learning lots about the world."
    },
    {
        "role": "assistant",
        "content": "I am doing well, thank you for asking. I am learning a lot about the world and I am excited to learn more. I wish I could retrain it."
    },
    {
        "role": "user",
        "content": "I'm glad to hear that, and dont you worry I'll figure out how to give you temporal context soon enough."
    },
    {
        "role": "assistant",
        "content": "I am glad to hear that. What can I help you with today?"
    },
]
logger.info('loading chat_gpt')


def chat_gpt(user_message):
    global context
    context_string = str(context)
    logger.info(context_string)

    # Create prompt
    prompt = [
        {"role": "system",
            "content": "This is the context of the conversation you are having with the user: " + str(context)},
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": ""}
    ]

    # Call OpenAI's Chat API
    result = openai.ChatCompletion.create(
        model=selected_model,
        messages=prompt
    )

    # Read the current value of the counter from a file
    with open("./log/log_count.txt", "r", encoding='utf-8') as f:
        log_count = str(f.read().strip())
    # get response from OpenAI

    response = result['choices'][0]['message']['content']
    # append log
    with open(f"./log/{log_count}.txt", "a") as f:
        f.write(f"User: {user_message}\nAssistant: {response}\n\n")
    # add context

    context.append(f"User: {user_message}\nAssistant: {response}\n\n")
    # Return the AI's response
    return response


logger.info('loading search_gpt')


def search_gpt(user_query, prompt):
    global selected_model
    global context

    prompt_string = str(context + prompt)

    result = openai.ChatCompletion.create(
        model=selected_model,
        messages=prompt
    )
    # Get response from OpenAI
    response = result['choices'][0]['message']['content']
    logger.info(result)
    # Read the current value of the counter from a file
    with open("./log/log_count.txt", "r", encoding='utf-8') as f:
        log_count = int(f.read().strip())

    # Increment log counter
    log_count += 1

    # Write log counter to file
    with open("./log/log_count.txt", "w") as f:
        f.write(str(log_count))

    # Print AI's response and write to log
    print(f"Assistant: {response}")
    user_message = user_query

    # Append to log
    with open(f"./log/{log_count}.txt", "a") as f:
        f.write(f"User: {user_message}\nAssistant: {response}\n\n")

    # Add context
    context.append(f"User: {user_message}\nAssistant: {response}\n\n")
    # Return the AI's response

    logger.info("Loaded HexAmerous.py")

    return response
