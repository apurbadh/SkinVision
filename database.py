from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Text, Column, Integer, String

SQLALCHEMY_DATABASE_URL = "sqlite:///./skinvision.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    email = Column(String(256))
    quote = Column(String(512))
    image_url = Column(String(512))


class Disease(Base):

    __tablename__ = "disease"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    symptom = Column(Text())
    remedy = Column(Text())
    image_url = Column(String(256))
    shortcut = Column(String(256))

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine, checkfirst=True)
