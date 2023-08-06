
from pycamia import info_manager

__info__ = info_manager(
    project = "PyCAMIA",
    package = "batorch",
    fileinfo = "The inherited tensor from 'torch' with batch.",
    requires = "torch"
)

__all__ = """
    CPU
    GPU
    GPUs
    Tensor
    Size
    set_device
    get_device
    to_device
    turn_on_autodevice
    turn_off_autodevice
    get_cpu_memory_used
    get_gpu_memory_used
    inv
    diag
    batch_tensor
    channel_tensor
""".split()

import builtins, sys
from functools import wraps
from typing import Generator
from .tensorfunc import __all__ as tf_list
from .torch_namespace import *
from .device import GB, CPU, GPU, GPUs, AutoDevice, FixedDevice

with __info__:
    import torch
    import batorch as bt
    from pycamia import ByteSize
    from pycamia import avouch, touch, alias, execblock, void
    from pycamia import get_alphas, arg_tuple, max_argmax
    from pycamia import argmax as _argmax, item, to_list
    from pyoverload import Type, Array, isoftype, Iterable

_int = builtins.int
_min = builtins.min
_max = builtins.max
_abs = builtins.abs
_any = builtins.any
_all = builtins.all
_sum = builtins.sum
_range = builtins.range
_float = builtins.float
_num = (_int, _float)

_device = AutoDevice(verbose=True, always_proceed=True)
_total_cpu_memory_used = 0
_total_gpu_memory_used = 0

new_dim_inherit_methods = """multiply multiple""".split()
new_dim_methods = """unsqueeze unsqueeze_ multiply multiple""".split()
old_dim_methods = """
    squeeze squeeze_ transpose transpose_ movedim movedim_ splitdim repeated amplify ample sample pick split flip
    cummin cummax cumsum cumprod sum prod min max median mean std argmin argmax
""".split()
one_dim_methods_last = """multiply multiple repeated amplify ample sample split flip""".split()
one_dim_methods_first = """splitdim""".split()
avouch(all(x in new_dim_methods for x in new_dim_inherit_methods))

def set_device(device):
    if isinstance(device, AutoDevice): new_device = device
    elif isinstance(device, torch.device): new_device = FixedDevice(device)
    else: raise TypeError("Invalid device type. ")
    global _device
    _device = new_device

def get_device():
    global _device
    return _device

def to_device(x):
    global _device
    return _device(x)

def turn_on_autodevice(): _device.turn_on()
def turn_off_autodevice(): _device.turn_off()

def get_cpu_memory_used():
    global _total_cpu_memory_used
    return ByteSize(_total_cpu_memory_used)

def get_gpu_memory_used():
    global _total_gpu_memory_used
    return ByteSize(_total_gpu_memory_used)

def collect_memory(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret.device == CPU.main_device:
            global _total_cpu_memory_used
            _total_cpu_memory_used += ret.byte_size()
        else:
            global _total_gpu_memory_used
            _total_gpu_memory_used += ret.byte_size()
        return ret
    return wrapper

def kwget(kwargs, key, default):
    if kwargs is None: return default
    else: return kwargs.get(key, default)


class Size(tuple):

    @classmethod
    def __new_shape__(cls, shape, **kwargs):
        avouch(isinstance(shape, tuple), f"Invalid initialization of bt.Size (need tuple): {shape}.")
        with_batch = kwargs.get("with_batch", False)
        feature_range = kwargs.get("feature_range", None)
        n_sequence_dim = kwargs.get("n_sequence_dim", 0)
        avouch(isinstance(with_batch, bool), f"Invalid initialization of bt.Size (non bool argument 'with_batch': {type(with_batch)}; If you did not input it manually, reach out for developers with Error Code: B522).")
        avouch(isinstance(n_sequence_dim, int), f"Invalid initialization of bt.Size (non int argument 'n_sequence_dim': {type(n_sequence_dim)}; If you did not input it manually, reach out for developers with Error Code: B523).")
        avouch(feature_range is None or isinstance(feature_range, list) and len(feature_range) == 2, f"Invalid initialization of bt.Size (non list argument 'feature_range': {type(feature_range)}; If you did not input it manually, reach out for developers with Error Code: B524).")
        input_feature = feature_range is not None

        raw_size = []
        for i, x in enumerate(shape):
            # time/sequence dimension
            if isinstance(x, list) and len(x) == 1 and isinstance(x[0], list):
                if len(x[0]) > 0: raw_size.extend(x[0]); n_sequence_dim += len(x[0])
                else: n_sequence_dim += 1; raw_size.append(-1)
                continue
            avouch(n_sequence_dim == 0, f"Invalid initialization of bt.Size (sequence dimensions can only be the last dimensions): {shape}.")
            if isinstance(x, _int):
                avouch(x >= -1, "Invalid initialization of bt.Size (Size cannot have negative values except -1 indicating an arbitrary number): {shape}.")
                raw_size.append(x); continue
            # batch dimension
            if isinstance(x, dict) and len(x) == 0:
                avouch(i == 0, f"Invalid initialization of bt.Size (batch dimension can only be the first dimension): {shape}.")
                raw_size.append(-1); with_batch = True; continue
            if isinstance(x, set) and len(x) == 1:
                avouch(i == 0, f"Invalid initialization of bt.Size (batch dimension can only be the first dimension): {shape}.")
                raw_size.append(x.pop()); with_batch = True; continue
            # feature dimension
            if feature_range is not None: i += feature_range[1] - feature_range[0] - 1
            if isinstance(x, list):
                avouch(feature_range is None or feature_range[1] == 0 or feature_range[1] == i, f"Invalid initialization of bt.Size (feature dimensions should be neighboring dimensions): {shape}.")
                avouch(all([isinstance(y, _int) for y in x]), f"Invalid initialization of bt.Size (representation for feature dimensions should be a list of integers): {shape}.")
                if len(x) == 0: raw_size.append(-1); len_feat = 1
                else: raw_size.extend(x); len_feat = len(x)
                if feature_range is None: feature_range = [i, i + len_feat]
                else: feature_range[1] += len_feat
                continue
            avouch(None, f"Invalid initialization of bt.Size (unacceptable type, please contact the developers for more information; Error Code: B521): {shape}.")

        n_dim = len(raw_size)
        if input_feature: feature_range = [x if x >= 0 else x + n_dim for x in feature_range]

        return cls.__new_raw__(raw_size, with_batch, feature_range, n_sequence_dim)

    @classmethod
    def __new_size__(cls, size, **kwargs):
        avouch(isinstance(size, Size), f"Invalid initialization of bt.Size (need bt.Size object): {size}")
        kwargs.setdefault("with_batch", size.with_batch)
        kwargs.setdefault("feature_range", size.feature_range)
        kwargs.setdefault("n_sequence_dim", size.n_sequence_dim)
        return cls.__new_raw__(list(size), **kwargs)

    @classmethod
    def __new_raw__(cls, size, with_batch=False, feature_range=None, n_sequence_dim=0):
        if feature_range is not None: avouch(isinstance(feature_range, list) and len(feature_range) == 2, f"Invalid initialization of bt.Size (argument 'feature_range' has length {len(feature_range)} instead of 2; If you did not input it manually, reach out for developers with Error Code: B525).")
        avouch(not with_batch or feature_range is None or feature_range[0] > 0, f"Invalid initialization of bt.Size (conflict betach and feature dimensions; If you did not input it manually, reach out for developers with Error Code: B526).")
        self = super().__new__(cls, size)
        self.with_batch = with_batch
        self.feature_range = feature_range
        self.n_sequence_dim = n_sequence_dim
        self.n_dim = self.ndim = len(size)
        return self

    def __new__(cls, *args, **kwargs):
        """bt.Size
        Usages:
            bt.Size(shape: torch.Tensor/bt.Tensor/bt.Size/generator/tuple/str, with_batch=False, feature_range=None)
            bt.Size(*shape: python_repr[int/len0-list/len1-list/len0-dict/len1-set], with_batch=False, feature_range=None)
        """
        if len(args) == 1 and hasattr(args[0], 'shape'): return Size.__new_shape__(arg.shape, **kwargs)
        if len(args) == 1 and isinstance(args[0], Generator): return Size.__new_shape__(tuple(args[0]), **kwargs)
        if len(args) == 1 and isinstance(args[0], tuple): return Size.__new_shape__(args[0], **kwargs)
        if len(args) == 1 and isinstance(args[0], str): return Size.__new_shape__(eval(args[0]), **kwargs)
        if len(args) == 1 and isinstance(args[0], Size): return Size.__new_size__(args[0], **kwargs)
        return Size.__new_shape__(args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.with_batch = self.with_batch
        self.feature_range = self.feature_range
        self.n_sequence_dim = self.n_sequence_dim
        self.n_dim = self.n_dim
        self.ndim = self.n_dim

    ## batch dimension:
    @property
    def has_batch(self): return self.with_batch

    @alias("batch_dim_", "batch_dimension_", "with_batchdim")
    def with_batch_(self, wbatch):
        if wbatch == 0: wbatch = True
        avouch(isinstance(wbatch, bool), "'bt.Size.with_batch_' only takes input bool or integer 0.")
        self.with_batch = wbatch
        return self

    @alias("nbatch", "batch_size")
    @property
    def n_batch(self):
        avouch(self.with_batch, f"'bt.Size' object {self} does not have batch dimension.")
        return self[0]

    @alias("nbatchdim")
    @property
    def n_batch_dim(self):
        return _int(self.with_batch)

    ## channel dimension: 
    @property
    def has_channel(self): return self.n_feature_dim == 1

    @alias("channel_dimension")
    @property
    def channel_dim(self):
        avouch(self.n_feature_dim == 1, f"Cannot get channel dimension from size with {self.n_feature_dim} feature dimensions.")
        return self.n_feature_dim[0]

    @channel_dim.setter
    def channel_dim(self, dim):
        avouch(dim is None or isinstance(dim, _int) and - self.n_dim <= dim < self.n_dim, f"Channel dimension of {self} should in [{-self.n_dim}, {self.n_dim - 1}].")
        return self.channel_dim_(dim)

    @alias("channel_dimension_", "with_channeldim")
    def channel_dim_(self, dim):
        avouch(dim is None or isinstance(dim, _int) and - self.n_dim <= dim < self.n_dim, f"Channel dimension of {self} should in [{-self.n_dim}, {self.n_dim - 1}].")
        if dim is None: self.feature_range = None
        else: self.feature_range = [dim, dim + 1]
        return self

    @alias("nchannel", "channel_size")
    @property
    def n_channel(self):
        avouch(self.n_feature_dim == 1, f"Cannot get channel dimension from size with {self.n_feature_dim} feature dimensions.")
        return self[self.channel_dim]

    @alias("nchanneldim")
    @property
    def n_channel_dim(self):
        return _int(self.has_channel)

    ## feature dimensions:
    @property
    def has_feature(self): return self.feature_range is not None

    @alias("with_featurerange")
    def feature_range_(self, frange):
        avouch(frange is None or isinstance(frange, list) and len(frange) == 2, "'bt.Size.feature_range_' only takes input list of length 2.")
        if frange is not None: avouch(self.n_batch_dim <= frange[0] < self.sequence_start and self.n_batch_dim <= frange[1] < self.sequence_start, 
                                      f"Feature range should be between {self.n_batch_dim} and {self.sequence_start}, or there will be conflict. ")
        self.feature_range = frange
        return self

    @property
    def feature_start(self): return self.sequence_start if self.feature_range is None else self.feature_range[0]

    @feature_start.setter
    def feature_start(self, dim):
        if dim < 0: dim += self.n_dim
        avouch(self.n_batch_dim <= dim < self.sequence_start, f"Feature start should be between {self.n_batch_dim} and {self.sequence_start}, or there will be conflict. ")
        if self.feature_range is None: self.feature_range = [dim, self.n_dim]
        else: self.feature_range[0] = dim

    @property
    def feature_stop(self): return self.sequence_start if self.feature_range is None else self.feature_range[1]

    @feature_stop.setter
    def feature_stop(self, dim):
        if dim < 0: dim += self.n_dim
        avouch(self.n_batch_dim <= dim < self.sequence_start, f"Feature stop should be between {self.n_batch_dim} and {self.sequence_start}, or there will be conflict. ")
        if self.feature_range is None: self.feature_range = [self.n_batch_dim, dim]
        else: self.feature_range[1] = dim

    @alias("nfeaturedim")
    @property
    def n_feature_dim(self):
        return self.feature_stop - self.feature_start

    @alias("nfeature")
    @property
    def n_feature(self):
        avouch(self.feature_range is not None, f"Cannot get feature dimensions from size {self}.")
        p = 1
        for i in range(*self.feature_range): p *= self[i]
        return p

    @alias("feature_size")
    @property
    def feature(self):
        return self[slice(self.feature_start, self.feature_stop)]

    def with_feature(self, size):
        avouch(len(size) == self.n_feature_dim, f"Cannot substitute feature in {self} by {size} as their dimensions are not the same.")
        return (self[:self.feature_start] + size + self[self.feature_stop:]).feature_range_(self.feature_range)

    ## sequence dimensions:
    @alias("has_time")
    @property
    def has_sequence(self): return self.n_sequence_dim > 0

    @alias("with_ntimedim")
    @alias("with_nsequencedim")
    @alias("n_time_dim_")
    def n_sequence_dim_(self, number):
        avouch(number is None or isinstance(number, int), "'bt.Size.n_sequence_dim_' only takes integer.")
        if number is None: number = 0
        self.n_sequence_dim = number
        return self

    @alias("with_timedim")
    @alias("with_sequencedim")
    @alias("time_dim_")
    def sequence_dim_(self, with_seq):
        avouch(with_seq is None or isinstance(with_seq, bool), "'bt.Size.sequence_dim_' only takes bool.")
        self.n_sequence_dim = 1 if with_seq else 0
        return self

    @property
    def sequence_start(self): return self.n_dim - self.n_sequence_dim

    @sequence_start.setter
    def sequence_start(self, dim):
        if dim < 0: dim += self.n_dim
        self.n_sequence_dim = self.n_dim - dim

    @alias("ntime")
    @alias("ntimeline")
    @alias("nsequence")
    @alias("n_time")
    @alias("n_timeline")
    @property
    def n_sequence(self):
        avouch(self.n_sequence_dim > 0, f"Cannot get sequence dimensions from size {self}.")
        p = 1
        for i in range(-self.n_sequence_dim, 0): p *= self[i]
        return p

    @alias("time_size")
    @alias("sequence_size")
    @property
    def sequence(self):
        return self[self.sequence_start:]

    @alias("with_time")
    def with_sequence(self, size):
        avouch(len(size) == self.n_sequence_dim, f"Cannot substitute sequence in {self} by {size} as their dimensions are not the same.")
        return (self[: self.sequence_start] + size).n_sequence_dim_(self.n_sequence_dim)

    ## space dimensions:
    @property
    def has_space(self): return self.n_space_dim > 0

    @alias("nspacedim")
    @property
    def n_space_dim(self):
        return self.n_dim - self.feature_stop + self.feature_start - self.n_batch_dim - self.n_sequence_dim

    @alias("leftspacedim")
    @property
    def left_space_dim(self):
        return self.feature_start - self.n_batch_dim

    @alias("rightspacedim")
    @property
    def right_space_dim(self):
        return self.n_dim - self.feature_stop - self.n_sequence_dim

    @alias("nspace")
    @property
    def n_space(self):
        avouch(self.n_space_dim > 0, f"Cannot get space dimensions from size {self}.")
        p = 1
        for i in range(self.n_batch_dim, self.feature_start): p *= self[i]
        for i in range(self.feature_stop, self.sequence_start): p *= self[i]
        return p

    @alias("space_size")
    @property
    def space(self):
        return self[self.n_batch_dim: self.feature_start] + self[self.feature_stop: self.sequence_start]

    def with_space(self, size):
        avouch(len(size) == self.n_space_dim, f"Cannot substitute space in {self} by {size} as their dimensions are not the same.")
        return self[:self.n_batch_dim] + size[:self.feature_start - self.n_batch_dim] + self.feature + size[self.feature_start - self.n_batch_dim:] + self.sequence

    ## special dimensions:
    @property
    def has_special(self): return self.has_batch or self.has_feature or self.has_sequence

    @alias("nspecialdim")
    @property
    def n_special_dim(self):
        return self.n_batch_dim + self.feature_stop - self.feature_start + self.n_sequence_dim

    @property
    def special_dims(self):
        return ([0] if self.with_batch else []) + list(range(self.feature_start, self.feature_stop)) + list(range(self.sequence_start, self.n_dim))

    def special_from(self, other):
        avouch(isinstance(other, (Size, Tensor)), f"Invalid input for Size.special_from: {type(other)}. ")
        avouch(self.n_dim == other.n_dim, f"Dimension mismatch when inheriting special dimensions: {other} to {self}. ")
        self.with_batch = other.with_batch
        self.feature_range = other.feature_range
        self.n_sequence_dim = other.n_sequence_dim
        return self

    def remove_special(self):
        self.with_batch = False
        self.feature_range = None
        self.n_sequence_dim = 0
        return self

    ## all dimensions:
    @alias("nele")
    @property
    def n_ele(self):
        p = 1
        for i in range(self.n_dim): p *= self[i]
        return p

    ## methods:
    @alias("clone")
    def copy(self): return Size(self)

    @alias("raw")
    def tuple(self): return tuple(self)

    @property
    def python_repr(self):
        batch = {self[0]}
        feature = list(self[self.feature_start: self.feature_stop])
        sequence = [list(self[self.sequence_start:])]
        return (((batch,) if self.with_batch else tuple()) + self[self.n_batch_dim: self.feature_start] + 
                ((feature,) if len(feature) > 0 else tuple()) + self[self.feature_stop: self.sequence_start] + ((sequence,) if self.n_sequence_dim > 0 else tuple())).tuple()

    @alias("__repr__")
    def __str__(self):
        rep = self.python_repr
        return f"batorch.Size{rep}".replace(',)', ')')
    
    ## operations:
    def __getitem__(self, k):
        if isinstance(k, _int): return super().__getitem__(k)
        avouch(isinstance(k, slice), f"Slicing of 'bt.Size' only takes integers or slices, not {k}. ")
        s, e = k.start, k.stop
        if s is None: s = 0
        if e is None: e = self.n_dim
        if s < 0: s += self.n_dim
        if e < 0: e += self.n_dim
        with_batch = s == 0 and e > 0 and self.with_batch
        if self.feature_range is None: feature_range = None
        else:
            feature_range = [_min(_max(x - s, 0), e - s) for x in self.feature_range]
            if feature_range[0] == feature_range[1]: feature_range = None
        n_sequence_dim = _min(_max(self.n_sequence_dim + e - self.n_dim, 0), e - s)
        return self.__class__.__new_raw__(super().__getitem__(k), with_batch=with_batch, feature_range=feature_range, n_sequence_dim=n_sequence_dim)
    
    @alias('__iadd__')
    def __add__(self, other):
        avouch(isinstance(other, tuple), "Only Size + tuple is available for 'bt.Size' as a python tuple, please use `size << 2` to increase the space for size numerically. ")
        feature_range = self.feature_range
        n_sequence_dim = 0 if len(other) > 0 else self.n_sequence_dim
        if isinstance(other, Size) and len(other) > 0:
            if self.feature_range is None:
                if other.feature_range is not None: feature_range = [x + self.n_dim for x in other.feature_range]
            elif other.feature_range is not None and self.feature_range[1] == self.n_dim and other.feature_range[0] == 0: feature_range = [self.feature_range[0], other.feature_range[1] + self.n_dim]
            if other.n_sequence_dim == other.n_dim: n_sequence_dim = other.n_sequence_dim + self.n_sequence_dim
            else: n_sequence_dim = other.n_sequence_dim
        return self.__class__.__new_raw__(super().__add__(other), with_batch=self.with_batch, feature_range=feature_range, n_sequence_dim=n_sequence_dim)
        
    def __radd__(self, other):
        avouch(isinstance(other, tuple), "Only tuple + Size is available for 'bt.Size' as a python tuple, please use `size <<(>>) 2` to increase(decrease) the space for size numerically. ")
        if isinstance(other, Size): return other.__add__(self)
        return self.__class__.__new_raw__(other + self.tuple(), with_batch=False if len(other) > 0 else self.with_batch, feature_range=[x + len(other) for x in self.feature_range] if self.feature_range is not None else None, n_sequence_dim=self.n_sequence_dim)
    
    @alias('__imul__', '__rmul__')
    def __mul__(self, other):
        avouch(isinstance(other, _int), "Only Size * int is available for 'bt.Size' as a python tuple, please use `size **(//) 2` to multiply(devide) the space for size numerically. ")
        return self.__class__.__new_raw__(super().__mul__(other), with_batch=self.with_batch, 
                                          feature_range=[0, self.n_dim * other] if self.n_feature_dim == self.n_dim else self.feature_range,
                                          n_sequence_dim=self.n_dim * other if self.n_sequence_dim == self.n_dim else self.n_sequence_dim)
    
    ## element-wise operations:
    @staticmethod
    def __op__(self, other, *, operation):
        avouch(isinstance(self, Size), "Inner problem: if 'bt.Size.__op__' is not called manually, please contact the developers with Error Code: B526")
        avouch(isinstance(other, (_num, tuple)), f"Element-wise operations are only used for numbers or tuples, not {type(other)}.")
        op = lambda x, y: _max(_int(operation(x, y)), 1) if x > 0 else -1
        if isinstance(other, _num): return self.with_space(op(x, other) for x in self.space)
        other_batch = 0
        other_feature = (0,)
        other_sequence = (0,)
        other_space = (0,)
        if isinstance(other, Size):
            if other.with_batch: other_batch = other.n_batch
            if other.has_feature: other_feature = other.feature
            if other.has_sequence: other_sequence = other.sequence
            if other.has_space: other_space = other.space
        elif isinstance(other, tuple): other_space = other
        else: avouch(None, f"Cannot perform element-wise operation between types {type(self)} and {type(other)}. ")
        if len(other_feature) == 1: other_feature *= self.n_feature_dim
        if len(other_sequence) == 1: other_sequence *= self.n_sequence_dim
        if len(other_space) == 1: other_space *= self.n_space_dim
        avouch(isinstance(other_batch, _num), f"Invalid operation between {self} and {other}: conflict in batch dimension. ")
        avouch(isinstance(other_feature, tuple) and len(other_feature) == self.n_feature_dim, f"Invalid operation between {self} and {other}: conflict in feature size. ")
        avouch(isinstance(has_sequence, tuple) and len(has_sequence) == self.n_sequence_dim, f"Invalid operation between {self} and {other}: conflict in sequence size. ")
        avouch(isinstance(other_space, tuple) and len(other_space) == self.n_space_dim, f"Invalid operation between {self} and {other}: conflict in space size. ")
        return self.__class__.__new_raw__(tuple(
            op(x, other_batch) if i == 0 and self.with_batch else (
            op(x, other_space[i - self.n_batch_dim]) if self.n_batch_dim <= i < self.feature_start else (
            op(x, other_feature[i - self.feature_start]) if self.feature_start <= i < self.feature_stop else (
            op(x, other_space[i - self.feature_stop + self.feature_start - self.n_batch_dim]) if self.feature_stop <= i < self.sequence_start else (
            op(x, other_sequence[i - self.sequence_start])
        )))) for i, x in enumerate(self)), with_batch=self.with_batch, feature_range=self.feature_range, n_sequence_dim=self.n_sequence_dim)
        
    @alias('__ilshift__', '__rlshift__')
    def __lshift__(self, other): return Size.__op__(self, other, operation=lambda x, y: x + y)
    @alias('__irshift__')
    def __rshift__(self, other): return Size.__op__(self, other, operation=lambda x, y: x - y)
    def __rrshift__(self, other): return Size.__op__(self, other, operation=lambda x, y: y - x)
    @alias('__ipow__', '__rpow__')
    def __pow__(self, other): return Size.__op__(self, other, operation=lambda x, y: x * y)
    @alias('__ifloordiv__')
    def __floordiv__(self, other): return Size.__op__(self, other, operation=lambda x, y: x // y)
    def __rfloordiv__(self, other): return Size.__op__(other, self, operation=lambda x, y: y // x)
    
    def __xor__(self, other):
        avouch(isinstance(self, Size) and isinstance(other, tuple), "xor for bt.Size only accept two tuples.")
        if not isinstance(other, Size): other = Size.__new_raw__(other)
        # batch:
        swap = False
        if not self.has_batch and other.has_batch: self, other = other, self; swap = True
        if self.has_batch and not other.has_batch: other = Size({1}) + other
        if swap: self, other = other, self
        
        # sequence:
        swap = False
        if not self.has_sequence and other.has_sequence: self, other = other, self; swap = True
        if self.has_sequence and not other.has_sequence: other = other + Size([[1] * self.n_sequence_dim])
        if swap: self, other = other, self
        avouch(self.n_sequence_dim == other.n_sequence_dim, f"Mismatched sequence dimensions: {self.sequence} and {other.sequence}.")
        
        # feature:
        swap = False
        if not self.has_feature and other.has_feature: self, other = other, self; swap = True
        if self.has_feature and not other.has_feature:
            avouch(other.n_space_dim == 0 or other.n_space_dim == self.n_space_dim, f"Mismatched space dimensions: {self.space} and {other.space}.")
            if other.n_space_dim == 0: other = other[:other.n_batch_dim] + Size((1,) * (self.feature_start - self.n_batch_dim) + ([1],) * (self.n_feature_dim) + (1,) * (self.n_dim - self.n_sequence_dim - self.feature_stop)) + other[other.sequence_start:]
            else: other = other[:self.feature_start] + Size([1] * self.n_feature_dim) + other[self.feature_start:]
        if swap: self, other = other, self
        avouch(self.n_feature_dim == other.n_feature_dim, f"Mismatched feature dimensions: {self.feature} and {other.feature}.")
        
        # left space:
        swap = False
        if self.left_space_dim == 0 and other.left_space_dim > 0: self, other = other, self; swap = True
        if self.left_space_dim > 0 and other.left_space_dim == 0: other = other[:other.n_batch_dim] + Size((1,) * self.left_space_dim) + other[other.feature_start:]
        if swap: self, other = other, self
        avouch(self.left_space_dim == other.left_space_dim, f"Mismatched space dimensions: {self.space} and {other.space}.")
        
        # righ space:
        swap = False
        if self.right_space_dim == 0 and other.right_space_dim > 0: self, other = other, self; swap = True
        if self.right_space_dim > 0 and other.right_space_dim == 0: other = other[:other.feature_stop] + Size((1,) * self.right_space_dim) + other[other.feature_stop:]
        if swap: self, other = other, self
        avouch(self.right_space_dim == other.right_space_dim, f"Mismatched space dimensions: {self.space} and {other.space}.")
        
        return self, other
            
        # avouch(self.with_batch and other.has_feature or self.has_feature and other.with_batch, f"Inner problem: 'bt.Size.__xor__' failed to match sizes {self} and {other}. Please contact the developers for more information (Error Code: B529). ")
        # if isinstance(other, Size) and not self.has_special: self, other = other, self
        # if not isinstance(other, Size) or not other.has_special:
        #     if len(other) == self.n_dim: pass
        #     elif len(other) == self.n_space_dim: other = ((1,) if self.with_batch else tuple()) + other[:self.feature_start - self.n_batch_dim] + (1,) * self.n_feature_dim + other[self.feature_start - self.n_batch_dim:]
        #     elif len(other) == self.n_feature_dim: other = (1,) * self.feature_start + other + (1,) * (self.n_dim - self.n_feature_dim - self.feature_start)
        #     elif len(other) == self.n_dim - 1 and self.with_batch: other = (1,) + other
        #     else: avouch(None, f"Cannot match Sizes: tuple {other} to {self}")
        #     return self, other
        # if self.has_feature and other.has_feature:
        #     avouch(self.n_feature_dim == other.n_feature_dim, f"Cannot match Sizes with different feature size: {self} and {other}")
        #     if self.right_space_dim == 0 and other.left_space_dim == 0: other = other[:_int(other.with_batch)] + other[other.feature_stop:] + other.feature
        #     if other.right_space_dim == 0 and self.left_space_dim == 0: other = other[:_int(other.with_batch)] + other.feature + other[_int(other.with_batch):other.feature_start]
        #     if self.left_space_dim > 1 and other.left_space_dim == 1 and not other.with_batch: other.with_batch_(True)
        #     if other.left_space_dim > 1 and self.left_space_dim == 1 and not self.with_batch: self.with_batch_(True)
        #     if self.left_space_dim == 0: self = self[:self.n_batch_dim] + (1,) * other.left_space_dim + self[self.n_batch_dim:]
        #     if other.left_space_dim == 0: other = other[:_int(other.with_batch)] + (1,) * self.left_space_dim + other[_int(other.with_batch):]
        #     if self.right_space_dim == 0: self = self + (1,) * other.right_space_dim
        #     if other.right_space_dim == 0: other = other + (1,) * self.right_space_dim
        #     if self.left_space_dim == other.left_space_dim + 1 and not self.with_batch: self.with_batch_(True)
        #     if other.left_space_dim == self.left_space_dim + 1 and not other.with_batch: other.with_batch_(True)
        #     avouch(self.left_space_dim == other.left_space_dim and self.right_space_dim == other.right_space_dim, f"Inner problem: 'bt.Size.__xor__' failed to match sizes {self} and {other}. Please contact the developers for more information (Error Code: B528). ")
        #     if self.with_batch and not other.with_batch: other = ((1,) + other).with_batch_(True)
        #     if not self.with_batch and other.with_batch: self = ((1,) + self).with_batch_(True)
        #     avouch(self.with_batch == other.with_batch, "Inner problem: if 'bt.Size.__xor__' is not called manually, please contact the developers with Error Code: B527")
        #     return self, other
        # if not self.has_feature and not other.has_feature:
        #     if self.n_space_dim > 1 and other.n_space_dim == 1 and not other.with_batch: other.with_batch_(True)
        #     if other.n_space_dim > 1 and self.n_space_dim == 1 and not self.with_batch: self.with_batch_(True)
        #     if self.n_space_dim == 0: self = self + (1,) * other.n_space_dim
        #     if other.n_space_dim == 0: other = other + (1,) * self.n_space_dim
        #     if self.n_space_dim == other.n_space_dim + 1 and not self.with_batch: self.with_batch_(True)
        #     if other.n_space_dim == self.n_space_dim + 1 and not other.with_batch: other.with_batch_(True)
        #     avouch(self.n_space_dim == other.n_space_dim, f"Inner problem: 'bt.Size.__xor__' failed to match sizes {self} and {other}. Please contact the developers for more information (Error Code: B528). ")
        #     if self.with_batch and not other.with_batch: other = ((1,) + other).with_batch_(True)
        #     if not self.with_batch and other.with_batch: self = ((1,) + self).with_batch_(True)
        #     avouch(self.with_batch == other.with_batch, "Inner problem: if 'bt.Size.__xor__' is not called manually, please contact the developers with Error Code: B527")
        #     return self, other
        # if self.with_batch == other.with_batch:
        #     self_right, other_right = self[self.n_batch_dim:] ^ other[_int(other.with_batch):]
        #     return self[:self.n_batch_dim] + self_right, other[:_int(other.with_batch)] + other_right
        # avouch(self.with_batch and other.has_feature or self.has_feature and other.with_batch, f"Inner problem: 'bt.Size.__xor__' failed to match sizes {self} and {other}. Please contact the developers for more information (Error Code: B529). ")
        # avouch(None, "bt.Size.__xor__ does not accept two sizes with batch in one of them and feature in the other. ")

def tensor(data, *, dtype=None, device=None, requires_grad=False, pin_memory=False): ...
def as_tensor(data, dtype=None, device=None): ...
def empty(*size, out=None, dtype=None, layout=torch.strided, device=None, requires_grad=False, pin_memory=False, memory_format=torch.contiguous_format): ...
def ones(*size, out=None, dtype=None, layout=torch.strided, device=None, requires_grad=False): ...
def zeros(*size, out=None, dtype=None, layout=torch.strided, device=None, requires_grad=False): ...
def empty_like(input, *, dtype=None, layout=None, device=None, requires_grad=False, memory_format=torch.preserve_format): ...
def ones_like(input, *, dtype=None, layout=None, device=None, requires_grad=False, memory_format=torch.preserve_format): ...
def zeros_like(input, *, dtype=None, layout=None, device=None, requires_grad=False, memory_format=torch.preserve_format): ...

class Tensor(torch.Tensor):
    
    @staticmethod
    def _make_subclass(cls, torch_tensor, requires_grad=None, device=None, with_batch=None, feature_range=void, **_):
        avouch(not _, "bt.Tensor only accept keyword arguments requires_grad, device, with_batch and feature_range")
        if device is not None and torch_tensor.device != device:
            avouch(isinstance(device, AutoDevice), "Please use `AutoDevice` in batorch.Tensor._make_subclass. Please contact the developers if you did not use Tensor._make_subclass directly (Error Code: B530). ")
            torch_tensor = device(torch_tensor)
        if isinstance(torch_tensor, Tensor) and cls == Tensor:
            if requires_grad is not None: torch_tensor.requires_grad = requires_grad
            if with_batch is not None: torch_tensor.with_batch = with_batch
            if feature_range is not void: torch_tensor.feature_range = feature_range
            return torch_tensor
        if requires_grad is None: requires_grad = torch_tensor.requires_grad
        self = torch.Tensor._make_subclass(cls, torch_tensor, requires_grad)
        if with_batch is None: with_batch = torch_tensor.with_batch if isinstance(torch_tensor, Tensor) else False
        if feature_range is void: feature_range = torch_tensor.feature_range if isinstance(torch_tensor, Tensor) else None
        self.with_batch = with_batch
        self.feature_range = feature_range
        return self

    @collect_memory
    def __new__(cls, *args, **kwargs):
        """bt.Tensor
        Usages:
            bt.Tensor(tensor: list/torch.Tensor/bt.Tensor/tensor with 'shape'/tensor with method '__tensor__', requires_grad=None, device=None, with_batch=None, feature_range=void)
            bt.Tensor(shape: tuple, requires_grad=None, device=None, with_batch=None, feature_range=void)
            bt.Tensor(*shape: int, requires_grad=None, device=None, with_batch=None, feature_range=void)
        """
        if len(args) >= 1 and isinstance(args[0], torch.Tensor): return Tensor._make_subclass(cls, *args, **kwargs)
        if len(args) >= 1 and hasattr(args[0], '__tensor__'): return Tensor._make_subclass(cls, args[0].__tensor__(), *args[1:], **kwargs)
        device = kwargs.pop('device', _device)
        if isinstance(device, AutoDevice): device = device.main_device
        if len(args) >= 1 and hasattr(args[0], 'shape') or isinstance(args[0], list): return Tensor._make_subclass(cls, torch.tensor(args[0], requires_grad=False, device=device), *args[1:], **kwargs)
        return Tensor._make_subclass(cls, super().__new__(torch.Tensor, *args, device=device), **kwargs)

    def __init__(self, *args, **kwargs):
        self.with_batch = self.with_batch
        self.feature_range = self.feature_range

    @property
    def shape(self): return Size.__new_raw__(super().shape, with_batch=self.with_batch, feature_range=self.feature_range)

    @alias("__str__")
    def __repr__(self, *args, **kwargs):
        string = super().__repr__(*args, **kwargs)
        if 'shape=' not in string:
            string = string.rstrip(')') + f', shape={self.shape})'
        return string.replace("tensor", "Tensor")
    
    ## utilities
    def byte_size(self):
        return ByteSize(self.element_size() * self.numel())
    
    ## dtypes
    @alias("as_type")
    def astype(self, dt):
        """
            numpy dtype v.s. torch dtype:
            ==============================
            numpy type // torch type
            ------------------------------
            void0, void::void // 
            object0, object_::object // 
            bool8, bool_::bool // torch.bool
            byte, int8::int8 // torch.int8
            short, int16::int16 // torch.short, torch.int16
            int32, intc::int32 // torch.int, torch.int32
            int0, int_, int64, intp, longlong, signedinteger::int64 // torch.long, torch.int64
            ubyte, uint8::uint8 // torch.uint8
            ushort, uint16::uint16 // 
            uint32, uintc::uint32 // 
            uint, uint0, uint64, Uint64, uintp, ulonglong::uint64 // 
            // torch.bfloat16 # 16bit, 范围大如32bit但精度低
            half, float16::float16 // torch.half, torch.float16
            single, float32::float32 // torch.float, torch.float32
            double, float64, float_, longdouble, longfloat, number::float64 // torch.double, torch.float64
            // torch.complex32
            csingle, complex64, singlecomplex::complex64 // torch.cfloat, torch.complex64
            cdouble, cfloat, clongdouble, clongfloat, complex_, complex128, longcomplex::complex128 // torch.cdouble, torch.complex128
            str0, str_, Str0::str // 
            bytes0, bytes_, string_::bytes // 
            datetime64::datetime64 // 
            timedelta64::timedelta64 // 
            # 量子计算类型
            // torch.qint8
            // torch.qint32
            // torch.quint8
            // torch.quint4x2
        """
        if isinstance(dt, str): return super().type(dt.replace('bt.', 'torch.')).as_subclass(self.__class__)
        if hasattr(dt, 'dtype'): dt = dt.dtype
        if isinstance(dt, torch.dtype): return super().type(dt).as_subclass(self.__class__)
        import numpy as np
        dt_name = np.dtype(dt).name
        dtype_map = {'uint16': "int32", 'uint32': "int64", 'uint64': "int64"}
        torch_dt = getattr(torch, dtype_map.get(dt_name, dt_name), None)
        avouch(torch_dt is not None, f"Invalid dtype {dt}: {dt_name} cannot be converted into torch dtype.")
        return super().type(torch_dt).as_subclass(self.__class__)

    def type(self, dt=None):
        if dt is None: return super().type().replace("torch.", "bt.")
        else: return self.astype(dt)
