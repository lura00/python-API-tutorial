# Set up a virtual environment
bash
- Set up a virtual env. in terminal enter "venv -3 -m <environment name>
- Enter the VE and set the interpreter by, "view-command pallete-'select enterpreter'-enter search patter to \your VE-name\Scripts\python.exe
- Set so your terminal is working in your VE: source /<sökväg>

# Install fastAPI
- in termninal enter: pip install fastapi[all]
- There can be an error, then you might need to install vs Build tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Check what you packages you installed: pip freeze

# Set up an API in python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")       #app = decorator .get = http-method ("/") = path
    async(optional) def root():
        return {"message": "Hello World"}

    @app.post("/createposts") post = http-method. Sends a post request with data to the API
    def create_post():
    return {"message": "seccesfully created post"}

# test that it works
- run in termninal: uvicorn (installed via fastapi[all]): uvicorn main(name on py-file):app (name of fastAPI() function)
- Output should look something like this:
    $ uvicorn main:app
    ?[32mINFO?[0m:     Started server process [?[36m23216?[0m]
    ?[32mINFO?[0m:     Waiting for application startup.
    ?[32mINFO?[0m:     Application startup complete.
    ?[32mINFO?[0m:     Uvicorn running on ?[1mhttp://127.0.0.1:8000?[0m (Press CTRL+C to quit)

- To test if this runs, copy the http-link on the bottom line, http://127.0.0.1:8000 and paste to your browser, you will see the message you typed in the py-code on the wep page.

# By now you should check the postmanAPI-tutorial.md to install postman for further URL testing.

# Make so you do not have to exit your Server after each change
- In terminal close your server and restart using --reload flag:
    uvicorn main:app --reload
- This will reload your server automaticaly after you change something in the code.

# Creating a Schema
- By downloading fastAPI you have access to pydantic, so we will start by import that.
    from pydantic import BaseModel
- create a class and decide how the schema/model for our post will look like, something like this:

    class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None

- No we can use class Post in our post request operation. And the API will look if our post operation contains a title with a string and then a content with a string.
the code can look like this:

    @app.post("/createposts")
    @app.post("/createposts")
    def create_post(new_post: Post):
    print(new_post)
    return {"data": "new post"}

- this will automatically give the same output/data as first draft in this tutorial.
- If we only wants to print the (ex) title we can modify this row:

    print(new_post) to this: print(new_post.title)

- Try this in postman by adding for example ("ratings": 4)to the Body and hit "send".

# Creating a dictionary with keyword "dict"
- By adding .dict() to new_post mentioned above we creat a dictionary. Like this piece of code:

    @app.post("/createposts")
    def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}

- By now we only needs to return "data": post to retrieve our post.

# CRUD
# CREATE
- POST /posts @app.post("/posts)
# READ
- GET /posts/:id @app.get("/posts/{id}") get specific post
    GET /posts @app.get("/posts")
# UPDATE
- PUT/PATCH /posts/:id @app.put("/posts/{id}")
# DELETE
- DELETE /posts/:id @app.delete("/posts/{id}")

# Storing posts in memory
- create and array, example:

    my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}

- id will not be hard coded one this is in a database and uses row-id.
- By adding things to memory we can use @app.get("/posts") and send in the array in the return statement.
    Someting like this:

    @app.get("/posts")
    def get_posts():
    return{"data": my_posts}

- This will automatically transform the code to JSON format so we can send it forward over our API.

# Creating posts from array
- add the array to the "@app.post()"-method like this

    @app.post("/posts")
    def create_post(post: Post):
    my_posts.append()
    return {"data": post_dict}

- Now we need to give our posts a id-number, so we do this: 
    from random import randrange

- Then to add a random number we do this:

    post_dict['id'] = randrange(0, 1000000)

- The full code block will look something like this, for a post from memory (array) and adding a random id number:

    @app.post("/posts")
    def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

- Every time we create a post we want to send back a 201 status_code. so to do this we add to:
    @app.post("/posts", status_code=status.HTTP_201_CREATED)
- More error handling further down.

# Get one post
- You will need a find_post function that can look like this:

    def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

- Then create a get_post html method:

   @app.get("/posts/{id: int}")  - /{id} path parameter {id: int} - sets what variable we want
    def get_post(id):
    post = find_post(id)
    print(post)
    return {"post_details": post}

- SEE postmanAPI-tutorial

# Structure your API
- Remember that fastAPI always go through top to bottom.
- So for instance you have one get request with URL posts/id and after you have a posts/latest.
- If you try to run "latest" your API will look for a pattern posts/variable.
- In this case you just have to put the posts/latest above the posts/ID because the posts/ID will
    still work if you enter posts/<a id number> because it is specific.

# Better error handling
- import from fastapi import Response, status
- Run the code like this: (Keep in mind this is the hard coded way to do it.)

    @app.get("/posts/{id}")  # /{id} path parameter
    def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f"post with id: {id} was not found"}
    print(post)
    return {"post_details": post}

- A nicer way is import this: from fastapi import HTTPException

    @app.get("/posts/{id}")  # /{id} path parameter
    def get_post(id: int, response: Response):
        post = find_post(id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                etail=f"post with id: {id} was not found")
        print(post)
        return {"post_details": post}
    
Example of a created post message (status_code):

    @app.post("/posts", status_code=status.HTTP_201_CREATED)
    def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# Delete post with id
- Create a decorator with http-method
    @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_post(id: int):
    # find the index in the array that has required id
    # my_posts.pop(index)
    index = find_index_post(id)    - Calls the find_index function and passes in the required ID

    if index == None:           
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

- Use a if-statement if inde(ID) does not exist we raise a different http-exception and passes on a different status message
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

- Create a "find_index" function  to locate the required ID:

    def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Update a post
- Create a decorator with "PUT" http-method, pass in the url in the braces.
- Use the already set schema for title, content etc.
- These two code lines can look like this:

    @app.put("/posts/{id}")
    def update_post(id: int, post: Post):

- We need something to tell us if the post we pass in as parameter doesn't exist, for example
    use the same code block as per in the "delete" function, this piece: 

        index = find_index_post(id)    - Calls the find_index function and passes in the required ID

        if index == None:           
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id {id} does not exist")
                
- Then we need to create something that will exhange the current post info in the array of posts
- This can look like this:

    post_dict = post.dict()  # convert post_dict to a dictionary
    post_dict['id'] = id
    my_posts[index] = post_dict # The "my_post" is our current hard coded post and we set it to "post_dict".
    return {"data": post_dict}

- The full code block for updating a post:

    @app.put("/posts/{id}")
    def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

- Once this code is done test it in Postman
- Create a new request, with HTTP-method "PUT".
- Add the same URL as in "Get-post" and pass in the id you want to change.
- Click in "body" --> "raw" --> "lang = JSON".
- Add the changes to be made, for example:
    {
        "title": "updated title",
        "content": "This is the new content"
    }

# FastAPIs built in documentation
- To see the documantation fastapi does for us, just paste the original url in your terminal.
- Then use /docs. Like this:
    127.0.0.1:8000/docs
- Once you are in, you can actually try your out your functions.
- Enter for example "get posts" and in the top right corner there is a button "try it out".
- We can also use "redoc". Sometimes docs or redoc can be used instead of postman to try our methods out.
    127.0.0.1:8000/redoc

