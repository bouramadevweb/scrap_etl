"""
Module de gestion ETL pour le traitement des données sur les fromages.
"""
import  requests
import  sqlite3
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

class CheeseETL:
    """ fromage class """
    def __init__(self, URL, db_path ):
        """ Constructeur """
        self.url = URL
        self.db_path = db_path
    # fonction extration
    def extract(self):
        """Extrait le contenu HTML de la page web."""
        response = requests.get(self.url)
        # test le statut 
        if response.status_code == 200:
            # si bon return  la reponse
            return response.text
        else:
            print(f"échec de la récupération de la page. Status code: {response.status_code}")
            return None
    # fonction qui fait la transformation
    def transform(self, html_content):

        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            data_fromage = []

            # Trouver la première table dans la page
            table = soup.find('table')

            if table:
                # Supposons que les colonnes de la table sont dans l'ordre :fromage, famille, pâte
                for row in table.find_all('tr')[1:]:  # Commencer à la deuxième ligne pour éviter les en-têtes
                    columns = row.find_all('td')
                    fromage = columns[0].text.strip()
                    family = columns[1].text.strip()
                    paste = columns[2].text.strip()
                    creation_date = datetime.now().strftime('%Y-%m-%d')

                    data_fromage.append((fromage, family, paste, creation_date))
            return data_fromage
            

        else:
            return None
    # fonction pour la connection
    def load(self, data):
        if data:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Créer la table si elle n'existe pas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cheese_ods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fromage TEXT,
                    family TEXT,
                    paste TEXT,
                    creation_date TEXT
                )
            ''')

            # Insérer les données dans la table
            cursor.executemany('''
                INSERT INTO cheese_ods (fromage, family, paste, creation_date)
                VALUES (?, ?, ?, ?)
            ''', data)

            # Valider les changements et fermer la connexion
            conn.commit()
            conn.close()
    
    def get_dataframe_from_db(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        conn = sqlite3.connect(self.db_path)
        query = 'SELECT * FROM cheese_ods'
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    # fonction qui execute etl
    def run_etl(self):
        html_content = self.extract()
        transformed_data = self.transform(html_content)
        self.load(transformed_data)


url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
DB_PATH = 'fromage_database.db'

etl = CheeseETL(url, DB_PATH)
etl.run_etl()

# Lire les données depuis la base de données avec Pandas
df_from_db = etl.get_dataframe_from_db()

# Afficher le DataFrame
print(df_from_db)
