import time
from datetime import datetime
import os
from os.path import realpath, normpath, dirname, abspath, isfile, isdir, basename
from os.path import join as pjoin
from ..data_io.file_io import filename_add_id, general_open2

class RotateOutputIsOpened(Exception):
    pass
class RotateOutputFilenameCollision(Exception):
    pass


class RotateOutput:
    def __init__(self, all_file_name, size_thres, *, logger=None, judge_base='size', buffering=0, fn_gen_func = None):
        self.all_file_name = all_file_name
        self.judge_base = judge_base

        if judge_base == 'size':
            self.size_thres = size_thres
            self.now_size = 0
        elif judge_base == 'num':
            self.num_thres = size_thres
            self.now_num = 0

        self.logger=logger
        self.buffering = buffering
        self.file_handle = None

        if fn_gen_func is None:
            self.fn_gen_func = self.default_fn_gen_func
            now_time = datetime.now()
            self.yyyymmdd_status = now_time.strftime('%Y%m%d')
            self.yyyymmdd_hhmmss_status = now_time.strftime('%Y%m%d_%H%M%S')
        else:
            self.fn_gen_func = fn_gen_func

    def __enter__(self):
        if self.logger is not None:
            self.logger.info("Open the RotateOutput context mgr, filename: %s", self.all_file_name)

        self.open()

        return self

    def default_fn_gen_func(self, all_file_name):
        dir_name = dirname(all_file_name)
        file_name = basename(all_file_name)

        now_time = datetime.now()

        if now_time.strftime('%Y%m%d') != self.yyyymmdd_status:
            self.yyyymmdd_status = now_time.strftime('%Y%m%d')
            self.yyyymmdd_hhmmss_status = now_time.strftime('%Y%m%d_%H%M%S')

        true_filename = pjoin(
            dir_name,
            filename_add_id(file_name, '_{0}'.format(self.yyyymmdd_hhmmss_status) )
        )

        return true_filename


    def open(self):
        if not self.is_closed():
            if self.logger is not None:
                err_msg = "RotateOutput is open now, filename: {0}".format(self.file_handle.name)
                self.logger.error(err_msg)
                raise RotateOutputIsOpened(err_msg)

        true_filename = self.fn_gen_func_check_isfile_wrapper()

        if self.buffering > 0:
            self.file_handle =\
                general_open2(
                    true_filename,
                    'wt',buffering=self.buffering)
        else:
            self.file_handle =\
                general_open2(
                    true_filename,
                    'wt')

        if self.logger is not None:
            self.logger.info("Open the RotateOutput file, filename: %s", true_filename)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

        if self.logger is not None:
            self.logger.info("Close the RotateOutput context mgr, filename: %s", self.all_file_name)

    def is_closed(self):
        return self.file_handle is None

    def close(self):
        true_filename = self.file_handle.name

        self.file_handle.close()

        if self.logger is not None:
            self.logger.info("Close the RotateOutput file, filename: %s", true_filename)

    def write(self,text):
        if self.judge_base == 'size':
            self.file_handle.write(text)
            self.now_size = self.now_size + len(text.encode('utf-8'))
        elif self.judge_base == 'num':
            self.file_handle.write(text)

    def flush(self):
        self.file_handle.flush()

    def write_end(self):
        if self.judge_base == 'num':
            self.now_num += 1

    def write_and_check_rotate(self, text):
        if self.judge_base == 'size':
            self.write(text)
            self.check_rotate()
        if self.judge_base == 'num':
            self.write(text)
            self.write_end()
            self.check_rotate()

    def rotate_file(self):
        pre_true_filename = self.file_handle.name
        self.file_handle.close()

        true_filename = self.fn_gen_func_check_isfile_wrapper()

        if self.buffering > 0:
            self.file_handle =\
                general_open2(
                    true_filename,
                    'wt',buffering=self.buffering)
        else:
            self.file_handle =\
                general_open2(
                    true_filename,
                    'wt')

        if self.logger is not None:
            self.logger.info("Rotate the RotateOutput file, from filename: %s to filename: %s", pre_true_filename, true_filename)

    def fn_gen_func_check_isfile_wrapper(self):
        result_filename = self.fn_gen_func(self.all_file_name)
        output_filename = result_filename

        file_id = 0

        while isfile(output_filename):
            file_id += 1

            if file_id > 50:
                if self.logger is not None:
                    err_msg = "RotateOutput filename {0} collision".format(output_filename)
                    self.logger.error(err_msg)
                    raise RotateOutputFilenameCollision(err_msg)

            output_filename = filename_add_id(result_filename, '_copy_{0}'.format(file_id))

        return output_filename

    def check_rotate(self):

        if self.judge_base == 'size':
            if self.now_size >= self.size_thres:
                self.now_size = 0

                self.rotate_file()

        elif self.judge_base == 'num':
            if self.now_num >= self.num_thres:
                self.now_num = 0

                self.rotate_file()

