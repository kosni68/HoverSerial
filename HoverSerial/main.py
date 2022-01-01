from HoverSerial import*
import time

def main():
    
    SERIAL_PORT = '/dev/serial0'
    SERIAL_BAUD = 38400

    hover_serial=Hoverboard_serial(SERIAL_PORT,SERIAL_BAUD)

    SPEED_MAX_TEST = 300
    iTestMax = SPEED_MAX_TEST
    iTest = 0
    steer = 0
    
    while True:
        
        speed = SPEED_MAX_TEST-2*abs(iTest)
        command = hover_serial.send_command(steer, 100)
        #print(f'\nSending:\nspeed: {speed}, command: {command}')
        
        #print('Receiving:')
        feedback = hover_serial.receive_feedback()
        #feedback = hover_serial.read_all()
        print(feedback)
                
        # calculate next test speed
        iTest += 10
        if (iTest > iTestMax):
            iTest = -iTestMax
        
        time.sleep(0.001)
        

if __name__ == "__main__":
    
    try:
        main()
    except KeyboardInterrupt:
        hover_serial.close()
            
