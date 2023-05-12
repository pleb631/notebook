# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy


class ConfigChecker(object):
    """
    This class performs sanity checks on configuration objects and (optionally) updates the configurations
        (e.g., synchronize specific key-value pairs) based on a set of rules. 

    Args:
        rule_list (list): A list of rules on which all checks and updates are based.
        allow_update (bool, optional): Whether or not to allow updating the configuration object.
    """

    def __init__(self, rule_list, allow_update=True):
        super().__init__()
        self.rule_list = rule_list
        self.allow_update = allow_update

    def apply_rule(self, k, cfg):
        rule = self.rule_list[k]
        try:
            rule.apply(cfg, self.allow_update)
        except Exception as e:
            raise RuntimeError(
                "Sanity check on the configuration file has failed. "
                "There should be some problems with your config file. "
                "Please check it carefully.\n"
                f"The failed rule is {rule.__class__.__name__}, and the error message is: \n{str(e)}"
            )

    def apply_all_rules(self, cfg):
        for i in range(len(self.rule_list)):
            self.apply_rule(i, cfg)

    def add_rule(self, rule):
        self.rule_list.append(rule)


class Rule(object):
    def check_and_correct(self, cfg):
        raise NotImplementedError

    def apply(self, cfg, allow_update):
        if not allow_update:
            cfg = copy.deepcopy(cfg)
        self.check_and_correct(cfg)


class DefaultPrimaryRule(Rule):
    def check_and_correct(self, cfg):
        items = [
            'batch_size', 'iters', 'train_dataset', 'optimizer', 'lr_scheduler',
            'loss', 'model'
        ]
        for i in items:
            assert i in cfg.dic, \
            'No {} specified in the configuration file.'.format(i)

