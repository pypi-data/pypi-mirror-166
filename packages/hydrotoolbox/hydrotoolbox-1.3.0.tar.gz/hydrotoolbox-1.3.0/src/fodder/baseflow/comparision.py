import numpy as np


def strict_baseflow(Q):
    dQ = (Q[2:] - Q[:-2]) / 2

    # 1. flow data associated with positive and zero values of dy / dt
    wet1 = np.concatenate([[True], dQ >= 0, [True]])

    # 2. previous 2 points before points with dy/dt≥0, as well as the next 3 points
    idx_first = np.where(wet1[1:].astype(int) - wet1[:-1].astype(int) == 1)[0] + 1
    idx_last = np.where(wet1[1:].astype(int) - wet1[:-1].astype(int) == -1)[0]
    idx_before = np.repeat([idx_first], 2) - np.tile(range(1, 3), idx_first.shape)
    idx_next = np.repeat([idx_last], 3) + np.tile(range(1, 4), idx_last.shape)
    idx_remove = np.concatenate([idx_before, idx_next])
    wet2 = np.full(Q.shape, False)
    wet2[idx_remove.clip(min=0, max=Q.shape[0] - 1)] = True

    # 3. five data points after major events (90th quantile)
    growing = np.concatenate([[True], (Q[1:] - Q[:-1]) >= 0, [True]])
    idx_major = np.where((Q >= np.quantile(Q, 0.9)) & growing[:-1] & ~growing[1:])[0]
    idx_after = np.repeat([idx_major], 5) + np.tile(range(1, 6), idx_major.shape)
    wet3 = np.full(Q.shape, False)
    wet3[idx_after.clip(min=0, max=Q.shape[0] - 1)] = True

    # 4. flow data followed by a data point with a larger value of -dy / dt
    wet4 = np.concatenate([[True], dQ[1:] - dQ[:-1] < 0, [True, True]])

    # dry points, namely strict baseflow
    dry = ~(wet1 + wet2 + wet3 + wet4)

    return dry
