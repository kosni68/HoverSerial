from HoverSerial import*
import threading
import time


def thread_send_command():

    #Constantes
    SPEED_MAX_TEST = 300  # [-] Maximum speed for testing
    SPEED_STEP = 2  # [-] Speed step
    TIME_SEND = 0.1  # [s] Sending time interval

    #Local variables
    iStep = SPEED_STEP
    iTest = 0
    steer = 0
    startTime = 0

    while True:

        # Calculate elapsed time
        elapsedTime = time.time() - startTime
        if elapsedTime < TIME_SEND:
            continue
        startTime = time.time()

        # Calculate test command speed
        speed = SPEED_MAX_TEST-2*abs(iTest)

        # Send commands
        hover_serial.send_command(steer, speed)
        print('Sending:\t steer: '+str(steer)+'speed: '+str(speed))

        # invert step if reaching limit
        iTest += iStep
        if (iTest >= SPEED_MAX_TEST or iTest <= -SPEED_MAX_TEST):
            iStep = -iStep


def thread_receive_feedback():

    while True:

        feedback = hover_serial.receive_feedback()

        if feedback == None:
            continue
        
        print('Receiving:\t', feedback)


if __name__ == "__main__":

    SERIAL_PORT = '/dev/serial0'
    SERIAL_BAUD = 38400
    hover_serial = Hoverboard_serial(SERIAL_PORT, SERIAL_BAUD)

    try:

        thread1 = threading.Thread(target=thread_send_command)
        thread1.start()

        thread2 = threading.Thread(target=thread_receive_feedback)
        thread2.start()

        thread1.join()
        thread2.join()

    except KeyboardInterrupt:
        print("Keyboard interrupt...")

    except Exception as e:
        print("Error: " + str(e))

    finally:
        hover_serial.close()
