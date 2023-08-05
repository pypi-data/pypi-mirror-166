#!/usr/bin/env python3
#
# The MIT License (MIT)
# Copyright © 2022 Leon Morten Richter (misc@leonmortenrichter.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the “Software”), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import argparse
import ast
import itertools
import pathlib
import sys
import typing

IGNORED_DIRS = ['venv', ]


def parse_file(path: typing.Union[str, pathlib.Path]) -> ast.AST:
    """Open a given file and parse it into a AST"""
    with open(path, 'r') as fd:
        tree = ast.parse(fd.read())
        return tree


def find_matching_test_files(
        start_dir: pathlib.Path, remaining: str = '', pattern: str = r'test_*.py'
) -> typing.Generator[pathlib.Path, None, None]:
    """
    Find path names that match a given pattern recursively.
    @param start_dir: The full path to the start searching
    @param remaining: A partial dir name to look for relative to start_dir
    @param pattern: The file pattern to look for. Refer to unittest discover
    """
    for path in start_dir.rglob(pattern):
        if any(x in str(path) for x in IGNORED_DIRS):
            continue

        if str(path.name).startswith(remaining):
            yield path


def find_matching_class_names(
    tree: ast.AST, partial: str
) -> typing.Generator[str, None, None]:
    """Find matching class names for a given AST"""
    for child in ast.iter_child_nodes(tree):
        if isinstance(child, ast.ClassDef):
            if child.name.startswith(partial):
                yield child.name


def find_matching_method_names(
    tree: ast.AST, classname: str, partial: str
) -> typing.Generator[str, None, None]:
    """Find matching method names for a given AST and classname"""
    # Try to find the class whose methods should be matched
    class_node = None
    for child in ast.iter_child_nodes(tree):
        if isinstance(child, ast.ClassDef):
            if child.name.startswith(classname):
                class_node = child
                break

    if class_node is None:
        # Class could not be found. Nothing to do..
        return

    # Iterate over all method names and try to match partial
    for child in ast.iter_child_nodes(class_node):
        if isinstance(child, ast.FunctionDef):
            if child.name.startswith(partial):
                yield child.name


def module_completions(partial: str) -> typing.Generator[str, None, None]:
    """Get completions for module names"""
    parts = partial.split('.')
    base = pathlib.Path('/'.join(parts[:-1]))

    for path in find_matching_test_files(base, parts[-1]):
        # Yield the file path in dotted notation:
        # tests/test_foo.py --> tests.test_foo
        name_without_ext = str(path.with_suffix(''))
        yield name_without_ext.replace('/', '.')


def classname_completions(partial: str) -> typing.Generator[str, None, None]:
    """Get completions for class names"""
    parts = partial.split('.')
    if not parts:
        return

    # Separate file path and partial class name
    base = parts[:-1]
    path = '/'.join(base) + '.py'
    fpath = pathlib.Path(path)

    if fpath.exists():
        tree = parse_file(fpath)
        for classname in find_matching_class_names(tree, parts[-1]):
            yield '.'.join(base + [classname, ])


def methodname_completions(partial: str) -> typing.Generator[str, None, None]:
    """Get completions for method names"""
    if partial.endswith('.'):
        # Remove repeating trailing dotted dots except one
        partial = partial.rstrip('.') + '.'

    parts = partial.split('.')
    if len(parts) < 2:
        return

    path, classname, partial = parts[:-2], parts[-2], parts[-1]
    fpath = pathlib.Path('/'.join(path) + '.py')
    if fpath.exists():
        tree = parse_file(fpath)
        for methodname in find_matching_method_names(tree, classname, partial):
            yield '.'.join(parts[:-1] + [methodname, ])


def get_arguments_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        'unittest-autocomp.py', description='Autocompletion for unittests'
    )

    parser.add_argument(
        dest='partial',
        nargs='?',
        default=''
    )

    return parser


def main(args: typing.List[str]) -> int:
    parser = get_arguments_parser()
    namespace = parser.parse_args(args)
    partial = namespace.partial

    # Three cases:
    # - completions for the module
    # - completions for the classname
    # - completions of the methodname
    matcher_functions = (
        module_completions,
        classname_completions,
        methodname_completions
    )
    for func in itertools.chain(matcher_functions):
        completions = func(partial)
        print(' '.join(completions))

    return 0


def run():
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)


if __name__ == '__main__':
    run()
