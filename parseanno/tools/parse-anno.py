# -*- coding: utf-8 -*-

"""
@date: 2020/7/21 下午8:32
@file: parse-anno.py
@author: zj
@description: 
"""

from parseanno.config import cfg
from parseanno.engine import AnnoProcessor, default_argument_parser


def main(parser):
    args = parser.parse_args()

    cfg.merge_from_file(args.config_file)
    cfg.freeze()

    processor = AnnoProcessor(cfg)
    processor.process()


if __name__ == '__main__':
    main(default_argument_parser())
