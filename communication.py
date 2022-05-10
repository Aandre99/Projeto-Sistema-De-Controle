import asyncio
import websockets
from collections import deque
from math import *
import numpy as np
import time
from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool

class RemoteControl(QRunnable):

    T = 0.01
    time = 0
    
    def __init__(self, verbose = False):
        super().__init__()
        self.verbose = verbose
        
    async def serverLoop(self, websocket, path):
        
        while True:
            startTime = time.time()

            await asyncio.sleep(self.T)

            self.time += self.T

            try:
                print('get references') if self.verbose else None
                references = []
                await websocket.send('get references')
                received = (await websocket.recv()).split(',')
                print(received) if self.verbose else None
                ref = float(received[1])

                if isnan(ref):
                    ref = 0.0


                print('get outputs') if self.verbose else None
                outputs = []
                await websocket.send('get outputs')
                received = (await websocket.recv()).split(',')
                print(received) if self.verbose else None
                out = float(received[1])
				
				# print(f'u = {u}') if self.verbose else None
				# await websocket.send('set input|'+f"{u}")
                # 
                ellapsedTime = 0.0

                while ellapsedTime < self.T:
                    time.sleep(0.0001)
                    endTime = time.time()
                    ellapsedTime = endTime - startTime


				# print('%.4f %.4f %.4f %.4f %.4f, (%.4f)'%(self.controller.time, ref, out, u, self.controller.T, ellapsedTime))				


            except Exception as e:
                print(e)
                print('System not active...') if self.verbose else None
                break

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