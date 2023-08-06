"""
Model Utils
-----------

"""

import torch


class ModelReconstructor(torch.nn.Module):
    def __init__(self, feature_extractor, classifier, connection_fn=None) -> None:
        super(ModelReconstructor, self).__init__()
        self.feature_extractor = feature_extractor
        self.classifier = classifier
        self.connection_fn = connection_fn

    def forward(self, input):
        features = self.feature_extractor(input)
        if self.connection_fn is not None:
            features = self.connection_fn(features)
        return self.classifier(features)


def get_output_size(in_size, pad, kernel, stride):
    if pad == "same":
        return in_size
    return ((in_size + 2 * pad - kernel) // stride) + 1
