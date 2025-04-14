# Chain Builder

This tool provides Autodesk Maya users a GUI to create a chain object. A chain object consists of a single object with naming convention `chain<num>` and a group with naming convention `chain_group<num>`.

## Script Setup

Upon downloading the script, you have 2 options for running the script:
1. Open the script directly within Maya's Script Editor, selecting all its contents, then running it through CTRL + Enter or similar
2. Create a userSetup.py in your Maya's user script folder/directory 
    - To ascertain the user script folder/directory see your Maya version's documentation on "Initializing the Maya Python environment" e.g. https://help.autodesk.com/view/MAYAUL/2023/ENU/?guid=GUID-640C1383-3FB8-410F-AE18-987A812B5914

## User Workflow

1. Run the `chain_builder.py` script.
2. Select the chain link object via the "Chain Link Object" dropdown menu.
3. Specify the number of links you want your chain to have in the "Number of Chain Links" field.
4. Specify the distance between consecutive links in the "Distance Between Links" field.
5. Select the direction of chain link generation by clicking one of the "Chain Orientation" radio buttons.
6. Click the "Create Chain" button to confirm your chain attributes, prompting the tool to check whether the following conditions are met:
    - "Chain Link Object" - Specified chain link object still exists
    - "Number of Chain Links" - A positive integer (whole number) is provided
    - "Distance Between Links" - A positive number is provided
    - "Chain Orientation" - One of the radio buttons is selected
7. If all conditions are met, an Information pop-up will appear to inform the user of the chain's group name & object name before creating the group & object. Otherwise, an Error pop-up will appear to inform the user of the problematic attributes.

## Future Work

- Allow chain objects to be created from NURBs polygons
- Group the chain's `chain<num>` object and `chain_group<num>` group together
- Add controls for pattern variation e.g. rotating every 2nd link 90 degrees with respect to the X-axis
- Let users preview their chain before creating it
- Add controls to let users create a curve that dictates the chain's path, then curve warp the chain to the curve
- Allow users to create chains featuring multiple distinct objects 
- Make it easier for users to edit the chain object after it's created e.g. to remove or add new chain links
- Improving GUI appearance e.g. replacing text title with a image featuring the GUI title and sample tool outputs
- Window preferences (e.g. resizing a window) can only be reset if the window is not closed before `chain_builder.py` is rerun. I don't know why this is the case, but will fix once I figure out why.