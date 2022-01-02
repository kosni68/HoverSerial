import serial # to communicate with the hoverboard

class Hoverboard_serial:
    
    def __init__(self,adresse,baud):
        self.uart = serial.Serial(adresse, baud, timeout=1)
        self.startBytes = bytes.fromhex('ABCD')[::-1] # lower byte first
        self.incomingBytesPrev = bytes()
        
    
    def send_command(self,steer, speed):
        '''
        Send a bytearray for controlling the hoverboard

        :param steer: -1000...1000
        :param speed: -1000...1000

        bytearray :
        Start frame(unsigned int16) : 0xABCD
        Steer(signed int16) : Steer with range -1000 to 1000
        Speed(signed int16) : Speed with range -1000 to 1000
        Checksum(unsigned int16) : XOR checksum
        '''
        steerBytes = steer.to_bytes(2, byteorder="little")
        speedBytes = speed.to_bytes(2, byteorder="little")
        checksumBytes = bytes(a^b^c for (a, b, c) in zip(self.startBytes, steerBytes, speedBytes))

        command = self.startBytes+steerBytes+speedBytes+checksumBytes
        
        self.uart.write(command)
        
    def receive_feedback(self):
        '''
        receive a bytearray to the hoverboard 
        return: bytearray convert to dictionnary

        bytearray :
        Start frame(unsigned int16) : 0xABCD
        Cmd1(signed int16) : Steer or Brake(hovercar) after normalizing and mixing
        Cmd2(signed int16) : Speed or Throttle(hovercar) after normalizing and mixing
        SpeedR(signed int16) : Measured right wheel speed in RPM
        SpeedL(signed int16) : Measured left wheel speed in RPM
        Battery Voltage(signed int16) : Calibrated Battery Voltage *100
        Temperature(signed int16) : Temperature in °C *10
        Led(unsigned int16) : Used to control the leds on the sideboard
        Checksum(unsigned int16) : XOR checksum

        '''

        incomingByte = self.uart.read()
        bufStartFrame = self.incomingBytesPrev+incomingByte
        
        if bufStartFrame != self.startBytes:
            self.incomingBytesPrev=incomingByte
            return
        else:
            feedback = {"cmd1":0, "cmd2":0, "speedR_meas":0, "speedL_meas":0, "batVoltage":0, "boardTemp":0, "cmdLed":0}
            checksumBytes=bufStartFrame
    
            for element in feedback.items():
                elementBytes=self.uart.read(2)
                feedback[element]=int.from_bytes(elementBytes, byteorder='big')
                checksumBytes = bytes(a^b for (a, b) in zip(checksumBytes, elementBytes))

            #print(feedback,feedback)
            lastBytes=self.uart.read(2)
            if checksumBytes == lastBytes:
                print("checksumBytes True")
                return feedback
            
            return
            
    def close(self):
        self.uart.close()
