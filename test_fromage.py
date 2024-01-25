import pytest
import sqlite3
from fromage import CheeseETL

@pytest.fixture
def etl_instance():
    url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
    db_path = ':memory:'  # Utilisation d'une base de données en mémoire pour les tests
    return CheeseETL(url, db_path)

def test_extract(etl_instance):
    html_content = etl_instance.extract()
    assert html_content is not None

def test_transform(etl_instance):
    html_content = etl_instance.extract()
    transformed_data = etl_instance.transform(html_content)
    assert transformed_data is not None
    assert len(transformed_data) > 0

# def test_load(etl_instance):
#     transformed_data = [('Cheese1', 'Family1', 'Paste1', '2022-01-01'),
#                         ('Cheese2', 'Family2', 'Paste2', '2022-01-02')]

#     etl_instance.load(transformed_data)

#     # Vérifier que les données ont été insérées dans la base de données
#     conn = sqlite3.connect(etl_instance.db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT COUNT(*) FROM cheese_ods")
#     count = cursor.fetchone()[0]
#     conn.close()

#     assert count == len(transformed_data)

# def test_get_dataframe_from_db(etl_instance):
#     transformed_data = [('Cheese3', 'Family3', 'Paste3', '2022-01-03'),
#                         ('Cheese4', 'Family4', 'Paste4', '2022-01-04')]

#     etl_instance.load(transformed_data)

#     # Vérifier que les données peuvent être lues avec Pandas
#     df = etl_instance.get_dataframe_from_db()
#     assert len(df) == len(transformed_data)

#     # Vérifier que les colonnes sont présentes
#     expected_columns = ['id', 'fromage', 'family', 'paste', 'creation_date']
#     assert all(col in df.columns for col in expected_columns)

#     # Vérifier que les données correspondent
#     for i, row in enumerate(transformed_data):
#         for j, col in enumerate(expected_columns[1:]):  # Ignorer la colonne 'id'
#             assert df.at[i, col] == row[j]

# # Autres tests peuvent être ajoutés selon les besoins
