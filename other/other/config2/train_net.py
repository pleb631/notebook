#!/usr/bin/env python
# encoding: utf-8


import sys
import argparse
sys.path.append('.')

from config import get_cfg
#from fastreid.engine import DefaultTrainer, default_argument_parser, default_setup, launch

def default_argument_parser():
    """
    Create a parser with some common arguments used by fastreid users.
    Returns:
        argparse.ArgumentParser:
    """
    parser = argparse.ArgumentParser(description="template")
    parser.add_argument("--config-file", default="other\CONFIG\Base-bagtricks.yml", metavar="FILE", help="path to config file")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="whether to attempt to resume from the checkpoint directory",
    )
    parser.add_argument("--eval-only", action="store_true", help="perform evaluation only")
    parser.add_argument("--num-gpus", type=int, default=1, help="number of gpus *per machine*")
    parser.add_argument("--num-machines", type=int, default=1, help="total number of machines")
    parser.add_argument(
        "--machine-rank", type=int, default=0, help="the rank of this machine (unique per machine)"
    )

    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    return parser.parse_args()

def setup(args):
    """
    Create configs and perform basic setups.
    """
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()

    return cfg


def main(args):
    cfg = setup(args)

    if args.eval_only:
        cfg.defrost()
    print(cfg)
    
    pass


    return 0


if __name__ == "__main__":
    args = default_argument_parser()
    print("Command Line Args:", args)
    main(args)

