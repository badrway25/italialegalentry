"""
The browser tests' live server and its port (tests/live_server.py).

pytest-django let the operating system choose the port, and this workstation's dynamic TCP range starts at 1024, among
the ports Chromium refuses before it connects (net::ERR_UNSAFE_PORT): the steward's W3-A run drew 4045. The port is now
drawn in LIVE_SERVER_PORTS, above every port a browser refuses, and bound — a taken port is skipped for the next draw,
so lanes running browser tests at once never share one; an address that names its port is honoured exactly.
"""

from __future__ import annotations

import os
import random
import socket
import urllib.request
from types import SimpleNamespace

import pytest
from django.contrib.staticfiles.handlers import StaticFilesHandler

from tests import live_server as plumbing


def _thread(**kwargs) -> plumbing.ChromiumSafeLiveServerThread:
    return plumbing.ChromiumSafeLiveServerThread("localhost", StaticFilesHandler, connections_override={}, **kwargs)


def _hold_a_port() -> socket.socket:
    """A socket bound to a port of LIVE_SERVER_PORTS on the live server's address, as another lane's server would be."""
    for port in plumbing.candidate_ports():
        held = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            held.bind(("127.0.0.1", port))
        except OSError:
            held.close()
            continue
        held.listen()
        return held
    raise AssertionError("no port of LIVE_SERVER_PORTS could be bound")


def test_every_draw_is_a_port_chromium_accepts():
    rng = random.Random(4045)
    for _ in range(500):
        ports = plumbing.candidate_ports(rng=rng)
        assert len(set(ports)) == len(ports) == plumbing.ATTEMPTS
        assert all(port in plumbing.LIVE_SERVER_PORTS for port in ports)
        assert not set(ports) & plumbing.CHROMIUM_UNSAFE_PORTS
    assert min(plumbing.LIVE_SERVER_PORTS) > max(plumbing.CHROMIUM_UNSAFE_PORTS), "the range must clear every refusal"
    assert max(plumbing.LIVE_SERVER_PORTS) < 32768, "the range must stay below the default dynamic ranges"
    assert 4045 in plumbing.CHROMIUM_UNSAFE_PORTS  # the port the W3-A run drew


def test_a_taken_port_is_skipped_for_the_next_draw(monkeypatch):
    taken, free = _hold_a_port(), _hold_a_port()
    free_port = free.getsockname()[1]
    free.close()
    try:
        monkeypatch.setattr(plumbing, "candidate_ports", lambda: [taken.getsockname()[1], free_port])
        thread = _thread()
        server = thread._create_server()
        try:
            assert thread.port == free_port == server.server_address[1]
        finally:
            server.server_close()
    finally:
        taken.close()


def test_every_draw_taken_is_an_error_not_a_shared_port(monkeypatch):
    taken = _hold_a_port()
    try:
        monkeypatch.setattr(plumbing, "candidate_ports", lambda: [taken.getsockname()[1]])
        thread = _thread()
        with pytest.raises(OSError):
            thread._create_server()
        assert thread.port == 0
    finally:
        taken.close()


def test_a_port_named_in_the_address_is_honoured_exactly(monkeypatch):
    held = _hold_a_port()
    port = held.getsockname()[1]
    held.close()
    monkeypatch.setattr(plumbing, "candidate_ports", lambda: pytest.fail("a named port is never drawn"))
    thread = _thread(port=port)
    server = thread._create_server()
    try:
        assert thread.port == port == server.server_address[1]
    finally:
        server.server_close()


def _wsgi_server(port: int):
    """The server the design preview's ``_runserver`` builds (Django's WSGIServer), without SO_REUSEADDR."""
    from django.core.servers.basehttp import WSGIRequestHandler, WSGIServer

    return WSGIServer(("127.0.0.1", port), WSGIRequestHandler, allow_reuse_address=False)


def test_a_server_built_outside_live_server_binds_a_port_chromium_accepts():
    """REVIEW_2 m4: the helper the design preview's ``_runserver`` can call instead of binding port 0."""
    server = plumbing.bind_a_port_chromium_accepts(_wsgi_server)
    try:
        port = server.server_address[1]
        assert port in plumbing.LIVE_SERVER_PORTS and port not in plumbing.CHROMIUM_UNSAFE_PORTS
    finally:
        server.server_close()


def test_the_helper_skips_a_taken_port_and_never_shares_one(monkeypatch):
    taken, free = _hold_a_port(), _hold_a_port()
    taken_port, free_port = taken.getsockname()[1], free.getsockname()[1]
    free.close()
    try:
        monkeypatch.setattr(plumbing, "candidate_ports", lambda: [taken_port, free_port])
        server = plumbing.bind_a_port_chromium_accepts(_wsgi_server)
        try:
            assert server.server_address[1] == free_port
        finally:
            server.server_close()
        monkeypatch.setattr(plumbing, "candidate_ports", lambda: [taken_port])
        with pytest.raises(OSError):
            plumbing.bind_a_port_chromium_accepts(_wsgi_server)
    finally:
        taken.close()


def test_the_summary_line_says_where_the_live_server_listened():
    class Reporter:
        def __init__(self):
            self.config, self.lines = SimpleNamespace(stash=pytest.Stash()), []

        def write_line(self, line):
            self.lines.append(line)

    def summary(url=None, drawn=None) -> list[str]:
        reporter = Reporter()
        if url:
            reporter.config.stash[plumbing.LIVE_SERVER_URL] = url
            reporter.config.stash[plumbing.LIVE_SERVER_DRAWN] = drawn
        plumbing.pytest_terminal_summary(reporter)
        return reporter.lines

    assert summary() == [], "no live server, no line"
    assert "drawn" in summary("http://localhost:23026", drawn=True)[0]
    assert "ERR_UNSAFE_PORT" in summary("http://localhost:4045", drawn=False)[0]
    assert summary("http://localhost:8789", drawn=False) == [
        "live server: http://localhost:8789 (as the address given)"
    ]


def test_the_live_server_fixture_listens_on_a_drawn_port(request, live_server):
    if request.config.getvalue("liveserver") or os.getenv("DJANGO_LIVE_TEST_SERVER_ADDRESS"):
        pytest.skip("an address was given: the live server listens where it says")
    port = int(live_server.url.rsplit(":", 1)[1])
    assert port in plumbing.LIVE_SERVER_PORTS and port not in plumbing.CHROMIUM_UNSAFE_PORTS
    assert request.config.stash[plumbing.LIVE_SERVER_URL] == live_server.url
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(f"{live_server.url}/healthz/", timeout=30) as response:
        assert response.status == 200


@pytest.mark.browser
def test_chromium_opens_the_drawn_port_and_refuses_the_one_the_w3a_run_drew(live_server, monkeypatch):
    playwright = pytest.importorskip("playwright.sync_api")
    monkeypatch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")  # Playwright's sync API runs an event loop in this thread
    with playwright.sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            assert page.goto(f"{live_server.url}/healthz/").status == 200
            with pytest.raises(playwright.Error, match="ERR_UNSAFE_PORT"):
                page.goto("http://localhost:4045/")
        finally:
            browser.close()
