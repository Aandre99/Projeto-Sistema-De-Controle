from queue import Queue
from math import isnan
import websockets
import threading
import asyncio
import time
import sys
import os


from PyQt6.QtWidgets import QApplication
from app_interface import JanelaApp

ref_buffer = Queue(maxsize=100)


async def serverLoop(self, websocket, path):

    while True:
        try:
            startTime = time.time()
            await asyncio.sleep(0.1)
            print("get references") if self.verbose else None
            await websocket.send("get references")
            received = (await websocket.recv()).split(",")
            print(received) if self.verbose else None
            ref = float(received[1])

            if isnan(ref):
                ref = 0.0

            print("get outputs") if self.verbose else None
            await websocket.send("get outputs")
            received = (await websocket.recv()).split(",")
            print(received) if self.verbose else None
            out = float(received[1])
            u = 5
            print(f"u = {u}") if self.verbose else None
            await websocket.send("set input|" + f"{u}")
            ellapsedTime = 0.0
            while ellapsedTime < self.controller.T:
                time.sleep(0.0001)
                endTime = time.time()
                ellapsedTime = endTime - startTime

            print(
                "%.4f %.4f %.4f %.4f %.4f, (%.4f)"
                % (self.controller.time, ref, out, u, self.controller.T, ellapsedTime)
            )
        except:
            print("System not active...") if self.verbose else None


def gui():

    gui = QApplication(sys.argv)
    window = JanelaApp(ref_buffer)
    window.show()
    gui.exec()


server = websockets.serve(serverLoop, "localhost", 6660)
asyncio.get_event_loop().run_until_complete(server)
y = threading.Thread(target=gui)
y.start()

asyncio.get_event_loop().run_forever()
y.join()
