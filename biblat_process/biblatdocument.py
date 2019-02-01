import inspect
from datetime import datetime

from biblat_process import tesauro


class DocumentoDict:

    def __init__(self, marc_dict):
        self.marc_dict = marc_dict

    def to_dict(self):
        properties = {}
        for name, value in \
                inspect.getmembers(self.__class__,
                                   lambda o: isinstance(o, property)):
            value = getattr(self, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                properties[name] = value
        return properties

    # @property
    # def numero_sistema(self):
    #     return self.marc_dict['035'][0]['a']

    @property
    def titulo_documento(self):
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def doi(self):
        if '024' in self.marc_dict and 'a' in self.marc_dict['024'][0]:
                return str(self.marc_dict['024'][0]['a'])
        return None

    @property
    def idioma(self):
        if '041' in self.marc_dict and 'a' in self.marc_dict['041'][0]:
            return str(self.marc_dict['041'][0]['a'])
        return None

    @property
    def paginacion(self):
        if '300' in self.marc_dict and 'e' in self.marc_dict['300'][0]:
                return str(self.marc_dict['300'][0]['e']).replace('P', '')\
                    .replace('p', '').replace('pp.', '')
        return None

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
                    'nombre': auth_corporative.get('a', None),
                    'dependencia': auth_corporative.get('b', None),
                    'pais': auth_corporative.get('c', None)
                }
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

                if institution_dict["pais"]:
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
