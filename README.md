# Project 4: Store Inventory

This console application allows the user to interact with data for a store's inventory. It keeps track of names, quantities, prices, updated dates of products that can be viewed, added, and deleted. The user can also export the inventory as a `csv` file.

**How to run the project locally:**

1. Create a virtual environment
    - Mac: **`python3 -m venv env`**
    - Windows: **`python -m venv env`**
2. Activate your environment
    - Mac: **`source ./env/bin/activate`**
    - Windows: **`.\env\Scripts\activate`**
3. Install dependancies: **`pip install -r requirements.txt`**
4. Run the file **`app.py`**

**What I've learned:**

- Using SQLAlchemy to create a Model
- Adding, deleting, updating, rolling back, and querying with SQLAlchemy ORM(session)
- File I/O
- Cleaning data from `csv` and importing it to db
- Exporting db as `csv`

**Objective:** 

Create a simple store inventory app to keep track of the stock.

**Flow:**

1. Products in **`inventory.csv`** are added to the database
2. User is prompted with a menu. 
    - **`v`** to view the details of a single product in the database,
        1. User is prompted to input a product id.
        2. The information of the chosen product is displayed.
    - **`a`** to add a new product to the database,
        1. User is prompted to input name, quantity, price, updated date of the new product
        2. Added message is displayed if successful.
    - **`b`** to make a backup of the entire contents of the database, or
        1. All products are exported to  `backup.csv`.
        2. Success message is displayed.
    - **`q`** to quit.

**SQLAlchemy Model:**

- **`Product`**
- Attributes: **`product_id`**(primary_key)**,  `product_name`**(string), **`product_quantity`**, **`product_price`**(integer) and **`date_updated`**(`datetime` object)

**Notes:**

- sqlite is used to create database.
- Prices are converted to cents ($3.19 becomes 319, for example)
- Avoiding duplicate products(csv import)**:** if a duplicate product name is found, the app will save the data that was most recently updated for that existing record.
- Menu option `a`: if a duplicate product name is found while the product is attempting to be added to the database, the app will check to see which product entry was most recently updated and only save that data.
- Menu option `b`: the backup CSV output file contains a header row with field titles
