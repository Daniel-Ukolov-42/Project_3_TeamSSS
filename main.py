# main.py

# imports
import gradio as gr
from dotenv import load_dotenv
import os

# custom theme to match Ticketmaster theme (blue)
from gradio.themes.base import Base
from gradio.themes.utils import colors

# theme class
class TicketmasterTheme(Base):
    def __init__(self):
        super().__init__()
        self.primary_hue = colors.blue

# load environment variables from the .env file
# key.env stores the api key to hide it
load_dotenv(dotenv_path='key.env')
API_KEY = os.getenv('TICKETMASTER_API_KEY')

# check if the api key was loaded successfully
if not API_KEY:
    raise ValueError('error: TICKETMASTER_API_KEY not found in .env file')

# import local functions for api and llm-based summarization
#
#
'''
FILE NAMES WHERE ON LOCAL MACHINE - NEED TO BE RENAMED BEFORE SUBMISSION
'''
#
#
#
from step3_api import fetch_events
from step2_llm import generate_summary

# function to search and display events
def search_and_display(location, keyword, max_results):
    # fetch events using the ticketmaster api
    events = fetch_events(location=location, keyword=keyword, max_results=max_results)

    # check for error in the response
    if events and 'error' in events[0]:
        return f'error: {events[0]["error"]}'

    # handle case when no events are found
    if not events:
        return 'no events found.'

    # format and return the results in markdown
    markdown = f'### Top {len(events)} Events\n\n'
    for i, event in enumerate(events, 1):
        summary = generate_summary(event['title'], event['summary'])
        markdown += f'#### {i}. [{event["title"]}]({event["url"]})\n'
        markdown += f'Date: {event["start_time"]}\n\n'
        markdown += f'Venue: {event["venue"]}\n\n'
        markdown += f'Summary: {summary}\n\n'
        markdown += '---\n\n'

    return markdown

# set up the gradio user interface with Ticketmaster blue theme
with gr.Blocks(theme=TicketmasterTheme(), title='event analyzer') as demo:
    # UI title and description
    gr.Markdown("<h1 style='color:#0070ce;'>Ticketmaster Event Finder & Summarizer</h1>")
    gr.Markdown("Search for events by state and see AI-generated summaries (Ollama model).")

    # input fields for user query
    with gr.Row():
        location = gr.Textbox(label='Location', placeholder='e.g. New York, Miami, San Francisco')
        keyword = gr.Textbox(label='Keyword', placeholder='e.g. sports, music, comedy')
        count = gr.Slider(1, 10, value=5, step=1, label='Number of Events')  # step=1 to ensure int values
        search_btn = gr.Button('Search Events')

    # output area to display results
    results = gr.Markdown(label='Results')

    # link the button click to the function
    search_btn.click(
        fn=search_and_display,
        inputs=[location, keyword, count],
        outputs=results
    )

# launch the gradio app
if __name__ == '__main__':
    demo.launch()
