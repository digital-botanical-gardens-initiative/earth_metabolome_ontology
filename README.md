# Earth Metabolome Ontology
The first version of a draft of the Earth Metabolome Initiative (EMI) ontology is available in [`emi.ttl`](emi.ttl) that can replace the enpkg vocabulary. 

For more details, see [EMI ontology draft documentation](http://www.dbgi.org/earth_metabolome_ontology/).


## Natural Product taxonomy
The [`npc_taxonomy.ttl`](npc_taxonomy.ttl) file is an SKOS-based OWL ontology for the structural classification of natural products derived from the [NPClassifier tool](https://pubs.acs.org/doi/10.1021/acs.jnatprod.1c00399). This OWL ontology was generated with the script in [`scripts`](scripts/natural_product_taxonomy).

For more details, see [Natural Product Classifier vocabulary](http://www.dbgi.org/earth_metabolome_ontology/docs-npc/index-en.html).

# Tutorial to generate RDF triples based on the EMI ontology

In this tutorial we will use a toy dataset and it requires mainly [MySQL](https://mysql.com) (version 8) and [Ontop](https://ontop-vkg.org) (version 5.1 or later) .

- Download the toy dataset in [ENPKG full](https://github.com/enpkg/enpkg_full)
- Download and install  
[MySQL 8.2](https://downloads.mysql.com/archives/community/) 
- To check, if MySQL was correctly installed 
```bash
mysql --version
```
- Install the Pipfile
```bash
cd scripts/sql_insert_emi_data
pipenv install
```
- If you do not have pipev, install it as shown below (see [more instructions](https://pipenv.pypa.io/en/latest/installation.html)).
```bash
pip install pipenv --user
```
- In case you have any issue connecting check https://gist.github.com/zubaer-ahammed/c81c9a0e37adc1cb9a6cdc61c4190f52?permalink_comment_id=4473133
- From the root of this directory, create a database `emi_db` with the sql statements from raw_mysql_schema.sql into the MySQL server
```bash
mysql -u root -p < scripts/sql_insert_emi_data/raw_mysql_schema.sql
```
> **_NOTE:_** Optionally if an `emi_db` already exists in your MySQL server and if you want to start from scratch, you should drop it before running the `raw_mysql_schema.sql` script with the command above. Note that the data will be added in the database allowing duplicates. The command below will drop `emi_db`.
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
**We observe that the structure_metadata (sqlite) is missing for now.**


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
- Run the command below to intiate the insertion 
```bash

``` 
## Get Ontop

- Download and unzip it from https://sourceforge.net/projects/ontop4obda/files/ontop-5.1.1/ontop-cli-5.1.1.zip/download

- Get MySQL JDBC driver  
We recommend to download the version mysql-connector-j-8.2.0.jar from the MySQL download archive at
https://downloads.mysql.com/archives/c-j/

- Move the mysql-connector-j-8.2.0.jar to the ontop-cli-5.1.1/lib folder
- Create ontop properties text file `./ontop_config/emi-v0_1.properties` such as the example below (change the user, password, and, if necessary, the url parameter too)

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
PATH/TO/ontop-cli-5.1.1/ontop materialize -m ./ontop_config/emi-v0_1.obda -t ./ontop_config/emi-v0_1.ttl -p ./ontop_config/emi-v0_1.properties -f turtle --enable-annotations  --separate-files -o ./data/ontop
```
> **_NOTE:_**  you can allocated more memory to run ontop by editing the PATH/TO/ontop-cli-5.1.1/ontop file. For intance, `ONTOP_JAVA_ARGS="-Xmx16g"` instead of `ONTOP_JAVA_ARGS="-Xmx1g"`
> **_NOTE:_** If necessary you may need to specify the classpath for the mysql-connector-java .jar
```bash
export CLASSPATH=$CLASSPATH:/Applications/ontop-cli-5.1.1/lib/mysql-connector-java-8.2.0.jar
```




