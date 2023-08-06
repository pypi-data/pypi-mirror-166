from collections import Callable
import json
import sys
import traceback
from contextlib import contextmanager, ExitStack

from ..data_io.file_io import general_open, rec_get_content, rec_get_attr, general_open2

class _transError(Exception):
    pass

def _raise_transError(*args):
    try:
        raise _transError(*args)
    except Exception as e:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        raise

def _dict_to_rec_output(dict_data,attrs_order,outfile):
    outfile.write("@\n@Gais_REC:\n")
    if attrs_order is None:
        for attr in dict_data:
            outfile.write("@"+attr+":"+str(dict_data[attr])+'\n')

    else:
        for attr in attrs_order:
            if attr in dict_data:
                outfile.write("@"+attr+":"+str(dict_data[attr])+'\n')

    outfile.write("\n")

def rec_update_attr_name(input_fn, output_fn, update_map):

    with general_open2(input_fn,'rt',errors='surrogateescape') as infile, general_open2(output_fn,'wt',errors='surrogateescape') as outfile:
        for line in infile:
            line = line.strip()

            if len(line) > 0 and line[0] == '@' and line.find(':') > -1:
                line_attr = line[1:line.find(':')]

                if line_attr in update_map:
                    outfile.write('@' + update_map[line_attr] + line[line.find(':'):] + '\n')

                else:
                    outfile.write(line + '\n')

            else:
                outfile.write(line + '\n')

def rec_update_attr_content2(input_fn, output_fn, update_map, ref_attr_set = {}, gais_head='@\n@Gais_REC:'):
    with general_open2(input_fn,'rt',errors='surrogateescape') as infile, general_open2(output_fn,'wt',errors='surrogateescape') as outfile:
        now_attr = ''
        ref_content = {}
        insert_pos = {}
        buffer_array = []
        rec_head_list = list(filter(lambda ele: len(ele) > 0, gais_head.split('\n')))
        rec_head_set = set(rec_head_list)

        for line in infile:
            line = line.strip()

            if line in rec_head_set:
                if line == rec_head_list[-1]:
                    if len(buffer_array) > 0:
                        outfile.write(gais_head.rstrip() + '\n')
                        for i in insert_pos:
                            buffer_array[i] += update_map[insert_pos[i]](ref_content)
                        outfile.write('\n'.join(buffer_array).rstrip() + '\n\n')
                    now_attr = ''
                    ref_content = {}
                    insert_pos = {}
                    buffer_array = []
                continue

            if len(line) > 0 and line[0] == '@' and line.find(':') > -1:
                line_attr = line[1:line.find(':')]

                if line_attr in ref_attr_set:
                    now_attr = line_attr
                    ref_content[line_attr] = line[line.find(':')+1:]

                    if line_attr in update_map:
                        now_attr = line_attr
                        insert_pos[len(buffer_array)] = line_attr
                        buffer_array.append(line[:line.find(':')+1])

                    else:
                        buffer_array.append(line)


                else:
                    if line_attr in update_map:
                        now_attr = line_attr
                        insert_pos[len(buffer_array)] = line_attr
                        buffer_array.append(line[:line.find(':')+1])
                    else:
                        buffer_array.append(line)
                        now_attr = ''

            else:
                if now_attr in ref_attr_set:
                    ref_content[line_attr] += '\n' + line

                if now_attr in update_map:
                    continue

                else:
                    buffer_array.append(line)

        if len(buffer_array) > 0:
            outfile.write(gais_head.rstrip() + '\n')
            for i in insert_pos:
                buffer_array[i] += update_map[insert_pos[i]](ref_content)
            outfile.write('\n'.join(buffer_array).rstrip() + '\n\n')

def rec_update_attr_content(input_fn, output_fn, update_map, gais_head='@\n@Gais_REC:'):
    with general_open2(input_fn,'rt',errors='surrogateescape') as infile, general_open2(output_fn,'wt',errors='surrogateescape') as outfile:
        now_attr = ''
        now_content = {}
        for line in infile:
            line = line.strip()

            if gais_head == '@\n@Gais_REC:' and line == '@':
                continue

            if len(line) > 0 and line[0] == '@' and line.find(':') > -1:
                line_attr = line[1:line.find(':')]

                if line_attr in update_map:
                    now_attr = line_attr
                    now_content[now_attr] = line[line.find(':')+1:]

                else:
                    if now_attr in update_map:
                        outfile.write('@' + now_attr + ':' + update_map[now_attr](now_content[now_attr]).strip() + '\n')
                    if gais_head == '@\n@Gais_REC:' and line == '@Gais_REC:':
                        outfile.write('@\n' + line + '\n')
                    else:
                        outfile.write(line + '\n')
                    now_attr = ''

            else:
                if now_attr in update_map:
                    now_content[now_attr] += '\n' + line
                else:
                    outfile.write(line + '\n')

def json_to_rec(input_fn, output_fn, attrs_order = None, check_json_range = False):
    if attrs_order is not None and not isinstance(attrs_order,list):
        _raise_transError("attrs_order is not a list")

    with general_open(input_fn,'rt',errors='surrogateescape') as infile, general_open(output_fn,'wt',errors='surrogateescape') as outfile:
        if check_json_range:
            for line in infile:
                line = line.strip()
                if len(line) == 0:
                    continue
                start_pos = line.find('{')
                end_pos = line.rfind('}')

                if start_pos == -1 or end_pos == -1:
                    continue

                dict_data = json.loads(line[start_pos:end_pos+1])
                _dict_to_rec_output(dict_data,attrs_order,outfile)
        else:
            for line in infile:
                line = line.strip()
                if len(line) == 0:
                    continue
                dict_data = json.loads(line)
                _dict_to_rec_output(dict_data,attrs_order,outfile)


def rec_to_json(input_fn, output_fn, want_attrs = None, unwant_attrs = None, multi_line_attr_end_map = None, json_data_other_proc = None, json_data_other_proc_list = None):
    if want_attrs is not None and unwant_attrs is not None:
        _raise_transError("want_attrs and unwant_attrs are not None")

    if want_attrs is not None and not isinstance(want_attrs,set):
        _raise_transError("want_attrs is not a set")

    if unwant_attrs is not None and not isinstance(unwant_attrs,set):
        _raise_transError("unwant_attrs is not a set")

    if multi_line_attr_end_map is not None and not isinstance(multi_line_attr_end_map,dict):
        _raise_transError("multi_line_attr_end_map is not a dict")

    if json_data_other_proc is not None and not isinstance(json_data_other_proc, Callable):
        _raise_transError("json_data_other_proc is not a function")

    if json_data_other_proc_list is not None and not isinstance(json_data_other_proc_list,list):
        _raise_transError("json_data_other_proc_list is not a list")

    if json_data_other_proc is not None and json_data_other_proc_list is not None:
        _raise_transError("both json_data_other_proc_list and json_data_other_proc_list is not None")

    with general_open(input_fn,'rt',errors='surrogateescape') as infile, general_open(output_fn, 'wt',errors='surrogateescape') as outfile:
        now_attr = ''
        multi_line_array = []
        json_data = {}
        for line in infile:
            line = line.strip()
            if line == '@':
                continue
            elif line.startswith("@Gais_"):
                if len(json_data) == 0:
                    continue
                if len(now_attr) > 0:
                    json_data[now_attr] += "".join(multi_line_array)
                    multi_line_array = []
                    now_attr = ''

                if json_data_other_proc is not None:
                    json_data_other_proc(json_data)
                elif json_data_other_proc_list is not None:
                    for proc_func in json_data_other_proc_list:
                        proc_func(json_data)

                outfile.write(json.dumps(json_data, ensure_ascii=False)+'\n')
                json_data = {}

            else:
                attr = rec_get_attr(line)
                if attr is None:
                    if len(now_attr) > 0:
                        multi_line_array.append("\n"+line)

                elif len(attr) == 0:
                    if len(now_attr) > 0:
                        json_data[now_attr] += "".join(multi_line_array)
                        multi_line_array = []
                        now_attr = ''

                else:
                    if len(now_attr) > 0 and (multi_line_attr_end_map is not None and multi_line_attr_end_map[now_attr] != attr):
                        multi_line_array.append("\n"+line)
                        continue

                    if len(now_attr) > 0:
                        json_data[now_attr] += "".join(multi_line_array)
                        multi_line_array = []
                        now_attr = ''
                    if want_attrs is None and unwant_attrs is None:
                        json_data[attr] = rec_get_content(line)
                        if multi_line_attr_end_map is None or attr in multi_line_attr_end_map:
                            now_attr = attr

                    elif want_attrs is None and unwant_attrs is not None:
                        if attr not in unwant_attrs:
                            json_data[attr] = rec_get_content(line)
                            if multi_line_attr_end_map is None or attr in multi_line_attr_end_map:
                                now_attr = attr

                    elif want_attrs is not None and unwant_attrs is None:
                        if attr in want_attrs:
                            json_data[attr] = rec_get_content(line)
                            if multi_line_attr_end_map is None or attr in multi_line_attr_end_map:
                                now_attr = attr

        if len(json_data) != 0:
            if len(now_attr) > 0:
                json_data[now_attr] += "".join(multi_line_array)
                multi_line_array = []
                now_attr = ''

            if json_data_other_proc is not None:
                json_data_other_proc(json_data)
            elif json_data_other_proc_list is not None:
                for proc_func in json_data_other_proc_list:
                    proc_func(json_data)



def json_to_es(input_fn, output_fn, es_info = None, id_generator = None):
    if not isinstance(es_info,dict):
        _raise_transError("es_info is not a dict")

    if not isinstance(id_generator, Callable):
        _raise_transError("id_generator is not a function")

    with general_open(input_fn,'rt',errors='surrogateescape') as infile, general_open(output_fn, 'wt',errors='surrogateescape') as outfile:
        for line in infile:
            json_data = json.loads(line)

            es_info['index']['_id'] = id_generator(json_data)

            if es_info['index']['_id'] is not None:
                outfile.write(json.dumps(es_info, ensure_ascii=False)+'\n')
            else:
                continue
            outfile.write(json.dumps(json_data, ensure_ascii=False)+'\n')
            json_data = {}



def rec_to_es(input_fn, output_fn, es_info = None, id_generator = None, want_attrs = None, unwant_attrs = None, multi_line_attr_end_map = None, json_data_other_proc = None, json_data_other_proc_list = None):
    if want_attrs is not None and unwant_attrs is not None:
        _raise_transError("want_attrs and unwant_attrs are not None")

    if not isinstance(es_info,dict):
        _raise_transError("es_info is not a dict")

    if not isinstance(id_generator, Callable):
        _raise_transError("id_generator is not a function")

    if want_attrs is not None and not isinstance(want_attrs,set):
        _raise_transError("want_attrs is not a set")

    if unwant_attrs is not None and not isinstance(unwant_attrs,set):
        _raise_transError("unwant_attrs is not a set")

    if multi_line_attr_end_map is not None and not isinstance(multi_line_attr_end_map,dict):
        _raise_transError("multi_line_attr_end_map is not a dict")

    if json_data_other_proc is not None and not isinstance(json_data_other_proc, Callable):
        _raise_transError("json_data_other_proc is not a function")

    if json_data_other_proc_list is not None and not isinstance(json_data_other_proc_list,list):
        _raise_transError("json_data_other_proc_list is not a list")

    if json_data_other_proc is not None and json_data_other_proc_list is not None:
        _raise_transError("both json_data_other_proc_list and json_data_other_proc_list is not None")

    with general_open(input_fn,'rt',errors='surrogateescape') as infile, general_open(output_fn, 'wt',errors='surrogateescape') as outfile:
        now_attr = ''
        multi_line_array = []
        json_data = {}
        for line in infile:
            line = line.strip()
            if line == '@':
                continue
            elif line.startswith("@Gais_"):
                if len(json_data) == 0:
                    continue
                if len(now_attr) > 0:
                    json_data[now_attr] += "".join(multi_line_array)
                    multi_line_array = []
                    now_attr = ''

                es_info['index']['_id'] = id_generator(json_data)

                if es_info['index']['_id'] is not None:
                    outfile.write(json.dumps(es_info, ensure_ascii=False)+'\n')
                else:
                    json_data = {}
                    continue

                if json_data_other_proc is not None:
                    json_data_other_proc(json_data)
                elif json_data_other_proc_list is not None:
                    for proc_func in json_data_other_proc_list:
                        proc_func(json_data)

                outfile.write(json.dumps(json_data, ensure_ascii=False)+'\n')
                json_data = {}
                continue

            else:
                attr = rec_get_attr(line)
                if attr is None:
                    if len(now_attr) > 0:
                        multi_line_array.append("\n"+line)

                elif len(attr) == 0:
                    if len(now_attr) > 0:
                        json_data[now_attr] += "".join(multi_line_array)
                        multi_line_array = []
                        now_attr = ''

                else:
                    if len(now_attr) > 0 and (multi_line_attr_end_map is not None and multi_line_attr_end_map[now_attr] != attr):
                        multi_line_array.append("\n"+line)
                        continue


                    if len(now_attr) > 0:
                        json_data[now_attr] += "".join(multi_line_array)
                        multi_line_array = []
                        now_attr = ''
                    if want_attrs is None and unwant_attrs is None:
                        json_data[attr] = rec_get_content(line)
                        if multi_line_attr_end_map is None or attr in multi_line_attr_end_map:
                            now_attr = attr

                    elif want_attrs is None and unwant_attrs is not None:
                        if attr not in unwant_attrs:
                            json_data[attr] = rec_get_content(line)
                            if multi_line_attr_end_map is None or attr in multi_line_attr_end_map:
                                now_attr = attr

                    elif want_attrs is not None and unwant_attrs is None:
                        if attr in want_attrs:
                            json_data[attr] = rec_get_content(line)
                            if multi_line_attr_end_map is None or attr in multi_line_attr_end_map:
                                now_attr = attr

        if len(json_data) != 0:
            if len(now_attr) > 0:
                json_data[now_attr] += "".join(multi_line_array)
                multi_line_array = []
                now_attr = ''

            es_info['index']['_id'] = id_generator(json_data)
            if len(now_attr) > 0:
                json_data[now_attr] += "".join(multi_line_array)
                multi_line_array = []
                now_attr = ''
            if es_info['index']['_id'] is not None:
                outfile.write(json.dumps(es_info, ensure_ascii=False)+'\n')
                if json_data_other_proc is not None:
                    json_data_other_proc(json_data)
                elif json_data_other_proc_list is not None:
                    for proc_func in json_data_other_proc_list:
                        proc_func(json_data)
                outfile.write(json.dumps(json_data, ensure_ascii=False)+'\n')
                json_data = {}

class DataMergeModelBase:
    def __init__(self, input_model1, input_model2, output_model):
        self.input_model1 = input_model1
        self.input_model2 = input_model2
        self.output_model = output_model
        self.need_read_status = None
        self.break_when_model1_eof = False
        self.break_when_model2_eof = False

    @contextmanager
    def enter(self):
        with ExitStack() as stack:
            stack.enter_context(self.input_model1)
            stack.enter_context(self.input_model2)
            stack.enter_context(self.output_model)
            yield self

    def exec(self):
        self.need_read_status = 'both'
        model1_read_gen = self.read_wrapper(self.input_model1)
        model2_read_gen = self.read_wrapper(self.input_model2)

        while True:
            if self.need_read_status == 'both':
                model1_read_item = model1_read_gen.__next__()
                model2_read_item = model2_read_gen.__next__()

            elif self.need_read_status == '1':
                model1_read_item = model1_read_gen.__next__()

            elif self.need_read_status == '2':
                model2_read_item = model2_read_gen.__next__()

            if model1_read_item is None:
                if model2_read_item is None:
                    break

                self.output_model.only_model2_write(model2_read_item)
                self.need_read_status = '2'

            elif model2_read_item is None:
                self.output_model.only_model1_write(model1_read_item)
                self.need_read_status = '1'

            else:
                compare_result = self.compare(model1_read_item, model2_read_item)
                if compare_result > 0:
                    self.output_model.greater_than_write(model1_read_item, model2_read_item)
                    self.need_read_status = '2'
                elif compare_result < 0:
                    self.output_model.less_than_write(model1_read_item, model2_read_item)
                    self.need_read_status = '1'
                else:
                    self.output_model.equal_write(model1_read_item, model2_read_item)
                    self.need_read_status = 'both'

    def read_wrapper(self, read_model):
        for read_item in read_model.read():
            yield read_item

        while True:
            yield None

    def compare(self, model1_read_item, model2_read_item):
        pass

class DataMergeInputModelBase:
    def __init__(self, filename):
        self.filename = filename
        self.file_handle = None

    def __enter__(self):
        self.open_file()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_file()
        self.file_handle = None

    def open_file(self):
        self.file_handle = open(self.filename, 'rt')

    def close_file(self):
        self.file_handle.close()

    def read(self):
        pass

class DataMergeOutputModelBase:
    def __init__(self, filename):
        self.filename = filename
        self.file_handle = None

    def __enter__(self):
        self.open_file()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_file()
        self.file_handle = None

    def open_file(self):
        self.file_handle = open(self.filename, 'wt')

    def close_file(self):
        self.file_handle.close()

    def only_model1_write(self, model1_read_item):
        pass

    def only_model2_write(self, model2_read_item):
        pass

    def less_than_write(self, model1_read_item, model2_read_item):
        pass

    def greater_than_write(self, model1_read_item, model2_read_item):
        pass

    def equal_write(self, model1_read_item, model2_read_item):
        pass


