import os
import gzip

from biblat_schema.catalogs import SubDisciplina, Disciplina, NombreGeografico

from biblat_process.marc2dict import Marc2Dict
from biblat_process.biblatdocument import DocumentoDict
from biblat_process.settings import config
from .base import BaseTestCase


class TestBiblatDocument(BaseTestCase):


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

        disciplina = Disciplina(
            _id=self.generate_uuid_32_string(),
            nombre={
                'es': 'Biología',
                'en': 'Biology'
            }
        )
        disciplina.save()

        subdisciplina = SubDisciplina(
                _id=self.generate_uuid_32_string(),
                disciplina=disciplina,
                nombre={
                    'es': 'Taxonomía y sistemática',
                    'en': 'Taxonomy and systematics'
                }
        )
        subdisciplina.save()

        subdisciplina2 = SubDisciplina(
                _id=self.generate_uuid_32_string(),
                disciplina=disciplina,
                nombre={
                    'es': 'Botánica',
                    'en': 'Botany'
                }
        )
        subdisciplina2.save()

        nombregeografico = NombreGeografico(
                _id=self.generate_uuid_32_string(),
                nombre={
                    'es': 'Brasil',
                    'en': 'Brazil'
                },
                nota={
                    'es': 'Documentos históricos',
                    'en': 'History documents'
                }
        )
        nombregeografico.save()

        nombregeografico2 = NombreGeografico(
                _id=self.generate_uuid_32_string(),
                nombre={
                    'es': 'México',
                    'en': 'Mexico'
                },
                nota={
                    'es': 'Documentos históricos',
                    'en': 'History documents'
                }
        )
        nombregeografico2.save()

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

        self.assertEqual(len(documentos), 1)
        self.assertEqual(documentos[0]['autor'], autores_expected)
        self.assertEqual(len(documentos[0]['autor']), 2)
        self.assertIsNone(documentos[0]['doi'], "Opcional el DOI")
        self.assertIsNotNone(documentos[0]['fasciculo'], "Falta el fascículo")
        self.assertIsNotNone(documentos[0]['revista'], "Falta título de la revista")
        self.assertIsNotNone(documentos[0]['numero_sistema'], "Falta número de sistema")
        self.assertIsNotNone(documentos[0]['titulo_documento'], "Falta título del documento")
        self.assertIsNotNone(documentos[0]['fecha_creacion'], "Falta fecha de creación")
        self.assertIsNotNone(documentos[0]['fecha_actualizacion'], "Falta fecha de actualización")

    def test_cla01_document_fasciculo(self):
        print('test_cla01_document_fasciculo')
        self.maxDiff = None
        config.DB_FILES = ['test_cla01_520.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)
            print(documento_dict)

        self.assertIsNotNone(documentos[0]['fasciculo'], "Falta el fascículo")

    def test_cla_document_paginacion(self):
        print('test_cla01_document_paginacion')
        self.maxDiff = None
        config.DB_FILES = ['test_cla01_300.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)
            print(documento_dict)

        self.assertIsNotNone(documentos[0]['fasciculo'], "Faltan páginas")

    def test_cla01_document_autor_corporativo(self):
        print('test_cla01_document_autor_corporativo')
        self.maxDiff = None
        config.DB_FILES = ['test_cla01_autorcorporativo.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)
            print(documento_dict)

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

        self.assertIsNotNone(documentos[0]['resumen'], "Falta resumen")
        self.assertGreater(len(documentos[0]['resumen']), 2, "Debe tener 2 resumenes")

    def test_cla01_document_tipodocumento(self):
        print('test_cla01_document_tipodocumento')
        self.maxDiff = None
        config.DB_FILES = ['test_cla01.txt.gz']
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
        config.DB_FILES = ['test_cla01.txt.gz']
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

    def test_per01_document_subdisciplina(self):
        print('test_per01_document_subdisciplina')
        self.maxDiff = None
        config.DB_FILES = ['test_per01.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)
            print(documento_dict)

        self.assertIsNotNone(documentos[0]['subdisciplinas'], "Falta subdisciplina")

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

    def test_per_01_document_keywords(self):
        print('test_per01_document_keywords')
        self.maxDiff = None
        config.DB_FILES = ['test_per01.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)

        self.assertIsNotNone(documentos[0]['palabras_clave'], "Faltan keywords")

    def test_per01_document_nombresgeograficos(self):
        print('test_per01_document_nombresgeofraficos')
        self.maxDiff = None
        config.DB_FILES = ['test_per01_653.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)

        self.assertIsNotNone(documentos[0]['nombresgeograficos'], "Falta nombre geografico")

    def test_per01_document_referenciasdocumento(self):
        print('test_per01_document_referenciasdocumento')
        self.maxDiff = None
        config.DB_FILES = ['test_per01.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)

        self.assertIsNotNone(documentos[0]['referencias_documento'], "Falta referencias")
        self.assertTrue(documentos[0]['referencias_documento'], "No hay referencias")

    def test_per01_document_textocompleto(self):
        print('test_per01_document_textocompleto')
        self.maxDiff = None
        config.DB_FILES = ['test_per01.txt.gz']
        marc2dict = Marc2Dict()
        documentos = []

        texto_completo_expected = [
            {
                'url': 'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0031-10492009004100001&'
                       'lng=pt&nrm=iso&tlng=en',
                'descripcion': 'Texto completo (Ver HTML)'
            }
        ]

        for dict in marc2dict.get_dict():
            documento_dict = DocumentoDict(dict)
            documento_dict = documento_dict.to_dict()
            documentos.append(documento_dict)
            print(documento_dict)

        self.assertIsNotNone(documentos[0]['texto_completo'], "Falta URL del texto completo")
        self.assertEqual(documentos[0]['texto_completo'], texto_completo_expected)
        self.assertRegex(texto_completo_expected[0]['url'], '^http', "URL incorrecto")
