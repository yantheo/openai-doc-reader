# openai-doc-reader

openai-doc-reader est un outil basé sur l'API d'OpenAI (V2) conçu pour lire, analyser et interagir avec des documents. Ce projet permet aux utilisateurs de télécharger des fichiers (comme des PDF), de les transformer en vecteurs d'embeddings, puis d'interagir avec ces documents via une interface de chat alimentée par l'IA.

## Fonctionnalités

- **Téléchargement et Traitement de Documents** : Permet aux utilisateurs de télécharger des fichiers, qui sont ensuite traités pour en extraire des embeddings.
- **Analyse de Texte Avancée** : Utilise l'API d'OpenAI pour analyser le texte des documents et fournir des réponses contextuelles aux questions posées.
- **Interface de Chat Interactive** : Offre une interface utilisateur intuitive pour poser des questions sur le contenu des documents et obtenir des réponses en temps réel.
- **Citations et Références** : Fournit des réponses enrichies avec des citations et des références pour chaque réponse, permettant de retrouver facilement les informations source.

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/yantheo/openai-doc-reader.git

2. Accédez au répertoire:
   cd openai-doc-reader

3. Installez les dépendances :
   pip install -r requirements.txt

4. Configurez les variables d'environnement nécessaires en créant un fichier .env :
   OPENAI_API_KEY=your_openai_api_key

5. Lancer l'application:
   streamlit run app.py
