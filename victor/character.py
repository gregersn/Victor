from typing import Dict, Any, cast, Match
import re

PLACEHOLDER_REGEX = re.compile(r'{{\s*(\w+)\s*}}', flags=re.MULTILINE)


class Character:
    variables: Dict[str, Any]
    content: str

    def __init__(self):
        self.variables = {}
        self.content = ""

    def __str__(self):
        def repl(m: Match[str]):
            var_name: str = cast(str, m.group(1))
            return str(self.variables.get(var_name, "MISSING"))
        result = PLACEHOLDER_REGEX.sub(repl, self.content)
        return result
