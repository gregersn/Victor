"""Output utilities."""
from typing import Dict, List


BaseResultType = str | int | float | None
ResultType = BaseResultType | List[BaseResultType] | Dict[str, 'ResultType']


def result2string(result: Dict[str, ResultType]):
    """Convert a generator result to string."""
    output: List[str] = []
    for key, value in result.items():
        if value is None:
            continue
        if isinstance(value, list):
            output.append(f"{key}: {', '.join([str(v) for v in value])}")
            continue
        if isinstance(value, dict):
            output.append(f"{key}:")
            for subkey, subvalue in value.items():
                output.append(f"- {subkey}: {subvalue}")
            continue
        output.append(f"{key}: {value}")

    return "\n".join(output)
