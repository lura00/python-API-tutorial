# Install postman API
- https://www.postman.com/downloads/?utm_source=postman-home
- create a free account

# Test your URL in postman instead of the web browser
- Copy http-url from terminal and paste in postman and hit "Send"
- This will test if your get-path will work

# To create and save your project
- Press "create new collection" name it
- Go back to your GET/POST and hit "save as" enter a name and choose the new collection
- Hit save

# Send a html-method post request
- in postman change html method to post, ad url.
- check option "Body" and "raw" choose lang JSON.
- paste as example:
    {
    "title": "Top beaches in Sweden",
    "content": "check out this beaches"
    }
- go back to vscode(fastAPI) and make sure you have a code block with post method, like this:
    @app.post("/createposts")
    def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title {payload['title']} content: {payload['content']}"}
- You will see result in terminal when you have saved and hit "send" in postman.

# Get one specific post
- create a new GET in your workspace. copy the URL from your first GET-method and add the ID.

# How to send requests when you need to authorize yourself
- Go to login request type login data and retrieve a token.
- go to the other requests click on either "HEADER" add in "KEY" "Athorization" and in "VALUE"
    type "Bearer" capital B and paste the generated token.
- Or simply press on AUTHORIZATION --> type, choose Bearer token and paste the token.
- Now sending requests should work.

# Environments 
- Click on the border on the left a button callaed "environments".
- Name it, and then we can set for example environment variables, for example the test URL.
- This way I don't have to hard code the URL on every html-request.
- On the collections-site, choose environment on the top right corner of the site and chooose the one we  ceated.
- To use the new URL env-variable paste it like this where the URL goes on the requests: {{URL}}/posts.
- You can do one for JWT token as well so we don't have to login and paste the new token each time during testing.
- go to login-request, press the "test"-button on the right side there is links to different snippets.
- For this choos "set an env variable" this will appear:
    pm.environment.set("JWT", pm.response.json().access_token); the text inside is edited by me.