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
        button = "OK",
        defaultButton = "OK"
    )

    print(f"Warning pop-up response: {result}")

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

def update_curr_chain_link(*args):

    """
    Update the "curr_chain_link" text field's content to display the name
    of the currently selected object
    """
    selected_objs = cmds.ls(orderedSelection = True)

    # If multiple objects are selected, default to the first object selected
    if len(selected_objs) == 0:
        popup_warn(f"Please select an object")

    else:

        if len(selected_objs) > 1:
            popup_warn(f"Multiple objects selected, defaulting to first object {selected_objs[0]}")

        cmds.textField(curr_chain_link, edit = True, text = selected_objs[0])

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

def valid_chain_attrs():

    """
    This function checks the validity of the chain attributes defined by the controls
    "num_chain_links", "chain_link_spacing", "chain_orient"
    """

    chain_link = cmds.textField(curr_chain_link, query = True, text = True)
    issues = [] # Record any issues with provided chain attributes

    # Check if a chain link object has been selected and still exists
    if len(chain_link) == 0:
        issues.append("Chain Link Object - No object selected")
    else:
        try:
            cmds.select(chain_link)
        except Exception as error:
            issues.append(f"Chain Link Object - Cannot select object due to {type(error).__name__}: {error}")

    # Check whether the number of chain links is a positive integer
    num_links = cmds.textField(num_chain_links, query = True, text = True)
    if (num_links.isdigit() == False) or (num_links.isdigit() == True and int(num_links) <= 0):
        issues.append("Number of Chain Links - Expect a positive integer")

    # Check whether the chain link spacing (i.e. distance between consecutive chain links) is a positive number
    link_spacing = cmds.textField(chain_link_spacing, query = True, text = True)
    if (is_float(link_spacing) == False) or (is_float(link_spacing) == True and float(link_spacing) <= 0):
        issues.append("Distance Between Links - Expect a positive number")

    # Check whether a chain link orientation has been selected
    chain_orient_select = cmds.radioButtonGrp(chain_orient, query = True, select = True) # Selected radio button
    if not chain_orient_select > 0:
        issues.append("Chain Orientation - No orientation selected")

    if len(issues) != 0:
        issues = "\n\n".join(issues)
        popup_error(f"Cannot create chain due to the following issue(s):\n\n{issues}")
        return False

    return True

def create_chain(*args):

    """
    This function creates a chain based on the attributes defined by the controls
    "num_chain_links", "chain_link_spacing", "chain_orient"
    """

    if valid_chain_attrs():

        # Retrieve chain attributes

        chain_link = cmds.textField(curr_chain_link, query = True, text = True)

        if cmds.ls(chain_link, long = True, shapes = True):
            chain_link_transform = cmds.listRelatives(chain_link, parent=True, fullPath = True)[0]
        elif cmds.ls(chain_link, long = True, transforms = True):
            chain_link_transform = chain_link

        num_links = int(cmds.textField(num_chain_links, query = True, text = True))

        link_spacing = float(cmds.textField(chain_link_spacing, query = True, text = True))

        chain_orient_select = cmds.radioButtonGrp(chain_orient, query = True, select = True) # Selected radio button
        chain_orient_options = cmds.radioButtonGrp(chain_orient, query = True, labelArray3 = True) # Radio button options
        orientation = chain_orient_options[chain_orient_select-1]

        # Create more chain links then add them to the chain group
        all_chain_links = [chain_link_transform]
        cmds.makeIdentity(chain_link_transform, apply = True)
        for link_num in range(num_links-1):

            if link_num == 0:
                link_inst = cmds.instance(chain_link)[0]
                if orientation == "X-axis":
                    cmds.move(link_spacing, moveX = True, relative = True)

                elif orientation == "Y-axis":
                    cmds.move(link_spacing, moveY = True, relative = True)

                elif orientation == "Z-axis":
                    cmds.move(link_spacing, moveZ = True, relative = True)

            else:
                link_inst = cmds.instance(smartTransform = True)[0]

            print(f"Chain link obj {link_num} created: {link_inst}")
            all_chain_links.append(link_inst)

        # Group all chain links together
        chain_links = cmds.group(name = "chain_links", empty = True)
        for link in all_chain_links:
            cmds.parent(link, chain_links)

        # Merge chain links together to create a single chain object
        chain = cmds.polyUnite(chain_links, centerPivot = True, mergeUVSets = 1)
        chain_obj = cmds.rename(chain[0], "chain") # Rename object node
        polyUnite_chain = cmds.rename(chain[1], "polyUnite_chain") # Rename PolyUnite node

        chain_group = cmds.group(chain_links, chain_obj, name = "chain_group")
        popup_info(f"Creating group '{chain_group}' containing link group '{chain_links}' & chain object '{chain_obj}'")

def chain_builder_ui():

    # Close window if currently open and clear any prior changes to window dimensions
    if cmds.window(__WINDOW__, exists = True):
        cmds.deleteUI(__WINDOW__)
        cmds.windowPref(__WINDOW__, remove=True)

    # Create window
    cmds.window(__WINDOW__, title = "Chain Builder", widthHeight = [500, 300])

    # Construct controls
    layout_outermost = cmds.columnLayout("layout_outermost", adjustableColumn = True)

    cmds.text("Chain Builder", font = "boldLabelFont", height = 50)

    cmds.separator(height=10, style = "shelf")

    # Control to select the chain link object
    global chain_link_choices
    
    layout_select_chain_obj = cmds.rowLayout("layout_select_chain_obj", numberOfColumns = 3, adjustableColumn = 2)
    cmds.text("Chain Link Object: ", font = "boldLabelFont", align = "left")

    global curr_chain_link
    curr_chain_link = cmds.textField("curr_chain_link", editable = False, placeholderText = "Select an object")
    cmds.button(label="Update selection", command = update_curr_chain_link)

    cmds.setParent(layout_outermost)
    cmds.separator(height=10, style = "shelf")

    # Specify the number of links the chain should have 
    layout_num_chain_links = cmds.rowLayout("layout_num_chain_links", numberOfColumns = 2, adjustableColumn = 2)
    cmds.text("Number of Chain Links:", font = "boldLabelFont", align = "left")
    global num_chain_links
    num_chain_links = cmds.textField("num_chain_links", placeholderText = "Positive integer (e.g. 1, 10)")

    cmds.setParent(layout_outermost)

    # Specify chain link spacing i.e. the distance between consecutive chain links
    layout_link_spacing = cmds.rowLayout("layout_link_spacing", numberOfColumns = 2, adjustableColumn = 2)
    cmds.text("Distance Between Links:", font = "boldLabelFont", align = "left")
    global chain_link_spacing
    chain_link_spacing = cmds.textField("chain_link_spacing", placeholderText = "Positive number (e.g. 0.5, 1)")

    cmds.setParent(layout_outermost)

    # Specify the direction of chain link generation
    layout_chain_orient = cmds.rowLayout("layout_chain_orient", numberOfColumns = 4)
    cmds.text("Chain Orientation:", font = "boldLabelFont", align = "left")
    global chain_orient
    chain_orient = cmds.radioButtonGrp("chain_orient", numberOfRadioButtons = 3, 
                                    labelArray3=["X-axis", "Y-axis", "Z-axis"],
                                    columnWidth3 = [60, 60, 60])

    # Click button to create the chain with the specified attributes
    cmds.setParent(layout_outermost)
    cmds.separator(height=10, style = "shelf")
    cmds.button(label="Create Chain", width = 500, command = create_chain)

    # Display window
    cmds.showWindow(__WINDOW__)

# ================================ MAIN PROGRAM ================================

chain_builder_ui()