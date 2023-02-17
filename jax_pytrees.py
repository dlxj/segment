
# import jax
# import jax.numpy as jnp
# out = jax.vmap(lambda x: x ** 2)(jnp.arange(1))  
# print(out)



# https://jax.readthedocs.io/en/latest/notebooks/xmap_tutorial.html  需要仔细看的文档
import jax.numpy as np
from typing import Any, Callable

class ArrayType:
  def __getitem__(self, idx):
    return Any
f32 = ArrayType()
i32 = ArrayType()

x: f32[(2, 3)] = np.ones((2, 3), dtype=np.float32)
y: f32[(3, 5)] = np.ones((3, 5), dtype=np.float32)
z: f32[(2, 5)] = x.dot(y)  # matrix multiplication
w: f32[(7, 1, 5)] = np.ones((7, 1, 5), dtype=np.float32)
q: f32[(7, 2, 5)] = z + w  # broadcasting



a = f32[0]
b = 1


# import os
# os.environ["XLA_FLAGS"] = '--xla_force_host_platform_device_count=8' # Use 8 CPU devices

# import jax.numpy as jnp
# from jax import lax
# from jax.nn import one_hot, relu
# from jax.scipy.special import logsumexp

# def named_predict(w1, w2, image):
#   hidden = relu(lax.pdot(image, w1, 'inputs'))
#   logits = lax.pdot(hidden, w2, 'hidden')
#   return logits - logsumexp(logits, 'classes')

# def named_loss(w1, w2, images, labels):
#   predictions = named_predict(w1, w2, images)
#   num_classes = lax.psum(1, 'classes')
#   targets = one_hot(labels, num_classes, axis='classes')
#   losses = lax.psum(targets * predictions, 'classes')
#   return -lax.pmean(losses, 'batch')

# from jax.experimental.maps import xmap

# in_axes = [['inputs', 'hidden', ...],
#            ['hidden', 'classes', ...],
#            ['batch', 'inputs', ...],
#            ['batch', ...]]

# w1 = jnp.zeros((784, 512))
# w2 = jnp.zeros((512, 10))
# images = jnp.zeros((128, 784))
# labels = jnp.zeros(128, dtype=jnp.int32)


# def predict(w1, w2, images):
#   hiddens = relu(jnp.dot(images, w1))
#   logits = jnp.dot(hiddens, w2)
#   return logits - logsumexp(logits, axis=1, keepdims=True)

# def loss(w1, w2, images, labels):
#   predictions = predict(w1, w2, images)
#   targets = one_hot(labels, predictions.shape[-1])
#   losses = jnp.sum(targets * predictions, axis=1)
#   return -jnp.mean(losses, axis=0)

# print(loss(w1, w2, images, labels))

# loss = xmap(named_loss, in_axes=in_axes, out_axes=[...])
# print(loss(w1, w2, images, labels))





# import jax.numpy as jnp
# from jax.experimental.maps import xmap, Mesh
# x = jnp.arange(10).reshape((2, 5))
# r = xmap(jnp.vdot,
#      in_axes=({0: 'left'}, {1: 'right'}),
#      out_axes=['left', 'right', ...])(x, x.T)
# a = 1

# Array([[ 30,  80],
#        [ 80, 255]], dtype=int32)


# import jax.numpy as jnp
# from jax.experimental.maps import xmap, Mesh

# result = xmap(lambda x, y: jnp.multiply(x, y), [1, 2, 3], [4, 5, 6])

# print(result)
# # [4, 10, 18]


# import jax
# import jax.numpy as jnp
# import numpy as onp
# from jax.experimental.maps import xmap, Mesh
# # import tensorflow_probability.substrates.jax as tfp
# # tfd = tfp.distributions

# def loss(key):

#   init_z = jax.random.normal(key)

#   def scan_fn(prev_z, t):
#     new_z = jax.lax.cond(t == 0,
#             lambda _: prev_z,
#             lambda _: prev_z,
#             None)
#     return new_z, None

#   out, _ = jax.lax.scan(scan_fn, init_z, jnp.arange(10))

#   return 0.

# def step(key):
#   x = loss(key)
#   return jnp.mean(x, axis=('b'))

# xm_step = xmap(step, in_axes=['b',...], out_axes=[...], axis_resources={'b':'x'})

# devices = onp.array(jax.local_devices())

# key = jax.random.PRNGKey(0)
# keys = jax.random.split(key, num=jax.local_device_count())
# with Mesh(devices, ('x',)):
#   xm_step(keys)



# from collections import namedtuple
# import jax.numpy as np
# import jax

# testtup = namedtuple("testtup", ['x', 'y', 'n'])
# tup_list = [testtup(x=np.ones(5)*i, y=np.zeros(5) + i, n=i) for i in range(4)]

# def add_tup(t):
#     return np.sum(t.x + t.y) * t.n

# s = jax.jit(add_tup)(l[0])  # works!
# s_all = jax.vmap(add_tup)(l)  # doesn't work :/





# # https://github.com/google/jax/issues/3102
# from collections import namedtuple
# from jax import vmap, vjp
# from jax import tree_util
# import jax.numpy as np

# testtup = namedtuple("testtup", ['x', 'y', 'n'])
# tup_list = [testtup(x=np.ones(5)*i, y=np.zeros(5) + i, n=i) for i in range(4)]

# def add_tup(t):
#   return np.sum(t.x + t.y) * t.n


# def stackmap(f, lst):
#   stacked = tree_util.tree_multimap(lambda *args: np.stack(args), *lst)
#   out_stacked = vmap(f)(stacked)
#   _, outer_treedef = tree_util.tree_flatten([object()] * len(lst))
#   _, inner_treedef = tree_util.tree_flatten(out_stacked)
#   out_unstacked_transposed = tree_util.tree_map(list, out_stacked)
#   out_unstacked = tree_util.tree_transpose(outer_treedef, inner_treedef,
#                                            out_unstacked_transposed)
#   return out_unstacked

# s_all = stackmap(add_tup, tup_list)
# a = 1


# import time, os, jax, numpy as np, jax.numpy as jnp
# jax.config.update('jax_platform_name', 'cpu') # insures we use the CPU

# def timer(name, f, x, shouldBlock=True):
#    # warmup
#    y = f(x).block_until_ready() if shouldBlock else f(x)
#    # running the code
#    start_wall = time.perf_counter()
#    start_cpu = time.process_time()
#    y = f(x).block_until_ready() if shouldBlock else f(x)
#    end_wall = time.perf_counter()
#    end_cpu = time.process_time()
#    # computing the metric and displaying it
#    wall_time = end_wall - start_wall
#    cpu_time = end_cpu - start_cpu
#    cpu_count = os.cpu_count()
#    print(f"{name}: cpu usage {cpu_time/wall_time:.1f}/{cpu_count} wall_time:{wall_time:.1f}s")

# # test functions
# key = jax.random.PRNGKey(0)
# x = jax.random.normal(key, shape=(500000,), dtype=jnp.float64)
# x_mat = jax.random.normal(key, shape=(10000,10000), dtype=jnp.float64)
# f_numpy = np.cos
# f_vmap = jax.jit(jax.vmap(jnp.cos))
# f_xmap = jax.jit(jax.experimental.maps.xmap(jnp.cos, in_axes=[['batch']], out_axes=['batch']))
# f_dot = jax.jit(lambda x: jnp.dot(x,x.T)) # to show that JAX can indeed use all cores

# timer('numpy', f_numpy, x, shouldBlock=False)
# timer('vmap', f_vmap, x)
# timer('xmap', f_xmap, x)
# timer('dot', f_dot, x_mat)




# import jax
# from absl import app, logging

# def main(_):

#     dic1 = { 'a':[0,1,2], 'b':[3,4,5] }

#     def update(arr):

#         return 0

#     p_update = jax.pmap(update)

#     return 0

# if __name__ == '__main__':
#     app.run(main)


# # pip install git+https://github.com/deepmind/dm-haiku
# import contextlib
# import time
# from typing import NamedTuple

# import chex
# import haiku as hk
# import jax
# import jax.numpy as jnp
# import numpy as np
# from absl import app, logging

# @contextlib.contextmanager
# def timer(name: str):
#     begin = time.time_ns()
#     try:
#         yield begin
#     finally:
#         logging.info(f'Timer {name}[ms] {(time.time_ns() - begin) / int(1e6)}')


# class Input(NamedTuple):
#     x: chex.Array
#     a: chex.Array
#     b: chex.Array


# @hk.without_apply_rng
# @hk.transform
# def net(x: Input) -> chex.Array:
#     return hk.nets.MLP([128, 128,128, 1])((x.x - x.a) * x.b)


# apply_for_many = jax.vmap(net.apply, in_axes=(None, Input(None, 0, 0)))


# def main(_):
#     rng = jax.random.PRNGKey(42)

#     x = np.random.normal(size=(16, 8))
#     a = np.random.normal(size=(64))
#     b = np.random.normal(size=(64))

#     params = net.init(rng, Input(x, a[0], b[0]))

#     lr = jnp.logspace(-5, -2, jax.device_count())

#     def cost(x: chex.Array, a: chex.Array, b: chex.Array, params: hk.Params) -> chex.Array:
#         yhat = apply_for_many(params, Input(x, a, b))
#         return jnp.mean(yhat)

#     def update(params: hk.Params, x: Input, lr: chex.Array) -> chex.Array:
#         df = jax.grad(cost)(*x, params)
#         proposal = x.x - lr * df
#         proposal = jnp.where(proposal < 0., 0., proposal)
#         value = cost(proposal, a, b, params)
#         return value, proposal

#     jv_update = jax.jit(jax.vmap(update, in_axes=(None, None, 0)))
#     p_update = jax.pmap(update, in_axes=(None, None, 0))

#     @jax.jit
#     def select(values: chex.Array, proposals: chex.Array) -> chex.Array:
#         min_idx = jnp.argmin(values)
#         return proposals[min_idx, ...]

#     # jit
#     v, p = jv_update(params, Input(x, a, b), lr)
#     v, p = p_update(params, Input(x, a, b), lr)
#     new_x = select(v, p).block_until_ready()

#     with timer('pmap()'):
#         v, p = p_update(params, Input(x + 0.1, a, b), lr)
#         new_x = select(v, p).block_until_ready()

#     with timer('jit(vmap())'):
#         v, p = jv_update(params, Input(x + 0.1, a, b), lr)
#         new_x = select(v, p).block_until_ready()


#     return 0


# if __name__ == '__main__':
#     app.run(main)






# import jax
# import jax.numpy as jnp

# @jax.tree_util.register_pytree_node_class
# class ParamsDict:
#     def __init__(self, **kwargs):
#         self.params = {**kwargs}

#     def tree_flatten(self):
#         return jax.tree_flatten(self.params, lambda a: a is not self.params) # only flatten one step

#     @classmethod
#     def tree_unflatten(cls, aux, values):
#         return ParamsDict(**jax.tree_unflatten(aux, values))


# print('create e')
# e = ParamsDict(k=2,j=3)
# e.params['a'] = 0.0

# print('e1 = map over e')
# e1 = jax.tree_util.tree_map(lambda x: (x, 1.1), e)
# print('l = map over e, e1')
# l = jax.tree_util.tree_map(lambda a, b: 2.2, e, e1)

# a = 1


# from jax.tree_util import register_pytree_node_class
# import jax.numpy as jnp
# from jax.experimental import checkify
# import jax

# @register_pytree_node_class
# class Boxes:
#   def __init__(self, arr: jnp.ndarray):
#     self.arr = arr
#     assert arr.ndim > 1 and arr.shape[-1] == 4
  
#   def area(self) -> jnp.ndarray:
#     return (self.arr[..., 2] - self.arr[..., 0]) * (self.arr[..., 3] - self.arr[..., 1])

#   def tree_flatten(self):
#     return ((self.arr,), None)
  
#   @classmethod
#   def tree_unflatten(cls, _, children):
#     return cls(children[0])

# def func(x: Boxes):
#   return x.area() + 3

# box = Boxes(jnp.ones((2, 2, 4)))
# r = box.area()
# a = 1