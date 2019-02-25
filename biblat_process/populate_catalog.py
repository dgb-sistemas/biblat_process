#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import json
import logging

from biblat_schema.catalogs import Pais, Idioma
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
            'Idioma': 'Idioma.json',
            'TipoDocumento': 'TipoDocumento.tsv',
            'EnfoqueDocumento': 'EnfoqueDocumento.tsv',
            'Disciplina': 'Disciplina.json',
            'SubDisciplina': 'Subdisciplina.tsv',
            'NombreGeografico': 'NombreGeografico.tsv',
            'LicenciaCC': 'LicenciaCC.json',
            'SherpaRomeo': 'SherpaRomeo.json'
        }

    def pais(self):
        with open(os.path.join(self.data_dir, self.files['Pais']),
                  encoding="utf-8") as jsonf:
            paises = json.load(jsonf)
            for pais_data in paises:
                try:
                    pais = Pais(**pais_data)
                    pais.save()
                except Exception as e:
                    logging.error('Error al procesar %s' % str(pais_data))
                    logging.error('%s' % str(e))

    def idioma(self):
        with open(os.path.join(self.data_dir, self.files['Idioma']),
                  encoding="utf-8") as jsonf:
            idiomas = json.load(jsonf)
            for idioma_data in idiomas:
                try:
                    idioma = Idioma(**idioma_data)
                    idioma.save()
                except Exception as e:
                    logging.error('Error al procesar %s' % str(idioma_data))
                    logging.error('%s' % str(e))


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
        choices=['pais', 'idioma', 'all'],
        help='Seleccione proceso a ejecutar'
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.logging_level.upper(), 'INFO'),
        format=LOGGER_FMT)

    populate_catalog = PopulateCatalog()

    if args.catalog in ('pais', 'all'):
            populate_catalog.pais()

    if args.catalog in ('idioma', 'all'):
            populate_catalog.idioma()


if __name__ == "__main__":
    main()
