# Getting started
- Google heroku python and follow the intstructions.
- login type in terminal "heroku login"
- This will open up a heroku CLI website, put in the credentials.
- close the window, now you are logged in.

# Deply an app
git add .
git commit
- type in terminal, heroku create <app-name>

- Create a file on the main-dirr called Procfile
- add 
    web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
- host 0.0.0.0 accepts amy host(ip) and ${} takes any PORT that heroku gives us.

# Create a postgres database with heroku-command
- By typing heroku addons:create heroku-postgresql:hobby-dev in the terminal it will create and connect to a db

- Click on the new postgres db, settings, Db credentials to find all user-info.

- Go to Config vars in Heroku-app-website. Add config vars.  
    
DATABASE_URL: postgres://hxgcvyuwhdefmd:32172d4f3253f634698fcc5b39713e3b8331a3dd2bbe10564db839e8bd572854@ec2-50-19-32-96.compute-1.amazonaws.com:5432/d9ecf0g7e6odgc

DATABASE_HOSTNAME: ec2-50-19-32-96.compute-1.amazonaws.com

DATABASE_PORT
5432

DATABASE_USERNAME
hxgcvyuwhdefmd

DATABASE_PASSWORD
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

DATABASE_NAME
d9ecf0g7e6odgc

SECRET_KEY
XXXXXXXXXXXXXXXXXXXXXXXXX check env.-file

ALGORITHM
HS256

ACCESS_TOKEN_EXPIRE_MINUTES
60

- Open postgres, create a new server, ex callse heroku-postgres.
- Enter the all the credentials from the heroku settings and crate.
- Then there will drop down to a lot of databases from heroku.
- You only have access to one, so check the name of your db in heroku settings and look for that.

- To push the code to the production server database, aka heroku-postgres:
    ==> heroku run "alembic upgrade head"
- Then to get all the tables already created do an "git push", "alembic upgrade head", never do "alembic revision"
    To the production server, aka heroku-server. 