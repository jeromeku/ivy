"""
Collection of PyTorch gradient functions, wrapped to fit Ivy syntax and signature.
"""

# global
import torch as _torch


def variable(array_in):
    array_in.requires_grad = True
    return array_in


def execute_with_gradients(func, xs):
    func_ret = func(xs)
    if isinstance(func_ret, tuple):
        y = func_ret[0]
        rest = func_ret[1:]
    else:
        y = func_ret
        rest = tuple()
    y.backward()
    return (y, xs.map(lambda x, _: x.grad), *rest)


def gradient_descent_update(ws, dcdws, lr):
    ws = ws.map(lambda w, key_chain: (w - (dcdws if key_chain == '' else dcdws.at_key_chain(key_chain)) * lr))
    ws.map(lambda w, _: w.retain_grad())
    return ws


def adam_update(ws, dcdws, lr, mw, vw, step, beta1=0.9, beta2=0.999, epsilon=1e-7):
    step = step.type(_torch.float32)
    mw = dcdws.map(lambda dcdw, kc: beta1 * mw.at_key_chain(kc) + (1 - beta1) * dcdw)
    dcdws_sqrd = dcdws.map(lambda dcdw, _: dcdw ** 2)
    vw = dcdws_sqrd.map(lambda dcdw_sqrd, kc: beta2 * vw.at_key_chain(kc) + (1 - beta2) * dcdw_sqrd)
    beta1_pow = beta1 ** step
    beta2_pow = beta2 ** step
    alpha = lr * (1 - beta2_pow)**0.5 / (1 - beta1_pow + epsilon)
    ws = ws.map(lambda w, kc: w - alpha * mw.at_key_chain(kc) / (vw.at_key_chain(kc) ** 0.5 + epsilon))
    ws.map(lambda w, _: w.retain_grad())
    return ws, mw, vw


def stop_gradient(x):
    x.requires_grad = False
    return x
