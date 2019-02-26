# coding: utf-8
import os
import unittest

from mock import patch

from biblat_process import populate_catalog


def mock_init(self):
    test_path = os.path.dirname(os.path.realpath(__file__))
    test_files_path = os.path.join(test_path, 'test_files')
    self.data_dir = test_files_path
    self.files = {
        'Pais': 'Pais.json',
        'Idioma': 'Idioma.json',
        'TipoDocumento': 'TipoDocumento.json',
        'EnfoqueDocumento': 'EnfoqueDocumento.json',
        'Disciplina': 'Disciplina.json',
        'SubDisciplina': 'SubDisciplina.json',
        'NombreGeografico': 'NombreGeografico.json',
        'LicenciaCC': 'LicenciaCC.json',
        'SherpaRomeo': 'SherpaRomeo.json'
    }


@patch('biblat_process.populate_catalog.PopulateCatalog.__init__', new=mock_init)
class TestPopulateCatalog(unittest.TestCase):
    def test_pais(self):
        populate_catalog.main(['-c', 'pais'])

    @patch('biblat_process.populate_catalog.PopulateCatalog.__init__',
           new=mock_init)
    def test_idioma(self):
        populate_catalog.main(['-c', 'idioma'])
