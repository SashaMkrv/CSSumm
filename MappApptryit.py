##import sys
##sys.argv = [ sys.argv[0] ]        # so we can have command line 
##from kivy.config import Config
##
## override config values, no easy way to do it :/
##Config.set ( 'graphics', 'width', config.state.window_width)
##Config.set('graphics','fullscreen',1)
##Config.set('graphics','resizable',1)
##Config.set ( 'graphics', 'height', state.window_height)

import kivy
from kivy.app import App
from kivy.clock import Clock
#from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.uix.dropdown import DropDown

from kivy.uix.popup import Popup
#from kivy.uix.colorpicker import ColorPicker

from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import Color, Rectangle

##################################################################
gridFile = "grid1.txt"
gridData = None
try:
    with open(gridFile) as myFile:
        gridData = myFile.read()
        myFile.close()

except IOError as e:
    print "Unable to open %s" % gridFile

allcols = 10
allrows = 10

allColor = {"blue": (0, .1, 1., 1.),
            "red": (1., 0, 0, 1.),
            "green": (0, 1., .1, 1.),
            "purple": (1., 0, 1., 1,),
            "yellow": (1., .9, 0, 1.),
            "pink": (1., .2, .4, 1.),
            "orange": (1., .5, 0, 1.)}

class ThingButton(Button):
    ####OOOOOHHHH MY GOD YOU CAN TOTALLY DEFINE BUTTONS TOO
    #######KIVY i LOVE YOUUUUUU
    #in retrospect this is hardly shocking. STILL GREAT THO (YYYY)
    x = NumericProperty(0)
    y = NumericProperty(0)
    info = {'name':None}
    currColor=ListProperty((1., .2, .4, 1.))
    def __init__(self, **kwargs):
        super(ThingButton, self).__init__(**kwargs)
        self.text = '%d, %d' % (self.x, self.y)
        self.stuff={'info':'this is wow', 'grade':'89'}

    def on_press(self):
        if self.last_touch.x < self.parent.width/2:
            self.side = 'right'
        else:
            self.side= 'left'
            
        if self.info['name']:
            self.t = self.info['name']
        else:
            self.t = self.text
        
        popup = OptionsPopup(orig=self)
        popup.open()

class OptionsPopup(Popup):
    orig = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(OptionsPopup, self).__init__(**kwargs)
        self.size_hint = (.5, 1.)
        self.title = self.orig.t
        if self.orig.side == 'right':
            self.pos_hint = {'x':.5}
        else:
            self.pos_hint = {'x':0}
        self.content = OptionsContent(orig=self.orig)
        

class OptionsContent(BoxLayout):
    orig = ObjectProperty()
    listOInfos = ListProperty()
    def __init__(self, **kwargs):
        super(OptionsContent, self).__init__(**kwargs)
        self.orientation = 'vertical'

##        def on_color(instance, value):
##            self.orig.color = value
##            self.orig.canvas.after.clear()
##            self.orig.canvas.after.add(Color(*value))
##            self.orig.canvas.after.add(Rectangle(size=self.orig.size,
##                                                 pos=self.orig.pos))
##
##        
##        changeColor=ColorPicker()
##        changeColor.bind(color=on_color)

        def on_release_col(instance, x):
            colList = allColor[x]
            self.orig.canvas.after.clear()
            self.orig.canvas.after.add(Color(*colList))
            self.orig.canvas.after.add(Rectangle(size = self.orig.size,
                                                 pos = self.orig.pos))

        def on_text(instance, value):
            n = instance.hint_text
            self.orig.stuff[n] = value
            print self.orig.stuff

        colDropdown = DropDown()
        
        for col in allColor:
            btn = Button(text=col,
                         size_hint_y=None,
                         height = '48dp',
                         background_color = allColor[col])

            btn.bind(on_release=lambda btn: colDropdown.select(btn.text))

            colDropdown.add_widget(btn)
            print "%s" % col
            
        colButt = Button(text='pink',
                         size_hint_y = None,
                         height = '48dp',
                         background_color = allColor['pink'])
        
        colButt.bind(on_release=colDropdown.open)
        colDropdown.bind(on_select=lambda instance, x: setattr(colButt,
                                                               "text",
                                                               x))
        colDropdown.bind(on_select=lambda instance, x: setattr(colButt,
                                                               "background_color",
                                                               allColor[x]))

##        colDropdown.bind(on_select=lambda instance, x: setattr(self.orig,
##                                                               "currColor",
##                                                               x

        colDropdown.bind(on_select=on_release_col)
        self.add_widget(colButt)
        

        for item in self.orig.stuff:
            lump = BoxLayout(orientation='vertical',
                             size_hint_y=.3)
            lump.add_widget(Label(text=item,
                                  size_hint_y=.1))
            infoBox = TextInput(text=self.orig.stuff[item],
                                size_hint_y=.9,
                                hint_text=item)
            lump.add_widget(infoBox)
            
            self.add_widget(lump)

            self.listOInfos.append(infoBox)
            
        for item in self.listOInfos:
            item.bind(text=on_text)
            
class MapGrid(GridLayout):
    def on_resize(self, what_the_heck, are_these_ones):
        #well this doesn't even exist
        Clock.schedule_once(self.showColor, 0)
        
    def __init__(self, **kwargs):
        super(MapGrid, self).__init__(**kwargs)
        self.padding = '8dp'
        self.spacing = '8dp'
        self.cols = allcols
        for xC in range(allrows):
            for yC in range(allcols):
                butt = ThingButton(x=xC, y=yC)
                self.add_widget(butt)
                
        Clock.schedule_once(self.showColor, 1)
        self.bind(size=self.on_resize)

    def showColor(self, dt):
        for child in self.children:
            child.canvas.after.clear()
            with child.canvas.after:
                Color(*child.currColor)
                Rectangle(size=child.size,
                          pos=child.pos)

class MappApp(App):
    def build(self):
        bigFren = MapGrid()
        return bigFren

    def on_stop(self):
        pass
        

if __name__ == '__main__':
    mappapp=MappApp()
    mappapp.run()
