## Author
## Date: 

# this script is for LED control classes, including RGB and 4 digit signal


import RPi.GPIO as GPIO
import time
import tm1637


# Define a MAP function for mapping values.  Like from 0~255 to 0~100
def MAP(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class RGBLEDcontroller:
    """
    control RGB signal
    input:
    - pins: pins number of Red, Green and Blue (default : R = 16, Green = 20, Blue = 21)
    """
    def __init__(self, pins = {'Red':16, 'Green':20, 'Blue':21}):
        self.pins = pins

        # Set up a color table in Hexadecimal
        
    
    def setup(self):
        # Set the GPIO modes to BCM Numbering
        GPIO.setmode(GPIO.BCM)
        
        # Set all LedPin's mode to output and initial level to High(3.3v)
        for i in self.pins:
            GPIO.setup(self.pins[i], GPIO.OUT, initial=GPIO.HIGH)
            
        self.p_R = GPIO.PWM(self.pins['Red'], 2000)
        self.p_G = GPIO.PWM(self.pins['Green'], 2000)
        self.p_B = GPIO.PWM(self.pins['Blue'], 2000)

        # Set all begin with value 0
        self.p_R.start(0)
        self.p_G.start(0)
        self.p_B.start(0)

    def setColor(self, color):
        # configures the three LEDs' luminance with the inputted color value . 
	    # Devide colors from 'color' veriable
        R_val = (color & 0xFF0000) >> 16
        G_val = (color & 0x00FF00) >> 8
        B_val = (color & 0x0000FF) >> 0
        # these three lines are used for analyzing the col variables 
        # assign the first two values of the hexadecimal to R, the middle two assigned to G
        # assign the last two values to B, please refer to the shift operation of the hexadecimal for details.

        R_val = MAP(R_val, 0, 255, 0, 100)
        G_val = MAP(G_val, 0, 255, 0, 100)
        B_val = MAP(B_val, 0, 255, 0, 100)

        # Change the colors
        self.p_R.ChangeDutyCycle(R_val)
	    # Assign the mapped duty cycle value to the corresponding PWM channel to change the luminance. 
        self.p_G.ChangeDutyCycle(G_val)
        self.p_B.ChangeDutyCycle(B_val)

    def stop(self):
        # Stop all pwm channel
        self.p_R.stop()
        self.p_G.stop()
        self.p_B.stop()
	    # Release resource
        GPIO.cleanup()


class DigitLEDcontrolller:
    """
    Control
    """
    def __init__(self, clk = 5, dio = 4):
        self.tm = tm1637.TM1637(clk=clk, dio=dio)
        # self.tm.write([127, 255, 127, 127])

        # all LEDS off
        self.tm.write([0, 0, 0, 0])

        # show "12:59"
        # self.tm.numbers(12, 59)

    def setNumber(self, num1, num2):
        self.tm.numbers(num1, num2)

    def reset(self):
        self.tm.write([0, 0, 0, 0])