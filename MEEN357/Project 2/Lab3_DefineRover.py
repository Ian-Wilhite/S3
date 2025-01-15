def define_rover_1():
    # Initialize Rover dict with updated fields
    wheel = {'radius': 0.30,  # m
             'mass': 1}  # kg
             
    speed_reducer = {'type': 'reverted',
                     'diam_pinion': 0.04,  # m
                     'diam_gear': 0.07,  # m
                     'mass': 1.5}  # kg
                     
    motor = {'torque_stall': 170,  # N-m
             'torque_noload': 0,   # N-m
             'speed_noload': 3.80,  # rad/s
             'mass': 5.0,  # kg
             'effcy_tau': [0, 10, 20, 40, 70, 165],  # N-m
             'effcy': [0, 0.55, 0.75, 0.71, 0.50, 0.05]}  # [-]
             
    chassis = {'mass': 659}  # kg
    science_payload = {'mass': 75}  # kg
    power_subsys = {'mass': 90}  # kg
    
    wheel_assembly = {'wheel': wheel,
                      'speed_reducer': speed_reducer,
                      'motor': motor}
    
    rover = {'wheel_assembly': wheel_assembly,
             'chassis': chassis,
             'science_payload': science_payload,
             'power_subsys': power_subsys}
    
    planet = {'g': 3.72}  # m/s^2
    
    return rover, planet

def define_experiment():
    # Example experiment dictionary for testing
    experiment = {'time_range': [0, 1000],  # s
                  'initial_conditions': [0, 0],  # [velocity (m/s), position (m)]
                  'alpha_dist': [0, 10, 20, 30, 50],  # m
                  'alpha_deg': [0, 5, 10, 5, 0],  # degrees
                  'Crr': 0.1}  # Coefficient of rolling resistance
    
    return experiment

def define_end_event():
    # Example end_event dictionary for testing
    end_event = {'max_distance': 50,  # m
                 'max_time': 5000,  # s
                 'min_velocity': 0.01}  # m/s
    
    return end_event

def define_telemetry():
    # Example telemetry dictionary for storing results
    telemetry = {'Time': [],  # Time history [s]
                 'completion_time': 0,  # Time to complete mission [s]
                 'velocity': [],  # Rover velocity over time [m/s]
                 'position': [],  # Rover position over time [m]
                 'distance_traveled': 0,  # Total distance traveled [m]
                 'max_velocity': 0,  # Maximum velocity [m/s]
                 'average_velocity': 0,  # Average velocity [m/s]
                 'power': [],  # Power output of motor over time [W]
                 'battery_energy': 0,  # Total battery energy consumed [J]
                 'energy_per_distance': 0}  # Energy spent per meter traveled [J/m]
    
    return telemetry
