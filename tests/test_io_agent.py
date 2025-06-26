import types
from agents.io_agent import route_fetch
from schemas import Ticket
import sys
import importlib


def _fake_fetch(ticket_id: int) -> Ticket:
    return Ticket(ticket_id=ticket_id, body="Hello")

def test_route_fetch_dispatch(monkeypatch):
    # Dynamically insert a fake connector module
    fake_mod = types.ModuleType("connectors.fake_api_agent")
    fake_mod.fetch_ticket = _fake_fetch
    monkeypatch.syspath_prepend(".")          # ensure importable
    monkeypatch.setitem(
        sys.modules, "connectors.fake_api_agent", fake_mod
    )

    # Override registry via env-var
    monkeypatch.setenv(
        "CONNECTOR_REGISTRY_JSON",
        '{"mock": "connectors.fake_api_agent"}'
    )

     # 3Reload connector_registry so it picks up the new env-var.
    from utils import connector_registry

    importlib.reload(connector_registry)

    ticket = route_fetch("mock", 42)
    assert ticket.ticket_id == 42
