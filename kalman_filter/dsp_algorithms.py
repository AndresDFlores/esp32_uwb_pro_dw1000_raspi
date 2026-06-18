import kalman_filter as kf


def dsp_kalman(value):
    return kf.get_filtered_distance(anchor_id=1, raw_distance=value)