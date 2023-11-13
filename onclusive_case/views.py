from django.shortcuts import render
from dotenv import load_dotenv
import json
import os
import sys
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
import requests

from onclusive_case.az_text_analysis import AzTextAnalysis
from onclusive_case.video_indexer import VideoIndexer

load_dotenv()

# Get the environment variables
vi_account_id = os.getenv('vi_account_id')
vi_api_key = os.getenv('vi_api_key')
vi_location = os.getenv('vi_location')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class DictionaryOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a dictionary."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return json.loads(text)


def get_transcript(request):

    from_file = True
    video_id = '53a3c8a677'

    if from_file:
        summaries_file_path = f'onclusive_case/data/{video_id}_transcription.json'
        with open(summaries_file_path, 'r') as f:
            transcription = json.load(f)

    else:
        VI = VideoIndexer(vi_api_key=vi_api_key, vi_location=vi_location, vi_account_id=vi_account_id)
        list_of_videos = VI.get_all_videos_list()

        # Get the ID of the first video in the list
        video_id = list_of_videos[0]['id']

        index_data = VI.get_video_info(video_id)

        # Get the video insights
        insights_data = VI.get_video_insights(video_id)

        # get the transcript
        transcription, _ = VI.get_transcript_text_from_insights(insights_data)

        # save the transcript to a file
        os.makedirs(os.path.dirname(f'onclusive_case/data/{video_id}_transcription.json'), exist_ok=True)
        with open(f'onclusive_case/data/{video_id}_transcription.json', 'w') as f:
            json.dump(transcription, f)

    # # get named entities
    # first_video_insight = insights_data['videos'][0]
    # brands_list = first_video_insight['insights']['brands']
    # named_entities_list = []
    # for brand in brands_list:
    #     brand_name = brand['name']
    #     confidence = brand['confidence']
    #     instances = brand['instances']
    #     reference_url = brand['referenceUrl']
    #
    #     n_in_transcription = [instance for instance in instances if instance['brandType'] == 'Ocr']
    #     brand_is_in_transcription = True if len(n_in_transcription) > 0 else False
    #     instances_list = []
    #     for instance in instances:
    #         instance_type = instance['brandType']
    #         start = instance['start']
    #         end = instance['end']
    #         instances_list.append({'type': instance_type, 'start': start, 'end': end})
    #     named_entities_list.append({'name': brand_name, 'referenceUrl': reference_url, 'confidence': confidence, 'instances': instances_list, 'brand_is_in_transcription': brand_is_in_transcription})
    #
    # # get Named Entities from transcript
    # az_text_analysis = AzTextAnalysis()
    #
    # brands = []
    # for trans in transcription:
    #     entities = az_text_analysis.get_entities(trans['text'])
    #
    #     for entity in entities:
    #         if entity.category == 'Organization':
    #             brands.append({'brand': entity.text, 'text': trans['text'], 'start_time': trans['time']})
    #             break

    # organizations = set([entity['brand'] for entity in brands])
    #
    # audio_brands = []
    # for org in organizations:
    #     time_list = []
    #     for brand in brands:
    #         if org == brand['brand']:
    #             start_time = brand['start_time']
    #             time_list.append(start_time)
    #     audio_brands.append({'brand': org, 'times': time_list})

    # Define the file path for the summaries
    summaries_file_path = f'onclusive_case/data/{video_id}.json'

    # Check if the file already exists
    if os.path.exists(summaries_file_path):
        # Read the existing summaries from the file
        with open(summaries_file_path, 'r') as file:
            summaries = json.load(file)
    else:
        template = """
                As a helpful assistant, your task is to analyze a provided text with timestamps, identify brands mentioned within it, and generate concise summaries for each identified brand. Additionally, compile a list of timestamps where each brand is mentioned.
    
                When processing the text:
                - Identify named entities that qualify as brands.
                - For each brand, summarize its portrayal in the text, using specific examples or direct quotes for clarity and relevance.
                - Maintain consistency in detail across all brand summaries.
                - Ensure each summary directly connects to specific parts of the text, referencing relevant timestamps for context.
                - Distinguish between brands and non-brand entities, focusing exclusively on the brands.
    
                The final output should be a dictionary, where each key represents a brand. The value associated with each key should be an array (list) with two elements:
                1. A string providing a direct summary of how the brand is portrayed in the text.
                2. An array (list) of timestamps indicating when the brand is mentioned in the text.
    
                Provide the output strictly in this structured format.
                """

        human_template = "Find and Provide summaries for brands in this text: {text}"

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", human_template),
        ])
        chain = chat_prompt | ChatOpenAI() | DictionaryOutputParser()

        trans_with_times = ''
        for trans in transcription:
            t = trans['time'] + ': ' + trans['text']
            trans_with_times += t + '\n'

        summaries = chain.invoke({"text": trans_with_times})

        # Get sentiment analysis of summaries
        az_text_analysis = AzTextAnalysis()
        for brand in summaries:
            summary = summaries[brand][0]
            sentiment = az_text_analysis.get_sentiment(summary)
            summaries[brand].append(sentiment)

        os.makedirs(os.path.dirname(summaries_file_path), exist_ok=True)

        # Save the summaries to a file
        with open(summaries_file_path, 'w') as file:
            json.dump(summaries, file)

    context = {'transcription': transcription, 'brand_summaries': summaries}

    return render(request, 'onclusive_case.html', context)
