#coding=utf-8
from __future__ import absolute_import

import commands, os, re
from sys import getsizeof, stderr
from itertools import chain
from collections import deque
try:
    from reprlib import repr
except ImportError:
    pass

def total_size(o, handlers={}, verbose=False):
    """
    Returns the approximate memory footprint an object and its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print 'verbose:', s, type(o), repr(o), stderr

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)
    
    
def current_process_info():  
    pid = os.getpid()  
    res = commands.getstatusoutput('ps aux|grep '+str(pid))[1].split('\n')[0]  
  
    p = re.compile(r'\s+')  
    l = p.split(res)  
    info = {'user':l[0],  
        'pid':l[1],  
        'cpu':l[2],  
        'mem':l[3],  
        'vsa':l[4],  
        'rss':l[5],  
        'start_time':l[6]}  
    return info  