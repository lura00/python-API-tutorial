# Install PostgreSQL
- https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Choose tha latest version for whatever ops-system you have.
- Install the file
- Leave path to default
- You do not have to change port for this tutorial.
- Set a easy password to remember

# Run PostgreSQL
- start pgadmin (you can just search in your computer)
- Once open pgadming you will have to set a superUser-password
    Does not have to be the same as in the installer

# Types in postgresql
- Datatypes     -Postgres                    -python
    Numeric         Int, decimal, precision     Int, float
    Text            Varchar, text               String
    Bool            boolean                     boolean
    sequence        array                       list 

# Extra attributes
- Null, not null or null. Not null will not allow row to be null.
- Uniqe, set a key parameter to uniqe so only one can be entered to table.

# Create a server
- Under "server" click create --> server
- Name the server to a meaningful name.
- Set connection to whattever host or ip-adress. If you are using local host, just type "localhost"
- in the installment we set a port, in my case the default "5432" so we put that in the "port"-field.
- username by default is superuser "postgres"
- set password.

# Create a database
- Right click on the headline that says "databases --> create --> database
- Set a name for your database

# Create a table
- In your new database there is a dropdown menu, click on Schemas --> public
- Right click on tables --> create
- Name your table with a logic name
- In "Columns" hit + to enter a row, start by entering the headline of the row then
    datatype etc.

# Adding rows
- Right click on your new table
- Choose properties
- Once you are in there go too "Columns" and as mentioned above, do the same.
- You can choose between a lot of datatypes.
- If you for example choose Boolean you can set default value to ex. False 
    (if something is for sale or     not)
- If you want a timestamp there is a few datatypes. I choose timestamt with timezone.
    To let Postgres take care of this instead of fastAPI click on the edit button
    go to Constraints and ad "NOW()" to default, this will generate a timestamp.

# Perform a query
- Right click on your database name, select query tool.
- Now you can enter SQL-commands and filter your table for example:
    SELECT * FROM products;

    SELECT and FROM are sql commands and * and products is what I, the user want to get.
- So the above command will print everything (*) within my table "products".
- If I have a column named "name" I can change the * to "name" and only the name column will print.
- We can pass in as many parameters as we want as long as the exist in the table.