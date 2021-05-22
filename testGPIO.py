from gpiozero import LED, Button
from time import sleep

a0 = 19
a_plus = 13
a_minus = 6 
a1 = 5

b0 = 21
b_plus = 20
b_minus = 16
b1 = 12

c0 = 7
c_plus = 8
c_minus = 25
c1 = 24
gpio_in={'a0':a0, 'a1':a1, 'b0':b0, 'b1':b1, 'c0':c0, 'c1':c1}
gpio_out={'a_plus':a_plus, 'a_minus':a_minus, 'b_plus':b_plus, 'b_minus':b_minus, 'c_plus':c_plus, 'c_minus':c_minus}

for pin in gpio_out:
    led = LED(gpio_out[pin])
    led.on()
    sleep(1)
    led.off()


while True:
    for btn in gpio_in:
        # print(btn + " " + str(gpio_in[btn]))
        button = Button(gpio_in[btn])
        print(btn + " " + str(button.is_pressed))
    sleep(5)
    print("")

