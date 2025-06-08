# Chain Builder

This tool provides Autodesk Maya users a GUI to create a chain object in a non-procedural manner. The script automates the chain creation process depicted in [Model a Chain in Maya the simple way! - 3D Modeling Tutorial](https://www.youtube.com/watch?v=OGrMSgIYQWY) by Holly's Maya Tutorials.

A chain consists of a group with naming convention `chain_group<num>` containing:
    - `chain` - The chain object (transform & shape nodes)
    - `chain_links` - A group containing the chain's link objects

## Script Setup

Upon downloading the script, you have 2 options for running the script:
1. Open the script directly within Maya's Script Editor, selecting all its contents, then running it through CTRL + Enter or similar
2. Create a userSetup.py in your Maya's user script folder/directory to auto-run the script or set up a shelf icon that runs the script when clicked
    - To ascertain the user script folder/directory see your Maya version's documentation on "Initializing the Maya Python environment" e.g. https://help.autodesk.com/view/MAYAUL/2023/ENU/?guid=GUID-640C1383-3FB8-410F-AE18-987A812B5914

## User Workflow

1. Run the `chain_builder.py` script to launch the **Chain Builder** window.
2. Select the chain link object via the Outliner or View Panel, then confirm your selection by clicking the **Update selection** button in the **Chain Builder** window.
3. Specify the number of links you want your chain to have in the "Number of Chain Links" field.
4. Specify the distance between consecutive links in the "Distance Between Links" field.
5. Select the direction of chain link generation by clicking one of the "Chain Orientation" radio buttons.
6. Click the "Create Chain" button to confirm your chain attributes, prompting the tool to check whether the following conditions are met:
    - "Chain Link Object" - Specified chain link object still exists
    - "Number of Chain Links" - A positive integer (whole number) is provided
    - "Distance Between Links" - A positive number is provided
    - "Chain Orientation" - One of the radio buttons is selected
7. If all conditions are met, an Information pop-up will appear indicating that the following objects will be created:
    - The chain object
    - A group containing the chain's link objects
    - A parent group containing the chain object and the chain link group
    Otherwise, an Error pop-up will appear to inform the user of the problematic attributes.

## Future Work

- Only allow a chain to be created if the selected object is either a polygon object or a NURBs object
- Give users the option to include or omit the selected object from the `chain_link` group
    - If omitted, the `chain_link` group will just consist of instances of the selected object
- Add controls to let users create a curve that dictates the chain's path, then curve warp the chain to the curve
- Allow users to create chains featuring multiple distinct objects
- Add controls for pattern variation e.g. rotating every 2nd link 90 degrees with respect to the X-axis
- Let users preview their chain before creating it
- Make it easier for users to edit the chain object after it's created e.g. to remove or add new chain links
- Improving GUI appearance e.g. replacing text title with a image featuring the GUI title and sample tool outputs

## Issues Register

- NURBs polygons can be selected, but there are issues creating a chain object
    - NURBs polygons can be grouped together, but the polyUnite command outputs `# Error: RuntimeError: file <maya console> line 218: Invalid selection : polyUnite needs at least 2 polygonal objects.`
    - Investigating why this is the case

- Window preferences (e.g. resizing a window) can only be reset if the window is not closed before `chain_builder.py` is rerun. I don't know why this is the case, but will fix once I figure out why.
