"""
Module de gestion ETL pour le traitement des données sur les fromages.
"""
import  sqlite3
import  requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

class FromageETL:
    """ fromage class """
    def __init__(self, url, db_path ):
        """ Constructeur """
        self.url = url
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
    def transform(self, html_content):
        # fonction qui fait la transformation .
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            data_fromage = []

            # Trouver la première table dans la page
            table = soup.find('table')

            if table:
                #  les colonnes de la table dans l'ordre :fromage, famille, pâte ,date
                for row in table.find_all('tr')[1:]:  # Commencer à la deuxième ligne pour éviter les en-têtes
                    columns = row.find_all('td')
                    fromage = columns[0].text.strip().replace('', '')
                    family = columns[1].text.strip().replace('', '')
                    paste = columns[2].text.strip().replace('', '')
                    date = datetime.now().strftime('%Y-%m-%d')

                    data_fromage.append((fromage, family, paste, date))
            return data_fromage
            

        else:
            return None
    # fonction pour la connection
    def load(self, data):
        """.... """
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
                    date TEXT
                )
            ''')

            # Insérer les données dans la table
            cursor.executemany('''
                INSERT INTO cheese_ods (fromage, family, paste, date)
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
    def group_by_letter(self):
        """Charger les données depuis la base de données ."""
        df = self.get_dataframe_from_db()

        # Ajouter une colonne 'letter' représentant la première lettre du nom du fromage
        df['letter'] = df['fromage'].str[0].str.upper()

        # Grouper par la lettre et compter le nombre de fromages pour chaque lettre
        counts = df.groupby('letter').size().reset_index(name='cheese_count')

        return counts 
    def group_by_family(self):
        # Charger les données depuis la base de données
        df = self.get_dataframe_from_db()

        # Grouper par la colonne 'family' et compter le nombre de fromages pour chaque famille
        counts = df.groupby('family').size().reset_index(name='cheese_count')

        return counts
    def group_by_first_letter_of_family(self):
        # Charger les données depuis la base de données
        df = self.get_dataframe_from_db()

        # Ajouter une colonne 'family_first_letter' représentant la première lettre de la famille
        df['family_first_letter'] = df['family'].str[0].str.upper()

        # Grouper par la première lettre de la famille et compter le nombre de fromages pour chaque lettre
        counts = df.groupby('family_first_letter').size().reset_index(name='cheese_count')

        return counts

    # fonction qui execute etl
    def run_etl(self):
        
        html_content = self.extract()
        transformed_data = self.transform(html_content)
        self.load(transformed_data)


url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
DB_PATH = 'fromage_database.db'

etl = FromageETL(url, DB_PATH)
etl.run_etl()

# Lire les données depuis la base de données avec Pandas
df_from_db = etl.get_dataframe_from_db()

# Afficher le DataFrame
print(df_from_db)
counts_by_letter = etl.group_by_letter()
#print(counts_by_letter)
# Utilisation de la nouvelle méthode
counts_by_family = etl.group_by_family()
print(counts_by_family)
counts_by_first_letter = etl.group_by_first_letter_of_family()
#print(counts_by_first_letter)