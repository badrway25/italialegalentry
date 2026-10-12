"""
A minimal, synchronous Chrome DevTools Protocol client over a raw WebSocket — standard library only.

Why this exists, when the project already drives Chrome with Playwright
-----------------------------------------------------------------------
`connect_over_cdp` attaches to the BROWSER endpoint and then enumerates and attaches to every
target in the window. That is the right thing for a browser Playwright owns, and the wrong thing
for the shared, visible Chrome the QA scripts are required to use: on 24 September 2026 that window
also held a sign-in page with four hCaptcha iframes, and the attach stopped returning. Ninety
seconds of timeout, every time, on a browser whose HTTP endpoint answered instantly and whose
websocket completed its handshake in milliseconds — measured, both of them, before writing a line
of this file.

This client opens ONE websocket, to ONE page target, and never asks the browser about any other.
Nothing in an unrelated tab can hold it up, and it cannot disturb an unrelated tab either.

It implements exactly as much of RFC 6455 as CDP needs: masked client frames, the three payload
length forms, continuation frames (a `Runtime.evaluate` returning a page of HTML arrives
fragmented), and a pong for every ping. No compression is negotiated, so no permessage-deflate.

    from cdp import Page
    with Page.attach(url_contains="_design") as page:
        page.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
        page.reload()
        print(page.evaluate("document.title"))

`Page.attach` picks the first page target whose URL contains the given string, so a QA script names
the page it means instead of trusting tab order.
"""

from __future__ import annotations

import base64
import contextlib
import json
import os
import socket
import struct
import time
import urllib.request
from contextlib import contextmanager
from typing import Any
from urllib.parse import urlparse

DEVTOOLS = "http://127.0.0.1:9222"


class CDPError(RuntimeError):
    pass


class WebSocket:
    """Client side of RFC 6455, only as far as CDP requires."""

    def __init__(self, url: str, timeout: float = 30.0):
        parsed = urlparse(url)
        self.sock = socket.create_connection((parsed.hostname, parsed.port or 80), timeout=timeout)
        self.sock.settimeout(timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(request.encode())
        head = self._read_until(b"\r\n\r\n")
        if b"101" not in head.split(b"\r\n", 1)[0]:
            raise CDPError(f"upgrade rifiutato: {head.split(b'\r\n', 1)[0]!r}")
        self._buf = b""

    def _read_until(self, marker: bytes) -> bytes:
        data = b""
        while marker not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise CDPError("connessione chiusa durante l'handshake")
            data += chunk
        return data

    def _recv_exactly(self, n: int) -> bytes:
        while len(self._buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise CDPError("connessione chiusa dal browser")
            self._buf += chunk
        out, self._buf = self._buf[:n], self._buf[n:]
        return out

    def send(self, text: str) -> None:
        payload = text.encode()
        header = bytearray([0x81])  # FIN + text
        mask = os.urandom(4)
        length = len(payload)
        if length < 126:
            header.append(0x80 | length)
        elif length < (1 << 16):
            header.append(0x80 | 126)
            header += struct.pack(">H", length)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", length)
        header += mask
        masked = bytes(byte ^ mask[i % 4] for i, byte in enumerate(payload))
        self.sock.sendall(bytes(header) + masked)

    def recv(self) -> str:
        """One complete message, reassembling continuation frames and answering pings."""
        message = b""
        while True:
            first, second = self._recv_exactly(2)
            fin, opcode = first & 0x80, first & 0x0F
            length = second & 0x7F
            if length == 126:
                (length,) = struct.unpack(">H", self._recv_exactly(2))
            elif length == 127:
                (length,) = struct.unpack(">Q", self._recv_exactly(8))
            # The server never masks; if it did, the mask key would sit here.
            payload = self._recv_exactly(length) if length else b""
            if opcode == 0x9:  # ping -> pong, same payload, masked like any client frame
                self._control(0x8A, payload)
                continue
            if opcode == 0x8:  # close
                raise CDPError("il browser ha chiuso la connessione")
            if opcode == 0xA:  # pong, nothing to do
                continue
            message += payload
            if fin:
                return message.decode("utf-8", "replace")

    def _control(self, opcode: int, payload: bytes) -> None:
        mask = os.urandom(4)
        masked = bytes(byte ^ mask[i % 4] for i, byte in enumerate(payload))
        self.sock.sendall(bytes([opcode, 0x80 | len(payload)]) + mask + masked)

    def close(self) -> None:
        # A close frame is a courtesy; if the socket is already gone the courtesy is moot and the
        # only thing that matters is that the file descriptor is released.
        with contextlib.suppress(OSError):
            self._control(0x88, b"")
        self.sock.close()


class Page:
    def __init__(self, ws: WebSocket, target: dict):
        self.ws = ws
        self.target = target
        self._id = 0

    # -- attach ------------------------------------------------------------------

    @staticmethod
    def targets() -> list[dict]:
        # noqa S310: the scheme is not user input — DEVTOOLS is the loopback DevTools endpoint,
        # a module constant, and the only thing interpolated is a fixed path.
        with urllib.request.urlopen(f"{DEVTOOLS}/json/list", timeout=5) as response:  # noqa: S310
            return json.load(response)

    @classmethod
    @contextmanager
    def attach(cls, url_contains: str = "", timeout: float = 30.0):
        pages = [t for t in cls.targets() if t.get("type") == "page" and url_contains in t.get("url", "")]
        if not pages:
            raise CDPError(f"nessuna scheda il cui URL contenga {url_contains!r}")
        target = pages[0]
        ws = WebSocket(target["webSocketDebuggerUrl"], timeout=timeout)
        page = cls(ws, target)
        try:
            page.send("Page.enable")
            page.send("Runtime.enable")
            yield page
        finally:
            ws.close()

    # -- protocol ----------------------------------------------------------------

    def send(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        message_id = self._id
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") != message_id:
                continue  # an event, or an answer we are no longer waiting for
            if "error" in message:
                raise CDPError(f"{method}: {message['error'].get('message')}")
            return message.get("result", {})

    # -- the four things a QA script needs ---------------------------------------

    def evaluate(self, expression: str, await_promise: bool = True) -> Any:
        result = self.send(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": await_promise,
                "userGesture": True,
            },
        )
        if result.get("exceptionDetails"):
            detail = result["exceptionDetails"]
            text = detail.get("exception", {}).get("description") or detail.get("text")
            raise CDPError(f"eccezione nella pagina: {text}")
        return result.get("result", {}).get("value")

    def navigate(self, url: str, settle: float = 1.0) -> None:
        self.send("Page.navigate", {"url": url})
        self._wait_for_load(settle)

    def reload(self, settle: float = 1.0) -> None:
        self.send("Page.reload", {"ignoreCache": True})
        self._wait_for_load(settle)

    def _wait_for_load(self, settle: float) -> None:
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            try:
                if self.evaluate("document.readyState") == "complete":
                    break
            except CDPError:
                pass  # the context is being replaced by the navigation
            time.sleep(0.15)
        time.sleep(settle)

    def emulate(self, *, reduced_motion: str | None = None, forced_colors: str | None = None) -> None:
        """
        Set, or clear, the two preferences this project has to test under.

        Passing None for both clears every emulated feature — which is what a QA script must do
        before it detaches, because a Chrome window left in high contrast is a trap for whoever
        looks at it next and they will not connect it to a script that already exited.
        """
        features = []
        if reduced_motion:
            features.append({"name": "prefers-reduced-motion", "value": reduced_motion})
        if forced_colors:
            features.append({"name": "forced-colors", "value": forced_colors})
        self.send("Emulation.setEmulatedMedia", {"features": features})

    def viewport(self, width: int, height: int, scale: float = 1.0) -> None:
        """
        Resize the CSS viewport without touching the window.

        This is how a zoom level is tested honestly. `document.body.style.zoom` scales the page
        but leaves the viewport the size it was, so a layout that would reflow at 200% keeps its
        desktop columns and the test passes when the user's screen would not. Reducing the CSS
        viewport by the zoom factor is what the browser actually does: 400% of a 1280px window is
        a 320px viewport.
        """
        self.send(
            "Emulation.setDeviceMetricsOverride",
            {"width": width, "height": height, "deviceScaleFactor": scale, "mobile": False},
        )

    def viewport_reset(self) -> None:
        self.send("Emulation.clearDeviceMetricsOverride")

    def screenshot(self, path: str) -> str:
        data = self.send("Page.captureScreenshot", {"format": "png"})["data"]
        target = os.path.abspath(path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as handle:
            handle.write(base64.b64decode(data))
        return target


if __name__ == "__main__":
    import sys

    # The Windows console is cp1252 and this project's output is full of « » and accents; without
    # this line the script dies on its own report rather than on anything it measured.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    wanted = sys.argv[1] if len(sys.argv) > 1 else ""
    with Page.attach(url_contains=wanted) as page:
        print(json.dumps({"url": page.target.get("url"), "title": page.evaluate("document.title")}, ensure_ascii=False))
