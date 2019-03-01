# coding: utf-8
import json
import os
import unittest

from mock import patch
from mongoengine import connect
from biblat_schema.catalogs import Pais, Idioma, TipoDocumento

from biblat_process.settings import config
from biblat_process import populate_catalog
from biblat_process.populate_catalog import PopulateCatalog

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SCRIPT_PATH, 'test_files')


@patch.object(PopulateCatalog, 'data_dir', new=DATA_DIR)
class TestPopulateCatalog(unittest.TestCase):
    def setUp(self):
        self.connection = connect(db=config.MONGODB_NAME,
                                  host=config.MONGODB_HOST)

    def tearDown(self):
        self.connection.drop_database(config.MONGODB_NAME)

    def test_pais(self):
        populate_catalog.main(['-c', 'pais'])
        self.assertEqual(Pais.objects.count(), 3)
        with open(os.path.join(os.path.join(DATA_DIR, 'Pais.json')),
                  encoding="utf-8") as jsonf:
            expected_paises = json.load(jsonf)
            for expected_pais_data in expected_paises:
                pais = Pais.objects(_id=expected_pais_data['alpha2'])
                self.assertEqual(pais.count(), 1)
                pais = pais[0].to_mongo()
                for k in expected_pais_data:
                    self.assertEqual(expected_pais_data[k], pais[k])

    @patch.object(PopulateCatalog, 'files',
                  new={'Pais': 'Pais_long_value.json'})
    def test_pais_long_value(self):
        populate_catalog.main(['-c', 'pais'])
        self.assertEqual(Pais.objects.count(), 0)

    def test_idioma(self):
        populate_catalog.main(['-c', 'idioma'])
        self.assertEqual(Idioma.objects.count(), 3)
        with open(os.path.join(os.path.join(DATA_DIR, 'Idioma.json')),
                  encoding="utf-8") as jsonf:
            expected_idiomas = json.load(jsonf)
            for expected_idioma_data in expected_idiomas:
                idioma = Idioma.objects(_id=expected_idioma_data['iso_639_3'])
                self.assertEqual(idioma.count(), 1)
                idioma = idioma[0].to_mongo()
                for k in expected_idioma_data:
                    self.assertEqual(expected_idioma_data[k], idioma[k])

    @patch.object(PopulateCatalog, 'files',
                  new={'Idioma': 'Idioma_long_value.json'})
    def test_idioma_long_value(self):
        populate_catalog.main(['-c', 'idioma'])
        self.assertEqual(Idioma.objects.count(), 0)

    def test_tipo_documento(self):
        populate_catalog.main(['-c', 'tipo_documento'])
        self.assertEqual(TipoDocumento.objects.count(), 3)
        with open(os.path.join(os.path.join(DATA_DIR, 'TipoDocumento.json')),
                  encoding="utf-8") as jsonf:
            expected_tipos_documento = json.load(jsonf)
            for expected_tipos_documento in expected_tipos_documento:
                tipo_documento = TipoDocumento.objects(
                    nombre__es=expected_tipos_documento['nombre']['es']
                )
                self.assertEqual(tipo_documento.count(), 1)
                tipo_documento = tipo_documento[0].to_mongo()
                for k in expected_tipos_documento:
                    self.assertDictEqual(expected_tipos_documento[k],
                                     tipo_documento[k])
        # Verificar que no ingresen registros repetidos
        populate_catalog.main(['-c', 'tipo_documento'])
        self.assertEqual(TipoDocumento.objects.count(), 3)

    @patch.object(PopulateCatalog, 'files',
                  new={'TipoDocumento': 'TipoDocumento_invalid_id.json'})
    def test_tipo_documento_invalid_id(self):
        populate_catalog.main(['-c', 'tipo_documento'])
        self.assertEqual(TipoDocumento.objects.count(), 0)
