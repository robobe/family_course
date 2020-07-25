def linear_interpolate(var_value,
    low_output=1100, high_output=1900,
    var_low=1100, var_high=1900):

    if var_value <= var_low:
        return low_output

    if var_value >= var_high:
        return high_output

    p = (var_value - var_low) / (var_high - var_low)
    return low_output + p * (high_output - low_output)

def expo_curve(x, alpha):
    return (1.0 - alpha) * x + alpha * x * x * x

def constrain_value(my_value, min_value, max_value):
    return max(min(my_value, max_value), min_value)


def throttle_curve(thr_mid, alpha, thr_in):
    """
    throttle curve generator
    * thr_mid: output at mid stick
    * alpha: expo coefficient
    * thr_in: [0-1]
    """
    alpha2 = alpha + 1.25 * (1.0 - alpha) * (0.5 - thr_mid) / 0.5
    alpha2 = constrain_value(alpha2, 0.0, 1.0)
    thr_out = 0.0
    if thr_in > 0.5:
        t = linear_interpolate(thr_in, -1.0, 0.0, 0.0, 0.5)
        thr_out = linear_interpolate(expo_curve(t, alpha2),
            0.0, thr_mid,
            -1.0, 0.0)
    else:
        t = linear_interpolate(thr_in, 0.0, 1.0, 0.5, 1.0)
        thr_out = linear_interpolate(expo_curve(t, alpha2),
            thr_mid , 1.0, 
            -1.0, 0.0)
    return thr_out

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    import numpy as np
    import functools
    # x = linear_interpolate(1500)
    map_range = functools.partial(linear_interpolate,
        low_output=-1, 
        high_output=1,
        var_low=1100, 
        var_high=1900)
    f = functools.partial(expo_curve, alpha=1.0)
    x = np.arange(1100, 1900, 1, np.int16 )
    x1 = np.array(list(map(map_range, x)))
    y = np.array(list(map(f, x1)))

    map_range = functools.partial(linear_interpolate,
        low_output=0, 
        high_output=1,
        var_low=1100, 
        var_high=1900)
    f = functools.partial(throttle_curve, 0.5, 0.5)
    x1 = np.array(list(map(map_range, x)))
    y = np.array(list(map(f, x1)))
    x = np.array([1100,1200,1300,1400,1500,1600,1700,1800,1900])
    f = lambda x: (0.012*pow(x,2)) - (16.97*x) + 8857
    y = np.array(list(map(f, x)))
    plt.scatter(x,y)
    plt.show()
    

