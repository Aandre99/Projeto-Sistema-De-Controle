import asyncio
import websockets
from collections import deque
from math import *
import numpy as np
import time
from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool

class RemoteControl(QRunnable):

    T = 0.01
    time1 = 0
    
    def __init__(self, dynamicplotter, verbose = False):
        super().__init__()
        self.verbose = verbose
        self.dynamicplotter = dynamicplotter
        
    async def serverLoop(self, websocket, path):
        
        while True:
            startTime = time.time()

            await websocket.send('set input|'+f"{float(self.dynamicplotter.get_ref_value())}")
            await asyncio.sleep(self.T)

            self.time1 += self.T

            #try:

            #await websocket.send('set input|'+f"{float(self.dynamicplotter.get_ref_value())}")

            # print('get references') if self.verbose else None
            references = []
            await websocket.send('get references')
            received = (await websocket.recv()).split(',')
            # print(received) if self.verbose else None
            ref = float(received[1])

            if isnan(ref):
                ref = 0.0


            # print('get outputs') if self.verbose else None
            outputs = []
            await websocket.send('get outputs')
            received = (await websocket.recv()).split(',')
            # print(received) if self.verbose else None
            out1 = float(received[1])
            out2 = float(received[2])

            #self.dynamicplotter.updateplot_communication(ref,out1,out2,time)
            # print(f'u = {u}') if self.verbose else None
            #await websocket.send('set input|'+f"{self.dynamicplotter.get_ref_value()}")
            ellapsedTime = 0.0

            while ellapsedTime < self.T:
                time.sleep(0.0001)
                endTime = time.time()
                ellapsedTime = endTime - startTime

            self.dynamicplotter.updateplot_communication(ref,out1,out2,self.time1)

            # print('%.4f %.4f %.4f %.4f %.4f, (%.4f)'%(self.controller.time, ref, out, u, self.controller.T, ellapsedTime))				


            #except Exception as e:
            #    print(e)
            #    print('System not active...') if self.verbose else None
            #    break

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