#!/bin/env python3

from os import path, listdir, unlink
import shutil
from distutils.core import run_setup
from twine import cli as twine_cli
import semver


def rmrf(folder):
    for filename in listdir(folder):
        file_path = path.join(folder, filename)
        try:
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == "__main__":
    rmrf('build')
    rmrf('dist')
    rmrf('google_sdm.egg-info')

    with open("version", "r") as fh:
        version_str = fh.read()
    with open("version", "w") as fh:
        version = semver.VersionInfo.parse(version_str)
        fh.write(str(version.bump_patch()))

    run_setup('setup.py', script_args=['sdist', 'bdist_wheel'])
    twine_cli.dispatch(['upload', '--non-interactive', 'dist/*'])
