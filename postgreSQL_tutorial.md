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
