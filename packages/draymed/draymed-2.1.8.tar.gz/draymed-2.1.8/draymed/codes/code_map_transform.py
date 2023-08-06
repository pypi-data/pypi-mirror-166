import json
from pathlib import Path
from typing import Dict, List


def transform_codes(master_codes: List[Dict]) -> Dict[str, Dict[str, Dict[str, str]]]:
    output_codes: Dict[str, Dict[str, Dict[str, str]]] = {}
    for category_item in master_codes:
        output_codes[category_item["category"]] = {}
        category_group = output_codes[category_item["category"]]
        for code_item in category_item["values"]:
            category_group[code_item["code"]] = {
                "short": code_item["short"],
                "long": code_item["long"],
            }
    return output_codes


def get_code_map() -> Dict[str, Dict[str, Dict[str, str]]]:
    source_filepath: Path = Path(__file__).parent.parent / "data/master_codes.json"
    master_codes: List[Dict] = json.loads(source_filepath.read_text())
    return transform_codes(master_codes)
