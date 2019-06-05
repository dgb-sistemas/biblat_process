# -*- coding: utf-8 -*-
import os

"""
    Archivo de configuración de biblat_process

    Variables de entorno:
        - BIBLATP_REMOTE_ADDR: Dirección IP del servidor ALEPH
        - BIBLATP_REMOTE_USER: Usuario del servidor ALEPH
        - BIBLATP_REMOTE_PATH: Directorio remoto para descargar datos
        - BIBLATP_LOCAL_PATH: Directorio local para guardar los datos
        - BIBLATP_MONGODB_NAME:    nombre de la base (default: 'biblat')
        - BIBLATP_MONGODB_HOST:    host del servicio (default: 'localhost')
        - BIBLATP_MONGODB_PORT:    puerto del servicio (default: 27017)
        - BIBLATP_MONGODB_USER:    [opcional] usuario de la base (default: None)
        - BIBLATP_MONGODB_PASS:    [opcional] password de la base (default: None)
"""

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


class Config:
    REMOTE_USER = os.environ.get('BIBLATP_REMOTE_USER', 'aleph')
    REMOTE_ADDR = os.environ.get('BIBLATP_REMOTE_ADDR', '127.0.0.1')
    REMOTE_PATH = os.environ.get(
        'BIBLATP_REMOTE_PATH',
        '/exlibris/aleph/a21_1/alephm/sql_report/anexo/biblat_process'
    )
    LOCAL_PATH = os.environ.get('BIBLATP_LOCAL_PATH',
                                os.path.join(SCRIPT_PATH, '../data'))
    DB_FILES = ['cla01.txt.gz', 'per01.txt.gz']

    MONGODB_NAME = os.environ.get('BIBLATP_MONGODB_NAME', 'biblat')
    MONGODB_HOST = os.environ.get('BIBLATP_MONGODB_HOST', 'localhost')
    MONGODB_PORT = os.environ.get('BIBLATP_MONGODB_PORT', 27017)
    MONGODB_USER = os.environ.get('BIBLATP_MONGODB_USER', None)
    MONGODB_PASS = os.environ.get('BIBLATP_MONGODB_PASS', None)


class DevelopmentConfig(Config):
    LOCAL_PATH = os.path.abspath(os.path.join(SCRIPT_PATH, '../data'))


class TestingConfig(Config):
    LOCAL_PATH = os.path.abspath(
        os.path.join(SCRIPT_PATH, '../tests/test_files')
    )

    MONGODB_NAME = 'biblat_test'
    MONGODB_HOST = 'mongomock://localhost/biblat_test'


class ProductionConfig(Config):
    LOCAL_PATH = os.path.abspath(os.path.join(SCRIPT_PATH, '../data'))


settings_selector = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

config = settings_selector[os.getenv('BIBLAT_PROCESS_CONFIG', 'default')]
