import json
from config import user, password, db_name
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Stock, Shop, Sale

DSN = f'postgresql://{user}:{password}@localhost:5432/{db_name}'
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
    c = input('Enter publisher name: ')
    for shop_name in session.query(Shop.name).join(Stock).join(Sale).join(Book).join(Publisher).\
            filter(Publisher.name == c).all():
        print(f'Shop name: {shop_name}')


shop_query()
session.close()