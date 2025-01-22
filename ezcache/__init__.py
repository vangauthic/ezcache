from typing import TYPE_CHECKING, List, Union, Dict, Optional, Any

# Import actual types for runtime
from ._types import *
from .api import EZCache as _BaseClient

# Create unified type exports

class EZCache(_BaseClient):
    """
    FULL DOCUMENTATION AVAILABLE AT https://developers.plane.so/api-reference/
    """
    if TYPE_CHECKING:
        ...

# Export everything needed
__all__ = [
    "EZCache",
]