# Architecture

- **Serveur MCP** : Expose des outils via le protocole MCP (SDK Python).
- **Client Agentic** : Utilise LangChain pour créer un agent ReAct qui découvre et appelle les outils.
- **LLM Local** : Ollama pour le raisonnement.
- **Outils** : Exemple avec SQLite, extensible (e.g., fichiers, APIs locales).