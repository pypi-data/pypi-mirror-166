import gzip
import os
from collections import deque

class _None_in_context_manager:
    def __init__(self):
        pass

    def __enter__(self):
        return None

    def __exit__(self, *args):
        pass

def general_open2(filename,mode='rt',**kwargs):
    if filename.endswith(".gz"):
        if 'buffering' in kwargs:

            if 'r' in mode:
                f = open(filename,'rb',buffering = kwargs['buffering'])
            elif 'w' in mode:
                f = open(filename,'wb',buffering = kwargs['buffering'])
            elif 'x' in mode:
                f = open(filename,'xb',buffering = kwargs['buffering'])

            del kwargs['buffering']

            return gzip.open(f,mode,**kwargs)
        else:
            return gzip.open(filename,mode,**kwargs)
    else:
        return open(filename,mode,**kwargs)

def general_open(filename,mode='rt',**kwargs):
    if filename is None:
        return _None_in_context_manager()
    if filename.endswith(".gz"):
        return gzip.open(filename,mode,**kwargs)
    else:
        return open(filename,mode,**kwargs)

def filename_add_id(filename,idname):
    slash_pos = filename.rfind('/')
    if slash_pos == -1:
        dot_pos = filename.find('.')
    else:
        dot_pos = filename.find('.',slash_pos)

    if dot_pos == -1:
        return filename + idname
    else:
        return filename[:dot_pos] + str(idname) + filename[dot_pos:]

def get_dirname(path):
    return os.path.dirname(os.path.abspath(path))

def rec_get_attr(line):
    if len(line) == 0 or line[0] != '@':
        return None

    if line == '@':
        return ''

    comma_pos = line.find(':')

    if comma_pos == -1:
        return line[1:]

    else:
        return line[1:comma_pos]

def rec_get_content(line):
    if len(line) == 0 or line[0] != '@':
        return line

    if line == '@':
        return ''

    comma_pos = line.find(':')

    if comma_pos == -1:
        return ''

    else:
        return line[comma_pos+1:]

def read_rec(infile, init_read, attr=None, attr_list=None):
    if attr is None and attr_list is None:
        raise Exception("Argument attr and attr_list is None in shno_lib.data_io.file_io read_rec")
    if attr is not None and attr_list is not None:
        raise Exception("Argument attr and attr_list is not None in shno_lib.data_io.file_io read_rec")

    content = ''
    attr_content = None
    attr_info = {}
    attr_set = set()
    now_attr = ''

    if attr_list is not None:
        attr_set = set(attr_list)

    if not init_read:
        content += '@\n@Gais_REC:\n'

    while True:
        line = infile.readline()

        if len(line) == 0:
            if attr is not None:
                return attr_content, content
            elif attr_list is not None:
                return attr_info, content
            else:
                return None, None

        elif attr_content is None:
            attr_content = ''

        if line == '@\n' and not init_read:
            continue

        if line.startswith('@Gais_'):
            if not init_read:
                if attr is not None:
                    return attr_content, content
                elif attr_list is not None:
                    return attr_info, content
                else:
                    return None, None
            else:
                init_read = False

        if line[0] == '@' and line.find(':') > -1:
            line_attr = line[1:line.find(':')]
            if attr is not None and line_attr == attr:
                attr_content = line[2+len(line_attr):].strip()
                now_attr = line_attr
            elif attr_list is not None and line_attr in attr_set:
                attr_info[line_attr] = line[2+len(line_attr):].strip()
                now_attr = line_attr
            else:
                now_attr = ''

        else:
            if attr is not None and now_attr == attr:
                attr_content += '\n' + line.strip()

            elif attr_list is not None and now_attr in attr_set:
                attr_info[now_attr] += '\n' + line.strip()

            else:
                now_attr = ''


        content += line

def line_startswith_gais_head(line, gais_head_list, infile):
    now_seek_pos = infile.tell()

    for i, gais_head_part in enumerate(gais_head_list):
        if line == gais_head_part + '\n':
            if i == len(gais_head_list)-1:
                return True
            line = infile.readline()
            continue

        else:
            infile.seek(now_seek_pos)
            return False

    infile.seek(now_seek_pos)
    return False


def read_rec_generator(infile, attr=None, attr_list=None, gais_head='@\n@Gais_REC:', unwant_attr=None, want_attr=None):
    if attr is None and attr_list is None:
        raise Exception("Argument attr and attr_list is None in shno_lib.data_io.file_io read_rec")
    if attr is not None and attr_list is not None:
        raise Exception("Argument attr and attr_list is not None in shno_lib.data_io.file_io read_rec")

    if unwant_attr is not None:
        mode = 'unwant'
        unwant_attr_set = set(unwant_attr)
    elif want_attr is not None:
        mode = 'want'
        want_attr_set = set(want_attr)
    else:
        mode = ''

    gais_head_list = gais_head.strip('\n').split('\n')

    content = gais_head.rstrip() + '\n'
    attr_content = None
    attr_info = {}
    attr_set = set()
    now_attr = ''

    if attr_list is not None:
        attr_set = set(attr_list)

    while True:
        line = infile.readline()

        if len(line) == 0:
            if attr is not None:
                yield attr_content, content
                break
            elif attr_list is not None:
                yield attr_info, content
                break
            else:
                break

        if line == gais_head_list[0] + '\n' and line_startswith_gais_head(line, gais_head_list, infile):
            if attr is not None:
                if content == gais_head.rstrip() + '\n' and attr_content is None:
                    continue
                else:
                    yield attr_content, content
                    content = gais_head.rstrip() + '\n'
                    attr_content = None
                    continue
            elif attr_list is not None:
                if content == gais_head.rstrip() + '\n' and len(attr_info) == 0:
                    continue
                else:
                    yield attr_info, content
                    content = gais_head.rstrip() + '\n'
                    attr_info = {}
                    continue
            else:
                break

        if line[0] == '@' and line.find(':') > -1:
            line_attr = line[1:line.find(':')]
            if attr is not None and line_attr == attr:
                attr_content = line[2+len(line_attr):].strip()
                now_attr = line_attr
            elif attr_list is not None and line_attr in attr_set:
                attr_info[line_attr] = line[2+len(line_attr):].strip()
                now_attr = line_attr
            else:
                now_attr = line_attr

        else:
            if attr is not None and now_attr == attr:
                attr_content += '\n' + line.strip()

            elif attr_list is not None and now_attr in attr_set:
                attr_info[now_attr] += '\n' + line.strip()

            else:
                # now_attr = ''
                pass

        if mode == 'want':
            if now_attr in want_attr_set:
                content += line
        elif mode == 'unwant':
            if now_attr not in unwant_attr_set:
                content += line
        else:
            content += line

def line_startswith_gais_head2(line, gais_head_list, infile, buffer_line_list):
    for i, gais_head_part in enumerate(gais_head_list):
        if line == gais_head_part + '\n':
            if i == len(gais_head_list)-1:
                return True
            line = infile.readline()
            buffer_line_list.append(line)
            continue

        else:
            return False

    return False


def read_rec_generator2(infile, attr=None, attr_list=None, gais_head='@\n@Gais_REC:', unwant_attr=None, want_attr=None):
    if attr is None and attr_list is None:
        raise Exception("Argument attr and attr_list is None in shno_lib.data_io.file_io read_rec")
    if attr is not None and attr_list is not None:
        raise Exception("Argument attr and attr_list is not None in shno_lib.data_io.file_io read_rec")

    if unwant_attr is not None:
        mode = 'unwant'
        unwant_attr_set = set(unwant_attr)
    elif want_attr is not None:
        mode = 'want'
        want_attr_set = set(want_attr)
    else:
        mode = ''

    gais_head_list = gais_head.strip('\n').split('\n')

    content_list = [gais_head.rstrip() + '\n']
    attr_content = None
    attr_info = {}
    attr_set = set()
    now_attr = ''
    buffer_line_list = deque()

    if attr_list is not None:
        attr_set = set(attr_list)

    while True:
        if len(buffer_line_list) == 0:
            line = infile.readline()
        else:
            buffer_line_list.popleft()
            continue

        if len(line) == 0:
            if attr is not None:
                yield attr_content, ''.join(content_list)
                break
            elif attr_list is not None:
                yield attr_info, ''.join(content_list)
                break
            else:
                break

        if line == gais_head_list[0] + '\n' and line_startswith_gais_head2(line, gais_head_list, infile, buffer_line_list):
            if attr is not None:
                if len(content_list) == 1 and attr_content is None:
                    continue
                else:
                    yield attr_content, ''.join(content_list)
                    content_list.clear()
                    content_list.append(gais_head.rstrip() + '\n')
                    attr_content = None
                    continue
            elif attr_list is not None:
                if len(content_list) == 1 and len(attr_info) == 0:
                    continue
                else:
                    yield attr_info, ''.join(content_list)
                    content_list.clear()
                    content_list.append(gais_head.rstrip() + '\n')
                    attr_info = {}
                    continue
            else:
                break

        if line[0] == '@':
            comma_pos = line.find(':')

            if comma_pos > -1:
                line_attr = line[1:comma_pos]
                if attr is not None and line_attr == attr:
                    attr_content = line[comma_pos+1:].strip()
                    now_attr = line_attr
                elif attr_list is not None and line_attr in attr_set:
                    attr_info[line_attr] = line[comma_pos+1:].strip()
                    now_attr = line_attr
                else:
                    now_attr = line_attr

            else:
                if attr is not None and now_attr == attr:
                    attr_content += '\n' + line.strip()

                elif attr_list is not None and now_attr in attr_set:
                    attr_info[now_attr] += '\n' + line.strip()

                else:
                    pass

        else:
            if attr is not None and now_attr == attr:
                attr_content += '\n' + line.strip()

            elif attr_list is not None and now_attr in attr_set:
                attr_info[now_attr] += '\n' + line.strip()

            else:
                pass

        if mode == 'want':
            if now_attr in want_attr_set:
                content_list.append(line)
        elif mode == 'unwant':
            if now_attr not in unwant_attr_set:
                content_list.append(line)
        else:
            content_list.append(line)







