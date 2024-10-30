# Important Object Labeling Tool

This Python script provides a graphical user interface (GUI) for identifying which targets on an image are important and which are not, following the object detection results from the YOLO series or other powerful models, and to rank the importance of the significant targets. 

## Demo
![Demo.png](https://github.com/Zhao-Qihao/Useful-Tools/blob/main/docs/demo.png)

## Features

- Load images from a folder or a single image file.
- Draw bounding boxes on images using right-click and drag.
- Load and display existing ground truth data from text files.
- Select important object bounding boxes.
- Rank the importance of the targets.
- Save new bounding box annotations to a ground truth file.
- Navigate through multiple images in a sequence.
- Reset current image to its original state without annotations.

## Installation

To use this tool, ensure you have Python installed on your system. Then, install the required packages using pip:

```bash
pip install tk Pillow
```

## Usage

1. Run the script from the command line by executing python labeling_tool.py.
2. Use the 'Load Image Folder' button to load all images from a specified directory. While loading the image, the corresponding ground truth file will also be loaded, and the bounding boxes will be displayed on the image. At this point, you can click on the bounding box that you consider important with the mouse, and it will be saved automatically.
3. Use the 'Reset Current Image' button to clear all annotations and ground truth data for the current image.
4. Use the 'Draw Box' button When the ground truth file is missing some bounding box information for the targets and drag the right mouse button to draw a bounding box on the image, The bounding boxes you draw will be automatically appended and saved in the ground truth file without overwriting the original ground truth file. And then you need to click 'Reset Current Image' button to reload the image and boxes.
5. Use the 'Next Image' button to move to the next image in the sequence.
6. Use the 'Load Single Image' button to load a single image file.


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
