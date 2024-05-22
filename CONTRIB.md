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
- If you do not have pipev, install it (see [more instructions](https://pipenv.pypa.io/en/latest/installation.html)
```bash
pip install pipenv --user
```
- In case you have any issue connecting check https://gist.github.com/zubaer-ahammed/c81c9a0e37adc1cb9a6cdc61c4190f52?permalink_comment_id=4473133

- From the root of this directory, create a database with the sql statements from raw_mysql_schema.sql into the MySQL server
```bash
mysql -u root -p < scripts/sql_insert_emi_data/raw_mysql_schema.sql
````
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

- Edit the scripts/sql_insert_emi_data/config.py file and make sure that the path are pointing to the correct files.

## Allow for insertion in mysql

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

## Get Ontop

- Download and unzip it from https://sourceforge.net/projects/ontop4obda/files/ontop-5.1.1/ontop-cli-5.1.1.zip/download

- Get MySQL JDBC driver  
We recommend to download the version mysql-connector-j-8.2.0.jar from the MySQL download archive at
https://downloads.mysql.com/archives/c-j/

- Move the mysql-connector-j-8.2.0.jar to the ontop-cli-5.1.1/lib folder
- Create ontop properties text file `./ontop_config/emi-v0_1.properties` such as the example below (change the url parameter if necessary)

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






