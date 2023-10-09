import argparse
import os.path as osp
from mmcv import Config
import mmcv
from datasets import build_dataset
from models import build_detector
from runner import build_runner,ImageShowHook,build_hook


def parse_args():
    parser = argparse.ArgumentParser(description="detect_val_tool")
    parser.add_argument("config", type=str, help="train config file path")
    parser.add_argument('--work-dir', help='the dir to save logs and models')
    
    return parser.parse_args()  

def main():
    args = parse_args()
    cfg = Config.fromfile(args.config)
    
    
    # work_dir is determined in this priority: CLI > segment in file > filename
    if args.work_dir is not None:
    # update configs according to CLI args if args.work_dir is not None
        cfg.work_dir = args.work_dir
    elif cfg.get('work_dir', None) is None:
        # use config filename as default work_dir if cfg.work_dir is None
        cfg.work_dir = osp.join('./work_dirs',
                                osp.splitext(osp.basename(args.config))[0])
        
    
    datasets = [build_dataset(cfg.data.test)]
    
    model = build_detector(cfg.model)

    runs = build_runner(cfg.runner)
    for hook_cfg in cfg.hooks:
        runs.register_hook(build_hook(hook_cfg))
    runs.run(data_loaders=datasets[0],model=model)
    

if __name__ == "__main__":
    main()