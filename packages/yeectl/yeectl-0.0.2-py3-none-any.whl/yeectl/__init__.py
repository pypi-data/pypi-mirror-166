"""Main TUI implementation for yeectl

Author: Bean Robinson  
Created: 
"""

import os
import py_cui
import yeelight

__version__ = 'v0.0.2'

def findBulbs():
    #Array to store bulb objects in
    bulbs = {}
    #Dict of models and better display names for them
    models = {
            "color": "Colour bulb",
            "stripe": "Lightstrip",
            }
    #For each bulb on network
    for bulb in yeelight.discover_bulbs():
        #Get display name
        displayName = models[bulb["capabilities"]["model"]]
        #Append 
        count = 0
        for name in bulbs:
            if displayName in name:
                count += 1
        bulbname = displayName + " (" + str(count) + ")"
        bulbs[bulbname] = yeelight.Bulb(bulb["ip"])
    return bulbs

class YeectlApp:
    def __init__(self, master):
        self.bulbs = findBulbs()
        self.bulbNames = []
        self.selected = []
        for name in self.bulbs:
            self.bulbNames.append(name)

        self.master = master
        self.master.add_block_label(self.getBanner(), 0, 0, column_span=5)

        self.lightlist = self.master.add_checkbox_menu('Lights', 1, 0, row_span=2, column_span=2)
        self.lightlist.add_item_list(self.bulbNames)
        self.lightlist.add_key_command(py_cui.keys.KEY_ENTER, self.toggleBulbSelected)
        self.lightlist.set_selected_color(py_cui.CYAN_ON_BLACK)

        self.onbutton = self.master.add_button("On", 1, 2, command=self.on)
        self.offbutton = self.master.add_button("Off", 1, 3, command=self.off)
        self.brightbutton = self.master.add_button("Brightness", 1, 4, command=self.bright)

        self.colours = self.master.add_scroll_menu("Colours", 2, 2, column_span=2)
        self.colours.add_item_list(self.getColours())
        self.colours.add_key_command(py_cui.keys.KEY_ENTER, self.colour)
        self.colours.set_selected_color(py_cui.CYAN_ON_BLACK)

        self.xcolours = self.master.add_scroll_menu("XResources", 2, 4, column_span=1)
        self.xcolours.add_item_list(self.getXColours())
        self.xcolours.add_key_command(py_cui.keys.KEY_ENTER, self.xcolour)
        self.xcolours.set_selected_color(py_cui.CYAN_ON_BLACK)

    def getBanner(self):
        banner = ''
        banner += "                                             ___ \n"
        banner += "                                             `MM \n"
        banner += "                                       /      MM \n"
        banner += "____    ___  ____     ____     ____   /M      MM \n"
        banner += "`MM(    )M' 6MMMMb   6MMMMb   6MMMMb./MMMMM   MM \n"
        banner += " `Mb    d' 6M'  `Mb 6M'  `Mb 6M'   Mb MM      MM \n"
        banner += "  YM.  ,P  MM    MM MM    MM MM    `' MM      MM \n"
        banner += "   MM  M   MMMMMMMM MMMMMMMM MM       MM      MM \n"
        banner += "   `Mbd'   MM       MM       MM       MM      MM \n"
        banner += "    YMP    YM    d9 YM    d9 YM.   d9 YM.  ,  MM \n"
        banner += "     M      YMMMM9   YMMMM9   YMMMM9   YMMM9 _MM_\n"
        banner += "    d'                                           \n"
        banner += "(8),P                                            \n"
        banner += " YMM                                             "
        return banner

    def toggleBulbSelected(self):
        selected = self.lightlist.get()
        if selected not in self.selected:
            self.selected.append(selected)
        else:
            self.selected.remove(selected)

    def on(self):
        for name in self.selected:
            self.bulbs[name].turn_on()

    def off(self):
        for name in self.selected:
            self.bulbs[name].turn_off()

    def getColours(self):
        colours = {}
        customColours1 = self.loadCustomColours("~/.config/yeectl/colours")
        customColours2 = self.loadCustomColours("~/.config/yeectl/colors")
        if customColours1 == None and customColours2 == None:
            colours = { "Failed to load custom colours": (0, 0, 0) }
        else:
            if customColours1 != None:
                colours.update(customColours1)
            if customColours2 != None:
                colours.update(customColours2)
        return colours

    def loadCustomColours(self, filename):
        colours = {}
        try:
            with open(os.path.expanduser(filename), "r") as file:
                contents = file.readlines()
            lines = []
            for line in contents:
                lines.append(line)
            for line in lines:
                split = line.split(": ")
                name = split[0]
                hex = split[1]
                colours[name] = hex
            for colour in colours:
                colours[colour] = tuple(int(colours[colour].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
            return colours
        except:
            return None

    def getXColours(self):
        colours = {}
        try:
            with open(os.path.expanduser("~/.xresources"), "r") as file:
                contents = file.readlines()
            lines = []
            for line in contents:
                if "*.color" in line:
                    lines.append(line)
            for line in lines:
                hex = line.split(": ")[1]
                colours[hex] = []
            for colour in colours:
                colours[colour] = tuple(int(colour.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        except:
            colours = {
                        "Failed to load ~/.xresources": (0, 0, 0)
                      }
        return colours

    def colour(self):
        colour = self.getColours()[self.colours.get()]
        for name in self.selected:
            self.bulbs[name].set_rgb(colour[0], colour[1], colour[2])

    def xcolour(self):
        colour = self.getXColours()[self.xcolours.get()]
        for name in self.selected:
            self.bulbs[name].set_rgb(colour[0], colour[1], colour[2])

    def bright(self):
        self.master.show_text_box_popup("Enter the desired brightness:", command=self.brightvalid)

    def brightvalid(self, text):
        try:
            num = int(text)
            if num <= 100 and num >= 0:
                for name in self.selected:
                    self.bulbs[name].set_brightness(num)
            else:
                self.master.show_error_popup("Error", "Please enter an integer between\n0 and 100 (inclusive).")
        except:
            self.master.show_error_popup("Error", "Please enter an integer.")

def main():
    root = py_cui.PyCUI(3, 5)
    wrapper =  YeectlApp(root)
    root.set_title('YEECTL')
    root.toggle_unicode_borders()
    root.start()
