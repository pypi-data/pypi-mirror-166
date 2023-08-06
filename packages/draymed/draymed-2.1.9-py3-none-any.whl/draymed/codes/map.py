"""
Contains all of the snomed/draymed codes used in dhos, arranged in categories

"""
from typing import Dict

from draymed.codes.code_map_transform import get_code_map

code_map: Dict[str, Dict[str, Dict[str, str]]] = get_code_map()
