import pytest
import sqlite3
from fromage import FromageETL

@pytest.fixture
def etl_instance():
    url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
    db_path = ':memory:'  # Utilisation d'une base de données en mémoire pour les tests
    return FromageETL(url, db_path)

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

