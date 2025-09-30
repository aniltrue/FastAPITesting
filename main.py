import pathlib

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
import time

from fastapi.staticfiles import StaticFiles

app = FastAPI()
static_dir = pathlib.Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def root():
    return {"message": "Hello from FastAPI behind IIS/ARR!"}

@app.get("/health")
def health():
    return {"status": "ok", "ts": time.time()}

@app.get("/ws_test.html", response_class=HTMLResponse)
def websocket_test_page():
    html_path = static_dir / "ws_test.html"
    return html_path.read_text(encoding="utf-8")

# ---- WebSocket echo endpoint ----
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        # initial hello so we can see that upgrade worked
        await ws.send_text("connected")
        # simple ping loop on the side (optional)
        async def pinger():
            while True:
                await asyncio.sleep(15)
                try:
                    await ws.send_text("ping")
                except Exception:
                    break

        ping_task = asyncio.create_task(pinger())

        # echo loop
        while True:
            msg = await ws.receive_text()
            if msg.lower() in {"quit", "close", "exit"}:
                await ws.send_text("bye")
                await ws.close()
                break
            await ws.send_text(f"echo: {msg}")
    except WebSocketDisconnect:
        pass
    finally:
        # ensure background task is cancelled
        for t in asyncio.all_tasks():
            # cancel only our ping task
            if t is not asyncio.current_task() and t.get_coro().__name__ == "pinger":
                t.cancel()
