"""Error handling."""
import platform
import sys


def missing_tk_inter():
    """Suggest resolution to missing tk."""
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    # if platform mac
    if platform.system() == "Darwin":
        suggestion = f"try `brew install python-tk@{python_version}`"

        return suggestion
