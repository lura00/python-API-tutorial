# import default image
FROM python:3.9.7

# The default dir to work from
WORKDIR /usr/src/app

# copy requirements list and add to workdir using ./
COPY requirements.txt ./

# Run pip install requirements
RUN pip install --no-cache-dir -r requirements.txt

# This lines copy all code from . = my app-folder and .. is the routers-folder within app-folder.
COPY . .

# this starts the image.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# In termninal, to build the imgage: "docker build -t <name of image> ."  
# (the . stands for "root dir" wich is where the dockerfile is stored in the folder you work from)

# To see all your images: "docker image ls"

# Docker exec -it <name> bash to go to image interactive mode.

# Push to docker-hub
# create an account on docker-hub create repo, name it.
# login to docker in your terminal.
# The image that been created must name the same as the repo.
# If change needs to bo done on the name, "docker image tag <name of existing image> <new name, same as repo-link>"
# docker push <name of image>