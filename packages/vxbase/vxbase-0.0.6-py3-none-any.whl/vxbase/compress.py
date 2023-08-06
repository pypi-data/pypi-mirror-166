import logging
from os import path
from shutil import move
import tarfile
from types import is_iterable

_logger = logging.getLogger(__name__)


def compress_files(name, files, dest_folder=None, cformat='bz2'):
    """ Compress a file, set of files or a folder in the specified cforma

    :param name: Desired file name w/o extension
    :param files: A list with the absolute o relative path to the files
                      that will be added to the compressed file
    :param dest_folder: The folder where will be stored the compressed file
    :param cformat: Desired format for compression, only supported bz2 and gz
    """
    if not dest_folder:
        dest_folder = '.'
    if cformat not in ['bz2', 'gz', 'tar']:
        raise RuntimeError('Unknown file format "{}"'.format(cformat))
    ext = ''
    if cformat == 'gz':
        fobject, modestr = tarfile.open, 'w:gz'
        ext = 'tar.gz'
    elif cformat == 'tar':
        fobject, modestr = tarfile.open, 'w:'
        ext = 'tar'
    elif cformat == 'bz2':
        fobject, modestr = tarfile.open, 'w:bz2'
        ext = 'tar.bz2'
    _logger.debug("Generating compressed file: %s in %s folder",
                  name, dest_folder)

    bkp_name = '{0}.{1}'.format(name, ext)
    full_tmp_name = path.join(
        dest_folder,
        '._{}'.format(bkp_name)
    )
    full_name = path.join(dest_folder, bkp_name)

    with fobject(full_tmp_name, mode=modestr) as tar_file:
        for fname in files:
            if is_iterable(fname):
                tar_file.add(fname[0], path.join(name, fname[1]))
            else:
                basename = path.basename(fname)
                tar_file.add(fname, path.join(name, basename))
    move(full_tmp_name, full_name)
    return full_name
