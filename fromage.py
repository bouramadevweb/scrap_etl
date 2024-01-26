import sqlite3
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

class FromageETL:
    def __init__(self, url, db_path):
        """
        Constructeur de la classe.

        Args:
            url (str): L'URL de la page web à extraire.
            db_path (str): Le chemin vers la base de données SQLite.
        """
        self.url = url
        self.db_path = db_path

    def extract(self):
        """
        Extrait le contenu HTML de la page web.

        Returns:
            str: Le contenu HTML de la page web.
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"échec de la récupération de la page. Status code: {response.status_code}")
            return None

    def transform(self, html_content):
        """
        Transforme le contenu HTML en une liste de tuples.

        Args:
            html_content (str): Le contenu HTML à transformer.

        Returns:
            list: Une liste de tuples représentant les données extraites.
        """
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            data_fromage = []

            table = soup.find('table')

            if table:
                for row in table.find_all('tr')[1:]:
                    columns = row.find_all('td')
                    fromage = columns[0].text.strip()
                    family = columns[1].text.strip()
                    paste = columns[2].text.strip()
                    date = datetime.now().strftime('%Y-%m-%d')

                    data_fromage.append((fromage, family, paste, date))
            return data_fromage
        else:
            return None

    def load(self, data):
        """
        Charge les données dans la base de données SQLite.

        Args:
            data (list): La liste de tuples représentant les données à charger.
        """
        if data:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cheese_ods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fromage TEXT,
                    family TEXT,
                    paste TEXT,
                    date TEXT
                )
            ''')

            cursor.executemany('''
                INSERT OR IGNORE INTO cheese_ods (fromage, family, paste, date)
                VALUES (?, ?, ?, ?)
            ''', data)

            conn.commit()
            conn.close()

    def get_dataframe_from_db(self):
        """
        Récupère les données de la base de données sous forme de DataFrame.

        Returns:
            DataFrame: Un DataFrame contenant les données de la base de données.
        """
        conn = sqlite3.connect(self.db_path)
        query = 'SELECT * FROM cheese_ods'
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def group_by_family(self):
        """
        Groupe les données par famille et compte le nombre de fromages pour chaque famille.

        Returns:
            DataFrame: Un DataFrame contenant le nombre de fromages par famille.
        """
        df = self.get_dataframe_from_db()
        counts = df.groupby('family').size().reset_index(name='cheese_count')
        return counts

    def run_etl(self):
        """
        Exécute le processus ETL complet.
        Extrait les données, les transforme, puis les charge dans la base de données.
        """
        html_content = self.extract()
        transformed_data = self.transform(html_content)
        self.load(transformed_data)
url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
DB_PATH = 'my_database.db'

etl = FromageETL(url, DB_PATH)
etl.run_etl()

# Lire les données depuis la base de données avec Pandas
df_from_db = etl.get_dataframe_from_db()

# Afficher le DataFrame
#print(df_from_db)
#counts_by_letter = etl.group_by_letter()
#print(counts_by_letter)
# Utilisation de la nouvelle méthode
counts_by_family = etl.group_by_family()
print(counts_by_family)
#counts_by_first_letter = etl.group_by_first_letter_of_family()
#print(counts_by_first_letter)