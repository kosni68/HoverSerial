from HoverSerial import*
import threading
import time


def thread_send_command():

    #constantes
    SPEED_MAX_TEST = 300  # [-] Maximum speed for testing
    SPEED_STEP = 20  # [-] Speed step
    TIME_SEND = 100  # [ms] Sending time interval

    #local variables
    iStep = SPEED_STEP
    iTest = 0
    steer = 0
    start_time = 0

    while True:

        # Calculate elapsed_time
        elapsed_time = time.time() - start_time
        if elapsed_time < TIME_SEND:
            continue
        start_time = time.time()

        # Calculate test command speed
        speed = SPEED_MAX_TEST-2*abs(iTest)

        # Send commands
        hover_serial.send_command(steer, 100)
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
        else:
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
