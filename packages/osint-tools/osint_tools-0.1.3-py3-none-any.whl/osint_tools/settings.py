from functools import lru_cache
from pydantic import BaseSettings
from os import environ
from typing import List

class _BaseSettings(BaseSettings):
    ENUM_ERROR = {'detail': "value is not a valid enumeration member; permitted: 'male', 'female'"}
    FILE_TYPE_ERROR = 'Upload File Error: Incorrect File Type.'
    # INVALID_DOC_ERR: Callable = lambda x: f"{x}: Text PDF or Invalid File"

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    ACCEPT_PDF: List[str] = [".pdf"]
    ACCEPT_IMAGE: List[str] = ['.jpg', '.png']
    ACCEPT_FILES: List[str] = ACCEPT_IMAGE + ACCEPT_PDF
    FILE_CONVERSION_LIST: List[str] = ['.jpeg']

    WHICH_LOGGER: str= environ.get('WHICH_LOGGER')
    PORT: int = environ.get('PORT')
    
    APP_NAME: str = environ.get("APP_NAME")
    APP_VERSION: str = environ.get("APP_VERSION")
    ENV_NAME: str = environ.get("ENV_NAME")

    INPUT_BUCKET: str = environ.get('INPUT_BUCKET')
    BUCKET_NAME: str = f'{APP_NAME}-{APP_VERSION}-{ENV_NAME}-{INPUT_BUCKET}'

    AWS_REGION: str = environ.get('AWS_REGION')
    MONGO_URI: str = environ.get('MONGO_URI')
    MONGO_DB_NAME: str = environ.get('MONGO_DB_NAME', 'develop_db')

    # PROD_URL: HttpUrl = 'https://asdasdasd.com'

# class DevSettings(_BaseSettings):
    # ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # DATA_DIR = os.path.join(ROOT_DIR, 'data')
    # COMPANY_ENUM_FILE: str = environ.get('COMPANY_ENUM_FILE')
    # BASE_DIR_FILES: Path = environ.get('BASE_DIR_FILES')

@lru_cache()
def get_settings() -> BaseSettings:
    return _BaseSettings()
