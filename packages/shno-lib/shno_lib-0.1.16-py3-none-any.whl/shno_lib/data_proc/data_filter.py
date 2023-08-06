from ..data_io.file_io import general_open, rec_get_content, rec_get_attr, read_rec
from os.path import isdir
from os.path import isfile
from os.path import join as pjoin
from collections import Callable
import traceback
import types
import os
import sys

class _filterError(Exception):
    pass
def _raise_filterError(*args):
    try:
        raise _filterError(*args)
    except Exception as e:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        raise

def rec_attr_uniq(input_fn, output_fn, uniq_attr, mode = 'set'):
    if mode != 'set' and mode != 'hch':
        _raise_filterError("mode is not 'set' and 'hch'")

    def uniq_func(attr_content,attr_set):
        if attr_content not in attr_set:
            attr_set.add(attr_content)
            return True

        else:
            return False

    rec_attr_filter(
        input_fn,
        output_fn,
        filter_attr = uniq_attr,
        filter_func = uniq_func,
    )




def rec_attr_filter(input_fn, output_fn, attr_fn = None, filter_attr = None, filter_func = None, mode = 'want'):
    if filter_func is not None and not isinstance(filter_func, Callable):
        _raise_filterError("filter_func is not a function")

    if not isinstance(filter_attr,str) and not isinstance(filter_attr,list):
        _raise_filterError("filter_attr is not a string and not a list")

    if mode != 'want' and mode != 'unwant':
        _raise_filterError("mode != 'want' and mode != 'unwant'")

    if attr_fn is None and filter_func is None:
        _raise_filterError("attr_fn is None and filter_func is None")

    attr_set = set()

    if attr_fn is not None:
        with general_open(attr_fn,'rt') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue

                attr_set.add(line)

    with general_open(input_fn,'rt',errors='surrogateescape') as rf, general_open(output_fn,'wt',errors='surrogateescape') as wf:
        if isinstance(filter_attr,str):
            attr_content, rec_content = read_rec(rf,True,attr=filter_attr)
        elif isinstance(filter_attr,list):
            attr_content, rec_content = read_rec(rf,True,attr_list=filter_attr)

        if filter_func is None:
            if mode == 'want' and attr_content in attr_set:
                wf.write(rec_content.rstrip() +'\n\n')

            elif mode == 'unwant' and not attr_content in attr_set:
                wf.write(rec_content.rstrip() +'\n\n')

        elif attr_fn is None:
            if mode == 'want' and filter_func(attr_content,attr_set):
                wf.write(rec_content.rstrip() +'\n\n')

            elif mode == 'unwant' and not filter_func(attr_content,attr_set):
                wf.write(rec_content.rstrip() +'\n\n')

        else:
            if mode == 'want' and filter_func(attr_content,attr_set):
                wf.write(rec_content.rstrip() +'\n\n')

            elif mode == 'unwant' and not filter_func(attr_content,attr_set):
                wf.write(rec_content.rstrip() +'\n\n')



        if attr_content is not None:
            while True:
                if isinstance(filter_attr,str):
                    attr_content, rec_content = read_rec(rf,False,attr=filter_attr)
                elif isinstance(filter_attr,list):
                    attr_content, rec_content = read_rec(rf,False,attr_list=filter_attr)

                if (isinstance(filter_attr,str) and attr_content is None) or (isinstance(filter_attr,list) and attr_content == {}):
                    break
                if filter_func is None:
                    if mode == 'want' and attr_content in attr_set:
                        wf.write(rec_content.rstrip() +'\n\n')

                    elif mode == 'unwant' and not attr_content in attr_set:
                        wf.write(rec_content.rstrip() +'\n\n')

                elif attr_fn is None:
                    if mode == 'want' and filter_func(attr_content,attr_set):
                        wf.write(rec_content.rstrip() +'\n\n')

                    elif mode == 'unwant' and not filter_func(attr_content,attr_set):
                        wf.write(rec_content.rstrip() +'\n\n')

                else:
                    if mode == 'want' and filter_func(attr_content,attr_set):
                        wf.write(rec_content.rstrip() +'\n\n')

                    elif mode == 'unwant' and not filter_func(attr_content,attr_set):
                        wf.write(rec_content.rstrip() +'\n\n')


def rec_general_filter(input_fn, output_fn, attr_fn = None, filter_func = None, filter_func_list = None, multi_line_attr_end_map = None, mode = 'want', output_flag = 'wt'):
    if filter_func is None and filter_func_list is None:
        _raise_filterError("filter_func and filter_func_list is None")

    if filter_func is not None and not isinstance(filter_func, Callable):
        _raise_filterError("filter_func is not a function")

    if filter_func_list is not None and not isinstance(filter_func_list, list):
        _raise_filterError("filter_func is not a function")

    if mode != 'want' and mode != 'unwant':
        _raise_filterError("mode != 'want' and mode != 'unwant'")

    if multi_line_attr_end_map is not None and not isinstance(multi_line_attr_end_map,dict):
        _raise_transError("multi_line_attr_end_map is not a dict")

    attr_set = set()

    if attr_fn is not None:
        with general_open(attr_fn,'rt') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue

                attr_set.add(line)

    with general_open(input_fn,'rt',errors='surrogateescape') as infile, general_open(output_fn, output_flag, errors='surrogateescape') as outfile:
        now_attr = ''
        rec_content = ''
        multi_line_array = []
        json_data = {}
        for line in infile:
            line = line.strip()
            if line == '@':
                continue
            elif line.startswith("@Gais_"):
                if len(json_data) == 0:
                    rec_content = '@\n@Gais_REC:\n'
                    continue
                if len(now_attr) > 0:
                    json_data[now_attr] += "".join(multi_line_array)
                    multi_line_array = []
                    now_attr = ''

                if filter_func is not None:
                    if (filter_func(json_data,attr_set) and mode == 'want') or (not filter_func(json_data,attr_set) and mode == 'unwant'):
                        outfile.write(rec_content.rstrip() +'\n\n')
                        # outfile.write(json.dumps(json_data, ensure_ascii=False)+'\n')
                elif filter_func_list is not None:
                    write_able = True
                    for func in filter_func_list:
                        if not ((func(json_data,attr_set) and mode == 'want') or (not func(json_data,attr_set) and mode == 'unwant')):
                            write_able = False
                            break
                    if write_able:
                        outfile.write(rec_content.rstrip() +'\n\n')
                        # outfile.write(json.dumps(json_data, ensure_ascii=False)+'\n')

                json_data = {}
                rec_content = '@\n@Gais_REC:\n'

            else:
                rec_content += line + '\n'
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

                    json_data[attr] = rec_get_content(line)
                    if multi_line_attr_end_map is None or attr in multi_line_attr_end_map:
                        now_attr = attr

        if len(json_data) != 0:
            if len(now_attr) > 0:
                json_data[now_attr] += "".join(multi_line_array)
                multi_line_array = []
                now_attr = ''

            if filter_func is not None:
                if (filter_func(json_data,attr_set) and mode == 'want') or (not filter_func(json_data,attr_set) and mode == 'unwant'):
                    outfile.write(rec_content.rstrip() +'\n\n')
                    # outfile.write(json.dumps(json_data, ensure_ascii=False)+'\n')
            elif filter_func_list is not None:
                write_able = True
                for func in filter_func_list:
                    if not ((func(json_data,attr_set) and mode == 'want') or (not func(json_data,attr_set) and mode == 'unwant')):
                        write_able = False
                        break
                if write_able:
                    outfile.write(rec_content.rstrip() +'\n\n')
                    # outfile.write(json.dumps(json_data, ensure_ascii=False)+'\n')

def _need_check_keyword(attr,target_attrs,untarget_attrs):
    return (target_attrs is not None and attr in target_attrs) or (untarget_attrs is not None and attr not in untarget_attrs)

def rec_keyword_filter(input_fn, output_fn, kw_list, search_func = None, mode='want', target_attrs = None, untarget_attrs = None):
    if search_func is not None and not isinstance(search_func, Callable):
        _raise_filterError("search_func is not a function")

    if not isinstance(kw_list,list):
        _raise_filterError("kw_list is not a list")

    if mode != 'want' and mode != 'unwant':
        _raise_filterError("mode != 'want' and mode != 'unwant'")

    if target_attrs is not None and untarget_attrs is not None:
        _raise_filterError("target_attrs and untarget_attrs are not None")

    if target_attrs is not None and not isinstance(untarget_attrs,set):
        _raise_filterError("target_attrs is not a set")

    if target_attrs is not None and not isinstance(untarget_attrs,set):
        _raise_filterError("untarget_attrs is not a set")


    with general_open(input_fn,'rt',errors='surrogateescape') as rf, general_open(output_fn,'wt',errors='surrogateescape') as wf:
        rec_content = ''
        search_success = False
        now_in_attr = ''
        for line in rf:
            line = line.strip()
            if len(line) == 0 or line == '@':
                continue

            if line.startswith('@Gais'):
                if len(rec_content) > 0:
                    if (search_success and mode == 'want') or (not search_success and mode=='unwant'):
                        wf.write(rec_content.rstrip()+'\n\n')

                rec_content = '@\n@Gais_REC:\n'
                search_success = False
                continue

            else:
                rec_content += line + '\n'

                attr = rec_get_attr(line)
                content = rec_get_content(line)

                if attr is not None and len(attr) > 0:
                    now_in_attr = attr

                if _need_check_keyword(now_in_attr,target_attrs,untarget_attrs) and not search_success:
                    if search_func is not None:
                        search_func(content,kw_list)

                    else:
                        for keyword in kw_list:
                            if content.find(keyword) >= 0:
                                search_success = True
                                break


def rec_attr_reroute_filter(input_fn, attr_fn = None, filter_attr = None, filter_func = None, positive_output_fn = None, negative_output_fn = None):
    if filter_func is not None and not isinstance(filter_func, Callable):
        _raise_filterError("filter_func is not a function")

    if not isinstance(filter_attr,str):
        _raise_filterError("filter_attr is not a string")

    if attr_fn is None and filter_func is None:
        _raise_filterError("attr_fn is None and filter_func is None")

    attr_set = set()

    if attr_fn is not None:
        with general_open(attr_fn,'rt') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue

                attr_set.add(line)

    with general_open(input_fn,'rt',errors='surrogateescape') as rf,\
        general_open(negative_output_fn,'wt',errors='surrogateescape') as negative_wf,\
        general_open(positive_output_fn,'wt',errors='surrogateescape') as positive_wf:

        attr_content, rec_content = read_rec(rf,True,filter_attr)

        if filter_func is None:
            if attr_content in attr_set:
                if positive_wf is not None:
                    positive_wf.write(rec_content.rstrip() +'\n\n')

            else:
                if negative_wf is not None:
                    negative_wf.write(rec_content.rstrip() +'\n\n')

        elif attr_fn is None:
            if filter_func(attr_content,attr_set):
                if positive_wf is not None:
                    positive_wf.write(rec_content.rstrip() +'\n\n')

            else:
                if negative_wf is not None:
                    negative_wf.write(rec_content.rstrip() +'\n\n')

        else:
            if filter_func(attr_content,attr_set):
                if positive_wf is not None:
                    positive_wf.write(rec_content.rstrip() +'\n\n')

            else:
                if negative_wf is not None:
                    negative_wf.write(rec_content.rstrip() +'\n\n')


        if attr_content is not None:
            while True:
                attr_content, rec_content = read_rec(rf,False,filter_attr)

                if attr_content is None:
                    break
                if filter_func is None:
                    if attr_content in attr_set:
                        if positive_wf is not None:
                            positive_wf.write(rec_content.rstrip() +'\n\n')

                    else:
                        if negative_wf is not None:
                            negative_wf.write(rec_content.rstrip() +'\n\n')

                elif attr_fn is None:
                    if filter_func(attr_content,attr_set):
                        if positive_wf is not None:
                            positive_wf.write(rec_content.rstrip() +'\n\n')

                    else:
                        if negative_wf is not None:
                            negative_wf.write(rec_content.rstrip() +'\n\n')

                else:
                    if filter_func(attr_content,attr_set):
                        if positive_wf is not None:
                            positive_wf.write(rec_content.rstrip() +'\n\n')

                    else:
                        if negative_wf is not None:
                            negative_wf.write(rec_content.rstrip() +'\n\n')




def rec_keyword_reroute_filter(input_fn, kw_list, search_func = None, target_attrs = None, untarget_attrs = None, positive_output_fn = None, negative_output_fn = None): 
    if search_func is not None and not isinstance(search_func, Callable):
        _raise_filterError("search_func is not a function")

    if not isinstance(kw_list,list):
        _raise_filterError("kw_list is not a list")

    if target_attrs is not None and untarget_attrs is not None:
        _raise_filterError("target_attrs and untarget_attrs are not None")

    if target_attrs is not None and not isinstance(target_attrs,set):
        _raise_filterError("target_attrs is not a set")

    if untarget_attrs is not None and not isinstance(untarget_attrs,set):
        _raise_filterError("untarget_attrs is not a set")


    with general_open(input_fn,'rt',errors='surrogateescape') as rf,\
        general_open(negative_output_fn,'wt',errors='surrogateescape') as negative_wf,\
        general_open(positive_output_fn,'wt',errors='surrogateescape') as positive_wf:

        rec_content = ''
        search_success = False
        now_in_attr = ''
        for line in rf:
            line = line.strip()
            if len(line) == 0 or line == '@':
                continue

            if line.startswith('@Gais'):
                if len(rec_content) > 0:
                    if search_success:
                        if positive_wf is not None:
                            positive_wf.write(rec_content.rstrip()+'\n\n')
                    else:
                        if negative_wf is not None:
                            negative_wf.write(rec_content.rstrip()+'\n\n')

                rec_content = '@\n@Gais_REC:\n'
                search_success = False
                continue

            else:
                rec_content += line + '\n'

                attr = rec_get_attr(line)
                content = rec_get_content(line)

                if attr is not None and len(attr) > 0:
                    now_in_attr = attr

                if _need_check_keyword(now_in_attr,target_attrs,untarget_attrs) and not search_success:
                    if search_func is not None:
                        search_func(content,kw_list)

                    else:
                        for keyword in kw_list:
                            if content.find(keyword) >= 0:
                                search_success = True
                                break


class filter_rerouter:
    def __init__(self):
        self.node_map = {}
        self.tmp_output_counter = {}

    def add_node(self, node):
        self.node_map[node.name] = node

    def set_node_output_tmp(self, node_name, positive_or_negative):
        if node_name not in self.node_map:
            _raise_filterError("input_fn is not a string")

        if positive_or_negative != 'positive' and positive_or_negative != 'negative':
            _raise_filterError("positive_or_negative != 'positive' and 'negative'")

        if positive_or_negative == 'positive':
            self.tmp_output_counter[self.node_map[node_name].positive_child] = -1

        elif positive_or_negative == 'negative':
            self.tmp_output_counter[self.node_map[node_name].negative_child] = -1

    def _connect_nodes(self):
        node_list = list(self.node_map.values())

        for node in node_list:
            if isinstance(node.parent, tuple):
                parent_tuple = node.parent
                parent_node_name = node.parent[0]
                positive_or_negative = node.parent[1]

                if parent_node_name not in self.node_map:
                    _raise_filterError("ConnectError in node " + node_name + "'s parent " + str(parent_tuple) + ": " + parent_node_name + " does not exist in node map")

                if positive_or_negative == 'positive':
                    node.parent = self.node_map[parent_node_name].positive_child

                elif positive_or_negative == 'negative':
                    node.parent = self.node_map[parent_node_name].negative_child

                if node.parent is None:
                    _raise_filterError("ConnectError in node " + node_name + "'s parent " + str(parent_tuple) + ": get a None parent")

                if node.parent in self.tmp_output_counter:
                    if self.tmp_output_counter[node.parent] == -1:
                        self.tmp_output_counter[node.parent] = 1
                    else:
                        self.tmp_output_counter[node.parent] += 1


    def exec(self):
        self._connect_nodes()

        node_list = list(self.node_map.values())
        node_finish_num = 0

        while node_finish_num < len(node_list):
            for node in node_list:
                if node.status == 'pending' and isfile(node.parent):
                    node.run()

                    node_finish_num += 1
                    if node.parent in self.tmp_output_counter:
                        self.tmp_output_counter[node.parent] -= 1

                        if self.tmp_output_counter[node.parent] == 0:
                            os.remove(node.parent)





class rerouter_node:
    def __init__(self, name, filter_func, positive_output_fn = None, input_fn = None, input_node = None, negative_output_fn = None):
        if input_fn is not None and not isinstance(input_fn, str):
            _raise_filterError("input_fn is not a string")

        if input_fn is not None and not isfile(input_fn):
            _raise_filterError("input_fn is not an existing file")

        if input_node is not None and not isinstance(input_node, tuple):
            _raise_filterError("input_node is not a tuple")

        if input_fn is None and input_node is None:
            _raise_filterError("Both input_node and input_fn are None")

        if input_fn is not None and input_node is not None:
            _raise_filterError("Both input_node and input_fn are not None")

        if positive_output_fn is not None and not isdir(os.path.dirname(positive_output_fn)):
            _raise_filterError("positive_output_fn's dirname is invalid")

        if negative_output_fn is not None and not isdir(os.path.dirname(negative_output_fn)):
            _raise_filterError("negative_output_fn's dirname is invalid")

        if input_fn is not None:
            self.parent = input_fn
        elif input_node is not None:
            self.parent = input_node

        self.name = name
        self.positive_child = positive_output_fn
        self.negative_child = negative_output_fn
        self.filter_func = filter_func

        self.status = 'pending' # [pending, running, stop, done]

    def run(self):
        if not isinstance(self.parent, str):
            _raise_filterError("self.parent is not a string")

        self.status = 'running'
        self.filter_func(
            input_fn = self.parent,
            positive_output_fn = self.positive_child,
            negative_output_fn = self.negative_child,
        )

        self.status = 'done'



# class filter_assemblyLine:
    # def __init__(self):


