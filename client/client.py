import asyncio
import nest_asyncio
import httpx
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents.format_scratchpad import format_log_to_str
#from langchain.agents.output_parsers import ReActSingleInputOutputParser, ReActJsonInputOutputParser
from langchain_mcp_adapters.tools import MCPTool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langchain.tools import tool
from typing import Any, Optional, Callable, Awaitable


nest_asyncio.apply()

REACT_PROMPT = """Vous êtes un assistant intelligent. Répondez à la question en utilisant les outils disponibles : {tools}

Instructions :
- Suivez le format suivant pour structurer votre réponse :
  - Question : la question posée
  - Pensée : réfléchissez à ce qu'il faut faire
  - Action : l'action à prendre [{tool_names}]
  - Entrée Action : l'entrée pour l'action (e.g., requête SQL)
  - Observation : résultat de l'action
  - ... (répétez Pensée/Action/Entrée/Observation si nécessaire)
  - Pensée : je connais la réponse finale
  - Réponse Finale : la réponse à la question

{agent_scratchpad}
"""

class LocalLangchainMCPClient:
    def __init__(self, mcp_server_url="http://127.0.0.1:8000"):
        self.llm = ChatOllama(
            model="phi3",
            temperature=0.5
        )

        server_config = {
            "default": {
                "url": f"{mcp_server_url}/sse",
                "transport": "sse",
                "options": {
                    "timeout": 10,
                    "retry_connect": True,
                    "max_retries": 3,
                    "read_timeout": 5.0,
                    "write_timeout": 5.0
                }
            }

        }
        self.mcp_client = MultiServerMCPClient(server_config)
        self.tools = []
        self.agent_executor = None


    async def discover_tools(self):
        print("Discovering tools...")
        try:
            self.tools = await self.mcp_client.get_tools()
            print(f"Tools discovered: {self.tools}")
            self.tools = [MCPTool(tool, self.mcp_client) for tool in self.tools]
        except AttributeError as e:
            print(f"Error with get_tools: {e}. Trying list_tools...")

    def create_agent(self):
        prompt = ChatPromptTemplate.from_template(REACT_PROMPT)
        agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    async def run_query(self, query: str):
        if not self.agent_executor:
            await self.discover_tools()
            self.create_agent()
        result = await asyncio.to_thread(self.agent_executor.invoke, {"input": query})
        return result['output']

async def main():
    client = LocalLangchainMCPClient()
    queries = [
        "Ajoute une personne nommée Alice, âge 26, profession Développeuse",
        "Lis toutes les données de la table people"
    ]
    for q in queries:
        result = await client.run_query(q)
        print(f"Résultat pour : '{q}' : {result}")


if __name__ == '__main__':
    asyncio.run(main())
