# coding: utf-8
import os
import gzip
import unittest
from biblat_process.marc2dict import Marc2Dict
from biblat_process.biblatjournal import RevistaDict
from biblat_process.settings import config


class TestBiblatJournal(unittest.TestCase):

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

    def tearDown(self):
        for root, paths, files in os.walk(self.test_files_path):
            for file in files:
                if file.endswith('.gz'):
                    os.unlink(os.path.join(root, file))

    def test_cla01_journal(self):
        print('Prueba de revista para test_cla01_journal')
        self.maxDiff = None
        config.DB_FILES = ['test_cla01.txt.gz']
        marc2dict = Marc2Dict()
        revistas = []

        registro_expected = [
            {
                'base_datos': 'CLA01000300023',
                'titulo_revista': 'Revista geográfica',
                'issn': '0031-0581',
                'pais': None,
                'idioma': ['spa']
            }
        ]

        for dict in marc2dict.get_dict():
            print(dict)
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
        print('Prueba del campo disciplina de revista en CLASE')
        self.maxDiff = None
        config.DB_FILES = ['test_cla01.txt.gz']
        marc2dict = Marc2Dict()
        revistas = []
        disciplina_expected = [
            {
                'idioma': None,
                'palabra_clave': 'Geociencias'
            }
        ]

        for dict in marc2dict.get_dict():
            revista_dict = RevistaDict(dict)
            revista_dict = revista_dict.to_dict()
            revistas.append(revista_dict)

        self.assertIsNotNone(revistas[0]['disciplina'], "Falta disciplina")

    def test_per01_journal(self):
        print('Prueba de revista para test_per01_journal')
        self.maxDiff = None
        config.DB_FILES = ['test_per01.txt.gz']
        marc2dict = Marc2Dict()
        revistas = []

        registro_expected = [
            {
                'base_datos': 'PER01000339138',
                'titulo_revista': 'Papeis avulsos de zoologia',
                'issn': '0031-1049',
                'pais': 'BR',
                'idioma' : ['eng']
            }
        ]

        for dict in marc2dict.get_dict():
            print(dict)
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
        print('Prueba del campo disciplina de revista en PERIODICA.')
        self.maxDiff = None
        config.DB_FILES = ['test_per01.txt.gz']
        marc2dict = Marc2Dict()
        revistas = []
        disciplina_expected = [
            {
                'idioma': None,
                'palabra_clave': 'Biología'
            }
        ]

        for dict in marc2dict.get_dict():
            revista_dict = RevistaDict(dict)
            revista_dict = revista_dict.to_dict()
            revistas.append(revista_dict)

        self.assertIsNotNone(revistas[0]['disciplina'], "Falta disciplina")
