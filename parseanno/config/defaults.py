from yacs.config import CfgNode as CN

_C = CN()

_C.ANNO = CN()
# 原始标注
_C.ANNO.PARSER = 'labelimg'
# 结果标注
_C.ANNO.CREATOR = 'yolov5'
# 保存classmap
_C.ANNO.SAVE_CLASSMAP = True
# 详细输出
_C.ANNO.VERBOSE = True

# ---------------------------------------------------------------------------- #
# LabelImg
# ---------------------------------------------------------------------------- #

_C.LABELIMG = CN()
# 根目录 - 作为解析器
_C.LABELIMG.SRC_DIR = ''
# 根目录 - 作为保存器
_C.LABELIMG.DST_DIR = ''
# 图像后缀名
_C.LABELIMG.IMG_EXTENSION = '.png'
# 标注文件后缀名
_C.LABELIMG.ANNO_EXTENSION = '.xml'

# ---------------------------------------------------------------------------- #
# YoLoV5
# ---------------------------------------------------------------------------- #

_C.YOLOV5 = CN()
_C.YOLOV5.SRC_DIR = ''
_C.YOLOV5.DST_DIR = ''
_C.YOLOV5.IMG_EXTENSION = '.png'
_C.YOLOV5.ANNO_EXTENSION = '.txt'

# ---------------------------------------------------------------------------- #
# TLT
# ---------------------------------------------------------------------------- #

_C.TLT = CN()
_C.TLT.SRC_DIR = ''
_C.TLT.DST_DIR = ''
_C.TLT.IMG_EXTENSION = '.png'
_C.TLT.ANNO_EXTENSION = '.txt'

# ---------------------------------------------------------------------------- #
# VisDrone
# ---------------------------------------------------------------------------- #

_C.VISDRONE = CN()
_C.VISDRONE.SRC_DIR = ''
_C.VISDRONE.DST_DIR = ''
_C.VISDRONE.IMG_EXTENSION = '.jpg'
_C.VISDRONE.ANNO_EXTENSION = '.txt'