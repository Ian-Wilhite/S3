import numpy as np
import math
import scipy.integrate as sc
#import math
from scipy.interpolate import interp1d, interpolate
from scipy.integrate import solve_ivp
#from end_of_mission_event import end_of_mission_event

def define_rover_1():   # or define_rover()
    # Initialize Rover dict for testing
    wheel = {'radius':0.30,
             'mass':1}
    speed_reducer = {'type':'reverted',
                     'diam_pinion':0.04,
                     'diam_gear':0.07,
                     'mass':1.5}
    motor = {'torque_stall':170,
             'torque_noload':0,
             'speed_noload':3.80,
             'mass':5.0,
             'effcy_tau':np.array([0,10,20,40,75,165]),
             'effcy':np.array([0,0.60,0.75,0.73,0.55,0.05])}
    
        
    chassis = {'mass':659}
    science_payload = {'mass':75}
    power_subsys = {'mass':90}
    
    wheel_assembly = {'wheel':wheel,
                      'speed_reducer':speed_reducer,
                      'motor':motor}
    

    rover = {'wheel_assembly':wheel_assembly,
             'chassis':chassis,
             'science_payload':science_payload,
             'power_subsys':power_subsys}
    
    planet = {'g':3.72}
    
    # return everything we need
    return rover, planet

def get_mass(rover):
    """
    Inputs:  rover:  dict      Data structure containing rover parameters
    
    Outputs:     m:  scalar    Rover mass [kg].
    """
    
    # Check that the input is a dict
    if type(rover) != dict:
        raise Exception('Input must be a dict')
    
    # add up mass of chassis, power subsystem, science payload, 
    # and components from all six wheel assemblies
    m = rover['chassis']['mass'] \
        + rover['power_subsys']['mass'] \
        + rover['science_payload']['mass'] \
        + 6*rover['wheel_assembly']['motor']['mass'] \
        + 6*rover['wheel_assembly']['speed_reducer']['mass'] \
        + 6*rover['wheel_assembly']['wheel']['mass'] \
    
    return m

def get_gear_ratio(speed_reducer):
    """
    Inputs:  speed_reducer:  dict      Data dictionary specifying speed
                                        reducer parameters
    Outputs:            Ng:  scalar    Speed ratio from input pinion shaft
                                        to output gear shaft. Unitless.
    """
    
    # Check that 1 input has been given.
    #   IS THIS NECESSARY ANYMORE????
    
    # Check that the input is a dict
    if type(speed_reducer) != dict:
        raise Exception('Input must be a dict')
    
    # Check 'type' field (not case sensitive)
    if speed_reducer['type'].lower() != 'reverted':
        raise Exception('The speed reducer type is not recognized.')
    
    # Main code
    d1 = speed_reducer['diam_pinion']
    d2 = speed_reducer['diam_gear']
    
    Ng = (d2/d1)**2
    
    return Ng

def tau_dcmotor(omega, motor):
    """
    Inputs:  omega:  numpy array      Motor shaft speed [rad/s]
             motor:  dict             Data dictionary specifying motor parameters
    Outputs:   tau:  numpy array      Torque at motor shaft [Nm].  Return argument
                                      is same size as first input argument.
    """
    
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception ('First input should be scalar or vector.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega],dtype=float) # make the scalar a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input should be scalar or vector.')

    # Check that the second input is a dict
    if type(motor) != dict:
        raise Exception('Second input must be a dict')
        
    # Main code
    tau_s    = motor['torque_stall']
    tau_nl   = motor['torque_noload']
    omega_nl = motor['speed_noload']
    
    # initialize
    tau = np.zeros(len(omega),dtype = float)
    for i in range(len(omega)):
        if omega[i] >= 0 and omega[i] <= omega_nl:
            tau[i] = tau_s - (tau_s-tau_nl)/omega_nl *omega[i]
        elif omega[i] < 0:
            tau[i] = tau_s
        elif omega[i] > omega_nl:
            tau[i] = 0
        
    return tau

def F_rolling(omega, terrain_angle, rover, planet, Crr):
    """
    Inputs:           omega:  numpy array     Motor shaft speed [rad/s]
              terrain_angle:  numpy array     Array of terrain angles [deg]
                      rover:  dict            Data structure specifying rover 
                                              parameters
                    planet:  dict            Data dictionary specifying planetary 
                                              parameters
                        Crr:  scalar          Value of rolling resistance coefficient
                                              [-]
    
    Outputs:           Frr:  numpy array     Array of forces [N]
    """
    
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega],dtype=float) # make the scalar a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')
        
    # Check that the second input is a scalar or a vector
    if (type(terrain_angle) != int) and (type(terrain_angle) != float) and (not isinstance(terrain_angle, np.ndarray)):
        raise Exception('Second input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(terrain_angle, np.ndarray):
        terrain_angle = np.array([terrain_angle],dtype=float) # make the scalar a numpy array
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
    
    v_rover = r*omega/Ng
    
    Fn = np.array([m*g*math.cos(math.radians(x)) for x in terrain_angle],dtype=float) # normal force
    Frr_simple = -Crr*Fn # simple rolling resistance
    
    Frr = np.array([math.erf(40*v_rover[ii]) * Frr_simple[ii] for ii in range(len(v_rover))], dtype = float)
    
    return Frr

def F_gravity(terrain_angle, rover, planet):
    """
    Inputs:  terrain_angle:  numpy array   Array of terrain angles [deg]
                     rover:  dict          Data structure specifying rover 
                                            parameters
                    planet:  dict          Data dictionary specifying planetary 
                                            parameters
    
    Outputs:           Fgt:  numpy array   Array of forces [N]
    """
    
    # Check that the first input is a scalar or a vector
    if (type(terrain_angle) != int) and (type(terrain_angle) != float) and (not isinstance(terrain_angle, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(terrain_angle, np.ndarray):
        terrain_angle = np.array([terrain_angle],dtype=float) # make the scalar a numpy array
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
    
    Fgt = np.array([-m*g*math.sin(math.radians(x)) for x in terrain_angle], dtype = float)
        
    return Fgt

def F_drive(omega, rover):
    """
    Inputs:  omega:  numpy array   Array of motor shaft speeds [rad/s]
             rover:  dict          Data dictionary specifying rover parameters
    
    Outputs:    Fd:  numpy array   Array of drive forces [N]
    """
    
    # Check that 2 inputs have been given.
    #   IS THIS NECESSARY ANYMORE????
    
    # Check that the first input is a scalar or a vector
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega],dtype=float) # make the scalar a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')

    # Check that the second input is a dict
    if type(rover) != dict:
        raise Exception('Second input must be a dict')
    
    # Main code
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    tau_out = tau*Ng
    
    r = rover['wheel_assembly']['wheel']['radius']
    
    # Drive force for one wheel
    Fd_wheel = tau_out/r 
    
    # Drive force for all six wheels
    Fd = 6*Fd_wheel
    
    return Fd

def F_net(omega, terrain_angle, rover, planet, Crr):
    """
    Inputs:           omega:  list     Motor shaft speed [rad/s]
              terrain_angle:  list     Array of terrain angles [deg]
                      rover:  dict     Data structure specifying rover 
                                      parameters
                     planet:  dict     Data dictionary specifying planetary 
                                      parameters
                        Crr:  scalar   Value of rolling resistance coefficient
                                      [-]
    
    Outputs:           Fnet:  list     Array of forces [N]
    """
    
    # Check that the first input is a scalar or a vector
    if (type(omega) != int) and (type(omega) != float) and (not isinstance(omega, np.ndarray)):
        raise Exception('First input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(omega, np.ndarray):
        omega = np.array([omega],dtype=float) # make the scalar a numpy array
    elif len(np.shape(omega)) != 1:
        raise Exception('First input must be a scalar or a vector. Matrices are not allowed.')
        
    # Check that the second input is a scalar or a vector
    if (type(terrain_angle) != int) and (type(terrain_angle) != float) and (not isinstance(terrain_angle, np.ndarray)):
        raise Exception('Second input must be a scalar or a vector. If input is a vector, it should be defined as a numpy array.')
    elif not isinstance(terrain_angle, np.ndarray):
        terrain_angle = np.array([terrain_angle],dtype=float) # make the scalar a numpy array
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
    Fd = F_drive(omega, rover)
    Frr = F_rolling(omega, terrain_angle, rover, planet, Crr)
    Fg = F_gravity(terrain_angle, rover, planet)
    
    Fnet = Fd + Frr + Fg # signs are handled in individual functions
    
    return Fnet

def motorW(v, rover):
    """
    Inputs:         v:  1D numpy array     rover translational velocity [m/s]
                rover:  dict               data structure containing rover parameters
                
    Outputs:        w:  1D numpy array     motor speed [rad/s]
    """
    if type(v) != int and type(v) != float and not isinstance(v, np.ndarray): #checks v is a scalar or vector
        raise Exception('v must be a scalar or vector')
    elif not isinstance(v, np.ndarray): #a scalar input is converted into a numpy array
        v = np.array([v],dtype=float)
    elif len(np.shape(v)) != 1: #checks that array is 1 dimension
        raise Exception('v must be scalar or 1d vector')
    if type(rover) != dict: #checks rover is dictionary
        raise Exception('rover must be a dict') 
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer']) #access the gear ratio by calling get_gear_ratio function
    w = np.array([(i/rover['wheel_assembly']['wheel']['radius'])*Ng for i in v],dtype=float) # w(omega) = v/r * gear ratio
    return w

def rover_dynamics(t, y, rover, planet, experiment): 
    """
    Inputs:     t          scalar             time sample [s]
                y          1D numpy array     two-element array of dependent variables: 
                                              rover velocity[m/s] and rover position [m]
                rover      dict               data structure containing rover definition
                planet     dict               data structure containing planet definition
                experiment dict               data structure containing experiment definition

    Outputs:    dydt       1D numpy array     two-element array of first derivatives of state vector: 
                                              rover acceleration [m/s^2] and rover velocity [m/s]
    """
    if type(t) != float and type(t) != int: #checks that t is a scalar
        raise Exception('t should be scalar')
        
    if not isinstance(y, np.ndarray) and len(y) != 2: #checks that y is an array with 2 elements
        raise Exception('y must be two element numpy array')
    elif len(np.shape(y)) != 1: #cheks that y is 1 dimension array
        raise Exception('y must be 1d')
    
    if type(rover) != dict or type(planet) != dict or type(experiment) != dict: #checks that all 3 last inputs are dictionaries
        raise Exception('last 3 inputs should all be dictionaries')
    
    alpha_fun = interpolate.interp1d(experiment['alpha_dist'], experiment['alpha_deg'], kind = 'cubic', fill_value='extrapolate') #creates an interpolation function
    terrain_angle = float(alpha_fun(y[1])) #evaluates the terrain angle with known position using interpolation
        
    w = motorW(float(y[0]),rover) #evaluates the motor speed with known velocity using interpolation

    f = F_net(w, terrain_angle, rover, planet, experiment['Crr']) #evaluates the net force acting on the rover
    m = get_mass(rover) #gets mass of the rover
    
    dydt = [] 
    dydt.append(float(f/m)) #from Newton's 2nd Law a=f/m
    dydt.append(y[0]) #velocity is given as the first element in y
    
    return dydt

def mechpower(v, rover): 
    """
    Inputs:     v:      1D numpy array     rover velocity obtained from a simulation [m/s]
                rover:  dict               data structure containing rover definition
            
    Outputs:    P       1D numpy array     instantaneous power output of a single motor [W]    
    """
    if type(v) != int and type(v) != float and not isinstance(v, np.ndarray): #checks that v is a scalar or vector
        raise Exception('v must be a scalar or vector')
    elif not isinstance(v, np.ndarray): #changes scalar into a numpy array
        v = np.array([v],dtype=float)
    elif len(np.shape(v)) != 1: #checks that array is 1 dimension
        raise Exception('v must be scalar or 1d vector')
    if type(rover) != dict: #checks that rover is a dictionary
        raise Exception('rover must be dict')
    p = []    
    for i in range (len(v)):
        w = motorW(float(v[i]), rover) #evaluates motor speed
        tau = tau_dcmotor(w, rover['wheel_assembly']['motor']) #evaluates the motor shaft torque
        p.append(float(w*tau)) #power = angular velocity * torque
    return p 

def battenergy(t, v, rover): 
    """
    Inputs:     t      1D numpy array     array of time samples from a rover simulation [s]
                v      1D numpy array     array of rover velocity data from a simulation [m/s]
                rover  dict               data structure containing rover definition
    Outputs:    E      scalar             total electrical energy consumed from the rover battery over the input simulation profile [J]
    """
    if type(t) == list:
        t = np.array(t)
    if type(t) != int and type(t) != float and not isinstance(t, np.ndarray): #checks that t is a scalar or vector
        raise Exception('t must be a scalar or vector')
    elif not isinstance(t, np.ndarray): #changes scalar t into a numpy array
        t = np.array([t],dtype=float)
    elif len(np.shape(t)) != 1: #checks t is 1 dimension array
        raise Exception('t must be scalar or 1d vector')
    
    if type(v) == list: #checks if v is list and assigns it as an array
        v = np.array(v)
    if type(v) != int and type(v) != float and not isinstance(v, np.ndarray): #checks that v is a scalar or vector
        raise Exception('v must be a scalar or vector')
    elif not isinstance(v, np.ndarray): #changes scalar v into a numpy array
        v = np.array([v],dtype=float)
    elif len(np.shape(v)) != 1: #checks v is 1 dimension array
        raise Exception('v must be scalar or 1d vector')
    
    if len(t) != len(v): #checks that t and v are the same length numpy array
        raise Exception('t and v must be the same size') 
    if type(rover) != dict: #checks that rover is a dictionary
        raise Exception('rover must be dict')    
        
    p_batt = []
    for i in range (len(t)):
        p_motor = mechpower(float(v[i]),rover) #evaluates the instantaneous power of a single motor
        w = motorW(float(v[i]),rover) #evaluates motor speed
        tau = tau_dcmotor(w, rover['wheel_assembly']['motor']) #evaluates motor torque
        n = interpolate.interp1d(rover['wheel_assembly']['motor']['effcy_tau'], rover['wheel_assembly']['motor']['effcy'], kind = 'cubic', fill_value='extrapolate') #creates interpolation function to evaluate efficiency coefficient
        effy = n(tau) #evaluates the efficiency of the motor at a certain torque
        p_batt.append(6*float(p_motor/effy)) #p_batt(t) = p_motor(t)/n(torque(t)), effy=n(torque(t)), and rover has 6 motors     

    #change if we can’t use built-in functions for this part#
    E = sc.trapezoid(p_batt, t) #energy is integral of power
    return E

def simulate_rover(rover, planet, experiment, end_event):
    """
    Inputs:
             rover:  dict                dict containing rover definition       
            planet:  dict                dict containing the planet definition
        experiment:  dict                dict containing the parameters of the trajectory to be followed by the rover
         end_event:  dict                dict containing the conditions to terminate simulation of rover dynamics
         
    Outputs: 
            rover:  dict                 dict containing the parameters of the rover, including updated telemetry information
    """
    
    if type(rover) != dict:  #checks that rover is a dictionary
        raise Exception('First input must be a dict')
    
    if type(planet) != dict:    #checks if planet is dictionary
        raise Exception('Second input must be a dict')
    
    if type(experiment) != dict: #checks if experiment is  dictionary
        raise Exception('Third input must be a dict')
    
    if type(end_event) != dict: # checks if end event is dictionary
        raise Exception('Fourth input must be a dict')
    
    def trajectory(t,y): #function using rover_dynamics but with just two inputs
        t = float(t)     #makes t a float value to function properly works
        f1 = rover_dynamics(t, y, rover, planet, experiment) #sets f1 to  rover_dyanamics with only t and y as inputs
        return f1
    time_range = experiment['time_range'] #sets variable to time range array
    y_i = experiment['initial_conditions'] #sets intial conditions for input to ivp
    end_event = end_of_mission_event(end_event) #defines end event conditions
    
    solution = sc.solve_ivp(trajectory, time_range, y_i, method='RK45', events=end_event) #using ivp solver  with defined inputs
    
    rover['telemetry'] = {"Time": solution.t, "completion_time": solution.t[-1], "velocity": solution.y[0,:], #defines time as t sol which is an array, makes completition time the final time value, velocity is the array from y sol
                          "position": solution.y[1,:], "distance_traveled": solution.y[1,-1], "max_velocity": max(solution.y[0,:]), #position is the y1 solution, the distance traveled is the final position array value, max velocity is the max velocity array value,
                          "average_velocity": np.mean(solution.y[0, :]), "power": mechpower(solution.y[0,:], rover), #average velocity is just mean of the y0 solution, power utilizes the mechpower function with v input.
                          "battery_energy": battenergy(solution.t, solution.y[0,:], rover), #this uses the battery energy input to determine the energy required given a time array and velocity array
                          "energy_per_distance": battenergy(solution.t, solution.y[0,:],rover)/solution.y[1,-1]} #this takes the energy required and divides it by the distance travelled to determine J/m
    return rover

def end_of_mission_event(end_event):
    """
    Defines mission termination conditions based on 
    rover distance, simulation time, and minimum velocity.           
    """
    
    mission_distance = end_event['max_distance']
    mission_max_time = end_event['max_time']
    mission_min_velocity = end_event['min_velocity']
    
    distance_left = lambda t,y: mission_distance - y[1]
    distance_left.terminal = True
    
    time_left = lambda t,y: mission_max_time - t
    time_left.terminal = True
    
    velocity_threshold = lambda t,y: y[0] - mission_min_velocity;
    velocity_threshold.terminal = True
    velocity_threshold.direction = -1
    
    events = [distance_left, time_left, velocity_threshold]
    
    return events

