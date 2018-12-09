from os import path as ospath


class SyntaxError(ValueError):
    def __init__(self):
        ValueError.__init__(self, 'Invalid syntax, path must be\
("/path/to/dir" | "/path/to/impl": ("/path/to/header" | h)')


IMPL_TEMPLATE = '''\
#include "{header}"
'''

HEAD_TEMPLATE = '''\
#ifndef UTILS_H
#define UTILS_H

#endif
'''


def register_source(path, create):
    '''
    Register utils source file in path. If file does
    not exist, create? it.
    Note:
        - It should support path as parent directory

    Raise ValueError(msg) if argument is wrong

    Return path field under utils.pkg file
    '''
    cpp_h = path.split(':')

    # if no ':' present, assume argument is a directory
    if len(cpp_h) == 1:
        impl_path = ospath.join(path, 'utils.cpp')
        head_path = ospath.join(path, 'utils.h')
    # first element is implementation, 2nd is header
    elif len(cpp_h) == 2:
        impl_path = cpp_h[0]
        # if 2nd element is 'h', use same path for header
        if cpp_h[1] == 'h':
            known_impl_exts = ['.cpp', '.cc']
            for ext in known_impl_exts:
                head_path = impl_path.replace(ext, '.h')
                if head_path != impl_path:
                    break
            if head_path == impl_path:
                head_path = impl_path + '.h'
        else:
            head_path = cpp_h[1]
    else:
        raise SyntaxError()

    # check parent path existence
    impl_parent = ospath.dirname(impl_path)
    if not ospath.isdir(impl_parent):
        raise ValueError('Unable to find "{}"'.format(impl_parent))
    head_parent = ospath.dirname(head_path)
    if not ospath.isdir(head_parent):
        raise ValueError('Unable to find "{}"'.format(head_parent))

    # create or wimp
    if not ospath.isfile(impl_path):
        if create:
            with open(impl_path, 'w') as implf:
                implf.write(IMPL_TEMPLATE.format(header=head_path))
        else:
            raise ValueError(
                'Implementation file {}, does not exist'.format(impl_path))
    if not ospath.isfile(head_path):
        if create:
            with open(head_path, 'w') as headf:
                headf.write(HEAD_TEMPLATE)
        else:
            raise ValueError(
                'Header file {}, does not exist'.format(head_path))

    # path field
    return '{}:{}'.format(impl_path, head_path)
