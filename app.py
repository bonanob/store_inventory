import csv
import datetime

from models import Base, session, engine, Product


def menu():
    while True:
        choice = input('''
            \nSTORE INVENTORY
            \rv > View Singel Product
            \ra > Add New Product
            \rb > Backup Entire Inventory
            \rWhat would you like to do? ''')
        if choice.lower() in ('v', 'a', 'b'):
            return choice
        else:
            input('''
                  \nPlease choose one of the options above(v, a or b).
                  \rPress enter to try again.''')


def clean_price(price_str):
    try:
        # try:
        #     price_float = float(price_str)
        # except ValueError:
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


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data, None)
        for row in data:
            product_in_db = session.query(Product).filter(
                Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = int(row[2])
                date = clean_date(row[3])
                new_product = Product(
                    product_name=name, product_quantity=quantity, product_price=price, date_updated=date)
                session.add(new_product)
        session.commit()


def app():
    menu()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # menu()
    add_csv()
