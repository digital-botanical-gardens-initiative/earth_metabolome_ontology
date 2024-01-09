
from sqlite3_to_mysql import SQLite3toMySQL
from canopus.insert_data import *
from db_cresentials import *
import mysql.connector



if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database,
        allow_local_infile=True,
        autocommit=True)

    SQLDataInsertion.sql_insert_emi_data(
        '/Users/tarcisio/Documents/git_repositories/enpkg_full/tests/data/output',
       'sample_metadata', "_metadata.tsv", mydb)
    SQLDataInsertion.sql_insert_emi_data(
       '/Users/tarcisio/Documents/git_repositories/enpkg_full/tests/data/output',
    'canopus_compound_summary', "_WORKSPACE_SIRIUS/canopus_compound_summary.tsv", mydb, "pos/")
    SQLDataInsertion.sql_insert_emi_data(
       '/Users/tarcisio/Documents/git_repositories/enpkg_full/tests/data/output',
        'taxon_metadata', "_taxo_metadata.tsv", mydb, "taxo_output/")
    SQLDataInsertion.sql_insert_emi_data(
        '/Users/tarcisio/Documents/git_repositories/enpkg_full/tests/data/output', 'features_quant',
        '_features_quant_pos.csv', mydb, "pos/", terminated_by=",")
    SQLDataInsertion.sql_insert_emi_data(
        '/Users/tarcisio/Documents/git_repositories/enpkg_full/tests/data/output',
        'compound_identifications', "_WORKSPACE_SIRIUS/compound_identifications.tsv", mydb, "pos/")
    SQLDataInsertion.sql_insert_emi_data(
        '/Users/tarcisio/Documents/git_repositories/enpkg_full/tests/data/output',
        'isdb_reweighted_flat', "_isdb_reweighted_flat_pos.tsv", mydb, "pos/isdb/")
    SQLDataInsertion.sql_insert_emi_data(
        '/Users/tarcisio/Documents/git_repositories/enpkg_full/tests/data/output',
        'molecular_network_metadata', "_mn_metadata_pos.tsv", mydb, "pos/molecular_network/")
    SQLDataInsertion.sql_insert_emi_data(
        '/Users/tarcisio/Documents/git_repositories/enpkg_full/tests/data/output',
        'molecular_network', "_mn_pos.graphml", mydb, "pos/molecular_network/")
    SQLDataInsertion.sql_insert_emi_data(
        '/Users/tarcisio/Documents/git_repositories/enpkg_full/tests/data/output',
        'spec2vec_doc', "_features_ms2_pos.mgf", mydb, "pos/")


    #insert the SQLite3 structures_metadata.db in the mysql db
    conversion = SQLite3toMySQL(
        sqlite_file="/Users/tarcisio/Documents/git_repositories/enpkg_full/"
                    "05_enpkg_meta_analysis/structures_metadata.db",
        mysql_user=user,
        mysql_password=password,
        mysql_host=host,
        mysql_port=port,
        mysql_database=database,
        quiet=False,
    )
    conversion.transfer()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
