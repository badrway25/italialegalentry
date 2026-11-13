"""
The browser tests' live server, on a port Chromium accepts.

pytest-django's ``live_server`` binds port 0 unless told otherwise, so the operating system chooses — and this
workstation's dynamic TCP range starts at 1024 (``netsh int ipv4 show dynamicport tcp``: 1024 + 64 511), where Chromium
refuses seventeen ports before it connects (``net::ERR_UNSAFE_PORT``: 1719, 1720, 1723, 2049, 3659, 4045, …, 10080).
Windows hands those ports out in sequence, wrapping round the whole range, so the failure comes and goes with the
sequence: the steward's W3-A run drew 4045 (the review of integration checkpoint 3, «outside this branch») — a
browser-suite failure with no cause in the code.

``live_server`` below draws the port itself, at random, from ``LIVE_SERVER_PORTS`` — above every port a browser
restricts, outside the default dynamic ranges of Windows (49152–65535) and Linux (32768–60999) — and binds it. The bind
is the test of freedom, so there is no window between choosing and using: two lanes running browser tests at once each
get a port of their own, and a port that is taken — by another lane, by an outgoing connection (this machine draws
those from the same range), by a Hyper-V reservation — is skipped for the next draw. A ``--liveserver`` address or
``DJANGO_LIVE_TEST_SERVER_ADDRESS`` that names a port still decides, as with pytest-django.

The root conftest.py imports the fixture and the summary hook, so they hold for tests/ and for every apps/*/tests. A
server a test builds itself, outside ``live_server``, draws its port the same way through
``bind_a_port_chromium_accepts``.
"""

from __future__ import annotations

import os
import random
from collections.abc import Callable, Iterator

import pytest
from django.test.testcases import LiveServerThread

#: The ports above 1023 that Chromium refuses, as the installed one (Playwright's Chromium 153) answered every port from
#: 1024 to 32767 on 16 October 2026 (docs/design-v5/QA/v54/devops/NOTES.md, second pass, item 4). None lies in
#: LIVE_SERVER_PORTS, where it answered no refusal at all.
CHROMIUM_UNSAFE_PORTS = frozenset(
    {1719, 1720, 1723, 2049, 3659, 4045, 5060, 5061, 6000, 6566, 6665, 6666, 6667, 6668, 6669, 6697, 10080}
)

#: Where the live server's port is drawn: above 10080, the highest port a browser refuses; below 32768, where the
#: default dynamic ranges of Linux (32768–60999) and Windows (49152–65535) begin.
LIVE_SERVER_PORTS = range(20000, 32768)

#: How many draws before giving up: each one a port found taken.
ATTEMPTS = 50

#: The live server's address, kept for the run's summary line.
LIVE_SERVER_URL = pytest.StashKey[str]()
#: Whether its port was drawn here, or named by the address given.
LIVE_SERVER_DRAWN = pytest.StashKey[bool]()

_draw = random.SystemRandom()  # never the seeded `random`: two lanes with one seed would draw one sequence


def candidate_ports(count: int = ATTEMPTS, rng: random.Random = _draw) -> list[int]:
    """``count`` distinct ports of LIVE_SERVER_PORTS in random order, none that Chromium refuses."""
    return [port for port in rng.sample(LIVE_SERVER_PORTS, count) if port not in CHROMIUM_UNSAFE_PORTS]


def bind_a_port_chromium_accepts[Server](bind: Callable[[int], Server]) -> Server:
    """
    ``bind(port)`` on drawn ports until one binds, and its result — the next draw when the bind fails: taken
    (EADDRINUSE, WSAEADDRINUSE) or reserved (WSAEACCES: Hyper-V's exclusions lie inside LIVE_SERVER_PORTS on this
    workstation); the last error when every draw fails, never a shared port.

    For a server a test builds itself, outside ``live_server``: the design preview's ``_runserver``
    (tests/frontend/test_design_preview.py) binds ``("127.0.0.1", 0)`` and opens that port in Chromium — the W3-A
    flake's mechanism (the review of the second pass, REVIEW_2 m4). There, ``bind_a_port_chromium_accepts(lambda port:
    Server(("127.0.0.1", port), WSGIRequestHandler, allow_reuse_address=False))``. The bind is the test of freedom only
    without SO_REUSEADDR: on Windows two sockets that both set it bind one port — two of Django's WSGIServers with their
    default ``allow_reuse_address=True`` did, on this workstation. Django's live server passes ``False``; so must the
    server built here.
    """
    refused: OSError | None = None
    for port in candidate_ports():
        try:
            return bind(port)
        except OSError as error:
            refused = error
    raise refused or OSError("no port drawn")


class ChromiumSafeLiveServerThread(LiveServerThread):
    """Django's live server thread, binding a drawn port — and the next draw when the bind fails — unless given one."""

    def _create_server(self, connections_override=None):
        if self.port:  # an address that names its port: exactly that one, as Django does
            return super()._create_server(connections_override=connections_override)
        create = super()._create_server  # Django's: allow_reuse_address=False, so a bind never shares a port

        def bind(port: int):
            self.port = port
            return create(connections_override=connections_override)

        try:
            return bind_a_port_chromium_accepts(bind)
        except OSError:
            self.port = 0
            raise


@pytest.fixture(scope="session")
def live_server(request) -> Iterator:
    """pytest-django's ``live_server`` — the same object, the same settings handling — on a port Chromium accepts."""
    from pytest_django.live_server_helper import LiveServer

    address = request.config.getvalue("liveserver") or os.getenv("DJANGO_LIVE_TEST_SERVER_ADDRESS") or "localhost"
    server = LiveServer(address, start=False)
    drawn = not server.thread.port
    if drawn:
        thread = server.thread
        server.thread = ChromiumSafeLiveServerThread(
            thread.host, thread.static_handler, connections_override=thread.connections_override
        )
        server.thread.daemon = True
    server.start()
    request.config.stash[LIVE_SERVER_URL] = server.url
    request.config.stash[LIVE_SERVER_DRAWN] = drawn
    yield server
    server.stop()


def pytest_terminal_summary(terminalreporter) -> None:
    """One line at the end of a run that started the live server: where it listened, should a browser complain."""
    stash = terminalreporter.config.stash
    url = stash.get(LIVE_SERVER_URL, None)
    if not url:
        return
    if stash.get(LIVE_SERVER_DRAWN, False):
        terminalreporter.write_line(
            f"live server: {url} (a port drawn by tests/live_server.py, which Chromium accepts)"
        )
    elif int(url.rsplit(":", 1)[1]) in CHROMIUM_UNSAFE_PORTS:
        terminalreporter.write_line(f"live server: {url} — as the address given; Chromium refuses it (ERR_UNSAFE_PORT)")
    else:
        terminalreporter.write_line(f"live server: {url} (as the address given)")
