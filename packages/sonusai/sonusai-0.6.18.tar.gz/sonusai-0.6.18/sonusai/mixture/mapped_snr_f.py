import numpy as np


def calculate_snr_f_statistics(truth_f: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    """Calculate statistics of snr_f truth data.

    For now, includes mean and variance of the raw values (usually energy)
    and mean and standard deviation of the dB values (10 * log10).
    """
    classes = truth_f.shape[1]

    snr_mean = np.zeros(classes, dtype=np.single)
    snr_var = np.zeros(classes, dtype=np.single)
    snr_db_mean = np.zeros(classes, dtype=np.single)
    snr_db_std = np.zeros(classes, dtype=np.single)

    for c in range(classes):
        tmp = truth_f[:, c]
        tmp = tmp[np.isfinite(tmp)]

        if len(tmp) == 0:
            snr_mean[c] = -np.inf
            snr_var[c] = -np.inf
        else:
            snr_mean[c] = np.mean(tmp)
            snr_var[c] = np.var(tmp)

        tmp2 = 10 * np.ma.log10(tmp).filled(-np.inf)
        tmp2 = tmp2[np.isfinite(tmp2)]

        if len(tmp2) == 0:
            snr_db_mean[c] = -np.inf
            snr_db_std[c] = -np.inf
        else:
            snr_db_mean[c] = np.mean(tmp2)
            snr_db_std[c] = np.std(tmp2)

    return snr_mean, snr_var, snr_db_mean, snr_db_std


def calculate_mapped_snr_f(truth_f: np.ndarray, snr_db_mean: np.ndarray, snr_db_std: np.ndarray) -> np.ndarray:
    """Calculate mapped SNR from standard SNR energy per bin/class."""
    import scipy.special as sc

    mapped_snr_f = np.zeros((truth_f.shape[0], truth_f.shape[1]), dtype=np.single)
    snr_db_std_r2 = snr_db_std * np.sqrt(2)
    old_err = np.seterr(invalid='ignore')
    for f in range(truth_f.shape[0]):
        num = 10 * np.ma.log10(truth_f[f, :]).filled(-np.inf) - snr_db_mean
        val = sc.erf(num / snr_db_std_r2)
        mapped_snr_f[f, :] = 0.5 * (1 + val)
    np.seterr(**old_err)

    return mapped_snr_f
