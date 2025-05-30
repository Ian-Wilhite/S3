"""
###########################################################################
# This file contains subfunctions for Phase 1 of the TAMU MEEN 357 project
#
# Created by: MEEN 357 Instructional Team
# Last Modified: 4 October 2023
###########################################################################
"""

import math
import numpy as np

def get_mass(rover):
    """
    Inputs: 
        rover: dict 
            Data structure containing rover parameters
    Outputs: 
        m: scalar 
            Rover mass [kg].
    """
    # Check that the input is a dict
    if type(rover) != dict:
        raise Exception('Input must be a dict')

    # Add up mass of chassis, power subsystem, science payload,
    # and components from all six wheel assemblies
    m = rover['chassis']['mass'] + \
        rover['power_subsys']['mass'] + \
        rover['science_payload']['mass'] + \
        6 * rover['wheel_assembly']['motor']['mass'] + \
        6 * rover['wheel_assembly']['speed_reducer']['mass'] + \
        6 * rover['wheel_assembly']['wheel']['mass']
    return m

def get_gear_ratio(speed_reducer):
    """
    Inputs: 
        speed_reducer: dict 
            Data dictionary specifying speed reducer parameters
    Outputs: 
        Ng: scalar 
            Speed ratio from input pinion shaft to output gear shaft. Unitless.
    """
    # Check that the input is a dict
    if type(speed_reducer) != dict:
        raise Exception('Input must be a dict')

    # Check 'type' field (not case sensitive)
    if speed_reducer['type'].lower() != 'reverted':
        raise Exception('The speed reducer type is not recognized.')

    # Main code
    d1 = speed_reducer['diam_pinion']
    d2 = speed_reducer['diam_gear']
    Ng = (d2 / d1) ** 2
    return Ng

def tau_dcmotor(omega, motor):
    """
    Inputs: 
        omega: numpy array 
            Motor shaft speed [rad/s]
        motor: dict 
            Data dictionary specifying motor parameters
    Outputs: 
        tau: numpy array 
            Torque at motor shaft [Nm]. Return argument is same size as first input argument.
    """
    # Check that the first input is a scalar or a vector
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega], dtype=float)  # make the scalar a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    # Check that the second input is a dict
    if type(motor) != dict:
        raise Exception('Second input must be a dict')

    # Main code
    tau_s = motor['torque_stall']
    tau_nl = motor['torque_noload']
    omega_nl = motor['speed_noload']

    # Initialize
    tau = np.zeros(len(omega), dtype=float)
    for ii in range(len(omega)):
        if omega[ii] >= 0 and omega[ii] <= omega_nl:
            tau[ii] = tau_s - (tau_s - tau_nl) / omega_nl * omega[ii]
        elif omega[ii] < 0:
            tau[ii] = tau_s
        elif omega[ii] > omega_nl:
            tau[ii] = 0
    return tau

def F_rolling(omega, terrain_angle, rover, planet, Crr):
    """
    Inputs: 
        omega: numpy array 
            Motor shaft speed [rad/s]
        terrain_angle: numpy array 
            Array of terrain angles [deg]
        rover: dict 
            Data structure specifying rover parameters
        planet: dict 
            Data dictionary specifying planetary parameters
        Crr: scalar 
            Value of rolling resistance coefficient [-]
    Outputs: 
        Frr: numpy array 
            Array of forces [N]
    """
    # Check that the first input is a scalar or a vector
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega], dtype=float)  # make the scalar a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    # Check that the second input is a scalar or a vector
    if (type(terrain_angle) != int) and (type(terrain_angle) != float) and (not isinstance(terrain_angle, np.ndarray)):
        raise Exception('Second input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(terrain_angle, np.ndarray):
        terrain_angle = np.array([terrain_angle], dtype=float)  # make the scalar a numpy array
    elif len(np.shape(terrain_angle)) != 1:
        raise Exception('Second input must be a scalar or a vector. Matrices are not allowed.')

    # Check that the first two inputs are of the same size
    if len(omega) != len(terrain_angle):
        raise Exception('First two inputs must be the same size')

    # Check that values of the second input are within the feasible range
    if max([abs(x) for x in terrain_angle]) > 75:
        raise Exception('All elements of the second input must be between -75 degrees and +75 degrees')

    # Check that the third input is a dict
    if type(rover) != dict:
        raise Exception('Third input must be a dict')

    # Check that the fourth input is a dict
    if type(planet) != dict:
        raise Exception('Fourth input must be a dict')

    # Check that the fifth input is a scalar and positive
    if (type(Crr) != int) and (type(Crr) != float):
        raise Exception('Fifth input must be a scalar')
    if Crr <= 0:
        raise Exception('Fifth input must be a positive number')

    # Main Code
    m = get_mass(rover)
    g = planet['g']
    r = rover['wheel_assembly']['wheel']['radius']
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    v_rover = r * omega / Ng
    Fn = np.array([m * g * math.cos(math.radians(x)) for x in terrain_angle], dtype=float)  # normal force
    Frr_simple = -Crr * Fn  # simple rolling resistance
    Frr = np.array([math.erf(40 * v_rover[ii]) * Frr_simple[ii] for ii in range(len(v_rover))], dtype=float)
    return Frr

def F_gravity(terrain_angle, rover, planet):
    """
    Inputs: 
        terrain_angle: numpy array 
            Array of terrain angles [deg]
        rover: dict 
            Data structure specifying rover parameters
        planet: dict 
            Data dictionary specifying planetary parameters
    Outputs: 
        Fgt: numpy array 
            Array of forces [N]
    """
    # Check that the first input is a scalar or a vector
    if (type(terrain_angle) != int) and (type(terrain_angle) != float) and (not isinstance(terrain_angle, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(terrain_angle, np.ndarray):
        terrain_angle = np.array([terrain_angle], dtype=float)  # make the scalar a numpy array
    elif len(np.shape(terrain_angle)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    # Check that values of the first input are within the feasible range
    if max([abs(x) for x in terrain_angle]) > 75:
        raise Exception('All elements of the first input must be between -75 degrees and +75 degrees')

    # Check that the second input is a dict
    if type(rover) != dict:
        raise Exception('Second input must be a dict')

    # Check that the third input is a dict
    if type(planet) != dict:
        raise Exception('Third input must be a dict')

    # Main Code
    m = get_mass(rover)
    g = planet['g']
    Fgt = np.array([-m * g * math.sin(math.radians(x)) for x in terrain_angle], dtype=float)
    return Fgt

def F_drive(omega, rover):
    """
    Inputs: 
        omega: numpy array 
            Array of motor shaft speeds [rad/s]
        rover: dict 
            Data dictionary specifying rover parameters
    Outputs: 
        Fd: numpy array 
            Array of drive forces [N]
    """
    # Check that the first input is a scalar or a vector
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega], dtype=float)  # Convert scalar to a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    # Check that the second input is a dict
    if type(rover) != dict:
        raise Exception('Second input must be a dict')

    # Main code
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])  # Torque at the motor shaft
    tau_out = tau * Ng  # Torque at the wheel after gear reduction
    r = rover['wheel_assembly']['wheel']['radius']  # Wheel radius

    # Drive force for one wheel
    Fd_wheel = tau_out / r

    # Drive force for all six wheels
    Fd = 6 * Fd_wheel

    return Fd

