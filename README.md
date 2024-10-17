# Earth Metabolome Ontology
The latest and official version of the Earth Metabolome Initiative (EMI) ontology is available in [`emi.ttl`](emi.ttl) that can replace the enpkg vocabulary, for example. 

**Any issue, change or suggestion should be done in [`emi.ttl`](emi.ttl)**. The ontology documentation, other ontology files in [docs](/docs) and [ontop_config](/ontop_config), and the [emi_no_import.ttl](emi_no_import.ttl) file are generated based on the [`emi.ttl`](emi.ttl). The  [emi_no_import.ttl](emi_no_import.ttl) is the same as [`emi.ttl`](emi.ttl) without imported ontologies. The ontology documentation is fully generated with the [WIDOCO tool](https://github.com/dgarijo/Widoco).

To open and edit the ontology, it can be done  with a text editor or an ontology editor such as [Protege](https://protege.stanford.edu). 

For more details, see the [EMI ontology documentation](https://www.dbgi.org/earth_metabolome_ontology/).


## Natural Product taxonomy
The [`npc_taxonomy.ttl`](npc_taxonomy.ttl) file is an SKOS-based OWL ontology for the structural classification of natural products derived from the [NPClassifier tool](https://pubs.acs.org/doi/10.1021/acs.jnatprod.1c00399). This OWL ontology was generated with the script in [`scripts`](scripts/natural_product_taxonomy).

For more details, see [Natural Product Classifier vocabulary](http://www.dbgi.org/earth_metabolome_ontology/docs-npc/index-en.html).

## Example of a knowledge graph using the EMI ontology
A knowledge graph was generated based on the EMI ontology with the [pf1600 dataset](https://doi.org/10.5281/zenodo.10827917) and structure metadata dataset [sqlite](https://zenodo.org/records/12534675). It contains more than 32 million triples and is accessible and downloadable via the SPARQL endpoint: [https://biosoda.unil.ch/graphdb/sparql](https://biosoda.unil.ch/graphdb/sparql).

# Tutorial to generate RDF triples based on the EMI ontology

**Summary**
1. [Introduction](#introduction)
2. [Allowing for insertion in mysql](#allowing-for-insertion-in-mysql)
3. [Inserting the sample data into a MySQL database](#inserting-the-sample-data-into-a-mysql-database)
4. [Generating the EMI-based RDF graph](#generating-the-emi-based-rdf-graph)
5. [Importing the generated RDF-based files in a triple store](#importing-the-generated-rdf-based-files-in-a-triple-store)
6. [Interacting with the EMI virtual knowledge graph (VKG)](#interacting-with-the-emi-virtual-knowledge-graph-vkg)

## Introduction
In this tutorial, we will use a toy dataset and it requires mainly [MySQL](https://mysql.com) (version 8) and [Ontop](https://ontop-vkg.org) (version 5.1 or later).

- Download the toy dataset from [ENPKG full](https://github.com/enpkg/enpkg_full).
- Download and install  
[MySQL 8.2](https://downloads.mysql.com/archives/community/). 
- To check, if MySQL was correctly installed 
```bash
mysql --version
```
- Install the [Pipfile](scripts/sql_insert_emi_data/Pipfile):
```bash
cd ./scripts/sql_insert_emi_data
pipenv install
```
- If you do not have pipev, install it as shown below (see [more instructions](https://pipenv.pypa.io/en/latest/installation.html)).
```bash
pip install pipenv --user
```
- In case you have any issue connecting check https://gist.github.com/zubaer-ahammed/c81c9a0e37adc1cb9a6cdc61c4190f52?permalink_comment_id=4473133
- From the root of this directory, create a database `emi_db` with the sql statements from raw_mysql_schema.sql into the MySQL server
```bash
mysql -u root -p < ./scripts/sql_insert_emi_data/raw_mysql_schema.sql
```
> **_NOTE:_** Optionally, if an `emi_db` already exists in your MySQL server and if you want to start from scratch (i.e., an empty database), you should drop it before running the `raw_mysql_schema.sql` script with the command above. Note that the data will be added in the database allowing duplicates. The command below will drop `emi_db`.
```bash
mysql -u root -p --execute="DROP DATABASE IF EXISTS emi_db ;"
```

- You can connect to the database as shown below     
```bash
mysql -u root -p
```
- Check if the schema was created

```sql
show databases;
use emi_db;
show tables;
```
Alternatively, you can use the MYSQL Workbench to work with the emi_db database

```bash
mysql-workbench
```
> **_NOTE:_** We observe that the structure_metadata (sqlite) is missing. Alternatively, you can consider to download an example from https://zenodo.org/records/12534675.


## Allowing for insertion in mysql

```bash
mysql -u root -p
```

```sql
SHOW VARIABLES LIKE "local_infile";
SET GLOBAL local_infile = 1;
SHOW VARIABLES LIKE "local_infile";
```
Loading local data is now enabled. To check it, you can run:
```sql
mysql> SHOW VARIABLES LIKE "local_infile";
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| local_infile  | ON    |
+---------------+-------+
1 row in set (0,01 sec)
```
## Inserting the sample data into a MySQL database
- Edit the scripts/sql_insert_emi_data/config.py file and make sure that the path are pointing to the correct files.
> **_NOTE:_** To generate also a SKOS-based version of the Open Tree of Life download the tsv files from https://tree.opentreeoflife.org/about/taxonomy-version and include in the config.py the directory path to these files by replacing the ```None``` value with this path.

- Run the command below to intiate the insertion in the emi_db database.
```bash
pipenv run python ./scripts/sql_insert_emi_data/main.py
```
> **_NOTE:_** Alternatively, you can run `python ./scripts/sql_insert_emi_data/main.py`, if you have all dependencies listed in [Pipfile](scripts/sql_insert_emi_data/Pipfile) installed in your python enviroment.

> **IMPORTANT**: This tutorial was only tested with the Python 3.9 version, but it might work in any other 3.x version.
 
## Generating the EMI-based RDF graph

- Download and unzip the **Ontop CLI** tool from https://sourceforge.net/projects/ontop4obda/files/ontop-5.1.1/ontop-cli-5.1.1.zip/download

- Get MySQL JDBC driver  
We recommend to download the version mysql-connector-j-8.2.0.jar from the MySQL download archive at
https://downloads.mysql.com/archives/c-j/

- Move the mysql-connector-j-8.2.0.jar to the `ontop-cli-5.1.1/lib` folder
- Create ontop properties text file `./ontop_config/emi-v0_2/emi-v0_2.properties` such as the example below (change the user, password, and, if necessary, the url parameter too)

```
jdbc.password=root
jdbc.user=root
jdbc.name=5e86f1b2-b7d8-4a17-9bc6-32b98b12ed79
jdbc.url=jdbc\:mysql\://localhost\:3306/emi_db
jdbc.driver=com.mysql.cj.jdbc.Driver
ontop.inferDefaultDatatype=True
```

- Run the ontop command line tool with the command below in the current directory. Please refer to the right path to the ontop tool 
```bash
PATH/TO/ontop-cli-5.1.1/ontop materialize -m ./ontop_config//emi-v0_2/emi-v0_2.obda -t ./ontop_config/emi-v0_2/emi-v0_2.ttl -p ./ontop_config/emi-v0_2/emi-v0_2.properties -f turtle --enable-annotations  --separate-files -o ./data/ontop
```
> **_NOTE:_**  you can allocated more memory to run ontop by editing the PATH/TO/ontop-cli-5.1.1/ontop file. For intance, `ONTOP_JAVA_ARGS="-Xmx16g"` instead of `ONTOP_JAVA_ARGS="-Xmx1g"`
> **_NOTE:_** If necessary you may need to specify the classpath for the mysql-connector-java .jar
```bash
export CLASSPATH=$CLASSPATH:/Applications/ontop-cli-5.1.1/lib/mysql-connector-java-8.2.0.jar
```
## Importing the generated RDF-based files in a triple store

For [GraphDB 10.6](https://graphdb.ontotext.com/), see [Loading data using importrdf](https://graphdb.ontotext.com/documentation/10.6/loading-data-using-importrdf.html).

For [Stardog](https://stardog.com), see [Adding data documentation section](https://docs.stardog.com/operating-stardog/database-administration/adding-data). 

For [Virtuoso](https://vos.openlinksw.com/owiki/wiki/VOS#2024-02-13%3A%20Virtuoso%207.2.12%20Released%2C%20Open%20Source%20Edition), see [Loading RDF data](https://docs.openlinksw.com/virtuoso/rdfperfloading/).

## Interacting with the EMI virtual knowledge graph (VKG)

Ontop allow us to build vitual knowledge graphs. With its plugin for Protege, we can query the VKG for more information see the section [Setting up the VKG using Ontop-Protégé](https://github.com/ontop/ontop-patterns-tutorial/blob/main/README.md#setting-up-the-vkg-using-ontop-protégé). 

> **_NOTE:_** We recommend to download and use the [Ontop+Protege 5.1.1](https://sourceforge.net/projects/ontop4obda/files/ontop-5.1.1/ontop-protege-bundle-platform-independent-5.1.1.zip/download). To build the VKG, you will also need all configuration files used to materialize the VKG in subsection [Generating the EMI-based RDF graph](#generating-the-emi-based-rdf-graph), notably `./ontop_config/emi-v0_2/emi-v0_2.obda`, `./ontop_config/emi-v0_2/emi-v0_2.ttl` and `./ontop_config/emi-v0_2/emi-v0_2.properties`. 

A full tutorial about Ontop-Protégé is available at (https://doi.org/10.1016/j.patter.2021.100346). 

