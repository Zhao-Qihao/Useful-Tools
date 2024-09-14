import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import math
import argparse

def get_gt_path(image_path, img_root_dir, gt_root_dir):
    """根据图片路径获取ground truth文件路径"""
    relative_path = os.path.relpath(image_path, start=img_root_dir)
    relative_path = os.path.dirname(relative_path)  # 移除文件名
    relative_path = os.path.dirname(relative_path)  # 移除 'images' 目录
    relative_path = os.path.join(relative_path, os.path.basename(image_path))  # 加上文件名
    gt_path = os.path.join(gt_root_dir, relative_path).replace(".png", ".txt").replace(".jpg", ".txt").replace(".jpeg", ".txt")
    print(gt_path)
    return gt_path

class LabelTool:
    def __init__(self, master, img_root_dir, gt_root_dir):
        self.master = master
        master.title("Labeling Tool")
        self.img_root_dir = img_root_dir
        self.gt_root_dir = gt_root_dir

        # 初始化变量
        self.image_path = None
        self.gt_path = None
        self.bounding_boxes = []
        self.labels = []
        self.confidences = []
        self.output_file = None
        self.image_files = []
        self.current_index = 0
        self.selection_count = 0
        self.new_bounding_boxes = []
        self.closest_bbox_set = set()       

        # 创建按钮
        self.create_buttons(master)

        # 创建画布
        self.canvas = tk.Canvas(master, width=2000, height=2000)
        self.canvas.grid(row=1, column=0, columnspan=8)  # 画布占据所有列
        # 绑定事件
        self.canvas.bind("<Button-1>", self.on_click)

    def create_buttons(self, master):
        # 创建按钮
        btn_load_image_folder = tk.Button(master, text="Load Image Folder", command=self.load_image_folder)
        btn_load_next_folder = tk.Button(master, text="Load Next Folder", command=self.load_next_folder)
        btn_load_single_image = tk.Button(master, text="Load Single Image", command=self.load_single_image)
        btn_previous_image = tk.Button(master, text="Previous Image", command=self.previous_image)
        btn_next_image = tk.Button(master, text="Next Image", command=self.next_image)
        btn_back2first = tk.Button(master, text="Back to First Image", command=self.back_to_first_image)
        btn_reset_current_image = tk.Button(master, text="Reset Current Image", command=self.reset_current_image)
        btn_draw_box = tk.Button(master, text="Draw Box", command=self.start_drawing_box)

        # 使用 grid 布局将按钮放置在画布上方
        btn_load_image_folder.grid(row=0, column=0)
        btn_load_next_folder.grid(row=0, column=1)
        btn_previous_image.grid(row=0, column=2)
        btn_next_image.grid(row=0, column=3)
        btn_back2first.grid(row=0, column=4)
        btn_load_single_image.grid(row=0, column=5)
        btn_reset_current_image.grid(row=0, column=6)
        btn_draw_box.grid(row=0, column=7)

        # 绑定键盘事件
        master.bind("<Left>", lambda event: self.previous_image())
        master.bind("<Right>", lambda event: self.next_image())

    def initialize(self):
        """
        初始化函数，可以在此处进行一些基本的设置或资源加载。
        """
        # 清除画布上的所有元素
        self.canvas.delete("all")

        # 重置所有与当前图片相关的数据
        self.bounding_boxes.clear()
        self.labels.clear()
        self.confidences.clear()
        self.new_bounding_boxes.clear()
        self.selection_count = 0  # 重置选择计数器
        self.closest_bbox_set.clear()       

    def load_image_folder(self):
        # 初始化
        self.initialize()
        self.current_index = 0  # 重置当前image_files索引

        initial_dir = os.path.expanduser(self.img_root_dir)
        folder_path = filedialog.askdirectory(initialdir=initial_dir)
        if not folder_path:
            return

        # 获取文件夹下所有图片文件，并按文件名排序
        self.image_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
        if not self.image_files:
            messagebox.showwarning("Warning", "No image files found in the selected folder.")
            return

        # 加载第一张图片及其对应的 ground truth 文件
        self.load_image(self.image_files[self.current_index])

    def load_next_folder(self):
        # 初始化
        self.initialize()
        self.current_index = 0  # 重置当前image_files索引

        # 如：self.image_path = "//sdc1/zqh/data/DADA2000-critical/DADA2000-critical/1/013/images/0240.png"
        # 分割路径，提取倒数第三级目录及其前面的目录
        head, tail = os.path.split(self.image_path)
        while tail != "images":
            head, tail = os.path.split(head)
        # 现在 head 是 "/sdc1/zqh/data/DADA2000-critical/DADA2000-critical/1/013"
        # tail 是 "images"

        # 再次分割一次，提取倒数第三级目录及其前面的目录
        parent_dir, second_last_dir = os.path.split(head)
        # 现在 head 是 "/sdc1/zqh/data/DADA2000-critical/DADA2000-critical/1"
        # tail 是 "013"
        next_folder_second_last_dir = str(int(second_last_dir)+1).zfill(3)
        next_folder_path = os.path.join(parent_dir, next_folder_second_last_dir, 'images')

        # 获取文件夹下所有图片文件，并按文件名排序
        self.image_files = sorted([os.path.join(next_folder_path, f) for f in os.listdir(next_folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
        if not self.image_files:
            messagebox.showwarning("Warning", "No image files found in the selected folder.")
            return

        # 加载第一张图片及其对应的 ground truth 文件
        self.load_image(self.image_files[self.current_index])

    def load_single_image(self):
        # 初始化
        self.initialize()

        initial_dir = os.path.expanduser(self.img_root_dir)
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes = [("All Files", "*.*"), ("Image Files", "*.jpg;*.jpeg;*.png"), ("Text Files", "*.txt")])
        print("Selected single image path:{}".format(file_path))
        if not file_path:
            print('No file selected.')
            return

        # 加载单张图片及其对应的 ground truth 文件
        self.load_image(file_path)

    def load_image(self, image_path):
        self.image_path = image_path
        print("Selected image path:{}".format(self.image_path))
        self.gt_path = get_gt_path(self.image_path, self.img_root_dir, self.gt_root_dir)

        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        if os.path.exists(self.gt_path):
            self.load_ground_truth()
        else:
            messagebox.showwarning("Warning", "Ground truth file not found.")
            self.gt_path = None

        self.new_bounding_boxes = []  # 新增边界框列表

    def load_ground_truth(self):
        # 关闭前一个文件的输出文件句柄
        if self.output_file:
            self.output_file.close()
            self.output_file = None

        # 确定输出文件路径
        base_name, ext = os.path.splitext(os.path.basename(self.gt_path))
        output_file_name = f"{base_name}_impo{ext}"
        self.output_file_path = os.path.join(os.path.dirname(self.gt_path), output_file_name)

        with open(self.gt_path, 'r') as f:
            for line in f:
                # 使用空格和逗号作为分隔符
                data = line.strip().split()
                # 假设标签总是位于第5个位置，且前面有四个数字
                x1, y1, x2, y2 = map(int, data[:4])
                label = ' '.join(data[4:-1])  # 将第5个位置及之后的所有项合并成一个字符串
                confidence = float(data[-1])
                self.bounding_boxes.append((x1, y1, x2, y2))
                self.labels.append(label)
                self.confidences.append(confidence)

        # 绘制边界框
        for bbox in self.bounding_boxes:
            self.canvas.create_rectangle(*bbox, outline='red')

    def start_drawing_box(self):
        self.canvas.bind("<Button-3>", self.on_start_drawing)
        self.canvas.bind("<B3-Motion>", self.on_drawing)
        self.canvas.bind("<ButtonRelease-3>", self.on_end_drawing)
        self.drawing_bbox = None
        self.drawing_bbox_id = None

    def on_start_drawing(self, event):
        self.drawing_bbox = (event.x, event.y, event.x, event.y)
        self.drawing_bbox_id = self.canvas.create_rectangle(*self.drawing_bbox, outline='blue', tags=("new_bounding_box",))

    def on_drawing(self, event):
        if self.drawing_bbox:
            x1, y1, _, _ = self.drawing_bbox
            self.canvas.coords(self.drawing_bbox_id, x1, y1, event.x, event.y)

    def on_end_drawing(self, event):
        if self.drawing_bbox:
            x1, y1, _, _ = self.drawing_bbox
            self.drawing_bbox = (x1, y1, event.x, event.y)
            self.canvas.itemconfig(self.drawing_bbox_id, outline='blue')
            self.new_bounding_boxes.append((x1, y1, event.x, event.y))
            self.save_new_bounding_boxes()
            self.canvas.unbind("<Button-3>")
            self.canvas.unbind("<B3-Motion>")
            self.canvas.unbind("<ButtonRelease-3>")

    def save_new_bounding_boxes(self):
        # 确保 ground truth 文件已经打开
        if self.gt_path:
            with open(self.gt_path, 'a') as gt_file:  # 使用 with 语句自动管理文件
                for bbox in self.new_bounding_boxes:
                    x1, y1, x2, y2 = bbox
                    label = "new_label"  # 可以自定义标签
                    confidence = 1.0  # 可以自定义置信度
                    gt_file.write(f"{x1} {y1} {x2} {y2} {label} {confidence:.2f}\n")
                gt_file.flush()
        
        self.new_bounding_boxes.clear()

    def next_image(self):
        # 初始化
        self.initialize()    

        # 检查当前图片是否为最后一张图片
        if self.current_index + 1 < len(self.image_files):
            self.current_index += 1
            self.load_image(self.image_files[self.current_index])

    def previous_image(self):
        # 初始化
        self.initialize()    

        # 检查当前图片是否为第一张图片
        if self.current_index - 1 < 0:
            self.current_index = len(self.image_files)
        self.current_index -= 1
        self.load_image(self.image_files[self.current_index])

    def back_to_first_image(self):
        # 初始化
        self.initialize()
        self.current_index = 0
        self.load_image(self.image_files[self.current_index])

    def reset_current_image(self):
        # 初始化
        self.initialize()    

        # 关闭输出文件句柄
        if self.output_file:
            self.output_file.close()
            self.output_file = None

        # 删除对应的 output 文件
        if self.output_file_path and os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)

        # 重新加载当前图片
        self.load_image(self.image_path)

    def on_click(self, event):
        # 获取点击位置
        x, y = event.x, event.y

        # 初始化最近框和最小距离
        closest_bbox = None
        min_distance = float('inf')

        # 检查点击是否在边界框内
        for i, bbox in enumerate(self.bounding_boxes):
            if bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]:
                # 计算框的中心点
                cx = (bbox[0] + bbox[2]) / 2
                cy = (bbox[1] + bbox[3]) / 2
                distance = math.sqrt((cx - x) ** 2 + (cy - y) ** 2)

                # 更新最近的框
                if distance < min_distance:
                    min_distance = distance
                    closest_bbox = i

        if closest_bbox is not None and closest_bbox not in self.closest_bbox_set:
            # 高亮选中的边界框
            self.highlight_selected_bbox(closest_bbox)

            # 保存对应的 ground truth
            self.save_selected_bbox(closest_bbox)
            self.closest_bbox_set.add(closest_bbox)

    def highlight_selected_bbox(self, index):
        # 绘制所有边界框
        for i, bbox in enumerate(self.bounding_boxes):
            if i != index:  # 只绘制未选中的边界框
                self.canvas.create_rectangle(*bbox, outline='red', tags=("bounding_box",))

        # 高亮选中的边界框
        x1, y1, x2, y2 = self.bounding_boxes[index]
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=3, tags=("highlight",))

    def save_selected_bbox(self, index):
        # 保存选中的边界框
        x1, y1, x2, y2 = self.bounding_boxes[index]
        label = self.labels[index]
        confidence = self.confidences[index]

        # 打开输出文件
        if self.selection_count == 0:
            self.output_file = open(self.output_file_path, 'w')
        else:
            self.output_file = open(self.output_file_path, 'a')
        # 追加到文件中
        if self.output_file:
            # 在保存时添加递增的整数
            self.output_file.write(f"{x1} {y1} {x2} {y2} {label} {confidence:.2f} {self.selection_count + 1}\n")
            self.output_file.flush()  # 立即刷新缓冲区
            self.selection_count += 1  # 更新选择计数器


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Labeling Tool for Images')
    parser.add_argument('--img_root_dir', type=str, default="/sdc1/zqh/data/DADA2000-critical/DADA2000-critical",
                        help='Root directory for image files')
    parser.add_argument('--gt_root_dir', type=str, default="/sdc1/zqh/data/DADA2000-critical/DADA2000-critical-detection",
                        help='Root directory for ground truth files')
    args = parser.parse_args()
    root = tk.Tk()
    app = LabelTool(root, img_root_dir=args.img_root_dir, gt_root_dir=args.gt_root_dir)
    root.mainloop()