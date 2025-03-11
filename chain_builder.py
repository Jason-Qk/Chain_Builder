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

# Construct controls
layout_outermost = cmds.columnLayout("layout_outermost", adjustableColumn = True)

cmds.text("Window Title", font = "boldLabelFont", height = 50) # Title to be replaced by image title

cmds.separator(height=10, style = "shelf")

# Select object to serve as chain link

# cmds.text("Select Chain Link Object: ", font = "boldLabelFont", align = "left", height = 30)
chain_link_choices = cmds.optionMenu(label = "Chain Link Object: ")


# layout_chain_link = cmds.rowLayout("layout_chain_link", numberOfColumns = 2, adjustableColumn = 2)

cmds.setParent(layout_outermost)
cmds.separator(height=10, style = "shelf")

# TODO: Define chain attributes
# - Direction of duplication - x/y/z axis
# - Pattern variation e.g. rotate every 2nd link 90 degrees

# TODO: Generate chain group then merge mesh

# TODO: Curve warp chain group onto a selected curve


# Display window
cmds.showWindow(__WINDOW__)
