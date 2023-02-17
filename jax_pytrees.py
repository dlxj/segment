
# import jax
# import jax.numpy as jnp
# out = jax.vmap(lambda x: x ** 2)(jnp.arange(1))  
# print(out)


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