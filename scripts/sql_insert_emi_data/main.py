from sqlite3_to_mysql import SQLite3toMySQL
from insert_data import *
from config import *
import mysql.connector

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        allow_local_infile=True,
        autocommit=True)
    if open_tree_of_life_dir is not None and open_tree_of_life_dir != "":
        SQLDataInsertion.sql_insert_emi_data(
            open_tree_of_life_dir,
            table_canonical_names['opentreeoflife'], ".tsv",  mydb, name_prefix="taxonomy",
            is_sample_folder=False, enclosed_by='', terminated_by='\t|\t')
        SQLDataInsertion.sql_insert_emi_data(
            open_tree_of_life_dir,
            table_canonical_names['opentreeoflife_synonym'], ".tsv", mydb, name_prefix="synonyms",
            is_sample_folder=False, enclosed_by='', terminated_by='\t|\t')
    SQLDataInsertion.sql_insert_emi_data(
        raw_data_root_folder,
        table_canonical_names['sample_metadata'], "_metadata.tsv", mydb, ionization=ionization_mode)
    SQLDataInsertion.sql_insert_emi_data(
        raw_data_root_folder, table_canonical_names['compound_summary'],
        "_WORKSPACE_SIRIUS/canopus_compound_summary.tsv", mydb, os.path.join(ionization_mode, ''),
        ionization=ionization_mode)
    SQLDataInsertion.sql_insert_emi_data(
        raw_data_root_folder, table_canonical_names['taxon_metadata'], "_taxo_metadata.tsv", mydb,
        os.path.join('taxo_output', ''), ionization=ionization_mode)
    SQLDataInsertion.sql_insert_emi_data(
        raw_data_root_folder, table_canonical_names['features_quant'],
        '_features_quant_' + ionization_mode + '.csv', mydb, os.path.join(ionization_mode, ''),
        ionization=ionization_mode, terminated_by=",")
    SQLDataInsertion.sql_insert_emi_data(
        raw_data_root_folder, table_canonical_names['compound_identifications'],
        "_WORKSPACE_SIRIUS/compound_identifications.tsv", mydb, os.path.join(ionization_mode, ''),
        ionization=ionization_mode)
    SQLDataInsertion.sql_insert_emi_data(
        raw_data_root_folder, table_canonical_names['isdb_reweighted_flat'],
        '_isdb_reweighted_flat_' + ionization_mode + '.tsv', mydb, os.path.join(ionization_mode, 'isdb', ''),
       ionization=ionization_mode)
    SQLDataInsertion.sql_insert_emi_data(
        raw_data_root_folder,
        table_canonical_names['molecular_network_metadata'], '_mn_metadata_' + ionization_mode + '.tsv', mydb,
        os.path.join(ionization_mode, 'molecular_network', ''), ionization=ionization_mode)
    SQLDataInsertion.sql_insert_emi_data(
        raw_data_root_folder,
        table_canonical_names['molecular_network'], '_mn_' + ionization_mode + '.graphml', mydb,
        os.path.join(ionization_mode, 'molecular_network', ''), ionization=ionization_mode)
    SQLDataInsertion.sql_insert_emi_data(
        raw_data_root_folder,
        table_canonical_names['spec2vec_doc'], '_features_ms2_' + ionization_mode + '.mgf', mydb,
        os.path.join(ionization_mode, ''), ionization=ionization_mode)

    if structure_metadata_sqlite_file is not None and structure_metadata_sqlite_file != "":
        # insert the SQLite3 structures_metadata.db in the mysql db
        conversion = SQLite3toMySQL(
            sqlite_file=structure_metadata_sqlite_file,
            mysql_user=user,
            mysql_password=password,
            mysql_host=host,
            mysql_port=port,
            mysql_database=database,
            quiet=False,
        )
        conversion.transfer()

    if trait_dir is not None and trait_dir != "":
        for table_name in table_canonical_names['trait_data'].values():
            if table_name in ["enpkg","trydbAll","interactions"]:
                SQLDataInsertion.sql_insert_emi_data(
                    trait_dir,
                    table_name, ".tsv", mydb, name_prefix=table_name,
                is_sample_folder=False, enclosed_by='"', terminated_by='\t')
            else:
                SQLDataInsertion.sql_insert_emi_data(
                    trait_dir,
                    table_name, ".csv", mydb, name_prefix=table_name,
                    is_sample_folder=False, enclosed_by='"', terminated_by=',')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
