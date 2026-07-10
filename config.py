from os import getenv, path

# DATABASE_URL = getenv("DATABASE_URL", "postgresql://postgres:7486250@localhost:5432/esoft")
APP_FOLDER = path.dirname(__file__)
UPLOADS_FOLDER = path.join(APP_FOLDER, 'uploads')


        