from gpiozero import LED, Button
from time import sleep


def set_io_pins(pins):
    for pin in pins.split(","):
        pinnum=pin.split("|")[0]
        pinval=pin.split("|")[1]
        led = LED(pinnum)
        if(pinval == "0"):
            led.off()
        else:
            led.on()


def get_io_pins(pins):
    res=[]
    for pin in pins.split(","):
        btn = Button(pin)
        r=str(pin)+"|";
        if(btn.is_pressed):
            r+="1"
        else:
            r+="0"
        res.append(r)
    return ",".join(res)

#print(get_io_pins("1,2,3,4,5,6"))
#set_io_pins("1|1,2|0")
