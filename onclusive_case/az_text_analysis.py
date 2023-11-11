from dotenv import load_dotenv
import os

# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


load_dotenv()


class AzTextAnalysis:
    def __init__(self):

        # Get Configuration Settings
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(cog_key)
        self.cog_client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)

    def get_language(self, text):

        # Use the Text Analytics detect_language function
        detected_language = self.cog_client.detect_language(documents=[text])[0]
        language = detected_language.primary_language.name

        # Return the language
        return language

    def get_sentiment(self, text):

        # Use the Text Analytics analyze_sentiment function
        sentiment_analysis = self.cog_client.analyze_sentiment(documents=[text])[0]
        sentiment = sentiment_analysis.sentiment

        # Return the sentiment
        return sentiment

    def get_key_phrases(self, text):
        # Default key phrases is empty
        key_phrases = []

        # Use the Text Analytics extract_key_phrases function
        phrases = self.cog_client.extract_key_phrases(documents=[text])[0].key_phrases
        if len(phrases) > 0:
            key_phrases = phrases

        # Return the key phrases
        return key_phrases

    def get_entities(self, text):

        # Use the Text Analytics recognize_entities function
        entities = self.cog_client.recognize_entities(documents=[text])[0].entities

        # Return the entities
        return entities

    def get_linked_entities(self, text):
        # Default linked entities is empty
        linked_entities = []

        # Use the Text Analytics recognize_linked_entities function
        entities = self.cog_client.recognize_linked_entities(documents=[text])[0].entities
        if len(entities) > 0:
            linked_entities = entities

        # Return the linked entities
        return linked_entities
