"""
connector_registry.py
Centralised lookup & conflict-checking for CRM connector modules.

"""

import importlib
import json
import logging
import os
from typing import Callable, Dict

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 📦 1. Built-in connectors that ship with the repo
# ---------------------------------------------------------------------------
_DEFAULT_REGISTRY: Dict[str, str] = {
    "zendesk": "connectors.zendesk_api_agent",
    # "salesforce": "connectors.salesforce_api_agent",
    # "intercom": "connectors.intercom_api_agent",
}

# ---------------------------------------------------------------------------
# 🛠️ 2. Optional overrides via the CONNECTOR_REGISTRY_JSON env var
# ---------------------------------------------------------------------------
try:
    _custom_registry: Dict[str, str] = json.loads(
        os.getenv("CONNECTOR_REGISTRY_JSON", "{}")
    )
except json.JSONDecodeError as e:
    raise RuntimeError("CONNECTOR_REGISTRY_JSON is not valid JSON") from e

# ---------------------------------------------------------------------------
# 🔒 3. Detect conflicting (duplicating) mappings
# ---------------------------------------------------------------------------
_conflicts: list[str] = []
for key, custom_path in _custom_registry.items():
    if key in _DEFAULT_REGISTRY and _DEFAULT_REGISTRY[key] != custom_path:
        _conflicts.append(
            f"Key '{key}': default → {_DEFAULT_REGISTRY[key]}  vs  override → {custom_path}"
        )

if _conflicts:
    raise RuntimeError(
        "Connector registry conflict — duplicate keys mapped to different modules:\n"
        + "\n".join(_conflicts)
    )

# ---------------------------------------------------------------------------
# 🗺️ 4. Final merged registry (override wins when path identical)
# ---------------------------------------------------------------------------
_CONNECTOR_REGISTRY: Dict[str, str] = {**_DEFAULT_REGISTRY, **_custom_registry}
logger.debug("Connector registry initialised: %s", _CONNECTOR_REGISTRY)

# ---------------------------------------------------------------------------
# 🚚 5. Public helpers
# ---------------------------------------------------------------------------
def connector_module_path(source: str) -> str:
    """Return the dotted-path module for a given CRM key."""
    try:
        return _CONNECTOR_REGISTRY[source]
    except KeyError:
        raise ValueError(
            f"Unknown connector '{source}'. Known: {', '.join(_CONNECTOR_REGISTRY)}"
        )


def resolve_tool(source: str, func_name: str) -> Callable:
    """
    Dynamically import the connector for *source* and return <module>.<func_name>.
    Used by IO-router tools.
    """
    module_path = connector_module_path(source)
    module = importlib.import_module(module_path)
    try:
        return getattr(module, func_name)
    except AttributeError as e:
        raise AttributeError(
            f"Connector '{module_path}' is missing required function '{func_name}'"
        ) from e