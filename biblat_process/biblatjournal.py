import inspect
from datetime import datetime

from biblat_process import tesauro
from biblat_schema.catalogs import Disciplina


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
        return self.marc_dict.get('035', [{'a': None}])[0].get('a', None)

    @property
    def titulo_revista(self):
        return self.marc_dict.get('222', [{'a': None}])[0].get('a', None)

    @property
    def titulo_abr_revista(self):
        # TODO revisar la etiqueta.
        return self.marc_dict.get('245', [{'a': None}])[0].get('a', None)

    @property
    def issn(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('022', [{'a': None}])[0].get('a', None)

    @property
    def pais(self):
        # TODO revisar la etiqueta
        pais = self.marc_dict.get('008', [{'e': None}])[0].get('e', None)
        if pais in tesauro.paises:
             pais = tesauro.paises[pais]
        else:
            pais = None
        return pais

    @property
    def disciplina(self):
        disc = Disciplina()
        if '698' in self.marc_dict:
            for disciplinadoc in self.marc_dict['698']:
                disc.meta = disciplinadoc.get('spa', None)
                disc.nombre = disciplinadoc.get('a', None)
        return disc

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
            idioma = str(self.marc_dict['041'][0]['a'])
            if idioma in tesauro.idioma:
                idioma = tesauro.idioma[idioma]
            else:
                idioma = None
        return idioma

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
