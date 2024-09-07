# Image Labeling Tool

This Python script provides a graphical user interface (GUI) for labeling images with bounding boxes. It allows users to load images, draw boxes around objects of interest, and save the annotations to a file.

## Structure
TODO

## Features

- Load images from a folder or a single image file.
- Draw bounding boxes on images using right-click and drag.
- Load and display existing ground truth data from text files.
- Save new bounding box annotations to a ground truth file.
- Navigate through multiple images in a sequence.
- Reset current image to its original state without annotations.

## Requirements

- Python 3.x
- Tkinter for GUI
- Pillow for image processing
- os and argparse for file and command-line argument handling

## Installation

To use this tool, ensure you have Python installed on your system. Then, install the required packages using pip:

```bash
pip install tk Pillow
```

## Usage

1. Run the script from the command line by executing python labeling_tool.py.
2. Use the 'Load Image Folder' button to load all images from a specified directory.
3. Use the 'Load Single Image' button to load a single image file.
4. Click and drag the right mouse button to draw a bounding box on the image.
5. Use the 'Next Image' button to move to the next image in the sequence.
6. Use the 'Reset Current Image' button to clear all annotations and ground truth data for the current image.
7. The ground truth data is saved automatically as you draw new bounding boxes.

Example:
```bash
python label_tool.py --gt_root_dir /path/to/ground/truth
```
The ```--gt_root_dir``` parameter specifies the root directory for ground truth files. The default value is ```/data/zqh/DADA2000/DADA2000-detection```.

## File Format
The tool expects ground truth data in text files with the following format:
```
x1 y1 x2 y2 label confidence
```
The tool saves data in text files with the following format:
```
x1 y1 x2 y2 label confidence important_ranking
```
Where ```x1 y1``` are the coordinates of the top-left corner of the bounding box, ```x2 y2``` are the coordinates of the bottom-right corner, ```label``` is a string representing the object class, and ```confidence``` is a float value representing the confidence of the annotation.The ```important_ranking``` field is used to rank the importance of the bounding box. It can be used to prioritize the bounding boxes for training.

## Notes
* The script assumes that the ground truth files have the same base name as the image files but with a .txt extension.
* The script uses the PIL library to handle image loading and display.
* The script uses the tkinter library to create the GUI and handle user interactions.