from ServoDriver import ServoDriver
import numpy as np
import time

# Define Specific Laser Pointer (LP) Class
class LP(ServoDriver):
    
    # Constructor
    def __init__(self, AZ=0, EL=1, delay=0.1):
        super().__init__(0x40, False)
        self.AZ = AZ # Azimuth is Channel Zero
        self.EL = EL # Elevation is Channel One
        self.delay = delay # seconds
        self.az_offset = 0
        self.el_offset = 5
        self.az = 0
        self.el = 0
        
    # Set the LP to a new Orientation
    def setLP(self, az, el):
        self.az = az
        self.setAngle(self.AZ, self.az - self.az_offset)
        time.sleep(self.delay)
        self.el = el
        self.setAngle(self.EL, self.el - self.el_offset)
        time.sleep(self.delay)
        
    # Move the LP to a new Orientation
    def moveLP(self, delta_az, delta_el):
        self.az = self.az + delta_az
        self.setAngle(self.AZ, self.az - self.az_offset)
        time.sleep(self.delay)
        self.el = self.el + delta_el
        self.setAngle(self.EL, self.el - self.el_offset)
        time.sleep(self.delay)    
        
    # Center the LP Orientation
    def centerLP(self):
        self.az = 0
        self.el = 0
        self.setLP(self.az, self.el)
        
    # Calibrate LP
    def calLP(self, new_az_offset, new_el_offset):
        print(f'Current Offset for Azimuth and Elevation \n    Az: {self.az_offset} deg \n    El: {self.el_offset} deg \n\n')
        self.az_offset = new_az_offset
        self.el_offset = new_el_offset
        print(f'New Offset \n    Az: {self.az_offset} deg \n    El {self.el_offset} deg \n\n')
        self.centerLP()
        
    # Draw a Circle
    def drawCircle(self, theta, delta):
        start_az = self.az
        start_el = self.el
        self.setLP(start_az, start_el + theta)
        time.sleep(self.delay)
        for k in np.arange(0, 2*np.pi, delta * np.pi/180):
            self.az = start_az + (theta * np.sin(k))
            self.el = start_el + (theta * np.cos(k))
            self.setLP(self.az, self.el)
        time.sleep(1)
        self.centerLP()
        
    # Draw a Square
    def drawSquare(self, theta, delta, corner="NW", dir="CW"):
        pass
        
    
        
    
    
    
        
    