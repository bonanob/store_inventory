import csv

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


def app():
    menu()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # menu()
    add_csv()
