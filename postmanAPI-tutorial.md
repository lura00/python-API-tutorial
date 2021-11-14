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