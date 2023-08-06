#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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
# ******************************************************************************
"""
BatchNormalization transformations on models.
"""
import numpy as np

from keras.layers import BatchNormalization, MaxPool2D, GlobalAvgPool2D

from ..models.utils import deep_clone_model


def invert_batchnorm_pooling(model):
    """ Inverts pooling and BatchNormalization layers in a model to have BN layer before pooling.

    Returns a new model where pooling and batch normalization layers are inverted. From a Keras
    model where pooling layers precede batch normalization layers, this function places the BN
    layers before pooling layers. This is the first step before folding BN layers into neural
    layers.

    Note:
        Inversion of layers is equivalent only if the gammas of BN layers are positive. The
        function raises an error if not.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: the updated model

    Raises:
        RuntimeError: if a candidate BatchNormalization layer has gamma values that are not strictly
            positive.
    """

    # Maps between successive pooling->BN layers. These pairs will be inverted when cloning.
    pool2bn_map = {}
    bn2pool_map = {}

    # Map BatchNormalization layers that have only one inbound layer being a MaxPool2D or GAP2D
    for layer in model.layers:
        if (isinstance(layer, BatchNormalization) and len(layer.inbound_nodes) == 1
                and isinstance(layer.inbound_nodes[0].inbound_layers,(MaxPool2D, GlobalAvgPool2D))):
            gammas = layer.get_weights()[0]
            if isinstance(layer.inbound_nodes[0].inbound_layers, MaxPool2D) and np.any(gammas <= 0):
                # It is impossible to invert MaxPool->BN with gammas <= 0
                raise RuntimeError(f"There are {np.sum(gammas <= 0)} negative gammas in the "
                                   f"BatchNormalization layer {layer.name}. Negative gammas are "
                                   "not supported.")
            bn2pool_map[layer] = layer.inbound_nodes[0].inbound_layers
            pool2bn_map[layer.inbound_nodes[0].inbound_layers] = layer

    if not pool2bn_map:
        return model

    def replace_layer(layer):
        if layer in pool2bn_map:
            # Replace pooling layer with the corresponding BN layer
            layer_bn = pool2bn_map[layer]
            config_bn = layer_bn.get_config()
            if isinstance(layer, GlobalAvgPool2D):
                config_bn['axis'] = [-1]
            return layer_bn.from_config(config_bn)
        if layer in bn2pool_map:
            # Replace BN layer with the corresponding pooling layer
            layer_pool = bn2pool_map[layer]
            return layer_pool.from_config(layer_pool.get_config())
        return layer.from_config(layer.get_config())

    return deep_clone_model(model, clone_function=replace_layer)
