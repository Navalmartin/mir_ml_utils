import torch.nn as nn


class AdaptorBase(object):

    def __init__(self, params: dict):
        self.params = params

    def __call__(self, model_ft: nn.Module) -> nn.Module:
        return model_ft


class AddLinearLayerAdaptor(AdaptorBase):
    """Add a linear layer to the given model. The layer can either
    be the LAST_LAYER in the network in which case this class adds a linear
    with dimensions (num_ftrs, num_ftrs) or by indicating the size of the output of the layer

    """

    def __init__(self, params: dict):
        super(AddLinearLayerAdaptor, self).__init__(params=params)

    def add_linear_layer(self, model_ft: nn.Module) -> nn.Module:

        if 'out' not in self.params:
            raise ValueError("The self.params is missing the 'out' keyword. "
                             "This should specify either 'LAST_LAYER' or the size of the"
                             "output of the layer")

        num_ftrs = model_ft.fc.in_features
        if self.params['out'] == 'LAST_LAYER':
            model_ft.fc = nn.Linear(num_ftrs, num_ftrs)
        else:
            model_ft.fc = nn.Linear(num_ftrs, self.params['out'])
        return model_ft

    def __call__(self, model_ft: nn.Module) -> nn.Module:
        return self.add_linear_layer(model_ft=model_ft)


class AddFlattenLayerAdaptor(AdaptorBase):

    def __init__(self, params: dict={}):
        super(AddFlattenLayerAdaptor, self).__init__(params=params)

    def __call__(self, model_ft: nn.Module) -> nn.Module:
        model_ft.fc = nn.Flatten()
        return model_ft


class ComposedAdaptor(AdaptorBase):

    def __init__(self, params: dict):
        super(ComposedAdaptor, self).__init__(params=params)

    def __call__(self, model_ft: nn.Module) -> nn.Module:

        for adaptor in self.params['adaptors']:
            model_ft = adaptor(model_ft)
        return model_ft


