from utils.button import Button
import utils.constants as constants

expanders = constants.get_expanders()

buttons = []
for index, pin in enumerate(constants.BUTTON_PINS):
    expander = expanders[ pin // 8 ]
    pin_number = pin % 8
    btn = Button(index, expander, pin_number)
    buttons.append(btn)

print("Polling...")
while True:
    for btn in buttons:
        btn.poll()
