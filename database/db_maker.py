from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy_utils import database_exists, create_database
import  os
import psycopg2
from psycopg2.errors import UndefinedTable,ProgrammingError

load_dotenv()
Base = declarative_base()

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    products = relationship('Product', back_populates='shop')

class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    products = relationship('Product', back_populates='type')

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    price_type = Column(String, nullable=False)
    price_unit = Column(Integer, nullable=False)
    price_unit_type = Column(String, nullable=False)
    shop_id = Column(Integer, ForeignKey('shop.id'))
    shop = relationship('Shop', back_populates='products')
    type_id = Column(Integer, ForeignKey('type.id'))
    type = relationship('Type', back_populates='products')
    date = Column(String, nullable=False)

class DbManager:
    def __init__(self):
        self.default_engine = create_engine(f"postgresql+psycopg2://{os.environ.get('MY_DB_NAME')}:{os.environ.get('MY_DB_CODE')}@{os.environ.get('MY_DB_ADDRESS')}/postgres")
        self.engine = create_engine(f"postgresql+psycopg2://{os.environ.get('MY_DB_NAME')}:{os.environ.get('MY_DB_CODE')}@{os.environ.get('MY_DB_ADDRESS')}/cheaplist_db")
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)


    def setup (self) -> None:
        with self.default_engine.connect() as conn:
            conn = conn.execution_options(isolation_level="AUTOCOMMIT")
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='cheaplist_db'"))
            if result.scalar() is None :
                conn.execute(text(f"CREATE DATABASE cheaplist_db ENCODING 'utf8' TEMPLATE template0;"))
                print('Database created using template0!')
            else :
                print('Database already exists!')

    def product_create_and_add (self, maintype: str, name: str,price: int, price_type: str, price_unit: int,price_unit_type: str, shop: str, date: str) -> None:
        session = self.Session()
        if session.query(Shop).filter_by(name=shop).first() is None:
            shop_model = Shop(name = shop)
        else :
            shop_model = session.query(Shop).filter_by(name=shop).first()
        if session.query(Type).filter_by(name=maintype).first() is None:
            type_model = Type(name = maintype)
        else :
            type_model = session.query(Type).filter_by(name=maintype).first()
        session.add_all([shop_model,type_model])
        product_model = Product(name=name, price=price, price_type=price_type, price_unit=price_unit, price_unit_type=price_unit_type, date=date, type= type_model, shop= shop_model)
        session.add(product_model)
        session.commit()
        print(f'{product_model.name} with shop_id{shop_model.id}  and type_id{type_model.id} !')
        session.close()

    def add_it(self, date: str,maintype: str) -> bool:
        session = self.Session()
        try:
            my_maintype= session.query(Type).filter_by(name=maintype).first()
            if session.query(Product).filter_by(date=date, type_id=my_maintype.id).first() is None:
                return True
            else:
                print(f'There is already {date} date in {my_maintype.name} type.')
                return False
        except UndefinedTable:
            return True
        except ProgrammingError:
            return True
        except AttributeError:
            return True

