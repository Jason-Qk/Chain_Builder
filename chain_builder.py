# Designed to run within Maya, this script generates a window that lets users create chain-like objects

import maya.cmds as cmds
import MASH.api as mapi

__WINDOW__ = "chain_builder_UI"

# ============================== FUNCTION LIBRARY ==============================


# ================================ MAIN PROGRAM ================================

# Close window if currently open including clearing changes to window dimensions
if cmds.window(__WINDOW__, exists = True):
    cmds.deleteUI(__WINDOW__)
    cmds.windowPref(__WINDOW__, remove=True)

# Create window
cmds.window(__WINDOW__, title = "Chain Builder", widthHeight = [500, 300])


# Display window
cmds.showWindow(__WINDOW__)
