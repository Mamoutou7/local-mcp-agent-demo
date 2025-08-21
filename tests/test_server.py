import unittest
import sqlite3
import os
import requests
import time
import threading

# Importez les fonctions du serveur
from server.server import init_db, add_people, read_data
from mcp.server.fastmcp import FastMCP


class TestMCPServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configurer le serveur MCP et la base de données avant les tests."""
        # Initialiser la base de données
        cls.db_file = "local-sqlite-demo.db"
        conn, cursor = init_db()
        conn.close()

        # Lancer le serveur MCP dans un thread séparé
        cls.server = FastMCP(name='local-sqlite-demo')
        cls.server_thread = threading.Thread(target=cls.server.run, kwargs={'server_type': 'sse'})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)  # Augmenter légèrement le temps d'attente pour assurer le démarrage

    @classmethod
    def tearDownClass(cls):
        """Nettoyer après les tests."""
        # Arrêter le serveur (optionnel, dépend de l'implémentation de FastMCP)
        # cls.server.stop()  # Ajouter si FastMCP a une méthode stop()

        # Supprimer la base de données
        if os.path.exists(cls.db_file):
            os.remove(cls.db_file)

    def setUp(self):
        """Réinitialiser la base de données avant chaque test."""
        conn, cursor = init_db()
        cursor.execute("DELETE FROM people")  # Vider la table
        conn.commit()
        conn.close()

    def test_add_people(self):
        """Tester l'outil add_people."""
        query = "INSERT INTO people (name, age, gender, profession) VALUES ('Alice', 25, 'F', 'Développeuse')"
        result = add_people(query)
        self.assertTrue(result, "L'ajout de données devrait réussir")

        # Vérifier que les données sont dans la base
        conn, cursor = init_db()
        cursor.execute("SELECT * FROM people WHERE name = 'Alice'")
        data = cursor.fetchall()
        conn.close()
        self.assertEqual(len(data), 1, "Une ligne devrait être insérée")
        self.assertEqual(data[0], (1, 'Alice', 25, 'F', 'Développeuse'), "Les données insérées sont incorrectes")

    def test_read_data(self):
        """Tester l'outil read_data."""
        # Ajouter des données pour le test
        conn, cursor = init_db()
        cursor.execute("INSERT INTO people (name, age, gender, profession) VALUES ('Bob', 30, 'M', 'Architecte')")
        conn.commit()
        conn.close()

        # Tester la lecture
        result = read_data("SELECT * FROM people")
        self.assertEqual(len(result), 1, "Une ligne devrait être lue")
        self.assertEqual(result[0], (1, 'Bob', 30, 'M', 'Architecte'), "Les données lues sont incorrectes")

    def test_read_data_empty(self):
        """Tester read_data sur une table vide."""
        result = read_data("SELECT * FROM people")
        self.assertEqual(result, [], "La lecture d'une table vide devrait retourner une liste vide")

    def test_add_people_invalid_query(self):
        """Tester add_people avec une requête SQL invalide."""
        query = "INSERT INTO people (wrong_column) VALUES ('Test')"
        result = add_people(query)
        self.assertFalse(result, "Une requête invalide devrait échouer")

    def test_server_connectivity(self):
        """Tester si le serveur MCP est accessible."""
        try:
            response = requests.get("http://127.0.0.1:8000/", timeout=5)  # Ajuster l'URL si nécessaire
            self.assertEqual(response.status_code, 200, "Le serveur devrait répondre avec un code 200")
        except requests.ConnectionError:
            self.fail("Le serveur MCP n'est pas accessible")


if __name__ == '__main__':
    unittest.main()