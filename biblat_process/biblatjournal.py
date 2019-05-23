import inspect
from datetime import datetime

from biblat_process import tesauro
from biblat_schema.catalogs import Disciplina


class RevistaDict:

    def __init__(self, marc_dict):
        self.marc_dict = marc_dict
        self.disciplinas_list = [i.nombre.es for i in Disciplina.objects()]
        self.disciplinas_list += [i.nombre.en for i in Disciplina.objects()]

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
        base = self.marc_dict.get('035', [{'a': None}])[0].get('a', None)
        return base[:5]

    @property
    def titulo_revista(self):
        return self.marc_dict.get('222', [{'a': None}])[0].get('a', None)

    @property
    def issn(self):
        # TODO revisar la etiqueta
        return self.marc_dict.get('022', [{'a': None}])[0].get('a', None)

    @property
    def pais(self):
        pais_marc = self.marc_dict.get('008', [{'e': None}])[0].get('e')
        return tesauro.paises.get(pais_marc)

    @property
    def disciplina(self):
        str_disciplina = self.marc_dict.get('698', [{'a': None}])[0].get('a', None)
        disciplina = Disciplina.objects(nombre__es=str_disciplina).first()
        return disciplina

    @property
    def idioma(self):
        idioma_marc = self.marc_dict.get('041', [{'a': None}])[0].get('a')
        return tesauro.idioma.get(idioma_marc)

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
