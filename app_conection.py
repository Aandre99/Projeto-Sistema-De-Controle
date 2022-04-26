import websockets
import threading
from queue import Queue
import os

ref_buffer = Queue(maxsize=100)
out1_buffer = Queue(maxsize=100)
out2_buffer = Queue(maxsize=100)
input_buffer = Queue(maxsize=100)

