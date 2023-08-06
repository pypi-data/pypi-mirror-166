# Copyright (c) 2022 Tianyi Wang
# All rights reserved.

# This source code is licensed under the GPL-3.0 license which can be found in the LICENSE file.


from torch import nn
from segmentation_models_pytorch.base.modules import Activation

from . import encoder
from .decoder import UnetDecoder

ENCODERS = [
    'convnext_tiny', 'convnext_small', 'convnext_base', 'convnext_large', 'convnext_xlarge',
]
ENCODER_DIMS = {
    'convnext_tiny': [96, 192, 384, 768],
    'convnext_small': [96, 192, 384, 768],
    'convnext_base': [128, 256, 512, 1024],
    'convnext_large': [192, 384, 768, 1536],
    'convnext_xlarge': [256, 512, 1024, 2048],
}


class InConv(nn.Module):
    """(convolution => [BN] => ReLU)"""

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.in_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.in_conv(x)


class ConvNeXtUnet(nn.Module):
    def __init__(self, num_classes, encoder_name, pretrained=False, in_22k=False, activation=None, in_channels=3,
                 bilinear=False, **kwargs):
        super().__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        self.bilinear = bilinear
        self.dims = ENCODER_DIMS[encoder_name]
        self.in_conv = InConv(self.in_channels, self.dims[0] // 2)

        try:
            encoder_model = getattr(encoder, encoder_name)
        except AttributeError:
            raise AttributeError(
                f"Wrong encoder name '{encoder_name}'. Available options are: {ENCODERS}"
            )

        self.convnext_encoder = encoder_model(pretrained, in_22k, **kwargs)

        self.unet_decoder = UnetDecoder(num_classes=self.num_classes, dims=self.dims, in_channels=self.in_channels,
                                        bilinear=self.bilinear)

        self.activation = Activation(activation)

    def forward(self, x):
        x = self.in_conv(x)
        x, features = self.convnext_encoder(x)
        x = self.unet_decoder(x, features)
        return self.activation(x)
