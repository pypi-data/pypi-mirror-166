#!/usr/bin/env python
'''
Created by Seria at 02/11/2018 3:38 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
import os
import csv
import h5py
from multiprocessing import cpu_count
from math import ceil
from torch.utils.data import Dataset, DataLoader
from torch.utils.data._utils.collate import default_collate
from torch import cuda

from ..law import Constant

__all__ = ('Tank', 'Depot', 'load_h5', 'load_csv')



def load_h5(data_path):
    assert data_path.endswith('h5') or data_path.endswith('hdf5')
    hdf5 = h5py.File(data_path, 'r')
    return hdf5

def load_csv(data_path, data_specf):
    assert data_path.endswith('csv') or data_path.endswith('txt')
    tdata = {}
    with open(data_path, 'r') as csvf:
        csvr = csv.reader(csvf, delimiter=Constant.CHAR_SEP, quotechar=Constant.FIELD_SEP)
        for l, line in enumerate(csvr):
            if l == 0:
                keys = line
                tdata = {k: [] for k in keys}
                continue
            for i, val in enumerate(line):
                if data_specf[keys[i]].startswith('int'):
                    tdata[keys[i]].append(int(val))
                elif data_specf[keys[i]].startswith('float'):
                    tdata[keys[i]].append(float(val))
                else:
                    tdata[keys[i]].append(val)
    return tdata



class Tank(Dataset):
    def __init__(self, *args, **kwargs):
        self._length = self.load(*args, **kwargs)

    def load(self, *args, **kwargs) -> int:
        raise NotImplementedError

    def fetch(self, idx):
        raise NotImplementedError

    def collate(self, batch):
        return default_collate(batch)

    def __getitem__(self, item):
        return self.fetch(item)

    def __len__(self):
        return self._length


class Depot(object):
    def __init__(self, engine):
        self.rank = int(os.environ.get('RANK', -1))
        self.nworld = int(os.environ.get('WORLD_SIZE', 1))
        if hasattr(engine, 'chip'):
            self._chip = engine.chip[self.rank]
        else:
            self._chip = None
        self._tanks = {}
        self._batch_size = {}
        self.MPE = {}

    def mount(self, tank, batch_size, shuffle=True, in_same_size=True, nworker=-1, prefetch=0):
        # >| get unique id
        tid = '0t' + hex(id(tank))[2:]
        # >| check argument validity
        if tid in self._tanks.keys():
            raise AttributeError('NEBULAE ERROR ⨷ this tank has already been mounted.')
        if nworker == 0 and prefetch > 0:
            raise ValueError('NEBULAE ERROR ⨷ the number of workers should be more than 1 when prefetcher is enabled.')
        assert nworker != 0, 'NEBULAE ERROR ⨷ the number of workers must be a positive integer.'
        if nworker == 0:
            cpu_prefetch = 2 # pytorch's default value for single process
        else:
            cpu_prefetch = max(1, prefetch) # at least be 1 in pytorch
        gpu_prefetch = prefetch > 0 and (self._chip is not None) and cuda.is_available() # no matter how many batches to prefetch is all the same

        # >| mount dataset
        self._batch_size[tid] = batch_size
        if in_same_size:
            self.MPE[tid] = len(tank) // (batch_size * self.nworld)
        else:
            self.MPE[tid] = ceil(len(tank) / (batch_size * self.nworld))
        nworker = cpu_count() if nworker <= 0 else nworker - 1
        if self.rank >= 0:
            from torch.utils.data import distributed as dist
            sampler = dist.DistributedSampler(tank)
            loader = DataLoader(tank, batch_size, sampler=sampler, collate_fn=tank.collate,
                                      drop_last=in_same_size, num_workers=nworker, prefetch_factor=cpu_prefetch)
        else:
            loader = DataLoader(tank, batch_size, shuffle, collate_fn=tank.collate,
                                      drop_last=in_same_size, num_workers=nworker, prefetch_factor=cpu_prefetch)
        # >| prefetch if necessary
        if gpu_prefetch:
            self._tanks[tid] = [tank, loader, loader.__iter__(), 0, cuda.Stream(device=self._chip)]
            self._prefetch(tid)
        else:
            self._tanks[tid] = [tank, loader, loader.__iter__(), 0]
        return tid

    def unmount(self, tid):
        assert tid in self._tanks.keys(), 'NEBULAE ERROR ⨷ this tank is not mounted in the depot.'
        self._tanks.pop(tid)
        self._batch_size.pop(tid)
        self.MPE.pop(tid)

    def _prefetch(self, tid):
        # self._fetched_data = self._fetch(tid)
        with cuda.stream(self._tanks[tid][4]):
            self._fetched_data = self._fetch(tid)
            # self.next_input = self.next_input.cuda(device=self.chip, non_blocking=True)

    def _fetch(self, tid):
        loader, iterator, counter = self._tanks[tid][1:4]
        if counter == self.MPE[tid]:
            iterator = loader.__iter__()
            self._tanks[tid][2:4] = iterator, 1
        else:
            self._tanks[tid][3] += 1
        return iterator.__next__()

    def _next(self, tid):
        if len(self._tanks[tid]) == 5:
            cuda.current_stream().wait_stream(self._tanks[tid][4])
            fetched_data = self._fetched_data
            self._prefetch(tid)
            return fetched_data
        else:
            return self._fetch(tid)

    def next(self, tid=None):
        if tid is None:
            ret = {}
            for k in self._tanks.keys():
                ret[k] = self._next(k)
            return ret
        else:
            return self._next(tid)