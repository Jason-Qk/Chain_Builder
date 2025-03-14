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

    if len(objects) > 0:

        for obj in objects:
            cmds.menuItem(label = obj, parent = chain_link_choices)
    
        # Only restore current selection if an item was selected and its item index is
        # not out-of-range (can occur if it was the last menu item and has been deleted)
        if curr_menu_item_index > 0 and curr_menu_item_index < len(objects):
            cmds.optionMenu(chain_link_choices, edit = True, select = curr_menu_item_index)

    else:
        
        cmds.menuItem(label = "(none)", parent = chain_link_choices)

def select_chain_link(*args):

    """
    This function matches the current selection in option menu "chain_link_choices"
    to the actual object in the view panel
    """

    curr_menu_item = cmds.optionMenu(chain_link_choices, query = True, value = True)
    if curr_menu_item != "(none)":
        cmds.select(curr_menu_item)

# ================================ MAIN PROGRAM ================================

# Close window if currently open
if cmds.window(__WINDOW__, exists = True):
    cmds.deleteUI(__WINDOW__)

# Create window and clear any prior changes to window dimensions
cmds.window(__WINDOW__, title = "Chain Builder", widthHeight = [500, 300])
cmds.windowPref(__WINDOW__, remove=True)

# Construct controls
layout_outermost = cmds.columnLayout("layout_outermost", adjustableColumn = True)

cmds.text("Window Title", font = "boldLabelFont", height = 50) # Title to be replaced by image title

cmds.separator(height=10, style = "shelf")

# Select object to serve as chain link
chain_link_choices = cmds.optionMenu("chain_link_choices", label = "Chain Link Object: ",
                                     beforeShowPopup = lambda *args: update_menu(),
                                     alwaysCallChangeCommand = True, changeCommand = select_chain_link)
update_menu()

cmds.separator(height=10, style = "shelf")

# TODO: Define chain attributes
# - Total number of Links
# - Distance between links
# - Direction of duplication - x/y/z axis
# - Pattern variation e.g. rotate every 2nd link 90 degrees
layout_num_chain_links = cmds.rowLayout("layout_num_chain_links", numberOfColumns = 2, adjustableColumn = 2)
cmds.text("Number of Chain Links:", font = "boldLabelFont", align = "left")
num_chain_links = cmds.textField("num_chain_links", placeholderText = "Positive Integer")

cmds.setParent(layout_outermost)

layout_link_spacing = cmds.rowLayout("layout_link_spacing", numberOfColumns = 2, adjustableColumn = 2)
cmds.text("Distance Between Links:", font = "boldLabelFont", align = "left")
num_chain_links = cmds.textField("num_chain_links", placeholderText = "Positive Float")

cmds.setParent(layout_outermost)

layout_chain_orient = cmds.rowLayout("layout_chain_orient", numberOfColumns = 4)
cmds.text("Chain Orientation:", font = "boldLabelFont", align = "left")
chain_orient = cmds.radioButtonGrp("chain_orient", numberOfRadioButtons = 3, 
                                   labelArray3=["X-axis", "Y-axis", "Z-axis"],
                                   columnWidth3 = [60, 60, 60])



# TODO: Generate chain group then merge mesh
cmds.setParent(layout_outermost)
cmds.separator(height=10, style = "shelf")

layout_create_chain = cmds.rowLayout("layout_create_chain", numberOfColumns = 2)
cmds.button(label="Create Chain", width = 250)
cmds.button(label="Reset", width = 250)







# TODO: Curve warp chain group onto a selected curve


# Display window
cmds.showWindow(__WINDOW__)
