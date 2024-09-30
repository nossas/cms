from typing import List, Tuple
from contrib.bonde.models import PlacesIBGE

def get_states(column_label="nome_uf") -> List[Tuple[str, str]]:
    states = PlacesIBGE.objects.values('uf', column_label).distinct()
    return sorted([(state['uf'], state[column_label]) for state in states], key=lambda x: x[1])

def get_ufs() -> List[Tuple[str, str]]:
    return get_states(column_label="nome_uf")

def get_choices(uf: str) -> List[Tuple[str, str]]:
    choices = PlacesIBGE.objects.filter(uf=uf).values('codigo_municipio_completo', 'nome_municipio').distinct()
    return sorted([(choice['codigo_municipio_completo'], choice['nome_municipio']) for choice in choices], key=lambda x: x[1])
