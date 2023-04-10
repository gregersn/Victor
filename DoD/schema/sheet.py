import random
from typing import Dict, List, Optional, Sequence, Any, Type, Union
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table


def random_table(table: Sequence[Any]):
    picked = random.choice(table)
    if isinstance(picked, list):
        return random_table(picked)
    return picked


class BaseSheet(BaseModel):
    def sheet(self):
        table = Table(title=self.__class__.__name__, show_header=False)

        table.add_column("Key")
        table.add_column("Value")

        for key, value in self:
            table.add_row(key.title(), value)
        console = Console()
        console.print(table)


class Section(BaseModel):
    ...
