from contextlib import contextmanager
import socket
from threading import Thread
from time import sleep

import httpx
import uvicorn


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@contextmanager
def run_app_server(app, host: str = "127.0.0.1", port: int | None = None):
    port = port or _free_port()
    config = uvicorn.Config(app=app, host=host, port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = Thread(target=server.run, daemon=True)
    thread.start()

    base_url = f"http://{host}:{port}"
    for _ in range(50):
        try:
            response = httpx.get(f"{base_url}/health", timeout=0.2)
            if response.status_code == 200:
                break
        except Exception:
            sleep(0.1)
    else:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError("server did not start in time")

    try:
        yield base_url
    finally:
        server.should_exit = True
        thread.join(timeout=5)
