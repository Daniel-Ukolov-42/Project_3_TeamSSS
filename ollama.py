#ollama.py

#necessary imports
import gradio as gr
import requests
from api import fetch_events


OLLAMA_API = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'tinyllama'  #ollama llm model were using

#function to generate summary using ollama
def generate_summary(title, summary):
   
    if not summary:
        return 'No description provided for this event.'

    #building the prompt for llm to use
    prompt = f'''
    Summarize the following event in 2-3 sentences, using clear language for someone deciding whether to attend.

    Title: {title}

    Description:
    {summary}
    '''
    #calling ollama api with model and prompt
    try:
        response = requests.post(
            OLLAMA_API,
            json={
                'model': OLLAMA_MODEL,
                'prompt': prompt,
                'stream': False,
                'temperature': 0.3
            }
        )
        #making sure we get a succesful request 
        if response.status_code == 200:
            return response.json().get('response', 'No summary returned.')
        else:
            return f'Error: Ollama returned status {response.status_code}'
    except Exception as e:
        return f'Error: {str(e)}'


def search_events(location, keyword, max_results):
    '''
    Fetch events and structure them with summary buttons
    '''
    events = fetch_events(location=location, keyword=keyword, max_results=max_results)

    #handle errors and empty results
    if events and 'error' in events[0]:
        return f'Error: {events[0]["error"]}'

    if not events:
        return 'No events found.'
    #list of gradio visual elemnts that will be displayed when the app runs
    components = []

    for event in events:
        with gr.Column():
            #displaying the event details
            components.append(gr.Markdown(f'**{event["title"]}**\n\n{event["start_time"]}\n\n{event["venue"]}\n\n{event["summary"][:300]}...'))

            #Output for the llm generated summary 
            summary_output = gr.Textbox(label='LLM Summary', lines=3)

            #button to trigger the generation of the summary 
            btn = gr.Button('Generate Summary')
            btn.click(
                fn=generate_summary,
                inputs=[gr.Textbox(value=event['title'], visible=False), gr.Textbox(value=event['summary'], visible=False)],
                outputs=summary_output
            )

            #add summary output to the list
            components.append(summary_output)

    return components

with gr.Blocks(title='Event Summarizer') as demo:
    gr.Markdown('# Event Summarizer with Ollama')
    gr.Markdown('Search for events and get AI-generated summaries of event descriptions.')

    #input fields for search 
    with gr.Row():
        location_input = gr.Textbox(label='Location', placeholder='e.g., San Francisco')
        keyword_input = gr.Textbox(label='Keyword', placeholder='e.g., startup, music')
        count_input = gr.Slider(minimum=1, maximum=10, value=3, step=1, label='Number of Events')
        search_button = gr.Button('Search Events')


    #column to hold the results 
    output_area = gr.Column()

    #when the search button is clicked trigger event fetch and summary 
    search_button.click(
        fn=search_events,
        inputs=[location_input, keyword_input, count_input],
        outputs=output_area
    )
#launching the app
if __name__ == '__main__':
    demo.launch(share=True)

