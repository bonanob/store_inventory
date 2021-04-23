import csv
import datetime
import time


from models import Base, session, engine, Product


def menu():
    """Main menu for the app"""
    while True:
        choice = input('''
            \nSTORE INVENTORY
            \rv > View Single Product
            \ra > Add New Product
            \rb > Backup Entire Inventory
            \rq > Quit
            \rWhat would you like to do? ''')
        if choice.lower() in ('v', 'a', 'b', 'q'):
            return choice.lower()
        else:
            input('''
                  \nPlease choose one of the options above(v, a, b or q).
                  \rPress enter to try again.''')


def clean_price(price_str):
    """cleans the price to int. $1.00 = 100

    Args:
        price_str (str): price as string

    Returns:
        int: original price * 100
    """
    try:
        try:
            price_float = float(price_str)
        except ValueError:
            price_float = float(price_str[1:])

    except ValueError:
        input('''
              \n***** PRICE ERROR *****
              \rThe Price should be a number without a currency label.
              \rEx: 5.99
              \rPress enter to try again.
              \r**********************''')
        return
    else:
        return int(price_float * 100)


def clean_date(date_str):
    """converts str to datetime.

    Args:
        date_str (str): date as str

    Returns:
        datetime
    """
    try:
        return_date = datetime.datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        input('''
              \n***** DATE ERROR *****
              \rDate formats should include a valid Month/Day/Year from the past.
              \rEx: 1/1/1000
              \rPress enter to try again.
              \r**********************''')
        return
    else:
        return return_date


def clean_id(id_str):
    """converts id_str to int and checks if it exist in the db

    Args:
        id_str (str): id as str

    Returns:
        int: id is int and is in db.
    """
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
              \n***** ID ERROR *****
              \rID should be a number.
              \rPress enter to try again.
              \r********************''')
        return
    else:
        if product_id in id_options:
            return product_id
        else:
            input(f'''
                  \n***** ID ERROR *****
                  \rOptions: {id_options}
                  \rPress enter to try again.
                  \r********************''')
            return


def view_product():
    """Prints product properties with provided id"""
    id_error = True
    while id_error == True:
        product_id = input('What is the the product ID? ')
        product_id = clean_id(product_id)
        if type(product_id) == int:
            id_error = False
    product_viewed = session.query(Product).filter(
        Product.product_id == product_id).one_or_none()
    print(f'''
            \n--------------------------------------------
            \rName: {product_viewed.product_name}
            \rPRICE: {product_viewed.product_price / 100}
            \rQTY:{product_viewed.product_quantity}
            \rDate Updated: {product_viewed.date_updated}
            \r--------------------------------------------''')
    time.sleep(2)


def add_product():
    """Adds product by user input.
    if conflict, user input is saved."""
    name = input('What is the name of the product? ')

    quantity_error = True
    while quantity_error == True:
        quantity = input('How many are there? ')
        try:
            int(quantity)
        except ValueError:
            quit_or_again = input('''
                    \nThe quantity must be an number.
                    \rPress enter to try again.''')
        else:
            quantity_error = False

    price_error = True
    while price_error == True:
        price = input('What is the price of the product?(ex. 3.99) ')
        price = clean_price(price)
        if type(price) == int:
            price_error = False

    date = datetime.datetime.now()

    # Delete conflicting instance.
    session.query(Product).filter(name == Product.product_name).delete()

    new_product = Product(product_name=name, product_quantity=quantity,
                          product_price=price, date_updated=date)
    session.add(new_product)
    session.commit()
    print(f'-- {name} was added. --')
    time.sleep(1)


def export_csv():
    """exports db to backup.csv"""
    with open('backup.csv', 'w', newline='') as csvfile:
        fieldnames = Product.__table__.columns.keys()
        product_writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, lineterminator='\n')

        product_writer.writeheader()
        for product in session.query(Product):
            product_writer.writerow({'product_id': product.product_id,
                                     'product_name': product.product_name,
                                     'product_quantity': product.product_quantity,
                                     'product_price': product.product_price,
                                     'date_updated': product.date_updated})
    print('-- Export successful. --')
    time.sleep(1)


def add_csv():
    """adds data from csv to db.
    if conflict, most recent entry is saved.
    """
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data, None)
        for row in data:
            product_in_db = session.query(Product).filter(
                Product.product_name == row[0]).one_or_none()
            name = row[0]
            price = clean_price(row[1])
            quantity = int(row[2])
            date = clean_date(row[3])
            new_product = Product(
                product_name=name, product_quantity=quantity, product_price=price, date_updated=date)

            if product_in_db is not None:
                db_time = product_in_db.date_updated
                db_time = datetime.datetime(
                    db_time.year, db_time.month, db_time.day)
                if date > db_time:
                    session.query(Product).filter(
                        Product.product_name == row[0]).delete()
                    session.add(new_product)
            else:
                session.add(new_product)
            session.flush()
        session.commit()


def app():
    app_running = True
    while app_running:
        menu_choice = menu()
        if menu_choice == 'v':
            view_product()
        elif menu_choice == 'a':
            add_product()
        elif menu_choice == 'b':
            export_csv()
        else:
            print('-- GOODBYE. --')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
