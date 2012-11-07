import os
import sys

muxpy_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, muxpy_dir)

from muxpy import main
main.run()
