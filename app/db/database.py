from databases import Database
import environ
from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False)
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_file = BASE_DIR / ".env"

if env_file.exists():
    environ.Env.read_env(str(env_file))
    print(f"Загружен .env из: {env_file}")
else:
    print(f"Файл .env не найден по пути: {env_file}")


db_user = env('DB_USER')
db_pass = env('DB_PASS')
db_host = env('DB_HOST')
db_name = env('DB_NAME')


DB_URL = f'mysql+asyncmy://{db_user}:{db_pass}@{db_host}/{db_name}'

print(DB_URL)

database = Database(DB_URL)

