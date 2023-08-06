
from datetime import datetime
from .rotate_output import RotateOutput

class DailyRotateOutput(RotateOutput):
    def __init__(self, file_name, size_thres, *, logger=None, judge_base='size', rotate_time = None, buffering=0, fn_gen_func = None):

        super().__init__(
                file_name,
                size_thres,
                logger = logger,
                judge_base = judge_base,
                buffering = buffering,
                fn_gen_func = fn_gen_func,
            )
        if logger is not None:
            logger.info("set rotate_time {0}".format(rotate_time))
        self.rotate_time = rotate_time
        self.pre_daily_rotate_time = None

    def check_rotate(self):
        now_time = datetime.now()
        now_date = now_time.strftime("%Y/%m/%d")
        now_hour_min = now_time.strftime("%H:%M")

        if self.rotate_time is not None:
            if now_date != self.pre_daily_rotate_time and now_hour_min >= self.rotate_time:
                if self.logger is not None:
                    self.logger.info("rotate_file triggers because now_hour_min({0}) >= self.rotate_time({1}) && now_date != self.pre_interval_rotate_time({2} != {3})".format(
                        now_hour_min,
                        self.rotate_time,
                        now_date,
                        self.pre_daily_rotate_time,
                        ))
                self.pre_daily_rotate_time = now_date
                if self.judge_base == 'size':
                    self.now_size = 0
                if self.judge_base == 'num':
                    self.now_num = 0

                self.rotate_file()

                return

        super().check_rotate()

