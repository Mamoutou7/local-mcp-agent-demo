# Local MCP Agent Demo

Un projet démo 100% local pour le Model Context Protocol (MCP), intégrant un agent AI avec des outils externes via un serveur local. Idéal pour les débutants en Agentic AI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Description
Ce projet implémente :
- Un serveur MCP local exposant des outils (e.g., gestion BDD SQLite).
- Un client agentic utilisant LangChain et Ollama pour raisonner et appeler les outils.

Tout fonctionne localement, sans internet après installation.

## Installation
1. Clonez le repo : `git clone https://github.com/Mamoutou7/local-mcp-agent-demo.git`
2. Installez les dépendances : `pip install -r requirements.txt`
3. Installez Ollama et pull un modèle : `ollama pull phi3`

## Usage
1. Lancez le serveur : `python server/server.py`
2. Dans un autre terminal, lancez le client : `python client/client.py`
3. Consultez les exemples dans `examples/queries.txt`.

## Architecture
Voir `docs/architecture.md` pour plus de détails.

## Contributions
Bienvenues ! Ouvrez une issue ou PR.

## Licence
MIT