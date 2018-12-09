#!/usr/bin/env python

import argparse
import json
import shutil

from os import path, getcwd, remove
from sys import stderr
from mod import *


def init(args):
    file_path = path.join(args.path, UTILS_FILE)
    if path.isfile(file_path):
        print('Project already initialized under {}'
              .format(args.path), file=stderr)
        return
    with open(file_path, 'w') as f:
        f.write('[]')


def register(args):
    if not path.isfile(UTILS_FILE):
        if args.init:
            init(argparse.Namespace(path='.'))
        else:
            print('No project initialized under {}'.format(getcwd()),
                  file=stderr)
            return

    # there cannot be repeated language instances per project
    utils = None
    lang_entry = {'lang': args.lang.lower(), 'path': None, 'deps': []}
    with open(UTILS_FILE) as utilsf:
        try:
            utils = json.load(utilsf)
        except json.JSONDecodeError:
            print('Corrupted UTILS_FILE', file=stderr)
            return
        for entry in utils:
            if entry['lang'] == args.lang:
                if args.update:
                    lang_entry = entry
                    break
                else:
                    print('Language {} already initialized in current project'
                          .format(args.lang), file=stderr)
                    return
        # if update
        if lang_entry['path'] is not None:
            utils.remove(lang_entry)

    # get language support
    lang = get_lang(args.lang)

    # create source files
    try:
        lang_entry['path'] = lang.register_source(args.path, args.create)
        # update application state
        utils.append(lang_entry)
    except ValueError as e:
        print('Could not register file(s) under {}: {}'.format(args.path, e))
        return

    # backup file
    backup = '{}.bak'.format(UTILS_FILE)
    shutil.copyfile(UTILS_FILE, backup)

    # save file
    with open(UTILS_FILE, 'w') as utilsf:
        try:
            json.dump(utils, utilsf)
        except TypeError:
            print('Could not serialize application state', file=stderr)
            shutil.copyfile(backup, UTILS_FILE)
            return

    # remove backup
    remove(backup)


def add(args):
    print('Not implemented', file=stderr)


def rm(args):
    print('Not implemented', file=stderr)


def ls(args):
    print('Not implemented', file=stderr)


def main():
    # main parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # init subcommand
    parser_init = subparsers.add_parser(
        'init', help='Initialize utils.pkg file on this project')
    parser_init.add_argument('path', help='Project root directory')
    parser_init.set_defaults(func=init)

    # create subcommand
    parser_register = subparsers.add_parser(
        'register', help='Registers utils.{lang_ext} file')
    parser_register.add_argument(
        '-p', '--path', help='Full path to utils.{lang_ext}', default='.')
    parser_register.add_argument(
        '-i', '--init', help='Initialize project and register.\
        If project is already initialized, this option is ignored.',
        action='store_true')
    parser_register.add_argument(
        '-c', '--create', help='Create file and register.\
        If utils.{lang_ext} already exists, this options is ignored.',
        action='store_true')
    parser_register.add_argument(
        '-u', '--update', help='Update file path', action='store_true')
    parser_register.add_argument(
        'lang', help='Language code', choices=SUPPORTED_LANGUAGES)
    parser_register.set_defaults(func=register)

    # add subcommand
    parser_add = subparsers.add_parser('add', help='Add package')
    parser_add.add_argument('repo', help='Git repository URI')
    parser_add.set_defaults(func=add)

    # rm subcommand
    parser_rm = subparsers.add_parser('rm', help='Remove package')
    parser_rm.add_argument('repo', help='Git repository URI')
    parser_rm.set_defaults(func=rm)

    # ls subcommand
    parser_ls = subparsers.add_parser('ls', help='List installed packages')
    parser_ls.set_defaults(func=ls)

    # execute
    args = parser.parse_args()
    # subcommands are required
    if getattr(args, 'func', None) is None:
        # force print usage
        parser.parse_args(['-h'])
        return
    args.func(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
