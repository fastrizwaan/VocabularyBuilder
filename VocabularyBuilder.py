#!/usr/bin/python
# Python3

import codecs
import os
import sys
import time
from random import sample, randint

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self):

        self.draw_main_window_headerbar()   # draw window
        self.define_variable()              # set variables
        self.read_file_and_import_data()    # read data from file
        self.generate_training_data()
        #self.ask_what_you_want()            # on startup ask what you want?
        self.set_vbox()
        self.start_learning(Gtk.Button())                  #instead of above let's start with quiz
        
     
         
    def set_vbox(self):
        #print("vbox")
        self.vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 0)
        self.add(self.vbox1)

    def start_learning(self, button):
        self.count = 0   

        self.change_to_learning_headerbar()
        self.generate_values(self.data)
        self.remove(self.vbox1)
        self.set_vbox()
        self.hb.props.title = "Vocabulary Builder 19"
        self.hb.props.subtitle = "Learning"
#        self.learningLabel = Gtk.Label()
#        self.learningLabel.set_label("Learning")
        
#        self.vbox1.pack_start(self.learningLabel, False, False, 0)

        self.show_learning_labels()
        #self.show_quiz_labels() #start with quiz
        
        

        ####
        self.hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.hbox0.set_property("width-request", 500)

        self.hbox0.set_property("height-request", 10)

        self.vbox1.pack_start(self.hbox0, False, False, 0)
        self.hbox0.pack_start(self.word_label, True, True, 0)
        self.hbox0.pack_start(self.word_difficulty, True, True, 0)
        self.vbox1.pack_start(self.word_meaning, False, False, 0)
        self.show_all()
        print(self.word)

   
    def start_quiz(self,button):
        self.count=0
        

        self.hb.props.title = "Vocabulary Builder 30"
        self.hb.props.subtitle = "Quiz"
        
        self.change_to_quiz_headerbar()
        self.generate_values(self.data)
        self.remove(self.vbox1)

        self.vbox1 = Gtk.Fixed()
        self.add(self.vbox1)
        self.button=['0','1','2','3','4']
        # add another horizontal box on 1st vbox
        self.vbox0 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=150)
        
        for x in range(0,5):
            self.button[x]=Gtk.CheckButton.new()
       
        self.vbox1.put(self.hbox0,0,0)
        self.vbox1.put(self.vbox0,0,50)
       
        self.hbox0.pack_start(self.word_label, True, True, 0)
        self.hbox0.pack_start(self.word_difficulty, True, True, 0)
       
        self.show_quiz_labels()

        #self.show_all()

    def on_button_toggled(self, button, name):
        
        if button.get_active():
            #debug# print("Im in toggled", self.correct)
            if self.correct != name:
                print("Incorrect!")
                #self.word_difficulty.set_markup("<span size=\"xx-small\"><b>" + self.difficulty + "</b></span>")
                output=button.get_label()
                #print(str(output))
                button.get_child().set_markup("<span><s>"+output +"</s></span>")
                          
            elif self.correct==name:
                print("Correct!!!!") 
                #button.set_active(True)
                
            for x in range(0,5):
                self.button[x].set_state_flags(Gtk.StateFlags.INSENSITIVE, True)
                #self.button[x].set_sensitive(False)
            
           # self.button[self.correct].set_sensitive(False)
            self.button[self.correct].set_state_flags(Gtk.StateFlags.CHECKED, True)
                
                #button.set_state_flags(Gtk.StateFlags.CHECKED, False)
                #self.show_quiz_labels()
                

    def read_file_and_import_data(self):
        #Open file and load Data#
        #-- File opening process --#
        try:
            fileName = "./vocab_data.tsv"
            file = codecs.open(fileName, "rb", encoding='UTF-8')
        except IndexError:
            print("Error: Please provide filename as argument")
            sys.exit(2)
        except IOError:
            print("Error: Cannot open file:", fileName)
            sys.exit(2)
    
        # load content from file
        
        for line in file:
            line=line.strip(os.linesep) #remove \r\n \n
            line = line.strip()         #remove trailing spaces and tabs 
            
            
            try:
            # expecting 5 tabs in a line 
            # 1st as word, 2nd as part of speech and 3rd as meaning
                #print(20* "LINE ")
                #print(line)
                (one,two,three,four,five,six) = line.split('\t')

                x = [one,two,three,four,five,six]
                #print(x)
                self.fileData.append(x)
            
        
            except ValueError:
                #If line does not contain 6 values separated  by 5 tabs then show that line
                print("*** Each Line with 6 values (word, pos, mean, example, difficutly, mastered) separated by Tabs")
                print("the bad line is")
                print('*'*50)
                print(line)
                print('*'*50)
                file.close()    #better to close file before exiting
                sys.exit(2)

        file.close()
        #Close file

    def define_variable(self):
        # Variables used in this program
        self.fileData=[]                        # Stores the date from file
        self.data=[]
        self.css=""                       #New list (data) from file data
        
        self.second=""
        self.third=""
        self.fourth=""
        self.fifth=""
        self.word =""
        self.difficulty=""
        self.meaning=""
        self.what = ''
        self.answer=""
        self.word_label = Gtk.Label()
        self.word_difficulty = Gtk.Label()
        self.word_meaning = Gtk.Label()
        self.icon = ""
        self.count=0


    def draw_main_window_headerbar(self):
        Gtk.Window.__init__(self, title="RadioButton Demo")
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "Vocabulary Builder 0.18"
        self.set_titlebar(self.hb)
        
                      
        self.set_border_width(15)
        self.set_size_request(500,400)
        self.set_default_size(500,400)
        self.set_resizable(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Back and next Buttons

        self.buttonBack = Gtk.Button.new()
        self.backIcon = Gio.ThemedIcon(name="go-previous-symbolic")
        self.backImage= Gtk.Image.new_from_gicon(self.backIcon, Gtk.IconSize.BUTTON)
        self.buttonBack.add(self.backImage)

        self.hb.pack_start(self.buttonBack)

        #self.buttonNext = Gtk.Button.new_with_label("Next >")
        self.buttonNext = Gtk.Button.new()
        self.nextIcon = Gio.ThemedIcon(name="go-next-symbolic")
        self.nextImage= Gtk.Image.new_from_gicon(self.nextIcon, Gtk.IconSize.BUTTON)
        self.buttonNext.add(self.nextImage)
        self.hb.pack_start(self.buttonNext)
        
        # Menu button on headerbar
        self.menu_button = Gtk.MenuButton()
        self.icon = Gio.ThemedIcon(name="open-menu-symbolic")
        self.image = Gtk.Image.new_from_gicon(self.icon, Gtk.IconSize.BUTTON)
        self.menu_button.add(self.image)
        self.hb.pack_end(self.menu_button)
        # connecting popover menu to menu_button
        #self.menu_button.connect("toggled", self.on_click_menubutton_on_headerbar)
        
        # Hide Close button
        #self.hb.set_show_close_button(False)

        # set button style 
        self.menu_button.set_relief(Gtk.ReliefStyle.NORMAL)
        #popover
        self.popover = Gtk.Popover()
        
        #in the pop up menu add menu items with button
        vbox = Gtk.Box(spacing=1, orientation=Gtk.Orientation.VERTICAL)
        vbox.set_border_width(5)
        menu_item_button1=Gtk.ModelButton()
        menu_item_button1.set_label("Learn Vocabulary")
        menu_item_button1.connect("clicked", self.start_learning)
        vbox.pack_start(menu_item_button1, True, True, 5)

        menu_item_button2=Gtk.ModelButton()
        menu_item_button2.set_label("Take Quiz")
        menu_item_button2.connect("clicked", self.start_quiz)
        vbox.pack_start(menu_item_button2, True, True, 5)
        
        menu_item_button3=Gtk.CheckButton()
        menu_item_button3.set_label("Dark Theme")
        menu_item_button3.connect("toggled", self.set_dark_theme)
        vbox.pack_start(menu_item_button3, True, True, 5)
        
        #add quit menu item
        menu_item_button4=Gtk.ModelButton()
        menu_item_button4.set_label("Quit")
        menu_item_button4.connect("clicked", Gtk.main_quit)
        vbox.pack_start(menu_item_button4, True, True, 5)
        
        #put the buttons in popover menu using vbox container
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        
        # add popover to menu button
        self.menu_button.set_popover(self.popover)

        # show the widgets
        self.popover.show_all()



    def change_to_learning_headerbar(self):
        self.hb.remove(self.buttonNext)
        self.hb.remove(self.buttonBack)
        self.count=0

        self.buttonBack = Gtk.Button.new()
        self.backIcon = Gio.ThemedIcon(name="go-previous-symbolic")
        self.backImage= Gtk.Image.new_from_gicon(self.backIcon, Gtk.IconSize.BUTTON)
        self.buttonBack.add(self.backImage)

        self.hb.pack_start(self.buttonBack)

        #self.buttonNext = Gtk.Button.new_with_label("Next >")
        self.buttonNext = Gtk.Button.new()
        self.nextIcon = Gio.ThemedIcon(name="go-next-symbolic")
        self.nextImage= Gtk.Image.new_from_gicon(self.nextIcon, Gtk.IconSize.BUTTON)
        self.buttonNext.add(self.nextImage)
        self.hb.pack_start(self.buttonNext)
        #self.buttonNext.set_label("LNext")
        self.buttonBack.connect("clicked", self.on_click_me_clicked_back_learn)
        self.buttonNext.connect("clicked", self.on_click_me_clicked_next_learn)
        
    def on_click_me_clicked_back_learn(self,widget):
        # generate values only when count>0
        if self.count >=1:
            self.count = self.count-1
            self.generate_values(self.data)
        self.show_learning_labels()

    def on_click_me_clicked_back_quiz(self,widget):
        # generate values only when count>0
        if self.count >=1:
            self.count = self.count-1
            self.generate_values(self.data)
        self.show_quiz_labels()


    def change_to_quiz_headerbar(self):
        self.hb.remove(self.buttonNext)
        self.hb.remove(self.buttonBack)
        
        #self.buttonNext.set_label("Qnext")
        self.count=0

        self.buttonBack = Gtk.Button.new()
        self.backIcon = Gio.ThemedIcon(name="go-previous-symbolic")
        self.backImage= Gtk.Image.new_from_gicon(self.backIcon, Gtk.IconSize.BUTTON)
        self.buttonBack.add(self.backImage)

        self.hb.pack_start(self.buttonBack)

        #self.buttonNext = Gtk.Button.new_with_label("Next >")
        self.buttonNext = Gtk.Button.new()
        self.nextIcon = Gio.ThemedIcon(name="go-next-symbolic")
        self.nextImage= Gtk.Image.new_from_gicon(self.nextIcon, Gtk.IconSize.BUTTON)
        self.buttonNext.add(self.nextImage)
        self.hb.pack_start(self.buttonNext)

        self.buttonBack.connect("clicked", self.on_click_me_clicked_back_quiz)
        self.buttonNext.connect("clicked", self.on_click_me_clicked_next_quiz)
    
    
    def on_click_me_clicked_next_learn(self,widget):
        # generate values only when count>0
        if self.count < self.indexMax:
            self.count = self.count+1
            self.generate_values(self.data)
        self.show_learning_labels()

    def on_click_me_clicked_next_quiz(self,widget):
        # generate values only when count>0
        if self.count < self.indexMax:
            self.count = self.count+1
            self.generate_values(self.data)
        self.show_quiz_labels()
    
    def set_dark_theme(self,button):
        if  button.get_active():
            settings = Gtk.Settings.get_default()
            settings.set_property("gtk-application-prefer-dark-theme", True)
        else:
            settings = Gtk.Settings.get_default()
            settings.set_property("gtk-application-prefer-dark-theme", False)

    def show_learning_labels(self):
        #self.word_label.set_markup("<span foreground=\"green\" font-desc=\"Arimo Bold 20\" size=\"x-large\">"+ self.word + "</span>")
        self.word_label.set_markup("<span size=\"xx-large\"><b>" + self.word + "</b></span>")
        self.word_label.set_halign(Gtk.Align.START)
        self.word_label.set_justify(Gtk.Justification.LEFT)
        #self.word_label.set_property("width-request", 0)
        #self.word_label.set_property("height-request", 10)
        
        #self.word_difficulty.set_markup("<span font-desc=\"Arimo 10\" size=\"x-large\"> ""[" + self.difficulty + "]""</span>")
        self.word_difficulty.set_markup("<span size=\"xx-small\"><b>" + self.difficulty + "</b></span>")
        self.word_difficulty.set_halign(Gtk.Align.END)
        self.word_difficulty.set_justify(Gtk.Justification.RIGHT)
        self.word_difficulty.set_line_wrap(True)

        # multiple meanings from single line to multiple lines
        #self.answer=self.answer.replace('; ', '\n')

        #self.word_meaning.set_markup("<span font-desc=\"Arimo 14\" size=\"x-large\">" + self.answer + "</span>")
        #self.word_difficulty.set_markup("[" + self.difficulty + "]")
        self.word_meaning.set_markup(self.answer)
        self.word_meaning.set_halign(Gtk.Align.START)
        self.word_meaning.set_justify(Gtk.Justification.FILL)
        self.word_meaning.set_line_wrap(True) 


    def show_quiz_labels(self):
        for x in range(0,5):
            #self.button[x].set_state_flags(Gtk.StateFlags.INSENSITIVE, False)
            self.button[x].set_active(False)
        self.word_label.set_markup("<span size=\"xx-large\"><b>" + self.word + "</b></span>")
        #self.word_label.set_markup("<span foreground=\"green\" font-desc=\"Arimo Bold 20\" size=\"x-large\"> "+ self.word + "</span>")
        self.word_label.set_selectable(True)
        self.word_label.set_halign(Gtk.Align.START)
        self.word_label.set_justify(Gtk.Justification.LEFT)
        #self.word_label.set_property("width-request", 0)
        #self.word_label.set_property("height-request", 10)

        self.word_difficulty.set_markup("<span size=\"xx-small\"><b>" + self.difficulty + "</b></span>")
        #self.word_difficulty.set_markup("<span font-desc=\"Arimo Bold 10\" size=\"x-large\"> ""[" + self.difficulty + "]""</span>")
        #self.word_difficulty.set_markup("[" + self.difficulty + "]")
        self.word_difficulty.set_halign(Gtk.Align.END)
        self.word_difficulty.set_justify(Gtk.Justification.RIGHT)
        self.word_difficulty.set_line_wrap(True)
        #self.word_difficulty.set_property("width-request", 500)
        #self.word_difficulty.set_property("height-request", 200)
        
        for x in range(0,5): #rizvan
            self.vbox0.remove(self.button[x])
            self.button[x]=Gtk.CheckButton.new()
            
            self.button[x].connect("clicked", self.on_button_toggled, x)
            self.button[x].set_label(self.randXList[x])
            self.button[x].get_child().set_justify(Gtk.Justification.FILL)
            self.button[x].get_child().set_line_wrap(True)
            #self.button[x].get_child().set_single_line_mode(True)
            self.button[x].set_property("width-request", 500)
            self.button[x].set_property("height-request", 00)
            self.vbox0.pack_start(self.button[x], False, False, 0)
            
        self.show_all()
        self.hbox0.set_property("width-request", 500)
        self.hbox0.set_property("height-request", 10)

        
        #headerbar button "click me"
        #self.buttonOK = Gtk.Button.new_with_label("Next >")
        #self.buttonOK.connect("clicked", self.on_click_me_clicked)
        

        

        # Afer generating new data remove radio selection
        for x in range(0,5):
            self.button[x].set_state_flags(Gtk.StateFlags.SELECTED, True)
        

    def generate_training_data(self):
        
        #New list (data) from file data
        needItems=10
        idxMax = len(self.fileData)-1    # total number of items in data list, -1 (0-25=26)
        r=sample(range(0, idxMax), needItems)

        for x in range(0,needItems):
            self.data.append(self.fileData[r[x]])
            #print(x)
        self.indexMax=len(self.data)-1

    def generate_values(self,data):
        #print("Hello values")
              
                
        #Max number of entries in the list
        

        # next and back needs count
        if  self.count > self.indexMax:  #if reached end of list
            self.count = self.indexMax
        elif self.count < 0:        #if reached the beginning of list
            self.count = 0

        # Disable Buttons based on counter
        # Back button
        if  self.count == 0:
            self.buttonBack.set_sensitive(False)
        elif  self.count > 0:
            self.buttonBack.set_sensitive(True)
        # Next button
        if  self.count == self.indexMax:
            self.buttonNext.set_sensitive(False)
        elif  self.count < self.indexMax:
            self.buttonNext.set_sensitive(True)


        #Get 5 random unique index values
        randList=sample(range(0, self.indexMax), 5)
        #print(self.data)
        # Get quiz word and answer and wrong answers
        
        quizWord=self.data[self.count][0]   # quiz word
        
        self.answer=self.data[self.count][1]    # correct answer
        self.difficulty=self.data[self.count][4]  # category of word to be displayed on right side
        answer1=self.fileData[randList[1]][1]    # wrong answer 1
        answer2=self.fileData[randList[2]][1]    # wrong answer 2
        answer3=self.fileData[randList[3]][1]    # wrong answer 3
        answer4=self.fileData[randList[4]][1]    # wrong answer 4
        #randomize radiobuttons
        randList2=sample(range(0, 5), 5)
        xlist=[self.answer, answer1, answer2, answer3, answer4]
        self.randXList=[xlist[randList2[0]], xlist[randList2[1]],xlist[randList2[2]],xlist[randList2[3]],xlist[randList2[4]]]
        #print(answer0)
        #print(xlist)
        self.first=self.randXList[0]
        self.second=self.randXList[1]
        self.third=self.randXList[2]
        self.fourth=self.randXList[3]
        self.fifth=self.randXList[4]
        self.correct=self.randXList.index(self.answer) #we have 1 2 3 4 here it is 0 1 2 3 hence add 1
        self.word=quizWord


# Main Program
win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
