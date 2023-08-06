import tensorflow as tf
import numpy as np
from models_rate import DenseRNN, SpikingReLU, SpikingSigmoid, SpikingTanh, Accumulate


def get_normalized_weights(model, x_test, percentile=100):
    all_activations = np.zeros([1, ])
    for layer in model.layers:
        activation = tf.keras.Model(inputs=model.inputs,
                                    outputs=layer.output)(x_test).numpy()
        all_activations = np.concatenate((all_activations, activation.flatten()))

    max_activation = np.percentile(all_activations, percentile)

    weights = model.get_weights()
    if max_activation == 0:
        print("\n" + "-"*32 + "\nNo normalization\n" + "-"*32)
    else:
        print("\n" + "-"*32 + "\nNormalizing by", max_activation, "\n" + "-"*32)
        for i in range(len(weights)):
            weights[i] /= (max_activation)

    # Testing normalized weights
    """model.set_weights(weights)
    max_activation = 0
    for layer in model.layers:
        print(type(layer))
        if isinstance(layer, tf.keras.layers.ReLU):
            activation = tf.keras.Model(inputs=model.inputs, outputs=layer.output)(x_test).numpy()
            print("Local max", np.amax(activation))
            if np.amax(activation) > max_activation:
                max_activation = np.amax(activation)
            print("Max", max_activation)"""
    return weights
