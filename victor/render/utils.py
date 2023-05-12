from typing import Any, Dict, List


def result2string(result: Dict[str, Any]):
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
            for key, v in value.items():
                output.append(f"- {key}: {v}")
            continue
        output.append(f"{key}: {value}")

    return "\n".join(output)
