"""Utilities that can be used at resolve-time, IOW inside the `commands()` function in package.py

Read the rez wiki for configuring rez to enable usage of these utils.

Requirements:
    - `package_definition_python_path` config setting
    - Download these utilities to `package_definition_python_path`

Usage:
    - Import utilities by using the `@include("commands_utils")` decorator with `commands()`
    - Call a utility inside `commands()` e.g. `commands_utils.foo_function(this, env)`
"""
import os
import subprocess
import rez.config


def normalize_path(path, typ="unix"):
    """Uses cypath util to convert paths to unix, windows, or mixed
    Warning: Only use when default_shell is gitbash
    """
    cmd = "cygpath"
    if typ == "unix":
        cmd += " -u"
    elif typ == "mixed":
        cmd += " -m"
    else:
        cmd += " -w"
    cmd += " \"{path}\"".format(path=path)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    if not p.returncode:
        return out.strip()


def get_root_path(this, env):
    """Format the root package path so that it's compatible with PATH
    Works around some issues if platform is Windows and using gitbash
    """
    config = rez.config.create_config()
    shell = config.get("default_shell")
    env.PACKAGE_ROOT_PATH = None

    if shell == "gitbash":
        env.PACKAGE_ROOT_PATH = normalize_path(str(this.root))
    else:
        env.PACKAGE_ROOT_PATH = str(this.root)


def set_root_path(this, env, *subdirs):
    """Prepend to PATH the pre-processed root package path if it exists
    Concats and appends subdirs to then end of the root package path before setting
    """
    if env.PACKAGE_ROOT_PATH:
        env.PATH.prepend(
            os.path.join("${PACKAGE_ROOT_PATH}", *subdirs).replace("\\", "/")
        )
    else:
        env.PATH.prepend(
            os.path.join(str(this.root), *subdirs).replace("\\", "/")
        )


def get_root_python_path(this, env):
    """Format the root package path so that it's compatible with PYTHONPATH
    Works around some issues if platform is Windows and using gitbash
    """
    config = rez.config.create_config()
    shell = config.get("default_shell")
    env.PACKAGE_ROOT_PYTHON_PATH = None

    if shell == "gitbash":
        env.PACKAGE_ROOT_PYTHON_PATH = normalize_path(str(this.root), typ="mixed")
    else:
        env.PACKAGE_ROOT_PYTHON_PATH = str(this.root)


def set_root_python_path(this, env, *subdirs):
    """Prepend to PYTHONPATH the pre-processed root package path if it exists
    Concats and appends subdirs to then end of the root package path before setting
    Warning: Overrides ``env_var_separators`` global config setting
    """
    config = rez.config.create_config()
    shell = config.get("default_shell")
    
    if shell == "gitbash":
        overrides = {"env_var_separators": {"PYTHONPATH": ";"}}
        rez.config.create_config(overrides)

    if env.PACKAGE_ROOT_PYTHON_PATH:
        env.PYTHONPATH.prepend(
            os.path.join("${PACKAGE_ROOT_PYTHON_PATH}", *subdirs).replace("\\", "/")
        )
    else:
        env.PYTHONPATH.prepend(
            os.path.join(str(this.root), *subdirs).replace("\\", "/")
        )
