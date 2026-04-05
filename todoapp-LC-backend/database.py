import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

#SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['DATABASE_USER']}:@{os.environ['DATABASE_HOST']}/{os.environ['DATABASE_NAME']}"

# user = os.environ['DATABASE_USER']
# password = os.environ['DATABASE_PASSWORD']
# host = os.environ['DATABASE_HOST']
# port = os.environ['DATABASE_PORT']
# db_name = os.environ['DATABASE_NAME']

# SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

# Esta lo ponemos por que usamos NEON, que requiere SSL y ya no usamos las variables de entorno individuales para la configuración de la base de datos, sino una única variable `DATABASE_URL` que contiene toda la información de conexión, incluyendo el usuario, contraseña, host, puerto y nombre de la base de datos. Además, se configura el engine de SQLAlchemy para requerir SSL al conectarse a la base de datos, lo cual es necesario para NEON.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"} # Esto es necesario para NEON, que requiere SSL para las conexiones a la base de datos.
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()