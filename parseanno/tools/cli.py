# -*- coding: utf-8 -*-

"""
@date: 2020/7/21 下午8:32
@file: cli.py
@author: zj
@description: 
"""

import sys
from parseanno.config import cfg
from parseanno.engine import AnnoProcessor, default_argument_parser
from parseanno.utils.misc import get_version


def main():
    args = default_argument_parser().parse_args()

    if args.version:
        print('ParseAnno: v{}'.format(get_version()))
        sys.exit(0)

    if not args.config_file:
        raise ValueError('A configuration file path is required')

    cfg.merge_from_file(args.config_file)
    cfg.freeze()

    processor = AnnoProcessor(cfg)
    processor.process()


if __name__ == '__main__':
    main()
