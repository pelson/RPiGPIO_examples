import RPi.GPIO as GPIO
import utils


if __name__ == '__main__':
    # Allow command line control of the buzzer port.
    args = utils.SensorArgs(['buzzer'])
 
    BUZZER_PORT = args['buzzer']
    GPIO.setmode(GPIO.BOARD if args.board_mode else GPIO.BCM)

    with utils.autocleanup():
        with utils.pwm(BUZZER_PORT, frequency=2) as buzzer_pwm:
            freq = 2
            while freq != 0:
                buzzer_pwm.ChangeFrequency(freq)
                freq = float(raw_input('How frequent? (0 == exit) [2]: '))

