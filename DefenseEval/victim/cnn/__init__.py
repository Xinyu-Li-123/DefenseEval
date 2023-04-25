'''
This is a classifier based on CNN. For the convenience of experiments, the parameter
is always loaded from a checkpoint file. This way, we can initialize either a vanilla model
or one with defense mechanism by simply loading its corresponding checkpoint.
'''

import OpenAttack
import torch 

class CNNClassifier(OpenAttack.Classifier):
    def __init__(self, ckpt_path):
        pass 

    def get_pred(self, input_):
        pass 

    def get_prob(self, input_):
        pass 