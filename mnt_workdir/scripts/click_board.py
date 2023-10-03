from tkinter import Tk, Canvas, Button, Toplevel
from PIL import Image, ImageTk

import numpy as np

import cv2  # type: ignore

from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

import json
import os
from typing import Any, Dict, List
import time


from parser import get_parser, get_amg_kwargs
from InferBot import InferBot
# 画像ファイルのパス
image_path = "/mnt/imgs/nobiru.jpg"
image_path2 = "/mnt/imgs/bujiramioya.jpg"

class ClickBoard:
    def __init__(self, args):
        # 画像のリサイズ
        self.max_width = 400  # 表示する画像の最大幅
        self.max_height= 400  # 表示する画像の最大高さ
        self.sub_max_width = 400
        self.sub_max_height = 400
        self.mode = 1
        self.point_dict = {'add':[], 'remove':[]}
        self.model = InferBot(args)

    def on_pixel_click(self, event):
        # クリックされたピクセルの座標を取得
        w, h = event.x, event.y
        target_w = self.max_size / self.max_width * w
        target_h = self.max_size / self.max_height * h
        # target_x = 
        if self.mode=='add':
            self.point_dict['add'].append([target_w, target_h])
        elif self.mode=='remove':
            self.point_dict['remove'].append([target_w, target_h])
        # elif self.mode=='clear':
        #     self.point_dict = {'add':[], 'remove':[]}
        print(f"mode {self.mode} Clicked at pixel coordinates: ({target_w}, {target_h}) ")


    def process(self, image_path):
        root = Tk()
        root.title("Image Viewer")

        # 画像の読み込み
        image = Image.open(image_path)
        origin_width = image.width
        origin_height = image.height
        self.max_size = max(origin_width, origin_height)
        image.thumbnail((self.max_width, self.max_height))

        # 画像の表示サイズ
        canvas_width = image.width
        canvas_height = image.height

        # ウィンドウの作成
        window = Toplevel(root)
        window.title("Clicker: click right image")
        # window = Tk()
        # window.title("Image Viewer")

        

        # キャンバスの作成
        self.canvas = Canvas(window, width=canvas_width, height=canvas_height)
        self.canvas.pack(side='right')

        # 画像の表示
        self.image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

        # キャンバス2の作成
        image.thumbnail((self.sub_max_width, self.sub_max_height))

        # 画像の表示サイズ
        canvas2_width = image.width
        canvas2_height = image.height

        self.canvas2 = Canvas(window, width=canvas2_width, height=canvas2_height)
        self.canvas2.pack()

        # 画像2の表示
        self.image_tk2 = ImageTk.PhotoImage(image)
        self.canvas2.create_image(0, 0, anchor="nw", image=self.image_tk2)
        # モード切り替えボタンの作成
        mode1_button = Button(window, text="add", command=self.set_mode_1)
        mode1_button.pack(side='left')
        mode2_button = Button(window, text="remove", command=self.set_mode_2)
        mode2_button.pack(side='left')
        mode3_button = Button(window, text="apply", command=self.set_mode_3)
        mode3_button.pack(side='left')
        mode4_button = Button(window, text="clear", command=self.set_mode_4)
        mode4_button.pack(side='left')
        mode5_button = Button(window, text="next", command=self.set_mode_5)
        mode5_button.pack(side='left')

        # クリックイベントのバインディング
        self.canvas.bind("<Button-1>", self.on_pixel_click)

        # イベントループの開始
        window.mainloop()
    
    def set_mode_1(self):
        self.mode = 'add'

    def set_mode_2(self):
        self.mode = 'remove'

    def set_mode_3(self):
        self.mode = 'apply'
        input_points = np.array(self.point_dict['add'] + self.point_dict['remove'])
        input_labels = np.array([1]*len(self.point_dict['add']) + [0]*len(self.point_dict['remove']))
        print(input_points.shape, len(input_points))
        print(len(input_labels))
        assert len(input_points.shape)!=len(input_labels)
        image = self.model.forward(image_path, input_points, input_labels)
        # image = Image.open(image_path2)
        
        origin_width = image.width
        origin_height = image.height
        self.max_size = max(origin_width, origin_height)
        image.thumbnail((self.max_width, self.max_height))
        self.image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

    def set_mode_4(self):
        self.mode = 'clear'
        self.point_dict = {'add':[], 'remove':[]}

    def set_mode_5(self):
        self.mode = 'next'


args = get_parser()
click_board = ClickBoard(args)
click_board.process(image_path)