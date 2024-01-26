# import pytest
# from fromage import FromageETL

# @pytest.fixture
# def fromage_etl_fixture():
#     url = 'https://www.laboitedufromager.com/liste-des-fromages-par-ordre-alphabetique/'
#     db_path = 'my_database.db '
#     return FromageETL(url, db_path)

# def test_extract(fromage_etl_fixture):
#     html_content = fromage_etl_fixture.extract()
#     assert html_content is not None

# def test_transform(fromage_etl_fixture):
#     html_content = "<table><tr><td>Fromage1</td><td>Famille1</td><td>Pâte1</td></tr></table>"
#     transformed_data = fromage_etl_fixture.transform(html_content)
#     assert transformed_data == [('Fromage1', 'Famille1', 'Pâte1', 'date')]

# def test_load(fromage_etl_fixture):
#     data = [('Fromage1', 'Famille1', 'Pâte1', 'date')]
#     fromage_etl_fixture.load(data)

#     df = fromage_etl_fixture.get_dataframe_from_db()
#     assert len(df) == 1

# def test_group_by_family(fromage_etl_fixture):
#     test_data = [('Fromage1', 'Famille1', 'Pâte1', 'date'),
#                  ('Fromage2', 'Famille1', 'Pâte2', 'date'),
#                  ('Fromage3', 'Famille2', 'Pâte3', 'date')]
#     fromage_etl_fixture.load(test_data)

#     counts_by_family = fromage_etl_fixture.group_by_family()
#     assert len(counts_by_family) == 2
#     assert counts_by_family.iloc[0]['cheese_count'] == 2
#     assert counts_by_family.iloc[1]['cheese_count'] == 1

# def test_run_etl(fromage_etl_fixture):
#     fromage_etl_fixture.run_etl()

#     df_from_db = fromage_etl_fixture.get_dataframe_from_db()
#     assert not df_from_db.empty

# def test_get_dataframe_from_db(fromage_etl_fixture):
#     data = [('Fromage1', 'Famille1', 'Pâte1', 'date'),
#             ('Fromage2', 'Famille1', 'Pâte2', 'date')]
#     fromage_etl_fixture.load(data)

#     df_from_db = fromage_etl_fixture.get_dataframe_from_db()
#     assert len(df_from_db) == 2

# def test_group_by_family_empty_db(fromage_etl_fixture):
#     counts_by_family = fromage_etl_fixture.group_by_family()
#     assert counts_by_family.empty

# def test_group_by_family_single_family(fromage_etl_fixture):
#     data = [('Fromage1', 'Famille1', 'Pâte1', 'date')]
#     fromage_etl_fixture.load(data)

#     counts_by_family = fromage_etl_fixture.group_by_family()
#     assert len(counts_by_family) == 1
#     assert counts_by_family.iloc[0]['cheese_count'] == 1

# def test_group_by_family_multiple_families(fromage_etl_fixture):
#     data = [('Fromage1', 'Famille1', 'Pâte1', 'date'),
#             ('Fromage2', 'Famille2', 'Pâte2', 'date'),
#             ('Fromage3', 'Famille1', 'Pâte3', 'date')]
#     fromage_etl_fixture.load(data)

#     counts_by_family = fromage_etl_fixture.group_by_family()
#     assert len(counts_by_family) == 2
#     assert counts_by_family.iloc[0]['cheese_count'] == 2
#     assert counts_by_family.iloc[1]['cheese_count'] == 1

# def test_group_by_family_no_data(fromage_etl_fixture):
#     counts_by_family = fromage_etl_fixture.group_by_family()
#     assert counts_by_family.empty
