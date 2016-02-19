# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:10:30 2016

@author: Pedro Leal
"""
import math

class actuator():
    """
    Actuator object where inputs:
    - F: is a dictionary with keys 'x' and 'y', the coordinates of 
      the forwards end in the global coordinate system (origin at the
      leading edge)
    - A: is a dictionary with keys 'x' and 'y', the coordinates of 
      the afterwards end in the global coordinate system (origin at the
      leading edge)
    - J: is a dictionary with keys 'x' and 'y', the coordinates of 
      the joint in the global coordinate system (origin at the
      leading edge)        
    - material: linear or SMA
    """
    #
    def __init__(self, F, A, J, material = 'linear'):
        """
        Initiate class and it's basic atributes:
        - f_1 and f_2: are the x & y coordinates of the forwards end in the
          local coordinate system (origin at the joint)
        - a_1 and a_2: are the x & y coordinates of the afterwards end in the
          local coordinate system (origin at the joint)
        """
        #Storing inputs in local coordinate system
        self.f_1 = F['x'] - J['x']
        self.f_2 = F['y'] - J['y']
        self.a_1 = A['x'] - J['x']
        self.a_2 = A['y'] - J['y']
        self.material = material
        
        # Projections of original wire length r
        self.r_1_0 = self.a_1 - self.f_1
        self.r_2_0 = self.a_2 - self.f_2
        self.length_r_0 = math.sqrt(self.r_1_0**2 + self.r_2_0**2)    
        
        #define initial values for r, theta and force
        self.theta = 0
        self.update()
        self.F = 0.


    def calculate_theta(self):
        """
        Calculate angle for given deformation epsilon.
        """
        #deformation = strain + 1
        eta = self.eps + 1.
        
        A1 = eta*self.r_1_0 + self.f_1
        A2 = eta*self.r_2_0 + self.f_2
        cos = (A2 + A1*(self.a_1/self.a_2))/(self.a_2 +(self.a_1/self.a_2)*self.a_1)
        sin = (self.a_1*cos - A1) / self.a_2
#        print sin, cos
        self.theta = math.degrees(math.atan2(sin,cos))
        self.update()
        return self.theta
        
    def update(self):
        """If vector length r or theta is changed, new coordinates are 
        calculated"""
        self.r_1 = self.a_1*math.cos(self.theta) - \
                   self.a_2*math.sin(self.theta) - self.f_1
        self.r_2 = self.a_2*math.cos(self.theta) + \
                   self.a_1*math.sin(self.theta) - self.f_2
        self.length_r = math.sqrt(self.r_1**2 + self.r_2**2)
        self.eps = self.length_r/self.length_r_0 - 1.
                  
    def calculate_torque(self):
        """Calculate torque given the actuator force: a \times F (where a is 
        global coordinates)"""

        #calculate componets of force vector        
        F_1 = self.F*self.r_1/self.length_r
        F_2 = self.F*self.r_2/self.length_r
#        print F_1, F_2
        #calculate torque
        self.torque = (self.a_1*math.cos(self.theta) - \
                       self.a_2*math.sin(self.theta))*F_2 - \
                      (self.a_2*math.cos(self.theta) + \
                       self.a_1*math.sin(self.theta))*F_1    
        return self.torque
     
    def calculate_force(self):
        if self.material == 'linear':
            k= 1.
            self.F = k*self.eps
        elif self.material == 'SMA':
            print "Put Edwin code here"

if __name__ == '__main__':
    chord = 1.
    #Hole positioning
    F_l = {'x': -1*chord, 'y': 1*chord}
    A_l = {'x': 1*chord, 'y': 1*chord}
    F_s = {'x': -1*chord, 'y': -1*chord}
    A_s = {'x': 1*chord, 'y': -1*chord}
    J = {'x': 0.*chord, 'y': 0.*chord}

    #Spring coefficient
    k = 1.

    #arm length to center of gravity
    a_w = 1.
    
    #Aicraft weight
    W = 1.
    
    #Linear actuator (s)
    l = actuator(F_l, A_l, J)
    #Sma actuator (l)
    s = actuator(F_s, A_s, J)
    
    l.calculate_theta()
    l.calculate_torque()
    s.calculate_theta()
    s.calculate_torque()
    
    counter = 0
    damping_counter = 0
    dampner = 0.95
    theta = 0
    
    tolerance = 1e-5
    #random high value to enter loop
    error_eps = 100000.
    previous_l_eps = 0.
    print 'iteration: ', counter
    print 'strain: ', s.eps
    print 'angle: ', s.theta
    print 'torque: ', s.torque
    while error_eps > tolerance:      
        #strain (epsilon) of linear actuator
        l.eps = dampner*previous_l_eps + (1.-dampner)*(1./k)/(l.a_1*math.sin(theta) + l.a_2*math.cos(theta)*l.r_1 - \
              (l.a_1*math.cos(theta) - l.a_2*math.sin(theta))*l.r_2)*(s.torque + \
              a_w*W*math.cos(theta))
        #update angle, r and strain at SMA actuator
        theta = l.calculate_theta()
        s.theta = theta
        s.update()
        l.update()
        #strain of SMA actuator
        s.calculate_force()
        s.calculate_torque()
        counter += 1
        
        #calculating error with final value 
        error_eps = abs(previous_l_eps - l.eps)
        #updating previous strain
        previous_l_eps = l.eps
#        damping_counter +=1
        print 'iteration: ', counter
        print 'strain: ', s.eps, l.eps
        print 'angle: ', s.theta, l.theta
        print 'torque: ', s.torque
        print "error: ", error_eps