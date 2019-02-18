import os
import gzip
import unittest
from biblat_process.marc2dict import Marc2Dict
from biblat_process.biblatdocument import DocumentoDict
from biblat_process.settings import config


class TestBiblatDocument(unittest.TestCase):

    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.test_files_path = os.path.join(self.test_path, 'test_files')

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

    def test_cla01_document(self):
        print('test_cla01_document')
        self.maxDiff = None
        config.DB_FILES = ['test_cla01.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        autores_expected = [
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
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)
            print(documento_dict)

        self.assertEqual(len(documentos), 1)
        self.assertEqual(documentos[0]['autor'], autores_expected)
        self.assertEqual(len(documentos[0]['autor']), 2)
        self.assertIsNone(documentos[0]['doi'], "Opcional el DOI")
        self.assertIsNotNone(documentos[0]['paginacion'], "Falta paginación")
        self.assertIsNotNone(documentos[0]['titulo_documento'], "Falta título del documento")

    def test_cla01_document_autor_corporativo(self):
        print('test_cla01_document_autor_corporativo')
        self.maxDiff = None
        config.DB_FILES = ['test_cla01_autorcorporativo.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        autor_corporativo_expected = [
            {
                'institucion': 'Grupo Expansión',
                'dependencia': None,
                'pais': 'México'
            }
        ]

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)

        self.assertEqual(documentos[0]['autor_corporativo'], autor_corporativo_expected)
        self.assertEqual(len(documentos[0]['autor_corporativo']), 1)

    def test_cla01_document_institucion(self):
        print('test_cla01_document_institucion')
        self.maxDiff = None
        config.DB_FILES = ['test_cla01.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        institucion_expected = [
            {
                'institucion': 'Instituto Nacional de Estadística, Geografía e Informática',
                'dependencia': None,
                'ciudad_estado': 'Aguascalientes',
                'pais': 'MX',
                'referencia': 1
            },
            {
                'institucion': 'Instituto Potosino de Investigación Científica y Tecnológica',
                'dependencia': None,
                'ciudad_estado': 'San Luis Potosí',
                'pais': 'MX',
                'referencia': 2
            }
        ]

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)

        self.assertEqual(documentos[0]['institucion'], institucion_expected)
        self.assertEqual(len(documentos[0]['institucion']), 2)

    def test_cla01_document_resumen(self):
            print('test_cla01_document_resumen')
            self.maxDiff = None
            config.DB_FILES = ['test_cla01_520.txt.gz']
            marc2dict = Marc2Dict()
            documentos = []

            for dict in marc2dict.get_dict():
                documento_dict = DocumentoDict(dict)
                documento_dict = documento_dict.to_dict()
                documentos.append(documento_dict)
                print(documento_dict)

            self.assertIsNotNone(documentos[0]['resumen'], "Falta resumen")

    def test_cla01_document_tipodocumento(self):
            print('test_cla01_document_tipodocumento')
            self.maxDiff = None
            config.DB_FILES = ['test_cla01_520.txt.gz']
            marc2dict = Marc2Dict()
            documentos = []

            for dict in marc2dict.get_dict():
                documento_dict = DocumentoDict(dict)
                documento_dict = documento_dict.to_dict()
                documentos.append(documento_dict)

            self.assertIsNotNone(documentos[0]['tipo_documento'], "Falta tipo de documento")

    def test_cla01_document_enfoquedocumento(self):
            print('test_cla01_document_enfoquedocumento')
            self.maxDiff = None
            config.DB_FILES = ['test_cla01_520.txt.gz']
            marc2dict = Marc2Dict()
            documentos = []

            for dict in marc2dict.get_dict():
                documento_dict = DocumentoDict(dict)
                documento_dict = documento_dict.to_dict()
                documentos.append(documento_dict)

            self.assertIsNotNone(documentos[0]['enfoque_documento'], "Falta enfoque de documento")

    def test_cla01_document_disciplina(self):
            print('test_cla01_document_disciplina')
            self.maxDiff = None
            config.DB_FILES = ['test_cla01_520.txt.gz']
            marc2dict = Marc2Dict()
            documentos = []

            for dict in marc2dict.get_dict():
                documento_dict = DocumentoDict(dict)
                documento_dict = documento_dict.to_dict()
                documentos.append(documento_dict)

            self.assertIsNotNone(documentos[0]['disciplina'], "Falta disciplina")

    def test_cla01_document_palabrasclave(self):
            print('test_cla01_document_palabraclave')
            self.maxDiff = None
            config.DB_FILES = ['test_cla01_520.txt.gz']
            marc2dict = Marc2Dict()
            documentos = []

            for dict in marc2dict.get_dict():
                documento_dict = DocumentoDict(dict)
                documento_dict = documento_dict.to_dict()
                documentos.append(documento_dict)

            self.assertIsNotNone(documentos[0]['palabras_clave'], "Faltan palabras clave")

    def test_per01_document_keywords(self):
            print('test_per01_document_keywords')
            self.maxDiff = None
            config.DB_FILES = ['test_per01.txt.gz']
            marc2dict = Marc2Dict()
            documentos = []

            for dict in marc2dict.get_dict():
                documento_dict = DocumentoDict(dict)
                documento_dict = documento_dict.to_dict()
                documentos.append(documento_dict)

            self.assertIsNotNone(documentos[0]['keyword'], "Faltan keywords")
