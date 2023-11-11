# Onclusive Showcase

Onclusive provides a comprehensive media monitoring solution.

## Introduction

Their clients are brands and organizations that aim to monitor their media presence, manage their reputation, and remain informed about real-time sentiments on various social platforms. Onclusive’s services capture content from a multitude of media channels, such as social platforms, mainstream press, podcasts, and more. They cover 104 languages and operate across over 130 markets. By meticulously analyzing over 6 million articles every day, they grant businesses an overarching perspective on their media imprint.

Previously, Onclusive's operations heavily depended on human expertise for tasks that demanded reading comprehension, writing, critical thinking, creativity, and interpersonal communication. However, with the integration of advanced AI solutions, they've seen transformative improvements in both efficiency and accuracy. The infusion of AI into their workflow has not only optimized their service delivery but also enriched the professional lives of their employees. Moving away from mundane tasks, their workforce now engages in roles with higher value, focusing on more intricate and impactful aspects of media analysis and client strategy. However, it's essential to note that this evolution came with its set of challenges. The company had to restructure their workforce, which unfortunately included layoffs.

## Their AI Process

- Find mentions of the client's name in text, audio, and video.
- Understand what the content is saying about the client.
- Determine if the content is positive, negative, or neutral.
- Create a brief summary of the mention.
- Share the findings with the client.

## What does it look like in practice?

### Find mentions of the client's name in text, audio, and video.

The process of identifying and classifying named entities in text into predefined categories such as persons, organizations, locations, date/time, and others is termed Named Entity Recognition (NER). Many free algorithms, like NLTK or spaCy, use deep learning models trained on large labeled datasets to predict which word or sequence of words correspond to named entities and to which categories they belong.

For domain-specific applications (for instance, a lesser-known company), tools are available to train custom NER models using your own annotated data.

Before running these algorithms, it's essential to have the data in text form (translated to the desired language if necessary). This is straightforward for text but not the case for audio and video. There are several algorithms for speech-to-text conversions. Among the most popular are Microsoft Azure Speech service and Google Speech Recognition. For videos, an algorithm is used to transcribe spoken phrases into text. Additionally, a computer vision algorithm performs Optical Character Recognition (OCR) to read text in the video, recognize well-known brands, and for lesser-known companies, a model can be trained to recognize specific names as brands. This can be useful, for instance, to identify products, projects, or companies. Today's algorithms have advanced to the point of recognizing individual speakers based on their voice.

### Understand what the content is saying about the client's name.

AI offers several methods to extract key phrases from text and pinpoint the main themes or context. However, it's recommended to use a pre-built model or API trained on extensive datasets. Such models should support multiple languages and offer high accuracy. These algorithms can extract key phrases from text documents and highlight the main talking points.

You can also fine-tune these pre-built models for your specific domain or use case to achieve better accuracy.

### Determine if the content is positive, negative, or neutral.

Having identified our client in the media and extracted the key phrases and main talking points, we can proceed to perform sentiment analysis. There are various ways to conduct this, such as using VADER, which is free and can be used locally, or Azure AI Language, a cloud-based service offering sentiment analysis. These tools employ machine learning algorithms to classify text into positive, negative, or neutral categories.

### Create a summary of the mention.

For this task, it's beneficial to use generative AI models like ChatGPT, GPT 3.5, GPT 4, and Bard. OpenAI, the company behind ChatGPT, primarily uses Microsoft Azure as its cloud platform, and Microsoft has invested $1 billion in OpenAI. Azure's OpenAI Service grants access to OpenAI's potent large language models, including ChatGPT, GPT, Codex, and Embeddings.

## The Synergy of Using a Cloud-Based System Like Azure

While there's a vast sea of algorithmic choices for media analysis tasks, the appeal of a unified cloud-based system like Azure cannot be overstated. Azure operates as a one-stop-shop for all AI solutions, offering a centralized platform where tools seamlessly integrate, reducing the complexities of inter-tool communications. By using Azure, businesses can sidestep the hurdles of setting up, maintaining, and updating individual algorithms, as Microsoft ensures that their services are always cutting-edge and readily available. Furthermore, with data security being paramount, Azure provides robust encryption and privacy measures. Consolidating all operations in Azure also facilitates easier data management, and efficient scalability. In essence, while individual algorithms might offer specialized capabilities, the comprehensive nature of Azure ensures a holistic, efficient, and smooth operational experience, making it an enticing choice for businesses looking for uncompromised efficiency.
