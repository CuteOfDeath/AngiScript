#Libraries
import PySimpleGUI as sg
import cv2
import numpy as np
import time
import pyautogui
from pynput import keyboard as listen
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from playsound import playsound
import threading
#Import settings file
settings_file_read = open("../data/settings.txt","r+")
settings_list = settings_file_read.readlines()
settings_file_read.close()
settings_list2 = []
for i in settings_list:
    settings_list2.append(i.strip())
settings_list.clear()
for i in settings_list2:
    settings_list.append(i.split(":"))
settings_dict = {}
for i in settings_list:
    settings_dict[i[0]] = eval(i[1])
#Classes
class macro():
    def __init__(self):
        self.current_field = ""
        self.currently_on = False
    def is_container_full(self):
        """Checks if pollen container full by checking if the 'pollen container full' message is on screen

        Returns:
            bool: Returns True if the message is on screen, False otherwise
        """
        if is_on_screen("../cache/index.png","../resources/pollen_container_full_message.png") == True:
            return True
        else:
            return False
    def has_mondo_spawned(self):
        """Checks if Mondo Chick has spawned by checking if "Mondo Chick has spawned!" message is on screen

        Returns:
            bool: Returns True if the message is on screen, False otherwise
        """
        if is_on_screen("../cache/index.png","../resources/mondo_chick_spawned_message.png") == True:
            return True
        else:
            return False
    def has_windy_spawned(self):
        """Checks if Windy Bee has spawned by checking if "[...]found Windy Bee in the[...]" message is on screen

        Returns:
            bool: Returns True if the message is on screen, False otherwise
        """
        if is_on_screen("../cache/index.png","../resources/windy_bee_spawned_message.png") == True:
            return True
        else:
            return False
    def macro_bullshit(self,field_multiplier="Small"):
        if self.currently_on == True:
            if field_multiplier == "Large":
                field_multiplier = 1
            elif field_multiplier == "Medium":
                field_multiplier = 0.75
            else:
                field_multiplier = 0.5
            mov_keys = ["d","w","a","s"]
            for i in range(len(mov_keys)):
                keyboard.press(mov_keys[i])
                if i % 2 == 0:
                    add_delay(1 * field_multiplier)
                else:
                    add_delay(2 * field_multiplier)
                keyboard.release(mov_keys[i])
#Functions
def additional_settings_window():
    layout = [[sg.Checkbox("Autoclicker mode",settings_dict["only_autoclick"],key="only_autoclick",background_color="#211C1C",tooltip="Turns the macro into a autoclicker.")],
              [sg.Text("Refresh rate",background_color="#211C1C"),sg.Input(key="mouseclick_input",size=(5,5),tooltip="Amount of delay in miliseconds between macro activations. WARNING! Putting anything else than natural numbers can and will crash the program!",default_text=settings_dict["mouseclick_delay"])],
              [sg.Button("Apply",key="apply",button_color="#CC9A4B")]]
    window = sg.Window("Additional Settings",layout,modal=True,size=(200,150),background_color="#211C1C",icon="../resources/icon.ico")
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "apply":
            settings_dict["only_autoclick"] = values["only_autoclick"]
            settings_dict["mouseclick_delay"] = values["mouseclick_input"]
            settings_file_write = open("../data/settings.txt","w+")
            for i in settings_dict.keys():
                settings_file_write.write(str(i) + ":" + str(settings_dict[i]) + "\n")
            settings_file_write.close()
            window.close()
            
    window.close()
def is_on_screen(image_directory,template_directory):
    """Checks if the image given in [image_directory] contains the image give in [template_directory].
    Code taken from: https://stackoverflow.com/questions/7853628/how-do-i-find-an-image-contained-within-an-image

    Args:
        image_directory (str): The directory of the checked imagew
        template_directory (str): The directory of the looked for image

    Returns:
        bool: returns True or False depending if the image contains the template
    """
    img_rgb = cv2.imread(image_directory)
    template = cv2.imread(template_directory)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    if len(np.where(res >= threshold)[0]) != 0:
        return True
    else:
        return False
def add_delay(delay_amount: int):
    """Adds a delay without using sleep(), thus allowing background processes to still run

    Args:
        delay_amount (float): delay time in seconds
    """
    start = time.time ()
    while time.time () < start + delay_amount:
        pass
def on_press(key):
    """Code used from https://pynput.readthedocs.io/en/latest/keyboard.html"""
    if key == Key.f6:
        if macro.currently_on == False:
            macro.currently_on = True
        else:
            macro.currently_on = False
#Variables
keyboard = KeyboardController()
mouse = MouseController()
macro = macro()
listener = listen.Listener(
    on_press=on_press)
listener.start()
#Layout Variable here!

f_select_field = [  [sg.OptionMenu(("Large","Medium","Small"),"Large",key="field_select")],
                    [sg.Checkbox("Use autoconverters when full ",settings_dict["do_autoconvert"],enable_events=True,size=[40,40],key="do_autoconvert",background_color="#211C1C",tooltip="Automatically uses an autoconverter when the 'containter full' message is detected")],
                    [sg.Text("Autoconverter hotbar key",key="autoconvert_text",visible=settings_dict["do_autoconvert"],background_color="#211C1C"),sg.Input(key="autoconvert_input",default_text=settings_dict["autoconvert_key"],visible=settings_dict["do_autoconvert"],tooltip="Set the hotkey the autoconverter is binded to")]]

f_settings = [[sg.Checkbox("Bag full notification",settings_dict["full_notif"],key="full_notif",background_color="#211C1C",tooltip="Plays a sound effect whenever your bag is full.")],
              [sg.Checkbox("Mondo Chick notification",settings_dict["mondo_notif"],key="mondo_notif",background_color="#211C1C",tooltip="Plays a sound effect whenever Mondo Chick spawns")],
              [sg.Checkbox("Windy Bee notification",settings_dict["windy_notif"],key="windy_notif",background_color="#211C1C",tooltip="Plays a sound effect whenever Windy Bee spawns")],
              [sg.Checkbox("Wealth Clock notification",settings_dict["clock_notif"],key="clock_notif",background_color="#211C1C",tooltip="Plays a sound effect whenever the Wealth Clock is charged, starts counting down from startup of the program")]]

layout = [  [sg.Image("../resources/logo.png",size=(50,50),background_color="#211C1C"),sg.Text("AngiScript",font=("Gill Sans MT",30),background_color="#211C1C")],
            [sg.Frame("Select Field",f_select_field,size=(207.5,150),background_color="#211C1C",title_color="#ECB457"),sg.Frame("Settings",f_settings,size=(207.5,150),background_color="#211C1C",title_color="#ECB457")],
            [sg.Button("Apply Settings",size=(52,1),key="apply_settings",button_color="#CC9A4B")],
            [sg.Button("Start/Stop (F6)",size=(25,2),key="start",button_color="#CC9A4B"),sg.Button("Additional Settings",size=(25,2),key="additional_settings",button_color="#CC9A4B")] ]
#-------
#window creation here!
window = sg.Window("AngiScript",layout,size=(450,300),background_color="#211C1C",icon="../resources/icon.ico")
#------
seconds = time.time()
stamp = seconds
clock_stamp = seconds + 3600
full_notif_cooldown = seconds + 10
macro_thread = threading.Thread(name="movement macro",target=macro.macro_bullshit,daemon=True)
macro_thread.start()
#Action
while True:
    seconds = time.time()
    event,values = window.read(timeout=settings_dict["mouseclick_delay"])
    if event == sg.WIN_CLOSED:
        break
    if event == "do_autoconvert":
        if values["do_autoconvert"] == True:
            window["autoconvert_text"].update(visible=True)
            window["autoconvert_input"].update(visible=True)
        else:
            window["autoconvert_text"].update(visible=False)
            window["autoconvert_input"].update(visible=False)
    if event == "start":
        if macro.currently_on == False:
            macro.currently_on = True
        else:
            macro.currently_on = False
    if macro.currently_on == True:
        if event == sg.TIMEOUT_EVENT:
            if settings_dict["only_autoclick"] == True:
                mouse.click(Button.left)
            else:
                mouse.press(Button.left)  
                macro.macro_bullshit(values["field_select"])
                if settings_dict["do_autoconvert"] == True or settings_dict["full_notif"] == True or settings_dict["mondo_notif"] == True or settings_dict["windy_notif"] == True:
                    if seconds > stamp + 1:
                        screenshot = pyautogui.screenshot()
                        screenshot.save("../cache/index.png")
                        if settings_dict["full_notif"] == True or settings_dict["do_autoconvert"] == True:
                            if seconds > full_notif_cooldown:
                                if macro.is_container_full() == True:
                                    if settings_dict["do_autoconvert"] == True:
                                        keyboard.press(settings_dict["autoconvert_key"])
                                        keyboard.release(settings_dict["autoconvert_key"])
                                    if settings_dict["full_notif"] == True:
                                        playsound("../resources/Card_Lock.wav")
                                    full_notif_cooldown = seconds + 10
                        if settings_dict["mondo_notif"] == True:
                            if macro.has_mondo_spawned() == True:
                                playsound("../resources/LongBird_SubAtk.wav")
                        if settings_dict["windy_notif"] == True:
                            if macro.has_windy_spawned() == True:
                                playsound("../resources/Fairy_Special.wav")
                        stamp = seconds
                mouse.release(Button.left)
    if seconds > clock_stamp:
        playsound("../resources/WealthClock.wav")
        clock_stamp += seconds + 3600
    if event == "additional_settings":
        additional_settings_window()
    if event == "apply_settings":
        macro_thread.args = values["field_select"]
        settings_dict["do_autoconvert"] = values["do_autoconvert"]
        settings_dict["autoconvert_key"] = values["autoconvert_input"]
        settings_dict["full_notif"] = values["full_notif"]
        settings_dict["mondo_notif"] = values["mondo_notif"]
        settings_dict["windy_notif"] = values["windy_notif"]
        settings_dict["clock_notif"] = values["clock_notif"]
        settings_file_write = open("../data/settings.txt","w+")
        for i in settings_dict.keys():
            settings_file_write.write(str(i) + ":" + str(settings_dict[i]) + "\n")
        settings_file_write.close()
    
            
window.close()
listener.stop()   