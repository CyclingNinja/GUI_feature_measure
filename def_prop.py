# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 15:55:35 2012

@author: sam
"""

import numpy as np
import astropy.units as u

# These will need to change dependant on the instrument you're using
# quantities are fiven in astropy units

# Define the quantities
# how many arcseconds in a pixel
arc_sec_pix = 0.6*u.arcsec
dist_per_arc = 0.725*u.Mm


class properties():
    def __init__(self, BBox, limb):
        self.BBox = BBox    
        self.limb = limb
        self.zone = None
        self.frames = []
        self.times = []
        self.points = []
    
    def __str__(self):
        if not hasattr(self, 'zone'):
            self.zone = None
        astr = """ A Spicule object
                 In frames: %s
                 with times: %s
                 has BBox: %s
                 has limb: %f
                 has location: %s
                 has points: %s """%(str(self.frames), str([i.strftime('%Y_%m_%d_%H_%M_%S') for i in self.times]),
                                     str(self.BBox), self.limb, str(self.zone), str(self.points))
        return astr
    
    def addstep(self, frame, time, A, B, C, D):
        self.frames.append(frame)
        self.times.append(time)
        self.points.append([A, B, C, D])
        
# define the measurements
    def length(self, frame):
      
        A = self.points[frame][0]
        B = self.points[frame][1]
        return (np.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)*dist_per_arc*arc_sec_pix)
        
    def all_length(self):
        return [self.length(i) for i in xrange(len(self.frames))]
        
    def width(self, frame):
        C = self.points[frame][2]
        D = self.points[frame][3]
        return (np.sqrt((C[0] - D[0])**2 + (C[1] - D[1])**2)*dist_per_arc*arc_sec_pix)
 
    def all_width(self):
        return [self.width(i) for i in xrange(len(self.frames))]


    def area(self, frame):
        l = self.length(frame)
        w = self.width(frame)
        return np.pi*(l/2.)*(w/2.)
        
    def all_area(self):
        return [self.area(i) for i in xrange(len(self.frames))]
                        
    def alt(self, frame):
        B = self.points[frame][1]
        A = self.points[frame][0]
        return (B[1] - A[1])
        
    def all_alt(self):
        return [self.alt(i) for i in xrange(len(self.frames))]
        
    def tilt(self, frame):
        A = self.points[frame][0]        
        B = self.points[frame][1]
        bigX = (B[0] - A[0])
        bigY = (B[1] - A[1])
        alpha1 = np.arctan2(bigY, bigX)
        alpha2 = np.rad2deg(alpha1)
        if alpha2 >= 90.0:
            return alpha2 - 90.0
        else:
            return 90.0 - alpha2

        
        
    def all_tilt(self):
        return [self.tilt(i) for i in xrange(len(self.frames))]
        
    def loc(self,frame):
        A = self.points[frame][0]
        meas = A[0] * (360.0/8000.0)
        return meas
        
    def all_loc(self):
        return[self.loc(i) for i in xrange(len(self.frames))]
    
    def lat(self, frame):
        A = self.points[frame][0]
        fi = A[0] * (360.0/8000.0)
        return fi
        

    def all_lat(self):
        return [self.lat(i) for i in xrange(len(self.frames))]
    
    def vel(self, frame):
        if frame == 0:
            dels = (self.length(frame + 1) - self.length(frame))
            delT = (self.times[frame + 1] - self.times[frame]).total_seconds()
            velocity = dels/delT
            return velocity
        elif frame == len(self.frames)-1:
            dels = (self.length(frame - 1) - (self.length(frame)))
            delT = (self.times[frame - 1] - self.times[frame]).total_seconds()
            velocity = dels/delT
            return velocity
        else:
            dels = (self.length(frame - 1) - self.length(frame + 1))
            delT = (self.times[frame - 1] - self.times[frame + 1]).total_seconds()
            velocity = dels/delT
            return velocity


    def all_vel(self):
        return [self.vel(i) for i in xrange(len(self.frames))]
        
    def lifetime(self):
        return self.times[-1] - self.times[0]
        
    def deltatime(self):
        origint = self.times[0]
        return np.array(self.times) - origint
        
        
