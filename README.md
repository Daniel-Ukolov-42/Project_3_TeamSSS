# Project_3_TeamSSS
Public version of Project 3


The goal of this was to create an AI powered web application that takes user input, pulls real time data from APIs, and uses an LLM to analyze the api data and give a detailed summary. In our project we decided to do an event finder and summarizer application. We used the Ticketmaster api to get real upcoming events from cities all over the world. After pulling the events based off user inputs we used tinyllama LLM to provide a summary of what the event was and other important details that would be useful to the user.

When completing this project we felt it was more sensible to use 3 files instead of 4. The Ollama file contains all code related to tinyllama LLM and some Gradio interface code. While the API includes all code related to pulling real time data from Ticketmaster API. Lastly, the main connects everything together and contains most of the Gradio code responsible for the layout of the app.

Responsibilities:
Roy Longarzo was responsible to for code in the Ollama file: this code send prompts to the ai model for summaries and also provides some interface code where users can click buttons 

Mia Castillo was responsible for code in the API file: this code pulls real time data from ticketmaster and formats it cleanly for analysis

Daniel Ukolov was responsible for code in the Main file:Connects user input to the API (City and event type) and to the LLM, Also sets up most of the app layout and theme using Gradio

All three members aided in debugging all code

