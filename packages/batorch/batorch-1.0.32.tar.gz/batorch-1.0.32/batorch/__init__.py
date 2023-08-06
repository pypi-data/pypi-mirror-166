
from pycamia import info_manager

__info__ = info_manager(
    project = 'PyCAMIA',
    package = 'batorch',
    author = 'Yuncheng Zhou',
    create = '2021-12',
    version = '1.0.31',
    contact = 'bertiezhou@163.com',
    keywords = ['torch', 'batch', 'batched data'],
    description = "'batorch' is an extension of package torch, for tensors with batch dimensions. ",
    requires = ['pycamia', 'torch', 'pynvml']
).check()

import torch
distributed = torch.distributed
autograd = torch.autograd
random = torch.random
optim = torch.optim
utils = torch.utils
linalg = torch.linalg
from .torchext import __all__
for f in __all__:
    exec(f"from .torchext import {f}")
    setattr(torch, f, eval(f))

import math
from .tensor import Tensor, tensor
e = tensor(math.e)
nan = tensor(math.nan)
inf = tensor(math.inf)
pi = tensor(math.pi)

from . import nn
from .device import free_memory_amount, all_memory_amount
from .tensor import CPU, GPU, GPUs, Tensor, Size, set_device, get_device, to_device, turn_on_autodevice, turn_off_autodevice, get_cpu_memory_used, get_gpu_memory_used, inv, diag, batch_tensor, channel_tensor, zeros, zeros_like, ones, ones_like, empty, empty_like, rand, rand_like, randn, randn_like, full, full_like, randint, randint_like, eye, eye_as, eye_like, cat, stack, t, unsqueeze, squeeze, tensor, tr, trace, bfloat16, bool, cdouble, cfloat, complex128, complex32, complex64, double, float, float16, float32, float64, half, int, int16, int32, int64, int8, long, qint32, qint8, quint8, short, uint8, BFloat16Storage, BoolStorage, ByteStorage, CharStorage, ComplexDoubleStorage, ComplexFloatStorage, DisableTorchFunction, DoubleStorage, FatalError, FloatStorage, HalfStorage, HalfStorageBase, IntStorage, JITException, LongStorage, QInt32Storage, QInt32StorageBase, QInt8Storage, QInt8StorageBase, QUInt8Storage, ShortStorage, Storage, device, dtype, enable_grad, finfo, iinfo, layout, memory_format, no_grad, qscheme, set_grad_enabled, Set, abs, abs_, absolute, acos, acos_, acosh, acosh_, adaptive_avg_pool1d, adaptive_max_pool1d, add, addbmm, addcdiv, addcmul, addmm, addmv, addmv_, addr, affine_grid_generator, align_tensors, all, allclose, alpha_dropout, alpha_dropout_, amax, amin, angle, any, arange, arccos, arccos_, arccosh, arccosh_, arcsin, arcsin_, arcsinh, arcsinh_, arctan, arctan_, arctanh, arctanh_, argmax, argmin, argsort, as_strided, as_strided_, as_tensor, asin, asin_, asinh, asinh_, atan, atan2, atan_, atanh, atanh_, atleast_1d, atleast_2d, atleast_3d, autocast_decrement_nesting, autocast_increment_nesting, avg_pool1d, baddbmm, bartlett_window, batch_norm, batch_norm_backward_elemt, batch_norm_backward_reduce, batch_norm_elemt, batch_norm_gather_stats, batch_norm_gather_stats_with_counts, batch_norm_stats, batch_norm_update_stats, bernoulli, bilinear, binary_cross_entropy_with_logits, bincount, binomial, bitwise_and, bitwise_not, bitwise_or, bitwise_xor, blackman_window, block_diag, bmm, broadcast_tensors, bucketize, can_cast, cartesian_prod, cdist, ceil, ceil_, celu, celu_, chain_matmul, channel_shuffle, cholesky, cholesky_inverse, cholesky_solve, choose_qparams_optimized, chunk, clamp, clamp_, clamp_max, clamp_max_, clamp_min, clamp_min_, clear_autocast_cache, clip, clip_, clone, combinations, compiled_with_cxx11_abi, complex, conj, constant_pad_nd, conv1d, conv2d, conv3d, conv_tbc, conv_transpose1d, conv_transpose2d, conv_transpose3d, convolution, cos, cos_, cosh, cosh_, cosine_embedding_loss, cosine_similarity, count_nonzero, cross, ctc_loss, cudnn_affine_grid_generator, cudnn_batch_norm, cudnn_convolution, cudnn_convolution_transpose, cudnn_grid_sampler, cudnn_is_acceptable, cummax, cummin, cumprod, cumsum, deg2rad, deg2rad_, dequantize, det, detach, detach_, diag_embed, diagflat, diagonal, digamma, dist, div, divide, dot, dropout, dropout_, dsmm, dstack, eig, einsum, embedding, embedding_bag, embedding_renorm_, empty_quantized, empty_strided, eq, equal, erf, erf_, erfc, erfc_, erfinv, exp, exp2, exp2_, exp_, expm1, expm1_, fake_quantize_per_channel_affine, fake_quantize_per_tensor_affine, fbgemm_linear_fp16_weight, fbgemm_linear_fp16_weight_fp32_activation, fbgemm_linear_int8_weight, fbgemm_linear_int8_weight_fp32_activation, fbgemm_linear_quantize_weight, fbgemm_pack_gemm_matrix_fp16, fbgemm_pack_quantized_matrix, feature_alpha_dropout, feature_alpha_dropout_, feature_dropout, feature_dropout_, fill_, fix, fix_, flatten, flip, fliplr, flipud, floor, floor_, floor_divide, fmod, fork, frac, frac_, frobenius_norm, from_file, from_numpy, gather, gcd, gcd_, ge, geqrf, ger, get_default_dtype, get_file_path, get_num_interop_threads, get_num_threads, get_rng_state, greater, greater_equal, grid_sampler, grid_sampler_2d, grid_sampler_3d, group_norm, gru, gru_cell, gt, hamming_window, hann_window, hardshrink, heaviside, hinge_embedding_loss, histc, hsmm, hspmm, hstack, hypot, i0, i0_, imag, import_ir_module, import_ir_module_from_buffer, index_add, index_copy, index_fill, index_put, index_put_, index_select, init_num_threads, initial_seed, instance_norm, int_repr, inverse, is_anomaly_enabled, is_autocast_enabled, is_complex, is_distributed, is_floating_point, is_grad_enabled, is_nonzero, is_same_size, is_signed, is_storage, is_tensor, is_vulkan_available, isclose, isfinite, isinf, isnan, isneginf, isposinf, isreal, istft, kaiser_window, kl_div, kthvalue, layer_norm, lcm, lcm_, le, lerp, less, less_equal, lgamma, linspace, load, lobpcg, log, log10, log10_, log1p, log1p_, log2, log2_, log_, log_softmax, logaddexp, logaddexp2, logcumsumexp, logdet, logical_and, logical_not, logical_or, logical_xor, logit, logit_, logspace, logsumexp, lstm, lstm_cell, lstsq, lt, lu, lu_solve, lu_unpack, manual_seed, margin_ranking_loss, masked_fill, masked_scatter, masked_select, matmul, matrix_exp, matrix_power, matrix_rank, max, max_pool1d, max_pool1d_with_indices, max_pool2d, max_pool3d, maximum, mean, median, merge_type_from_type_comment, meshgrid, min, minimum, miopen_batch_norm, miopen_convolution, miopen_convolution_transpose, miopen_depthwise_convolution, miopen_rnn, mkldnn_adaptive_avg_pool2d, mkldnn_convolution, mkldnn_convolution_backward_weights, mkldnn_max_pool2d, mkldnn_max_pool3d, mm, mode, movedim, mul, multinomial, multiply, mv, mvlgamma, nanquantile, nansum, narrow, native_batch_norm, native_group_norm, native_layer_norm, native_norm, ne, neg, neg_, negative, negative_, nextafter, nonzero, norm, norm_except_dim, normal, not_equal, nuclear_norm, numel, orgqr, ormqr, outer, pairwise_distance, parse_ir, parse_schema, parse_type_comment, pca_lowrank, pdist, pinverse, pixel_shuffle, poisson, poisson_nll_loss, polar, polygamma, pow, prelu, prepare_multiprocessing_environment, prod, promote_types, q_per_channel_axis, q_per_channel_scales, q_per_channel_zero_points, q_scale, q_zero_point, qr, quantile, quantize_per_channel, quantize_per_tensor, quantized_batch_norm, quantized_gru, quantized_gru_cell, quantized_lstm, quantized_lstm_cell, quantized_max_pool1d, quantized_max_pool2d, quantized_rnn_relu_cell, quantized_rnn_tanh_cell, rad2deg, rad2deg_, randperm, range, real, reciprocal, reciprocal_, relu, relu_, remainder, renorm, repeat_interleave, reshape, resize_as_, result_type, rnn_relu, rnn_relu_cell, rnn_tanh, rnn_tanh_cell, roll, rot90, round, round_, rrelu, rrelu_, rsqrt, rsqrt_, rsub, saddmm, save, scalar_tensor, scatter, scatter_add, searchsorted, seed, select, selu, selu_, set_anomaly_enabled, set_autocast_enabled, set_default_dtype, set_default_tensor_type, set_flush_denormal, set_num_interop_threads, set_num_threads, set_printoptions, set_rng_state, sgn, sigmoid, sigmoid_, sign, signbit, sin, sin_, sinh, sinh_, slogdet, smm, softmax, solve, sort, sparse_coo_tensor, split, split_with_sizes, spmm, sqrt, sqrt_, square, square_, sspaddmm, std, std_mean, stft, sub, subtract, sum, svd, svd_lowrank, symeig, take, tan, tan_, tanh, tanh_, tensordot, threshold, threshold_, topk, transpose, trapz, triangular_solve, tril, tril_indices, triplet_margin_loss, triu, triu_indices, true_divide, trunc, trunc_, unbind, unify_type_list, unique, unique_consecutive, unsafe_chunk, unsafe_split, unsafe_split_with_sizes, vander, var, var_mean, vdot, view_as_complex, view_as_real, vstack, wait, where, zero_ #**
from .tensorfunc import crop_as, pad, decimal, divide, equals, matpow, matprod, dot, down_scale, gaussian_kernel, norm, norm2, Fnorm, Fnorm2, frobenius_norm, meannorm, meannorm2, mean_norm, mean_norm2, Jacobian, grad_image, image_grid, up_scale, one_hot, permute_space, skew_symmetric, cross_matrix, uncross_matrix, summary #*
from .optimizer import CSGD, CADAM, Optimization, train, test #*

















































