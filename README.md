# Project 4: Store Inventory

Objective: Create a simple store inventory app using sqlite3 and SQLAlchemy

**Flow of the app:**

1. Products in **`inventory.csv`** are added to the database
2. User is prompted with a menu. **`v`** to view the details of a single product in the database, **`a`** to add a new product to the database, **`b`** to make a backup of the entire contents of the database, or **`q`** to quit.  
    - Displaying a product by its ID - Menu Option V

        gets and displays a product by its **`product_id`**.

    - Adding a new product to the database - Menu Option A

        adds a new product to the database. Users are prompted to enter the product's name, quantity, and price. 

    - Backup the database (Export new CSV) - Menu Option B

        makes a backup(.csv)of the database. 

**SQLAlchemy Model:**

- **`Product`**
- Attributes: **`product_id`** as **`primary_key`,  `product_quantity`**, **`product_price`** as an integer and price converted to cents ($3.19 becomes 319, for example) and **`date_updated`** as **`datetime`** object

**Notes:**

- Virtual python environment (project requirements: **`requirements.txt`**)
- Avoiding duplicate products(csv import)**:** if a duplicate product name is found, the app will save the data that was most recently updated for that existing record.
- Menu option: a: ****if a duplicate product name is found while the product is attempting to be added to the database, the app will check to see which product entry was most recently updated and only save that data.
- Menu option: b: ****the backup CSV output file contains a header row with field titles