import inspect
from datetime import datetime

from biblat_process import tesauro


class RevistaDict:

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

    @property
    def base_datos(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def titulo_revista(self):
        return self.marc_dict.get('222', [{'a': None}])[0].get('a', None)

    @property
    def titulo_abr_revista(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def issn(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def issn_electronico(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def pais(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def disciplina(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def licencia_cc(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def sherpa_romeo(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def idioma(self):
        if '041' in self.marc_dict and 'a' in self.marc_dict['041'][0]:
            return str(self.marc_dict['041'][0]['a'])
        return None

    @property
    def periodicidad(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def logo(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def portada(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

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
