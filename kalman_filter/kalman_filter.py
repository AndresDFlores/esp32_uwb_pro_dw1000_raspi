

class KalmanFilter1D:
    def __init__(self, process_noise=0.01, measurement_noise=0.1):
        # measurement_noise = your sensor uncertainty (0.1m for DW1000)
        self.q = process_noise   # how fast the true distance can change
        self.r = measurement_noise
        self.x = None            # state estimate
        self.p = 1.0             # estimate uncertainty

    def update(self, measurement):
        if self.x is None:
            self.x = measurement
            return self.x
        # Predict
        self.p += self.q
        # Update
        k = self.p / (self.p + self.r)       # Kalman gain
        self.x += k * (measurement - self.x)
        self.p *= (1 - k)
        return self.x

anchors = {
    1: (0.0, 0.0)
}

anchor_ids = list(anchors.keys())   # ["A0", "A1", "A2"]
filters = {anchor_id: KalmanFilter1D(process_noise=0.0001, measurement_noise=0.1) for anchor_id in anchor_ids}

def get_filtered_distance(anchor_id, raw_distance):
    return filters[anchor_id].update(raw_distance)


'''
# Tag barely moving / slow:
KalmanFilter1D(process_noise=0.001, measurement_noise=0.1)

# Tag walking speed (~1.5 m/s):
KalmanFilter1D(process_noise=0.05, measurement_noise=0.1)

# Fast-moving tag / robot:
KalmanFilter1D(process_noise=0.5, measurement_noise=0.1)
'''