from . import manager

@manager.TRANSFORMS.add_component
class RandomHorizontalFlip:
    def __init__(self, prob=0.5):
        self.prob = prob

    def __call__(self, data):
        return data


@manager.TRANSFORMS.add_component
class RandomVerticalFlip:
    def __init__(self, prob=0.1):
        self.prob = prob

    def __call__(self, data):
        return data

