import numpy as np

def euler_integrate(fun, t0, y0, tStop, h):
    T = np.arange(t0, tStop + h, h)
    Y = np.zeros(T.shape)
    Y[0] = y0

    for i in range(1, len(T)):
        Y[i] = Y[i-1] + h * fun(T[i-1], Y[i-1])
    
    return T, Y

def midpoint_integrate(fun, t0, y0, tStop, h):
    T = np.arange(t0, tStop + h, h)
    Y = np.zeros(T.shape)
    Y[0] = y0

    for i in range(1, len(T)):
        k1 = fun(T[i-1], Y[i-1])
        k2 = fun(T[i-1] + h / 2, Y[i-1] + h / 2 * k1)
        Y[i] = Y[i-1] + h * k2

    return T, Y

def heun_integrate(fun, t0, y0, tStop, h):
    T = np.arange(t0, tStop + h, h)
    Y = np.zeros(T.shape)
    Y[0] = y0

    for i in range(1, len(T)):
        k1 = fun(T[i-1], Y[i-1])
        k2 = fun(T[i-1] + h, Y[i-1] + h * k1)
        Y[i] = Y[i-1] + h / 2 * (k1 + k2)

    return T, Y


def RK4_integrate(fun, t0, y0, tStop, h):
    T = np.arange(t0, tStop + h, h)
    
    # Determine the size of the solution array based on the initial condition
    if np.isscalar(y0):  # For single ODEs
        Y = np.zeros(T.shape)
    else:  # For systems of ODEs
        Y = np.zeros((len(T), len(y0)))
    
    Y[0] = y0

    for i in range(1, len(T)):
        if np.isscalar(y0):  # For single ODEs
            k1 = fun(T[i-1], Y[i-1])
            k2 = fun(T[i-1] + h / 2, Y[i-1] + h / 2 * k1)
            k3 = fun(T[i-1] + h / 2, Y[i-1] + h / 2 * k2)
            k4 = fun(T[i-1] + h, Y[i-1] + h * k3)
            Y[i] = Y[i-1] + h / 6 * (k1 + 2*k2 + 2*k3 + k4)
        else:  # For systems of ODEs
            k1 = fun(T[i-1], Y[i-1])
            k2 = fun(T[i-1] + h / 2, Y[i-1] + h / 2 * k1)
            k3 = fun(T[i-1] + h / 2, Y[i-1] + h / 2 * k2)
            k4 = fun(T[i-1] + h, Y[i-1] + h * k3)
            Y[i] = Y[i-1] + h / 6 * (k1 + 2*k2 + 2*k3 + k4)
    
    return T, Y


