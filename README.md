# python-API/postman/postgreSQL-tutorial
Code + tutorial documented in md-files and py-files

# To install everything from requirements.txt folder:
- pip install -r requirements.txt



# UFW firewall
- sudo ufw status
- sudo uwf enable (to start)
- sudo ufw allow <add command like "https">
- sudo delete allow <example: http>

# Deploy to ubuntu
- in digitalocean create a ubuntu (or any other digital cloud server provider) VM
- create a user with root access
- apt install update && upgrade
- apt install python3
- apt install python-pip
- apt isntall virtualenv (or pip)
- apt install postgresql postgresql-contrib -y
- create password in postgres, "\password <username>" (postgres is default)
- see https://www.youtube.com/watch?v=0sOvCWFmrtA&t=41793s for postgres.conf files
- then "systemctl restart postgresql followed by "psql -U postgres"
- in /etc/postgresql/12/main "adduser <new-user>"
- to ssh in ubuntu you need to add a .ssh folder and the "auth_keys" and add the ssh-keygen.
- create a folder for the project
- git clone all the files from github to a subfolder "src".
- install all "requirements.tct" "pip install -r requirements.txt"
- activate virtualenv
- add a .env file to home directory with database-credentials, see external file.
- alembic upgrade head to push tables to our server-database
- now uvicorn-command works.
- install gunicorn if not isntalled. use this commmand instead to boot the app.
- "gunicorn -w (workers) 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 (0 = any ip:8000 = port).
 - Enter the /etc/systemd/system folder
 - add a new file, example "api.service" add whats in the gunicorn.service-file.
 - "systemctl start api" then test "systemctl status api" now the program will activate automated when server is booted.

 # Safer domain
 - Create a domain from any provider, I use namecheap.com using the.xyz domain costs about 1 dollar / month.
 - Establish connection between namecheap and digitalocean 
    - Go to "domain list" click "manage" 
    - Go to the column "nameserver" and change header to "custom DNS"
    - add these lines: "ns1.digitalcloud.com" then ns2 and ns3.
- go to digitalocean
    - Go to "networking" ==> "domains" ==> "manage domain" and add type "A" DNS-record. 
    - hostname @ and "value" the ip-adress from digitalocean. 
    - add a CNAME dns record as well and type hostname www.domain.xyz and direct to "@".
 - Then to get a more safe domain, "sudo apt install nginx"
 - in the nginx there is a defualt-file, under server_name ==> "location" delete the 3 lines and add whats in the nginx-textfile.
 - Make sure "snap" is installed. sudo snap refresh core
 - Then install certbot, follow the instructions on the certbot website: 
    https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal 

- If fail, try reboot it. It will ask to enter the domains and some Y/N questions.


