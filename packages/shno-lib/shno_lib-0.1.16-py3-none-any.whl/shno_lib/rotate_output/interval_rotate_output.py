
from datetime import datetime
from .rotate_output import RotateOutput

class IntervalRotateOutput(RotateOutput):
    def __init__(self, file_name, size_thres, *, logger=None, judge_base='size', buffering=0, rotate_interval=None, fn_gen_func = None):

        super().__init__(
                file_name,
                size_thres,
                logger = logger,
                judge_base = judge_base,
                buffering = buffering,
                fn_gen_func = fn_gen_func,
            )
        if logger is not None:
            logger.info("set rotate_interval {0}".format(rotate_interval))
        self.rotate_interval = rotate_interval
        self.pre_interval_rotate_time = datetime.now()

    def check_rotate(self):
        now_time = datetime.now()

        if self.rotate_interval is not None:
            if (now_time - self.pre_interval_rotate_time).seconds >= self.rotate_interval:

                if self.logger is not None:
                    self.logger.info("rotate_file triggers because now_time({0}) - self.pre_interval_rotate_time({1}) >= self.rotate_interval ({2} >= {3})".format(
                        now_time.strftime("%H:%M:%S"),
                        self.pre_interval_rotate_time.strftime("%H:%M:%S"),
                        (now_time - self.pre_interval_rotate_time).seconds,
                        self.rotate_interval,
                        ))

                self.pre_interval_rotate_time= now_time
                if self.judge_base == 'size':
                    self.now_size = 0
                if self.judge_base == 'num':
                    self.now_num = 0

                self.rotate_file()

                return

        super().check_rotate()
