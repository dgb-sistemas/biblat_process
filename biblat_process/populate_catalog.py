#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import json
import logging

from biblat_schema.catalogs import Pais
from mongoengine import connect

from biblat_process.settings import config

logger = logging.getLogger('claper_dump')

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
LOGGER_FMT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

connect(db=config.MONGODB_NAME, host=config.MONGODB_HOST)

class PopulateCatalog:
    def __init__(self):
        self.data_dir = os.path.join(SCRIPT_PATH, '../datos')
        self.files = {
            'Pais': 'Pais.json',
            'Idioma': 'Idioma.tsv',
            'TipoDocumento': 'TipoDocumento.tsv',
            'EnfoqueDocumento': 'EnfoqueDocumento.tsv',
            'Disciplina': 'Disciplina.json',
            'SubDisciplina': 'Subdisciplina.tsv',
            'NombreGeografico': 'NombreGeografico.tsv',
            'LicenciaCC': 'LicenciaCC.json',
            'SherpaRomeo': 'SherpaRomeo.json'
        }

    def pais(self):
        with open(os.path.join(self.data_dir, self.files['Pais']), encoding="utf-8") as jsonf:
            paises = json.load(jsonf)
            for pais_data in paises:
                pais = Pais(**pais_data)
                pais.save()


def main():
    parser = argparse.ArgumentParser(
        description="Llenado de catálogos de biblat_schema"
    )

    parser.add_argument(
        '--logging_level',
        '-l',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )

    parser.add_argument(
        '--catalog',
        '-a',
        default='all',
        choices=['pais', 'all'],
        help='Seleccione proceso a ejecutar'
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.logging_level.upper(), 'INFO'),
        format=LOGGER_FMT)

    populate_catalog = PopulateCatalog()

    if args.catalog in ('pais', 'all'):
            populate_catalog.pais()


if __name__ == "__main__":
    main()
