import multiprocessing
from functools import partial
from multiprocessing import Pool
from os.path import isfile
from os.path import join as pjoin
from collections import Callable
import traceback
import types
import sys
import os

class _DirExecError(Exception):
    pass

def _raise_DirExecError(*args):
    try:
        raise _DirExecError(*args)
    except Exception as e:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        raise

def dir_exec_func(func, dir_name, input_fn_pat, output_fn_pat, *, check_output = None, pos_args = (), kw_args = dict()):
    if not isinstance(func, Callable):
        _raise_DirExecError("func is not a function")

    if not isinstance(check_output, bool):
        _raise_DirExecError("check_output is not a bool")

    if not isinstance(pos_args, tuple):
        _raise_DirExecError("pos_args is not a tuple")

    if not isinstance(kw_args, dict):
        _raise_DirExecError("kw_args is not a dict")

    input_star_pos = input_fn_pat.find("*")
    output_star_pos = output_fn_pat.find("*")

    multi_in = input_star_pos >= 0
    multi_out = output_star_pos >= 0

    if not multi_in and multi_out:
        _raise_DirExecError("Input multiple files but output single file")
        
    if multi_in and not multi_out:
        _raise_DirExecError("Input single file but output multiple files")

    if multi_in:
        input_prefix = input_fn_pat[:input_star_pos]
        input_suffix = input_fn_pat[input_star_pos+1:]
        output_prefix = output_fn_pat[:output_star_pos]
        output_suffix = output_fn_pat[output_star_pos+1:]

    filename_list = os.listdir(dir_name)

    for filename in filename_list:
        if not isfile(pjoin(dir_name,filename)):
            continue

        if multi_in:
            if not filename.startswith(input_prefix) or not filename.endswith(input_suffix):
                continue
            else:
                input_fn_middle = filename[len(input_prefix):-len(input_suffix) if len(input_suffix) > 0 else None] 

        else:
            if filename != input_fn_pat:
                continue

        if multi_in:
            if check_output and isfile(pjoin(dir_name,output_prefix+input_fn_middle+output_suffix)):
                continue
            func(pjoin(dir_name,filename), pjoin(dir_name,output_prefix+input_fn_middle+output_suffix), *pos_args, **kw_args)
        else:
            if check_output and isfile(pjoin(dir_name,output_fn_pat)):
                continue
            func(pjoin(dir_name,input_fn_pat), pjoin(dir_name,output_fn_pat), *pos_args, **kw_args)


        
def multi_dir_exec_func(func, dir_names, input_fn_pat, output_fn_pat, *, check_output = None, worker_num = 1, pos_args = (), kw_args = dict()):
    if not isinstance(func, Callable):
        _raise_DirExecError("id_generator is not a function")

    if not isinstance(check_output, bool):
        _raise_DirExecError("check_output is not a bool")

    if not isinstance(dir_names, list):
        _raise_DirExecError("dir_names is not a list")

    if not isinstance(worker_num, int):
        _raise_DirExecError("worker_num is not a int")

    if pos_args is not None and not isinstance(pos_args, tuple):
        _raise_DirExecError("pos_args is not a tuple")

    if kw_args is not None and not isinstance(kw_args, dict):
        _raise_DirExecError("kw_args is not a dict")

    input_star_pos = input_fn_pat.find("*")
    output_star_pos = output_fn_pat.find("*")

    multi_in = input_star_pos >= 0
    multi_out = output_star_pos >= 0

    if not multi_in and multi_out:
        _raise_DirExecError("Input multiple files but output single file")
        
    if multi_in and not multi_out:
        _raise_DirExecError("Input single file but output multiple files")

    pool = Pool(worker_num)
    partial_dir_exec_func = partial(dir_exec_func, 
        input_fn_pat = input_fn_pat,        
        output_fn_pat = output_fn_pat,
        check_output = check_output,
        pos_args = pos_args,
        kw_args = kw_args,
    ) 

    pool.map(dir_exec_func,dir_names)

