from gpiozero import Buzzer
import time
buzzer = Buzzer(17)

while True:
    time.sleep(0.05)
    buzzer.on()

    time.sleep(0.05)
    buzzer.off()
