# Designed to run within Maya, this script generates a window that lets users create chain-like objects

import maya.cmds as cmds
import MASH.api as mapi

import re

__WINDOW__ = "chain_builder_UI"

# ============================== FUNCTION LIBRARY ==============================

def popup_info(message):

    result = cmds.confirmDialog(
        icon = "information",
        title = "Information",
        message = message,
        button = "OK",
        defaultButton = "OK"
    )

    print(f"Info pop-up response: {result}")

def popup_warn(message):

    result = cmds.confirmDialog(
        icon = "warning",
        title = "Warning",
        message = message,
        button = ["CONTINUE", "STOP"],
        defaultButton = "CONTINUE",
        cancelButton = "STOP"
    )

    print(f"Warning pop-up response: {result}")
    if result == "STOP":
        print("Terminating script")

def popup_error(message):

    result = cmds.confirmDialog(
        icon = "critical",
        title = "Error",
        message = message,
        button = ["OKAY", "HELP"],
        defaultButton = "OKAY"
    )

    print(f"Error pop-up response: {result}")
    if result == "HELP":
        import webbrowser
        webbrowser.open("https://www.linkedin.com/in/jason-js-quek")

# ------------------------------------------------------------------------------

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

def is_float(text):
    
    """
    This function indicates whether "text" is a positive float like "1.00", ".50"    
    """
    
    is_float = False
    if (len(text) > 0) and (re.search(r"(^\d+\.?\d*$)|(^.\d+$)", text) != None):
        is_float = True

    return is_float

def create_chain(*args):

    """
    This function creates a chain based on the attributes defined by the controls
    "num_chain_links", "chain_link_spacing", "chain_orient"
    """

    issues = [] # Record any issues with provided chain attributes

    chain_link = cmds.optionMenu(chain_link_choices, query = True, value = True)
    if chain_link == "(none)":
        issues.append("Chain Link Object - No object selected")

    try:
        cmds.select(chain_link)
    except Exception as error:
        issues.append(f"Chain Link Object - Cannot select object due to {type(error).__name__}: {error}")

    num_links = cmds.textField(num_chain_links, query = True, text = True)
    if (num_links.isdigit() == False) or (num_links.isdigit() == True and int(num_links) <= 0):
        issues.append("Number of Chain Links - Expect a positive integer")
    else:
        num_links == int(num_links)

    link_spacing = cmds.textField(chain_link_spacing, query = True, text = True)
    if (is_float(link_spacing) == False) or (is_float(link_spacing) == True and float(link_spacing) <= 0):
        issues.append("Distance Between Links - Expect a positive number")
    else:
        link_spacing = float(link_spacing)

    chain_orient_select = cmds.radioButtonGrp(chain_orient, query = True, select = True) # Selected radio button
    chain_orient_options = cmds.radioButtonGrp(chain_orient, query = True, labelArray3 = True) # Radio button options
    if chain_orient_select > 0:
        orientation = chain_orient_options[chain_orient_select-1]
    else:
        orientation = None
        issues.append("Chain Orientation - No orientation selected")

    print(f"Chain link obj: {chain_link}, Num. links: {num_links}, link spacing: {link_spacing}, chain orientation = {orientation}")
    if len(issues) != 0:
        error_message = "Cannot create chain due to the following issues:\n" + "\n\n".join(issues)
        popup_error(error_message)

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
chain_link_spacing = cmds.textField("chain_link_spacing", placeholderText = "Positive number")

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
cmds.button(label="Create Chain", width = 250, command = create_chain)
cmds.button(label="Reset", width = 250)







# TODO: Curve warp chain group onto a selected curve


# Display window
cmds.showWindow(__WINDOW__)
