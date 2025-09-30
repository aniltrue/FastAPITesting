import asyncio, websockets

async def main():
    uri = "ws://localhost:8080/ws"  # use wss://your-domain/ws on HTTPS
    async with websockets.connect(uri) as ws:
        await ws.send("hello")
        print(await ws.recv())

asyncio.run(main())
