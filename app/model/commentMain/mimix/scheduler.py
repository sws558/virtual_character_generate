# -*- coding: utf-8 -*-
import math

class ConstantScheduler():
    """
    """
    def __init__(self, train_config, optimizer):
        """
        """
        self.lr = train_config["lr"]
        self.optimizer = optimizer
    

    def step(self):
        """
        """
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = self.lr


def build_scheduler(train_config, optimizer):
    """
    """
    if "scheduler" not in train_config:
        return ConstantScheduler(train_config, optimizer)
    else:
        raise ValueError("scheduler not correct!")