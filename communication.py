import asyncio
import websockets
from collections import deque
from math import *
import numpy as np
import time
from websocketcontrol.controlers import *

from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool


class RemoteControl(QRunnable):

    T = 0.01
    time1 = 0

    def __init__(self, dynamicplotter, verbose=False):
        super().__init__()

        self.verbose = verbose
        self.dynamicplotter = dynamicplotter
        self.controllers = {
            "P": P(self.T),
            "PI": PI(self.T),
            "PD": PD(self.T),
            "PID": PID(self.T),
            "PI-D": PI_D(self.T),
            "I-PD": I_PD(self.T),
        }

    async def serverLoop(self, websocket, path):

        while True:

            # try:

            startTime = time.time()
            self.time1 += self.T

            await websocket.send("get references")
            received = (await websocket.recv()).split(",")
            ref = float(received[1])

            if isnan(ref):
                ref = 0.0

            await websocket.send("get outputs")
            received = (await websocket.recv()).split(",")

            out1 = float(received[2])
            out2 = float(received[1])

            current_output_block = self.dynamicplotter.saida
            outC = out1 if current_output_block == "Vermelho" else out2

            await websocket.send(
                "set input|"
                + f"{float(self.dynamicplotter.get_ref_value(outC, self.controllers))}"
            )
            await asyncio.sleep(self.T)

            ellapsedTime = 0.0
            while ellapsedTime < self.T:
                time.sleep(0.0001)
                endTime = time.time()
                ellapsedTime = endTime - startTime

            self.dynamicplotter.updateplot_communication(out1, out2, self.time1)

        # except Exception as e:
        #     print(e)
        #     print("System not active...") if self.verbose else None
        #     break

    @pyqtSlot()
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = websockets.serve(self.serverLoop, "localhost", 6660)
        asyncio.ensure_future(server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    server = RemoteControl(verbose=True)
    server.run()
