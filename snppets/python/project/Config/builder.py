import copy
from typing import Any, Optional

import yaml


from config import Config
from transform import manager
from utils import utils, logger
from utils.utils import CachedProperty as cached_property


class Builder(object):
    """
    The base class for building components. 

    Args:
        config (Config): A Config class.
        comp_list (list, optional): A list of component classes. Default: None
    """

    def __init__(self, config: Config, comp_list: Optional[list]=None):
        super().__init__()
        self.config = config
        self.comp_list = comp_list

    def build_component(self, cfg):
        """
        Create Python object, such as model, loss, dataset, etc.
        """
        cfg = copy.deepcopy(cfg)
        if 'type' not in cfg:
            raise RuntimeError(
                "It is not possible to create a component object from {}, as 'type' is not specified.".
                format(cfg))

        class_type = cfg.pop('type')
        com_class = self.load_component_class(class_type)

        params = {}
        for key, val in cfg.items():
            if self.is_meta_type(val):
                params[key] = self.build_component(val)
            elif isinstance(val, list):
                params[key] = [
                    self.build_component(item)
                    if self.is_meta_type(item) else item for item in val
                ]
            else:
                params[key] = val

        try:
            obj = self.build_component_impl(com_class, **params)
        except Exception as e:
            if hasattr(com_class, '__name__'):
                com_name = com_class.__name__
            else:
                com_name = ''
            raise RuntimeError(
                f"Tried to create a {com_name} object, but the operation has failed. "
                "Please double check the arguments used to create the object.\n"
                f"The error message is: \n{str(e)}")

        return obj

    def build_component_impl(self, component_class, *args, **kwargs):
        return component_class(*args, **kwargs)

    def load_component_class(self, class_type):
        for com in self.comp_list:
            if class_type in com.components_dict:
                return com[class_type]
        raise RuntimeError("The specified component ({}) was not found.".format(
            class_type))

    @classmethod
    def is_meta_type(cls, obj):
        # TODO: should we define a protocol (see https://peps.python.org/pep-0544/#defining-a-protocol)
        # to make it more pythonic?
        return isinstance(obj, dict) and 'type' in obj

    @classmethod
    def show_msg(cls, name, cfg):
        msg = 'Use the following config to build {}\n'.format(name)
        msg += str(yaml.dump({name: cfg}, Dumper=utils.NoAliasDumper))
        logger.info(msg[0:-1])


class SegBuilder(Builder):
    """
    This class is responsible for building components for semantic segmentation. 
    """

    def __init__(self, config, comp_list=None):
        if comp_list is None:
            comp_list = [
                manager.TRANSFORMS
            ]
        super().__init__(config, comp_list)

    @cached_property
    def val_dataset_class(self) -> Any:
        dataset_cfg = self.config.val_dataset_cfg
        assert dataset_cfg != {}, \
            'No val_dataset specified in the configuration file.'
        dataset_type = dataset_cfg.get('type')
        return self.load_component_class(dataset_type)

    @cached_property
    def val_transforms(self) -> list:
        dataset_cfg = self.config.val_dataset_cfg
        assert dataset_cfg != {}, \
            'No val_dataset specified in the configuration file.'
        transforms = []
        for item in dataset_cfg.get('transforms', []):
            transforms.append(self.build_component(item))
        return transforms

if __name__=='__main__':
    config = Config(r'D:\objectdetection\other\config1\test.yml')
    builder = SegBuilder(config)
    transforms = builder.val_transforms
    print(transforms)