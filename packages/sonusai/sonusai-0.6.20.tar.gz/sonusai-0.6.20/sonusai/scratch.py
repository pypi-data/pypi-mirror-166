import h5py
import numpy as np

from sonusai.mixture import calculate_mapped_snr_f
from sonusai.mixture import calculate_snr_f_statistics


def main():
    with h5py.File('/opt/Aaware/sonusai/scratch/senh1-snr30m15-test.h5', 'r') as f:
        truth_f = np.array(f['truth_f'])

    snr_mean, snr_var, snr_db_mean, snr_db_std = calculate_snr_f_statistics(truth_f)

    mapped_snr_f = np.zeros((truth_f.shape[0], truth_f.shape[1]), dtype=np.single)
    for f in range(truth_f.shape[0]):
        mapped_snr_f[f] = calculate_mapped_snr_f(truth_f[f], snr_db_mean, snr_db_std)

    with h5py.File('/opt/Aaware/sonusai/scratch/mapped_snr_f_test.h5', 'w') as f:
        f.create_dataset(name='truth_f', data=truth_f)
        f.create_dataset(name='mapped_snr_f', data=mapped_snr_f)
        f.create_dataset(name='snr_mean', data=snr_mean)
        f.create_dataset(name='snr_var', data=snr_var)
        f.create_dataset(name='snr_db_mean', data=snr_db_mean)
        f.create_dataset(name='snr_db_std', data=snr_db_std)


if __name__ == '__main__':
    main()
