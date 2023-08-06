from timeit import default_timer as timer

import h5py
import numpy as np

from sonusai.utils import EngineeringNumber


def main():
    filename = '/opt/Aaware/sonusai/tests/data/test_advanced_genmix.h5'
    dname = 'truth_t'

    with h5py.File(filename, 'r') as f:
        print(list(f.keys()))

    start = timer()
    with h5py.File(filename, 'r') as f:
        d = np.array(f[dname])
    end = timer()
    print(f'shape: {d.shape}')
    print(f'took {EngineeringNumber(end - start)}s')

    start = timer()
    with h5py.File(filename, 'r') as f:
        d = f[dname].shape
    end = timer()
    print(f'shape: {d}')
    print(f'type: {type(d)}')
    print(f'took {EngineeringNumber(end - start)}s')


if __name__ == '__main__':
    main()
