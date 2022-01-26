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

