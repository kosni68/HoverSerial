import struct # for values to bytes
import serial # to communicate with the hoverboard

class Hoverboard_serial:
    
    def __init__(self,adresse,baud):
        self.uart = serial.Serial(adresse, baud, timeout=1)
        self.startBytes = bytes.fromhex('ABCD')[::-1] # lower byte first
        self.incomingBytesPrev = bytes.fromhex('00')
        
    
    def send_command(self,steer, speed):
        '''
        Creates a bytearray for controlling the hoverboard

        :param steer: -1000...1000
        :param speed: -1000...1000
        :returns: command bytes
        '''
        steerBytes = struct.pack('h', steer)
        speedBytes = struct.pack('h', speed)
        checksumBytes = bytes(a^b^c for (a, b, c) in zip(self.startBytes, steerBytes, speedBytes))

        command = self.startBytes+steerBytes+speedBytes+checksumBytes
        
        self.uart.write(command)
        
    def receive_feedback(self):
        
        incomingByte = self.uart.read()
        #bufStartFrame = struct.pack('cc',self.incomingBytesPrev,incomingByte)
        bufStartFrame = self.incomingBytesPrev+incomingByte
        #print("bufStartFrame: ",bufStartFrame)
        
        if bufStartFrame != self.startBytes:
            self.incomingBytesPrev=incomingByte
            return
        else:
            feedback_dict = {"cmd1":0, "cmd2":0, "speedR_meas":0, "speedL_meas":0, "batVoltage":0, "boardTemp":0, "cmdLed":0}
            checksumBytes=bufStartFrame
            for key,value in feedback_dict.items():
                bytes_element=self.uart.read(2)
                feedback_dict[key] = struct.unpack('h', bytes_element)
                #print(key,bytes_element)
                #print(struct.unpack('h', bytes_element))
                checksumBytes = bytes(a^b for (a, b) in zip(checksumBytes, bytes_element))
                
            lastBytes=self.uart.read(2)
            if checksumBytes == lastBytes:
                print("checksumBytes True")
                return feedback_dict
            
            return
            
    def close(self):
        self.uart.close()
