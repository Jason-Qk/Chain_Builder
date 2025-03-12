# Designed to run within Maya, this script generates a window that lets users create chain-like objects

import maya.cmds as cmds
import MASH.api as mapi

__WINDOW__ = "chain_builder_UI"

# ============================== FUNCTION LIBRARY ==============================

def update_menu():

    """
    This function keeps the option menu "chain_link_choices" up-to-date
    whilst preserving the current selection
    """

    # Save current selection
    curr_menu_item_index = cmds.optionMenu(chain_link_choices, query = True, select = True)

    # Update option menu
    cmds.optionMenu(chain_link_choices, edit = True, deleteAllItems = True)
    objects = cmds.ls(long=True, type='mesh')
    for obj in objects:
        cmds.menuItem(label = obj, parent = chain_link_choices)
 
    # Only restore current selection if an item was selected and its item index is
    # not out-of-range (can occur if it was the last menu item and has been deleted)
    if curr_menu_item_index > 0 and curr_menu_item_index < len(objects):
        cmds.optionMenu(chain_link_choices, edit = True, select = curr_menu_item_index)

def select_chain_link(*args):

    """
    This function matches the current selection in option menu "chain_link_choices"
    to the actual object in the view panel
    """

    curr_menu_item = cmds.optionMenu(chain_link_choices, query = True, value = True)
    print("Current selection: ", curr_menu_item)
    cmds.select(curr_menu_item)

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
chain_link_choices = cmds.optionMenu("chain_link_choices", label = "Chain Link Object: ",
                                     beforeShowPopup = lambda *args: update_menu(),
                                     alwaysCallChangeCommand = True, changeCommand = select_chain_link)

cmds.setParent(layout_outermost)
cmds.separator(height=10, style = "shelf")

# TODO: Define chain attributes
# - Direction of duplication - x/y/z axis
# - Pattern variation e.g. rotate every 2nd link 90 degrees

# TODO: Generate chain group then merge mesh

# TODO: Curve warp chain group onto a selected curve


# Display window
cmds.showWindow(__WINDOW__)
