# Database migration tool
- Track changes to code and rollback for database models/tables
- Alembic is a tool to make changes in the database
- Alembic can automatically pull database models from sqlAlchemy and generate proper tables.

# Install Alembic
- pip install alembic

# Create a alembic folder
- alembic init <folder name>
- creates a new folder with important files and also a alembic.ini -file that is  not in the folder.

# Set up alembic
- In the env.py file:
    from app.models import Base
    Add the Base to: target_metadata = Base.metadata
- Next go to alembic.ini-file
    sqlAlchemy_URL set to bland and the go to anv.py to override that line in the ini-file.
- In alembic folder env.py-file
    Under the config -line add a new config: config.set_main_option and add the sqlAlchemy_URL. 
    Import the config.py file and the settings-function.
    Set all the parameters for access of the database to ex. settings.DATABASE_USERNAME, etc.

- In terminal window, type alembic --help to get help menu.

# Create a alembic message
- in terminal, by use of the -m flag:
    alembic revision -m "Message"
- This creates a new folder in the alembic-folder called versions.

# Entering the versions
- There will be a few auto-generated stuff.
- Two important functions called, upgrade and downgrade.
- These functions handles all the logic for creating our tables.
- Upgrade handles creating and update the table and downgrade rollbacks.

# Commands
- Always start in terminal window by typing alembic
- --help = Will give a list of suggestion commands
- upgrade followed by "revision-number" will update our database.
- Or upgrade followed by "head" will update DB by latest version. Upgrade can also be used with +1 or +2.
- downgrade followed by "down_revision" will rollback to previous version of DB-tables.
- Or downgrade followed by "-1" will do same as above. You can add "-5" to go back 5 versions.
- alembic revision -m "message" = will create a new version to add DB
- alembic current = Will show on what version we are at.
- alembic history = Will show history of whats been done.

# How to tell alembic to upgrade the postgres-db according to the SQLalchemy models
- first app.models import Base must be imported
- the commando: alembic revision --autogenerate -m "auto-vote" 
- By typing vote it looks in our models where vote can be found. And creates a revision
    Then shows the upgrades it will do.
- Then do "alembic upgrade head".
