import mouse
import pydirectinput as pdi

def minecraft(label):
    if label == "T pose":
        pdi.keyDown("ctrl")
        pdi.keyDown("w")
    else:
        pdi.keyUp("ctrl")
        pdi.keyUp("w")
        if label == "Dab":
            mouse.click()
        elif label == "Heart":
            mouse.right_click()
        elif label == "Left_hand_side":
            mouse.move(-20, 0, duration = 0.1, absolute = False)
        elif label == "Right_hand_side":
            mouse.move(20, 0, duration = 0.1, absolute = False)
        elif label == "Left_hand_up":
            mouse.wheel(delta = 1)
        elif label == "Right_hand_up":
            mouse.wheel(delta = -1)