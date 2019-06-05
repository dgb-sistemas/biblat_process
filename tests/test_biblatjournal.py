# coding: utf-8
import os
import gzip
import unittest
from biblat_process.marc2dict import Marc2Dict
from biblat_process.biblatjournal import RevistaDict
from biblat_process.settings import config
from biblat_schema.catalogs import Disciplina
from mongoengine import connect


class TestBiblatJournal(unittest.TestCase):
    connection = None
    model_class_to_delete = [Disciplina]

    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.test_files_path = os.path.join(self.test_path, 'test_files')
        self.config = {
            'local_path': self.test_files_path,
        }

        for root, paths, files in os.walk(self.test_files_path):
            for file in files:
                if file.endswith('.txt'):
                    with open(os.path.join(root, file), mode='rb') as f_in, \
                            gzip.open(os.path.join(root, file + '.gz'),
                                      'wb') as f_out:
                        f_out.writelines(f_in)

        self.connection = connect(db='mongoenginetest',
                                  host='mongomock://localhost',
                                  is_mock=True)
        # workaroud to fix "drop database" that run only once:
        # https://github.com/mongomock/mongomock/issues/371
        if self.model_class_to_delete:
            for model_class in self.model_class_to_delete:
                try:
                    model_class.objects.all().delete()
                except Exception:
                    pass

    def tearDown(self):
        for root, paths, files in os.walk(self.test_files_path):
            for file in files:
                if file.endswith('.gz'):
                    os.unlink(os.path.join(root, file))
        self.connection.drop_database('mongotest')

    def _make_disciplina_CLA01(self):
        dict_disciplina = {
            'base': [
                'CLA01'
                ],
            'nombre': {
                'es': 'Geografía',
                'en': 'Geography'
            }
        }

        disciplina = Disciplina(**dict_disciplina)
        disciplina.save()
        return disciplina

    def _make_disciplina_PER01(self):
        dict_disciplina = {
            'base': [
                'PER01'
                ],
            'nombre': {
                'es': 'Biología',
                'en': 'Biology'
            }
        }

        disciplina = Disciplina(**dict_disciplina)
        disciplina.save()
        return disciplina

    def test_cla01_journal(self):
        """Prueba de revista para test_cla01_journal"""
        self.maxDiff = None
        config.DB_FILES = ['test_cla01.txt.gz']
        marc2dict = Marc2Dict()
        revistas = []

        registro_expected = [
            {
                'base_datos': 'CLA01',
                'titulo_revista': 'Revista geográfica',
                'issn': '0031-0581',
                'pais': None,
                'idioma': ['spa']
            }
        ]

        for dict in marc2dict.get_dict():
            revista_dict = RevistaDict(dict)
            revista_dict = revista_dict.to_dict()
            revistas.append(revista_dict)
            print(revista_dict)

        self.assertEqual(len(revistas), 1)
        self.assertEqual(revistas[0]['titulo_revista'], registro_expected[0]['titulo_revista'])
        self.assertEqual(revistas[0]['issn'], registro_expected[0]['issn'])
        self.assertEqual(revistas[0]['pais'], registro_expected[0]['pais'])
        self.assertEqual(revistas[0]['idioma'], registro_expected[0]['idioma'])
        self.assertEqual(revistas[0]['base_datos'], registro_expected[0]['base_datos'])

    def test_disciplina_cla01_journal(self):
        """Prueba del campo disciplina de revista en CLASE"""
        disciplina = self._make_disciplina_CLA01()
        self.maxDiff = None
        config.DB_FILES = ['test_cla01.txt.gz']
        marc2dict = Marc2Dict()
        revistas = []

        for dict in marc2dict.get_dict():
            revista_dict = RevistaDict(dict)
            revistas.append(revista_dict)

        self.assertIsNotNone(revistas[0].disciplina, disciplina)

    def test_per01_journal(self):
        """Prueba de revista para test_per01_journal"""
        self.maxDiff = None
        config.DB_FILES = ['test_per01.txt.gz']
        marc2dict = Marc2Dict()
        revistas = []

        registro_expected = [
            {
                'base_datos': 'PER01',
                'titulo_revista': 'Papeis avulsos de zoologia',
                'issn': '0031-1049',
                'pais': 'BR',
                'idioma': ['eng']
            }
        ]

        for dict in marc2dict.get_dict():
            revista_dict = RevistaDict(dict)
            revista_dict = revista_dict.to_dict()
            revistas.append(revista_dict)
            print(revista_dict)

        self.assertEqual(len(revistas), 1)
        self.assertEqual(revistas[0]['titulo_revista'], registro_expected[0]['titulo_revista'])
        self.assertEqual(revistas[0]['issn'], registro_expected[0]['issn'])
        self.assertEqual(revistas[0]['pais'], registro_expected[0]['pais'])
        self.assertEqual(revistas[0]['idioma'], registro_expected[0]['idioma'])
        self.assertEqual(revistas[0]['base_datos'], registro_expected[0]['base_datos'])

    def test_disciplina_per_journal(self):
        """Prueba del campo disciplina de revista en PERIODICA."""
        disciplina = self._make_disciplina_PER01()
        self.maxDiff = None
        config.DB_FILES = ['test_per01.txt.gz']
        marc2dict = Marc2Dict()
        revistas = []

        for dict in marc2dict.get_dict():
            revista_dict = RevistaDict(dict)
            revistas.append(revista_dict)

        self.assertIsNotNone(revistas[0].disciplina, disciplina)
