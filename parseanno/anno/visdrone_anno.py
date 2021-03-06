# -*- coding: utf-8 -*-

"""
@date: 2020/7/17 下午7:40
@file: visdrone_anno.py
@author: zj
@description: 
"""

import os
import glob
import numpy as np
import cv2

from parseanno.anno import registry
from parseanno.anno.base_anno import BaseAnno
from parseanno.utils.utility import is_dir, check
from parseanno.utils.logger import setup_logger


@registry.ANNOS.register('visdrone')
class VisDroneAnno(BaseAnno):
    """
    [VisDrone](http://aiskyeye.com/)数据集用于无人机的目标检测训练
    下载地址：[VisDrone/VisDrone-Dataset](https://github.com/VisDrone/VisDrone-Dataset)
    数据存放格式：
    root/
        images/
        annotations/
    标注文件（.txt）和图像一一对应，每行表示一个标注对象，共8个字段
    参考[Object Detection in Images](http://aiskyeye.com/evaluate/results-format/). 其格式如下
    <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
    在类别中忽略ignored-regions/others
    """

    classmap = {'ignored-regions': 0, 'pedestrian': 1, 'people': 2, 'bicycle': 3, 'car': 4, 'van': 5, 'truck': 6,
                'tricycle': 7, 'awning-tricycle': 8, 'bus': 9, 'motor': 10, 'others': 11}

    def __init__(self, cfg):
        self.src_dir = cfg.VISDRONE.SRC_DIR
        self.img_extension = cfg.VISDRONE.IMG_EXTENSION
        self.anno_extension = cfg.VISDRONE.ANNO_EXTENSION
        self.verbose = cfg.ANNO.VERBOSE

        self.logger = setup_logger(__name__)

    def get_class_name(self, value):
        return [k for k, v in self.classmap.items() if v == value][0]

    def create_anno(self, anno_line) -> dict:
        # 忽略ignored-regions/others
        xmin, ymin, width, height, _, cate = anno_line[:6].astype(np.int)
        xmax = xmin + width
        ymax = ymin + height
        if cate == 0 or cate == 11:
            return dict()
        name = self.get_class_name(cate)
        return {'name': name, 'bndbox': [xmin, ymin, xmax, ymax]}

    def parse_anno(self, img_path, anno_path) -> dict:
        """
        解析visdrone图像和标注文件
        :returns: anno_obj
        """
        anno_obj = dict()

        img = cv2.imread(img_path)
        h, w = img.shape[:2]
        anno_obj['size'] = (w, h)

        anno_array = np.loadtxt(anno_path, dtype=np.str, delimiter=',')
        objects = list()
        if len(anno_array.shape) == 1:
            # 就一个标注对象
            obj = self.create_anno(anno_array)
            if obj:
                objects.append(obj)
        else:
            for anno_line in anno_array:
                obj = self.create_anno(anno_line)
                if obj:
                    objects.append(obj)
        if len(objects) == 0:
            return dict()
        anno_obj['objects'] = objects
        return anno_obj

    def process(self) -> dict:
        src_dir = self.src_dir
        img_extension = self.img_extension
        anno_extension = self.anno_extension
        verbose = self.verbose

        img_dir = os.path.join(src_dir, 'images')
        anno_dir = os.path.join(src_dir, 'annotations')
        is_dir(src_dir)
        is_dir(img_dir)
        is_dir(anno_dir)

        img_path_list = sorted(glob.glob(os.path.join(img_dir, '*' + img_extension)))
        anno_path_list = sorted(glob.glob(os.path.join(anno_dir, '*' + anno_extension)))
        check(img_path_list, anno_path_list)

        anno_data = dict()
        for i, (img_path, anno_path) in enumerate(zip(img_path_list, anno_path_list), 1):
            if verbose:
                self.logger.info('解析{}'.format(anno_path))

            anno_obj = self.parse_anno(img_path, anno_path)
            if anno_obj:
                anno_data[img_path] = anno_obj
            else:
                self.logger.info('{}中仅包含标注类型为ignored-regions或者others的目标'.format(img_path))

        return {'classmap': self.classmap, 'anno_data': anno_data}

    def save(self, anno_data):
        super(VisDroneAnno, self).save(anno_data)
