# ==================================================================
#            ______ _     _ _        __  __           _ 
#           |  ____(_)   | | |      |  \/  |         | |
#           | |__   _  __| | | ___  | \  / | ___   __| |
#           |  __| | |/ _` | |/ _ \ | |\/| |/ _ \ / _` |
#           | |    | | (_| | |  __/ | |  | | (_) | (_| |
#           |_|    |_|\__,_|_|\___| |_|  |_|\___/ \__,_|
#                                                        fidle.utils
# ==================================================================
# A simple module to host usefull functions for Fidle practical work
# Jean-Luc Parouty 2022

import os, sys
import numpy as np

from collections.abc import Iterable
import datetime
from IPython.display import display,Image,Markdown,HTML

import fidle.config as config



__version__   = config.VERSION


# -------------------------------------------------------------
# Display md
# -------------------------------------------------------------

def subtitle(t):
    '''
    Display a markdown subtitle
    args:
        text to print
    return:
        none
    '''
    display(Markdown(f'<br>**{t}**'))
    

def display_md(text):
    '''
    Display a markdown text
    args:
        text to print
    return:
        none
    '''
    display(Markdown(text))


def display_html(text):
    '''
    Display a HTML text
    args:
        html to print
    return:
        none
    '''
    display(HTML(text))


def display_img(img):
    '''
    Display an image
    args:
        image to print
    return:
        none
    '''
    display(Image(img))


def np_print(*args, precision=3, linewidth=120):
    '''
    Print numpy vectors with a given precision
    args:
        *args : list of numpy vectors
        precision : print precision (3)
        linewidth : line width (120)
    return:
        nothing
    '''
    with np.printoptions(precision=precision, linewidth=linewidth):
        for a in args:
            print(a)


# -------------------------------------------------------------
# Format data
# -------------------------------------------------------------

def hdelay(delay):
    '''
    Returns a duration in human readable format, like 01:14:28 543ms
    delay can be timedelta or seconds
    args:
        delay : in seconds or as a timedelta
    reurns:
        strings
    '''
    if type(delay) is not datetime.timedelta:
        delay=datetime.timedelta(seconds=delay)
    sec = delay.total_seconds()
    hh = sec // 3600
    mm = (sec // 60) - (hh * 60)
    ss = sec - hh*3600 - mm*60
    ms = (sec - int(sec))*1000
    return f'{hh:02.0f}:{mm:02.0f}:{ss:02.0f} {ms:03.0f}ms'


def hsize(num, suffix='o'):
    '''
    Returns a size in human readable version, like 4.3G
    args:
        num: size in bytes
    return:
        String
    '''
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return f'{num:3.1f} {unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f} Y{suffix}'



# -------------------------------------------------------------
# Folder cooking
# -------------------------------------------------------------


def mkdir(path):
    '''
    Create a subdirectory
    Mode is 0750, do nothing if exist
    args:
        path : directory to create
    return:
        none
    '''
    os.makedirs(path, mode=0o750, exist_ok=True)
    

def get_directory_size(path):
    """
    Return the directory size, but only 1 level
    args:
        path : directory path
    return:
        size in Mo
    """
    size=0
    for f in os.listdir(path):
        if os.path.isfile(path+'/'+f):
            size+=os.path.getsize(path+'/'+f)
    return size/(1024*1024)


# -------------------------------------------------------------
# Datasets cooking
# -------------------------------------------------------------


def shuffle_np_dataset(*data):
    """
    Shuffle a list of dataset
    args:
        *data : datasets
    return:
        *datasets mixed
    """
    print('Datasets have been shuffled.')
    p = np.random.permutation(len(data[0]))
    out = [ d[p] for d in data ]
    return out[0] if len(out)==1 else out


def rescale_dataset(*data, scale=1):
    '''
    Rescale numpy array with 'scale' factor
    args:
        *data : arrays
        scale : scale factor
    return:
        arrays of rescaled data
    '''
    print('Datasets have been resized with a factor ', scale)
    out = [ d[:int(scale*len(d))] for d in data ]
    return out[0] if len(out)==1 else out


def pick_dataset(*data,n=5):
    '''Return random subsets of n elements'''
    # ii = np.random.choice(range(len(data[0])), n)
    ii=np.random.choice( len(data[0]), n, replace=False)
    out = [ d[ii] for d in data ]
    return out[0] if len(out)==1 else out


# -------------------------------------------------------------
# Misc
# -------------------------------------------------------------


def update_progress(what,i,imax, redraw=False, verbosity=2, total_max=None):
    """
    Display a text progress bar, as :
    My progress bar : ############# 34%

    Args:
        what  : Progress bar name
        i     : Current progress
        imax  : Max value for i
        verbosity : progress bar verbosity (0: no bar, 1: one line, 2: full progress bar)
        
    Returns:
        nothing
    """
    if verbosity==0:   return
    if verbosity==1 and i<imax: return
    if total_max is None : total_max = imax 
    bar_length = min(40,imax)
    if (i%int(imax/bar_length))!=0 and i<imax and not redraw:
        return
    progress  = float(i/imax)
    block     = int(round(bar_length * progress))
    endofline = '\r' if progress<1 else '\n'
    text = "{:16s} [{}] {:>5.1f}% of {}".format( what, "#"*block+"-"*(bar_length-block), progress*100, total_max)
    print(text, end=endofline)

    
def rmax(l):
    """
    Recursive max() for a given iterable of iterables
    Should be np.array of np.array or list of list, etc.
    args:
        l : Iterable of iterables
    return: 
        max value
    """
    maxi = float('-inf')
    for item in l:
        if isinstance(item, Iterable):
            t = rmax(item)
        else:
            t = item
        if t > maxi:
            maxi = t
    return maxi


def rmin(l):
    """
    Recursive min() for a given iterable of iterables
    Should be np.array of np.array or list of list, etc.
    args:
        l : Iterable of iterables
    return: 
        min value
    """
    mini = float('inf')
    for item in l:
        if isinstance(item, Iterable):
            t = rmin(item)
        else:
            t = item
        if t < mini:
            mini = t
    return mini

