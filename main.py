# imports
import gradio as gr
from dotenv import load_dotenv
import os

# load environment variables from the .env file
# key.env stores the api key to hide it
load_dotenv(dotenv_path='key.env')
API_KEY = os.getenv('TICKETMASTER_API_KEY')

# check if the api key was loaded successfully
if not API_KEY:
    raise ValueError('error: TICKETMASTER_API_KEY not found in .env file')

# import local functions for api and llm-based summarization
'''
FILE NAMES WHERE ON LOCAL MACHINE - NEED TO BE RENAMED BEFORE SUBMISSION
'''
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
    markdown = f'### top {len(events)} events\n\n'
    for i, event in enumerate(events, 1):
        summary = generate_summary(event['title'], event['summary'])
        markdown += f'#### {i}. [{event["title"]}]({event["url"]})\n'
        markdown += f'date: {event["start_time"]}\n\n'
        markdown += f'venue: {event["venue"]}\n\n'
        markdown += f'summary: {summary}\n\n'
        markdown += '---\n\n'

    return markdown

# set up the gradio user interface
with gr.Blocks(title='event analyzer') as demo:
    # ui title and description
    gr.Markdown('# ticketmaster event analyzer')
    gr.Markdown('search for events and see ai-generated summaries using ollama')

    # input fields for user query
    with gr.Row():
        location = gr.Textbox(label='location', placeholder='e.g. new york, miami, san francisco')
        keyword = gr.Textbox(label='keyword', placeholder='e.g. sports, music, comedy')
        count = gr.Slider(1, 10, value=5, label='number of events')
        search_btn = gr.Button('search events')

    # output area to display results
    results = gr.Markdown(label='results')

    # link the button click to the function
    search_btn.click(
        fn=search_and_display,
        inputs=[location, keyword, count],
        outputs=results
    )

# launch the gradio app
if __name__ == '__main__':
    demo.launch()
