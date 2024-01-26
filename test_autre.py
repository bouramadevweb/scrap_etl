# # test_fromage_etl.py

# import pytest
# from fromage import FromageETL

# @pytest.fixture
# def etl_instance():
#     url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
#     db_path = 'test_database.db'
#     return FromageETL(url, db_path)

# def test_extract(etl_instance, mocker):
#     # Utiliser le module `mocker` pour simuler la réponse de requests.get
#     mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, text='<html><body></body></html>'))

#     html_content = etl_instance.extract()
#     assert html_content is not None

# def test_transform(etl_instance):
#     html_content = '<table><tr><td>Fromage</td><td>Famille</td><td>Pâte</td></tr><tr><td>Brie</td><td>Fromage</td><td>Molle</td></tr></table>'
#     transformed_data = etl_instance.transform(html_content)
    
#     assert transformed_data == [('Brie', 'Fromage', 'Molle', '24-02-2024')]

# def test_load(etl_instance):
#     data = [('Brie', 'Fromage', 'Molle', '2024-02-22')]
#     etl_instance.load(data)

#     df_from_db = etl_instance.get_dataframe_from_db()
#     assert not df_from_db.empty

# def test_group_by_letter(etl_instance):
#     etl_instance.run_etl()
#     counts_by_letter = etl_instance.group_by_letter()
#     assert not counts_by_letter.empty

# def test_group_by_family(etl_instance):
#     etl_instance.run_etl()
#     counts_by_family = etl_instance.group_by_family()
#     assert not counts_by_family.empty

# def test_group_by_first_letter_of_family(etl_instance):
#     etl_instance.run_etl()
#     counts_by_first_letter = etl_instance.group_by_first_letter_of_family()
#     assert not counts_by_first_letter.empty
