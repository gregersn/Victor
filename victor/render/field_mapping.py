from typing import Dict, TypedDict, Any, List, Union, Optional
from pathlib import Path
import yaml
import re

from victor.interpreter import get_interpreter

ExpandedMapping = Dict[str, str]
Values = Union[str, int]
ValueList = List[Dict[str, Values]]
ValueDict = Dict[str, Union[Values, 'ValueDict', ValueList]]


class DescribedMapping(TypedDict):
    name: str
    value: Union[str, int]
    subskills: List['DescribedMapping']


FormData = Dict[
    str,
    Union[
        int,
        str,
        List[DescribedMapping],
        'FormData'
    ]
]

FieldMapping = Dict[str, Union['FieldMapping', str]]


class SheetSchema(TypedDict):
    pdf: str
    fields: Dict[str, str]


def load_yaml(path: Path):
    assert path.exists()
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def get_value(values: Union[Dict[str, Any], List[Dict[str, Any]], None],
              path: List[str],
              variables: Optional[Dict[str, Any]] = None) -> Any:
    if len(path) > 1:
        if isinstance(values, Dict):
            return get_value(values[path[0]], path[1:], variables)
        elif isinstance(values, List):
            if path[0][0] == '{' and path[0][-1] == '}':
                key_name, search_value = path[0][1:-1].split(', ')
                for entry in values:
                    if entry[key_name] == search_value:
                        return get_value(entry, path[1:], variables)
            elif path[0][0] == '[' and path[0][-1] == ']':
                key = path[0][1:-1]
                return [v[key] for v in values]
            else:
                raise NotImplementedError(path)
    else:
        if (m := CALC_VALUE.match(path[0])) and variables is not None:
            return calc_value(m.group(1), variables)
        elif isinstance(values, Dict):
            return values[path[0]]
        elif isinstance(values, List):
            if path[0][0] == '{' and path[0][-1] == '}':
                key_name, value_name = path[0][1:-1].split(', ')
                print(key_name, value_name)
                return [(entry[key_name], entry[value_name])
                        for entry in values]
            elif path[0][0] == '[' and path[0][-1] == ']':
                key = path[0][1:-1]
                return [v[key] for v in values]
            else:
                raise NotImplementedError(path)
        else:
            raise NotImplementedError(path)


QUERY_KEY = re.compile(r'(.+)\{(\w*)\}')
LIST_KEY = re.compile(r'(.+)\{(\d+)[,\ ]+(\d+)}(.*)')
CALC_VALUE = re.compile(r'\$\((.*)\)')


def calc_value(expression: str, variables: Dict[str, Any]):
    interpreter = get_interpreter(expression, variables=variables)
    try:
        result = interpreter.interpret()
        return result[1][-1]

    except TypeError:
        return None


class RemappedData(TypedDict):
    pdf: Path
    fields: Dict[str, Any]


def remap_reverse(values: Path, schema: Path) -> RemappedData:
    stats = load_yaml(values)
    fields: SheetSchema = load_yaml(schema)

    mappings = fields['fields']

    remapped: Dict[str, Any] = {}

    for k, v in mappings.items():
        if m := LIST_KEY.match(k):
            name_start = m.group(1)
            start = int(m.group(2))
            end = int(m.group(3))
            name_end = m.group(4)
            indices = list(range(start, end + 1))

            if '#' in v:
                for i in range(start, end):
                    temp = v.replace('#', str(i))
                    try:
                        res = get_value(stats, temp.split('.'), remapped)
                    except KeyError:
                        continue
                    remapped[f'{name_start}{i}{name_end}'] = res
            else:
                res = get_value(stats, v.split('.'), remapped)
                while res:
                    n = f'{name_start}{indices.pop(0)}{name_end}'
                    remapped[n] = res.pop(
                        0)
        else:
            remapped[k] = get_value(stats, v.split('.'), remapped)

    return {'pdf': Path(fields['pdf']).expanduser(),
            'fields': remapped}


def remap(data: FormData,
          mapping: FieldMapping) -> Dict[str, Values]:
    remapped: Dict[str, Values] = {}
    for key, item in data.items():
        if isinstance(item, Dict):
            m = mapping[key]
            if isinstance(m, Dict):
                t = remap(item, m)
                remapped.update(t)
        elif isinstance(item, List):
            m = mapping[key]
            assert isinstance(m, Dict), m
            for entry in item:
                entry_name = entry['name']
                remapped_name = m[entry_name]
                if isinstance(remapped_name, str):
                    remapped[remapped_name] = entry['value']
                else:
                    if ('name' in remapped_name and
                            'value' in remapped_name):
                        subskill_count = len(entry['subskills'])
                        for i in range(subskill_count):
                            assert isinstance(entry['subskills'][i], dict)
                            skill = entry['subskills'][i]
                            assert isinstance(remapped_name['name'], str)
                            assert isinstance(remapped_name['value'], str)
                            t = remapped_name['name'].format(i + 1)
                            remapped[t] = skill['name']

                            remapped[remapped_name['value'].format(
                                i + 1)] = skill['value']

        elif isinstance(item, int):
            m = mapping[key]
            if isinstance(m, str):
                remapped[m] = item
        else:
            m = mapping[key]
            if isinstance(m, str):
                remapped[m] = str(item)

    return remapped
