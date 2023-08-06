import os
import subprocess
from os.path import join as pjoin
import time
import traceback

import requests

def import_multiple_rec(multi_rec_content, import_url, index_name, db_type, collision_handle='rupdate', timeout=None, retry_thres=3, recbeg="@\\n@Gais_REC:"):
    if len(multi_rec_content) == 0:
        return None

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'charset': 'UTF-8',
    }
    retry_cnt = 0
    while True:
        try:
            res = requests.post(\
                    import_url.rstrip('/') + '/rput',\
                    headers = headers,\
                    data=dict(db=index_name, format='text', recbeg=recbeg, record=multi_rec_content, operation=collision_handle),\
                    timeout=timeout,
                )
            return res
            break
        except requests.exceptions.Timeout:
            time.sleep(10)
            retry_cnt += 1
            if retry_cnt > retry_thres:
                raise

            continue


        except Exception as err:
            # print(traceback.format_exc())
            time.sleep(10)
            retry_cnt += 1
            if retry_cnt > retry_thres:
                raise

            continue



