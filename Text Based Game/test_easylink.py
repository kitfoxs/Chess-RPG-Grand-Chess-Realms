import sys
import os

# Add the build directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'build'))

import easylink

# Create an instance of ChessLink using the from_hid_connect method
chess_link = easylink.ChessLink.from_hid_connect()

# Connect to the device
chess_link.connect()

# Disconnect from the device
chess_link.disconnect()
