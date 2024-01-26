# Import des bibliothèques nécessaires
import pytest
from tkinter import Tk
from autre import FromageETLUI

# Fixture pour initialiser une instance de l'interface utilisateur
@pytest.fixture
def fromage_etl_ui_fixture():
    url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
    db_path = 'test_db.db'
    return FromageETLUI(url, db_path)

# Test de mise à jour de la base de données
def test_update_database(fromage_etl_ui_fixture):
    fromage_etl_ui_fixture.update_database()
    # Vérifie que la base de données contient des données après la mise à jour
    assert len(fromage_etl_ui_fixture.etl.get_dataframe_from_db()) > 0

# Test d'affichage du diagramme en camembert
def test_show_pie_chart(fromage_etl_ui_fixture):
    fromage_etl_ui_fixture.show_pie_chart()
    # Vérifie que la fenêtre du diagramme en camembert a été créée
    assert fromage_etl_ui_fixture.winfo_exists()

# Test d'affichage du taux de fiabilité
def test_show_reliability(fromage_etl_ui_fixture):
    fromage_etl_ui_fixture.show_reliability()
    # Vérifie que la fenêtre du taux de fiabilité a été créée
    assert fromage_etl_ui_fixture.winfo_exists()

# Test d'initialisation de l'interface utilisateur
def test_ui_initialization():
    url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
    db_path = 'test_db.db  '
    app = FromageETLUI(url, db_path)
    # Vérifie que l'instance créée est une instance de la classe Tk (Tkinter)
    assert isinstance(app, Tk)

# Test de fermeture de l'interface utilisateur
# def test_ui_close(fromage_etl_ui_fixture):
#     try:
#         fromage_etl_ui_fixture.destroy()
#         # Essayez d'accéder à une propriété après la destruction, cela devrait provoquer une erreur
#         assert not fromage_etl_ui_fixture.winfo_exists()
#     except _tkinter.TclError as e:
#         # Si une erreur TclError est levée, c'est attendu car la fenêtre a été détruite
#         assert "can't invoke \"winfo\" command: application has been destroyed" in str(e)



# Test du titre de l'interface utilisateur
def test_ui_title(fromage_etl_ui_fixture):
    # Vérifie que le titre de l'interface utilisateur est correct
    assert fromage_etl_ui_fixture.title() == "Fromage ETL"

# Test de présence du bouton de mise à jour
def test_ui_update_button(fromage_etl_ui_fixture):
    # Vérifie que le bouton de mise à jour existe dans l'interface utilisateur
    assert fromage_etl_ui_fixture.update_button.winfo_exists()

# Test de présence du bouton d'affichage du diagramme en camembert
def test_ui_pie_chart_button(fromage_etl_ui_fixture):
    # Vérifie que le bouton d'affichage du diagramme en camembert existe dans l'interface utilisateur
    assert fromage_etl_ui_fixture.show_pie_chart_button.winfo_exists()

# Test de présence du bouton d'affichage du taux de fiabilité
def test_ui_reliability_button(fromage_etl_ui_fixture):
    # Vérifie que le bouton d'affichage du taux de fiabilité existe dans l'interface utilisateur
    assert fromage_etl_ui_fixture.show_reliability_button.winfo_exists()

# Test du titre de la fenêtre du diagramme en camembert
def test_show_pie_chart_window_title(fromage_etl_ui_fixture):
    fromage_etl_ui_fixture.show_pie_chart()
    # Vérifie que le titre de la fenêtre du diagramme en camembert est correct
    pie_chart_window = fromage_etl_ui_fixture.children["!toplevel"]
    assert pie_chart_window.title() == "Diagramme en camembert"


def test_all_data_in_pie_chart(fromage_etl_ui_fixture):
    # Exécuter le processus ETL pour mettre à jour la base de données
    fromage_etl_ui_fixture.etl.run_etl()

    # Afficher le diagramme en camembert
    fromage_etl_ui_fixture.show_pie_chart()

    # Récupérer les données depuis la base de données
    df_from_db = fromage_etl_ui_fixture.etl.get_dataframe_from_db()

    # Récupérer les familles à partir des données
    families_in_data = set(df_from_db['family'])

    # Récupérer les familles à partir du diagramme en camembert
    counts_by_family = fromage_etl_ui_fixture.etl.group_by_family()
    families_in_pie_chart = set(counts_by_family['family'])

    # Vérifier que toutes les familles dans les données sont présentes dans le diagramme en camembert
    assert families_in_data.issubset(families_in_pie_chart)