import inspect
from datetime import datetime

from mongoengine import connect
from biblat_schema.catalogs import SubDisciplina, NombreGeografico
from biblat_schema.models import Revista

from biblat_process import tesauro
from biblat_process.settings import config

connect(
            db=config.MONGODB_NAME,
            host=config.MONGODB_HOST
        )

class DocumentoDict:

    def __init__(self, marc_dict):
        self.marc_dict = marc_dict
        self.subdisciplinas_list = [i.nombre.es for i in SubDisciplina.objects()]
        self.subdisciplinas_list += [i.nombre.en for i in SubDisciplina.objects()]
        self.nombresgeograficos_list = [i.nombre.es for i in NombreGeografico.objects()]
        self.nombresgeograficos_list += [i.nombre.en for i in NombreGeografico.objects()]

    def to_dict(self):
        properties = {}
        for name, value in \
                inspect.getmembers(self.__class__,
                                   lambda o: isinstance(o, property)):
            value = getattr(self, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                properties[name] = value
        return properties

    @property
    def revista(self):
        str_issn = self.marc_dict.get('022', [{'a': None}])[0].get('a')
        return Revista.objects(issn=str_issn).first()

    @property
    def fasciculo(self):
        result = []
        if '300' in self.marc_dict:
                for fasciculo in self.marc_dict['300']:
                    fasciculo_dict = {
                        'volumen': fasciculo.get('a', None),
                        'numero': fasciculo.get('b', None)
                    }
                    if fasciculo_dict['volumen']:
                        fasciculo_dict['volumen'] = int(str(fasciculo_dict['volumen']).replace('V', ''))
                    if fasciculo_dict['numero']:
                        fasciculo_dict['numero'] = int(str(fasciculo_dict['numero']).replace('N', ''))
                        result.append(fasciculo_dict)
        return result or None

    @property
    def numero_sistema(self):
        return self.marc_dict.get('035', [{'a': None}])[0].get('a')

    @property
    def titulo_documento(self):
        return self.marc_dict.get('245', [{'a': None}])[0].get('a')

    @property
    def doi(self):
        return self.marc_dict.get('024', [{'a': None}])[0].get('a')

    @property
    def idioma(self):
        idioma_marc = self.marc_dict.get('041', [{'a': None}])[0].get('a')
        return tesauro.idioma.get(idioma_marc)

    @property
    def autor(self):
        result = []
        if '100' in self.marc_dict:
            for auth in self.marc_dict['100']:
                auth_dict = {
                    'nombre': auth.get('a', None),
                    'correo_electronico': auth.get('6', None),
                    'referencia': auth.get('z', None)
                }
                if auth_dict['referencia']:
                    auth_dict['referencia'] = int(str(auth_dict['referencia']).
                                                  replace(')', '').
                                                  replace('(', ''))
                result.append(auth_dict)
        return result or None

    @property
    def autor_corporativo(self):
        result = []
        if '110' in self.marc_dict:
            for auth_corporative in self.marc_dict['110']:
                auth_corporative_dict = {
                    'institucion': auth_corporative.get('a', None),
                    'dependencia': auth_corporative.get('b', None),
                    'pais': auth_corporative.get('c', None)
                }

                if auth_corporative_dict['pais']:
                    auth_corporative_dict['pais'] = tesauro.paises[auth_corporative_dict['pais']]
                result.append(auth_corporative_dict)
        return result or None

    @property
    def institucion(self):
        result = []
        if '120' in self.marc_dict:
            for institution in self.marc_dict['120']:
                institution_dict = {
                    'institucion': institution.get('u', None),
                    'dependencia': institution.get('v', None),
                    'ciudad_estado': institution.get('w', None),
                    'pais': institution.get('x', None),
                    'referencia': institution.get('z', None)
                }

                if institution_dict['pais']:
                    institution_dict['pais'] = tesauro.paises[institution_dict['pais']]
                if institution_dict['referencia']:
                    institution_dict['referencia'] = int(str(institution_dict['referencia']).
                                                  replace(')', '').
                                                  replace('(', ''))
                result.append(institution_dict)
        return result or None

    @property
    def resumen(self):
        result = []
        if '520' in self.marc_dict:
            for resumen in self.marc_dict['520']:
                if 'a' in resumen:
                    resumen_dict = {
                        'idioma': 'spa',
                        'resumen': resumen.get('a', None)
                    }
                elif 'p' in resumen:
                    resumen_dict = {
                        'idioma': 'por',
                        'resumen': resumen.get('p', None)
                    }
                elif 'i' in resumen:
                    resumen_dict = {
                        'idioma': 'eng',
                        'resumen': resumen.get('i', None)
                    }
                else:
                    resumen_dict = {
                        'idioma': 'zxx',
                        'resumen': resumen.get('o', None)
                    }
                result.append(resumen_dict)
        return result or None

    @property
    def fecha_creacion(self):
        return datetime.strptime(
            self.marc_dict['CAT'][0]['c'] + self.marc_dict['CAT'][0]['h'],
            '%Y%m%d%H%M'
        )

    @property
    def fecha_actualizacion(self):
        return datetime.strptime(
            self.marc_dict['CAT'][-1]['c'] + self.marc_dict['CAT'][-1]['h'],
            '%Y%m%d%H%M'
        )

    @property
    def disciplina(self):
        result = []
        if '650' in self.marc_dict:
            for disciplinadoc in self.marc_dict['650']:
                disciplinadoc_dict = {
                    'idioma': disciplinadoc.get('spa', None),
                    'palabra_clave': disciplinadoc.get('a', None)
                }
                result.append(disciplinadoc_dict)
        return result or None

    @property
    def palabras_clave(self):
        result = []
        if '653' in self.marc_dict:
            for palabraclave in self.marc_dict.get('653', []):
                palabraclave = palabraclave.get('a', None)
                if palabraclave not in self.subdisciplinas_list and palabraclave not in self.nombresgeograficos_list:
                    palabraclave_dict = {
                        'idioma': 'spa',
                        'palabra_clave': palabraclave
                    }
                    result.append(palabraclave_dict)

            for keywords in self.marc_dict.get('654', []):
                if keywords not in self.subdisciplinas_list and keywords not in self.nombresgeograficos_list:
                    keywords_dict = {
                        'idioma': 'eng',
                        'palabra_clave': keywords.get('a', None)
                }
                result.append(keywords_dict)

        return result or None

    @property
    def subdisciplinas(self):
        result = []
        if '653' in self.marc_dict:
            for palabraclave in self.marc_dict.get('653', []):
                palabraclave = palabraclave.get('a', None)
                if palabraclave in self.subdisciplinas_list:
                    subdisciplina = SubDisciplina.objects(__raw__={'nombre.es': palabraclave}).first()
                    result.append(subdisciplina.id)

            for keyword in self.marc_dict.get('654', []):
                keyword = keyword.get('a', None)
                if keyword in self.subdisciplinas_list:
                    subdisciplina = SubDisciplina.objects(__raw__={'nombre.en': keyword}).first()
                    if subdisciplina and subdisciplina.id not in result:
                        result.append(subdisciplina.id)
        return result or None

    @property
    def nombresgeograficos(self):
        result = []
        if '653' in self.marc_dict:
            for palabraclave in self.marc_dict.get('653', []):
                palabraclave = palabraclave.get('a', None)
                if palabraclave in self.nombresgeograficos_list:
                    nombregeografico = NombreGeografico.objects(__raw__={'nombre.es': palabraclave}).first()
                    result.append(nombregeografico.id)

            for keyword in self.marc_dict.get('654', []):
                keyword = keyword.get('a', None)
                if keyword in self.nombresgeograficos_list:
                    nombregeografico = NombreGeografico.objects(__raw__={'nombre.en': keyword}).first()
                    if nombregeografico and nombregeografico.id not in result:
                        result.append(nombregeografico.id)
        return result or None

    @property
    def tipo_documento(self):
        result = []
        if '590' in self.marc_dict:
            for tipodocumento in self.marc_dict['590']:
                tipodocumento_dict = {
                    'tipo_documento': tipodocumento.get('a', None)
                }
                result.append(tipodocumento_dict)
        return result or None

    @property
    def enfoque_documento(self):
        result = []
        if '590' in self.marc_dict:
            for enfoquedocumento in self.marc_dict['590']:
                enfoquedocumento_dict = {
                    'enfoque_documento': enfoquedocumento.get('b', None)
                }
                result.append(enfoquedocumento_dict)
        return result or None

    @property
    def referencias_documento(self):
        if self.marc_dict.get('504', [{'a': None}])[0].get('a'):
            return True
        return False

    @property
    def texto_completo(self):
        result = []
        if '856' in self.marc_dict:
            for textocompleto in self.marc_dict['856']:
                textocompleto_dict = {
                    'url': textocompleto.get('u', None),
                    'descripcion': textocompleto.get('y', None)
                }
                result.append(textocompleto_dict)
        return result or None