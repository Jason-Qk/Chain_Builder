# Designed to run within Maya, this script generates a window that lets users create chain-like objects

import maya.cmds as cmds
import MASH.api as mapi

__WINDOW__ = "chain_builder_UI"

# ============================== FUNCTION LIBRARY ==============================

def select_chain_link(*args):

    # This function lets you select the chain link object from the "chain_link_choices" option menu

    print(chain_link_choices)

    # Save current selection before updating option menu list
    curr_select = cmds.optionMenu(chain_link_choices, query = True, select = True)
    print("curr select: ", curr_select)
    cmds.optionMenu(chain_link_choices, edit = True, deleteAllItems = True)

    objects = cmds.ls(long=True, type='mesh')
    for obj in objects:
        cmds.menuItem(label = obj, parent = chain_link_choices)

    # TODO: After list update, check whether current selection still exists
    # - if it does, restore the selection in the menu and in Maya GUI (cmds.select())

    cmds.optionMenu(chain_link_choices, edit = True, select = curr_select)

    # - Otherwise, indicate that selection cannot be found before defaulting to another item

    # print(item)

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
chain_link_choices = cmds.optionMenu("chain_link_choices", label = "Chain Link Object: ", alwaysCallChangeCommand = True, changeCommand = select_chain_link)
objects = cmds.ls(long=True, type='mesh')

for obj in objects:
    cmds.menuItem(label = obj, parent = chain_link_choices)

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
