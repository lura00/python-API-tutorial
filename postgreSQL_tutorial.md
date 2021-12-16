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

    SELECT and FROM are sql keywords and * and products is what I, the user want to get.
- So the above command will print everything (*) within my table "products".
- If I have a column named "name" I can change the * to "name" and only the name column will print.
- We can pass in as many parameters as we want as long as the exist in the table.

# QUERY - Usefull SQL-commands
- Change name on a column in your table:
    SELECT id AS products_id FROM products;
- And you can change as many columns as you want, just put "," after the last changed name.

- Filter your table with keyword "WHERE" and filter whatever you ad after, like this example I use id:
    SELECT * FROM products WHERE id = 10;
- This will show me the product with id-number 10.
- If you working with varchars (Strings) you want to wrap your search word in quotes ''
- You can filter insted of "=" use less then or greater then, to get a large aim.
    SELECT * FROM products WHERE price > 50;
    > | < | <= | != 
- SELECT * FROM products WHERE inventory > 0 AND price > 20; AND keyword
- SELECT * FROM products WHERE id = 1 OR id = 2 OR id = 3; OR keyword
- SELECT * FROM products WHERE id IN (1,2,3); IN keyword, similar to or but you ad a interval
- SELECT * FROM products WHERE name LIKE 'TV%'; LIKE keyword, if you want all fields containing the word
    TV in this case, use LIKE 'TV%' remember the % character. if you put it infront of % it will show the starting  letters if after % it will filter all words that ends on the character, like this:
    SELECT * FROM products WHERE name LIKE '%e';
- ad keyword NOT if you not want words that start with "TV%"
- How to ORDER BY:
    SELECT * FROM products ORDER BY price ASC; ORDER BY - keywords and ASC -keyword (ascending)
    - This will show us the price from lowest to most expensive
    - If you want to filter from most expensive to lowest change ASC to keyword DESC (descending)

- Example:
- ASC is default. so this line will first filter inventory in most to less. Then if we have
    inventory that all is the same it will start sorting price ASC.
- SELECT * FROM products ORDER BY inventory DESC, price;

example:
- Use more keywords, WHERE and ORDER BY:
    SELECT * FROM products WHERE price > 20 ORDER BY created_at DESC;

- LIMIT keyword, will limit your result by as many as you want:
    SELECT * FROM products WHERE price > 20 LIMIT 2;

- OFFSET keyword will skip as many lines you want:
    SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2; 
    Will skip the first two lines.

# Adding a line to table useing the SQL command
- The VALUES must matgch the order you have before keyword VALUES.
    INSERT INTO products (name, price, inventory ) VALUES ('Tortilla', 4, 1000);

# Print the item you added to a table without showing the whole table
 - INSERT INTO products (name, price, inventory ) VALUES ('car', 500, 10) returning*;
- Keyword "returning *"

# Deleting an item
- DELETE FROM products WHERE id = 10 RETURNING *; keyword DELETE and the specify

# Updating exisisting row
- UPDATE products SET name = 'flower tortilla', price = 40 WHERE id = 21; keywowrd UPDATE and SET
- Updating multiple rows:
    UPDATE products SET is_sale = true WHERE id > 15 RETURNING *; 

# Setting up a foreign key
- In postgres/pgAdmin right click on your table and choose properties
- I needed to add a user_id column, set datatype same as id (int)
- set to not null if thats required.
- Go ti constraints --> Foreign key
- Name it, ususally from what table it should connect with, in my case
    posts_users_fkey
- Choose the columns it should interact with. local, reference.
- in Action example choose "on delete" --> Cascade, this will if I delete a user with for ex. id 1, postgres will automatically delete   all posts created by user id 1.
- We do this foreign key to get a connection with users and posts, so we
    can see who posted what.
    So when a post is created the new column, user_id, will not accept the post unless there is a valid id of a user. If a id that does not exist is entered, it will not
    accept the post.
- The SQL code to check posts for this new id will be: SELECT * FROM posts WHERE user_id = 15;
- Delete user with id: DELETE FROM users where id = 14;

# Settings up a votes-table in postgres(pgAdmin)
- Create new table, called votes.
- Add in columns user-id and post-id. Since one user should only be able to like one post one time.
- Add a foreign key, see above how to do that.
    It should contain one key for votes_posts and one votes_users
    local column should be for posts, posts_id etc. reference public_posts and referencing id.
    And same for users.