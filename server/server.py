import sqlite3
import argparse
from mcp.server.fastmcp import FastMCP


mcp_server = FastMCP(name='local-sqlite-demo')


def init_db():
    conn = sqlite3.connect('local-sqlite-demo.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        profession TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

@mcp_server.tool(description="Ajouter des données à la table people via une requête SQL INSERT")
def add_people(query: str) -> bool:
    conn, cursor = init_db()
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erreur : {e}")
        return False
    finally:
        cursor.close()

@mcp_server.tool(description="Lire des données des la table via une requête SQL SELECT")
def read_data(query: str = "SELECT * FROM people") -> list:
    conn, cursor = init_db()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Erreur : {e}")
        return []
    finally:
        conn.close()

if __name__ == '__main__':
    print("Démarrage du server MCP local")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"],
    )

    args = parser.parse_args()
    mcp_server.run(args.server_type)
