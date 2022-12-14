import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from config import host, user, password, db_name, port
from models import create_tables, Publisher, Book, Stock, Shop, Sale

DSN = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def shop_query():
    try:
        c = input('Enter publisher name or id: ')
        for shop_name in session.query(Shop.name).join(Stock).join(Sale).join(Book).join(Publisher).\
                filter(Publisher.name == c).all():
            print('Shop name: {}'.format(*shop_name))
        for shop_name in session.query(Shop.name).join(Stock).join(Sale).join(Book).join(Publisher). \
                filter(Publisher.id == c).all():
            print('Shop name: {}'.format(*shop_name))
    except (Exception, psycopg2.Error) as error:
        return error


shop_query()
session.close()
