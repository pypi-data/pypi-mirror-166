from argparse import Namespace
from contextlib import suppress
import os
import subprocess
import unittest.mock
from itertools import chain
from pathlib import Path

from merge_requirements.manage_file import Merge
from pipreqsnb import pipreqsnb
from pipreqsnb.pipreqsnb import *

__all__ = ["CustomMerge", "pip_reqs_nb_mocked"]


class CustomMerge(Merge):
    """
    Custom merge method inherited from Merge class
    in merge_requirements.manage_file
    """

    def __init__(self, mf):
        super().__init__(mf)

    def pickup_deps(self, ignore_prefixes: list, unique=True):
        """
        Custom method to pick up dependencies

        Args:
            ignore_prefixes (list): list of prefixes to ignore
            unique (bool): if True, return unique dependencies

        Returns:
            list: list of dependencies

        """

        array = []

        for key, value in self.dict_libs.items():
            if len(value) > 0:
                array.append("".join("{}=={}".format(key, value)))
            else:
                array.append("".join("{}".format(key)))

        result = cleanup_deps(array, ignore_prefixes)

        if unique:
            result = list(set(result))

        return result


def cleanup_deps(deps: list, ignore_prefixes: list) -> list:
    """
    Cleanup dependencies from unwanted prefixes

    Args:
        deps (list): List of dependencies
        ignore_prefixes (list): List of prefixes to ignore

    Returns:
        list: List of dependencies without unwanted prefixes

    Raises:
        None

    """

    cleaned = []

    for dep in deps:

        if (
            next((p for p in ignore_prefixes if p in dep), None)
            is not None
        ):
            continue

        cleaned.append(dep)

    return cleaned


pipreqs_options_store = ['use-local', 'debug', 'print', 'force', 'no-pin']
pipreqs_options_args = ['pypi-server', 'proxy', 'ignore', 'encoding', 'savepath', 'diff', 'clean']


def pip_reqs_nb_mocked(path=None):
    path = path if path is None else os.getcwd()

    namespace = Namespace()

    for preqs_opt in pipreqs_options_store:
        namespace.__setattr__(preqs_opt, None)
    for preqs_opt in pipreqs_options_args:
        namespace.__setattr__(preqs_opt, None)

    namespace.path = str(os.getcwd())

    with suppress(TypeError):
        pip_reqs_nb(namespace)


def pip_reqs_nb(args):
    input_path = args.path
    is_file, is_nb = path_is_file(input_path)

    temp_file_name = '_pipreqsnb_temp_file.py'
    temp_path_folder_name = '__temp_pipreqsnb_folder'
    ignore_dirs = args.ignore if 'ignore' in args else None
    if is_file:
        temp_saving_path = os.path.join(os.getcwd(), temp_path_folder_name)
        if is_nb:
            ipynb_files = [input_path]
        else:
            ipynb_files = []
            os.makedirs(temp_saving_path, exist_ok=True)
            shutil.copyfile(input_path, os.path.join(temp_saving_path, temp_file_name))
    else:
        ipynb_files = get_ipynb_files(input_path, ignore_dirs=ignore_dirs)
        temp_saving_path = os.path.join(input_path, temp_path_folder_name)
    temp_file = os.path.join(temp_saving_path, temp_file_name)
    imports = []
    open_file_args = {}
    if args.encoding is not None:
        open_file_args['encoding'] = args.encoding
    for nb_file in ipynb_files:
        nb = json.load(open(nb_file, 'r', **open_file_args))
        try:
            for n_cell, cell in enumerate(nb['cells']):
                if cell['cell_type'] == 'code':
                    valid_lines = clean_invalid_lines_from_list_of_lines(cell['source'])
                    source = ''.join(valid_lines)
                    imports += get_import_string_from_source(source)
        except Exception as e:
            print(
                "Exception occurred while working on file {}, cell {}/{}".format(nb_file, n_cell + 1, len(nb['cells'])))
            raise e

    # hack to remove the indents if imports are inside functions
    imports = [i.lstrip() for i in imports]

    if is_file:
        args.savepath = set_requirements_savepath(args)
        args.path = temp_saving_path
    try:
        os.makedirs(temp_saving_path, exist_ok=True)
        with open(temp_file, 'a') as temp_file:
            for import_line in imports:
                temp_file.write('{}\n'.format(import_line))
        pipreqs_args = generate_pipreqs_str(args)

        # run_pipreqs(pipreqs_args)
        retcode = subprocess.Popen(
            f"pipreqs {pipreqs_args}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        ).wait()

        if retcode != 0:
            raise Exception(
                "Error while running requirements generation."
            )

        shutil.rmtree(temp_saving_path)
    except Exception as e:
        if os.path.isfile(temp_file):
            os.remove(temp_file)
        raise e
