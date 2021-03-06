"""
Collection of MXNet gradient functions, wrapped to fit Ivy syntax and signature.
"""

# global
import mxnet as _mx

variable = lambda x: x


def execute_with_gradients(func, xs):
    raise Exception('MXNet Symbolic mode does not support execute_with_gradients().')


def gradient_descent_update(ws, dcdws, lr):
    raise Exception('MXNet Symbolic mode does not support gradient_descent_update().')


def adam_update(ws, dcdws, lr):
    raise Exception('MXNet Symbolic mode does not support adam_update().')


stop_gradient = _mx.symbol.stop_gradient
