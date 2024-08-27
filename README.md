# openai-doc-reader

openai-doc-reader est un outil basé sur l'API d'OpenAI Assistant File Search & Vector Store (V2) conçu pour lire, analyser et interagir avec des documents. Ce projet permet aux utilisateurs de télécharger des fichiers (comme des PDF), de les transformer en vecteurs d'embeddings, puis d'interagir avec ces documents via une interface de chat alimentée par l'IA.

## Features

- **Document Upload and Processing: Allows users to upload files, which are then processed to extract embeddings.
- **Advanced Text Analysis: Utilizes the OpenAI API to analyze the text of documents and provide contextual responses to questions.
- **Interactive Chat Interface: Provides an intuitive user interface for asking questions about the document content and receiving real-time answers.
- **Citations and References: Enriches responses with citations and references for each answer, making it easy to locate the source information.

## Installation

1. Clone this repository :
   ```bash
   git clone https://github.com/yantheo/openai-doc-reader.git

2. Navigate to the directory :
   cd openai-doc-reader

3. Install the dependencies :
   pip install -r requirements.txt

4. Configure the necessary environment variables by creating a .env file: :
   OPENAI_API_KEY=your_openai_api_key
   
5. You need also to create your own thread id and assistant before running it

6. Run the application :
   streamlit run app.py

