# coding: utf-8
import os
import gzip
import unittest
from biblat_process.marc2dict import Marc2Dict
from biblat_process.biblatjournal import RevistaDict


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
        print('test_cla01_document')
        self.maxDiff = None
        self.config['db_files'] = 'test_cla01.txt.gz'
        marc2dict = Marc2Dict(self.config)
        revistas = []

        registro_expected = [
            {
                'nombre': 'Sandoval Montes, I',
                'correo_electronico': 'ismael.sandoval@inegi.org.mx',
                'referencia': 1
            },
            {
                'nombre': 'Ramos Leal, J.A',
                'correo_electronico': None,
                'referencia': 2
            }
        ]

        for dict in marc2dict.get_dict():
            print(dict)
            revista_dict = RevistaDict(dict)
            revista_dict = revista_dict.to_dict()
            revistas.append(revista_dict)
            print(revista_dict)

        self.assertEqual(len(revistas), 1)
        self.assertEqual(revistas[0]['autor'], registro_expected)
        self.assertEqual(len(revistas[0]['autor']), 2)

    def test_per01_journal(self):
        print('test_per01_document')
        self.maxDiff = None
        self.config['db_files'] = 'test_per01.txt.gz'
        marc2dict = Marc2Dict(self.config)
        revistas = []

        registro_expected = [
            {
                'nombre': 'Oppenheimer, Marina',
                'correo_electronico': 'marinaopp@yahoo.com.br',
                'referencia': 1
            },
            {
                'nombre': 'Silveira, Luis Fabio',
                'correo_electronico': 'lfsilvei@usp.br',
                'referencia': 1
            }
        ]

        for dict in marc2dict.get_dict():
            print(dict)
            revista_dict = RevistaDict(dict)
            revista_dict = revista_dict.to_dict()
            revistas.append(revista_dict)
            print(revista_dict)

        self.assertEqual(len(revistas),1)
        self.assertEqual(revistas[0]['autor'], registro_expected)
        self.assertEqual(len(revistas[0]['autor']), 2)
