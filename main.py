#!/usr/bin/env python
'''
Banana Learner
=============
Simple application for learning vocabulary.
'''

# TODO Geschwindigkeit https://github.com/chaosbuffalolabs/kivy-profilers/blob/master/README.md
# TODO https://blog.kivy.org/2014/01/building-a-background-application-on-android-with-kivy/
# TODO http://cheparev.com/kivy-recipe-service-customization/
# TODO https://stackoverflow.com/questions/30934445/kivy-swiping-carousel-screenmanager
# Geschwindigkeit mit timeit oder https://stackoverflow.com/questions/44677606/how-to-measure-the-speed-of-a-python-function
# TODO Toggle verwenden https://stackoverflow.com/questions/8381735/toggle-a-value-in-python

import kivy
kivy.require('1.7.0')
import json
from os.path import join, exists
from os import listdir
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from random import shuffle
#from time import sleep

class About(Screen):
    pass

class Home(Screen):
    pass

class Manage(Screen):
    pass

class ManageWordView(Screen):
    file = StringProperty()
    cap_x_1 = NumericProperty()
    cap_x_2 = NumericProperty()
    cap_x_3 = NumericProperty()
    cap_x_4 = NumericProperty()

class LearnView(Screen):
    file = StringProperty()
    shelf = NumericProperty()
    cap_x_1 = NumericProperty()
    cap_x_2 = NumericProperty()
    cap_x_3 = NumericProperty()
    cap_x_4 = NumericProperty()

    # def set_cap(self,cap_neu):
    #     app.voclist[app.act_word_index]['cap'] = cap_neu
    #     self.ids["cap"].pos_hint = {'x':0, 'y':0}
    #     self.ids["cap"].size_hint = 1,.5

class BananaLearnerApp(App):
    def build(self):
        kivy.Config.set('graphics', 'width',  380)
        kivy.Config.set('graphics', 'height', 630)
        self.title = 'Banana Learner'

        self.transition = SlideTransition(duration=.001)
        self.transition.direction = 'left'
        root = ScreenManager(transition=self.transition)
        self.about = About(name='about')
        root.add_widget(self.about)
        # self.manage = Manage(name='manage')
        # root.add_widget(self.manage)

        self.load_vocabulary_json()
        self.make_indexlists()
        self.act_word_index = 0
        self.act_show_index = 0
        self.act_shelf_index = 0
        self.act_indexlist = []
        self.home = Home(name='home')
        root.add_widget(self.home)
        root.current = 'home'
        return root
#============================
# (U.a.) beim Starten der App
#============================
    def load_vocabulary_json(self):
        if not exists(self.vocabulary_fn):
            print('Keine Vokabeldatei vorhanden.')
            return
        with open(self.vocabulary_fn) as fd:
            data = json.load(fd)
        shuffle(data)
        self.voclist = data

    def make_indexlists(self):
        self.indexlist0 = self.make_indexlist(0)
        self.indexlist1 = self.make_indexlist(1)
        self.indexlist2 = self.make_indexlist(2)
        self.indexlist3 = self.make_indexlist(3)
        # print('Die vier Listen:')
        # print(self.indexlist0)
        # print(self.indexlist1)
        # print(self.indexlist2)
        # print(self.indexlist3)

    def make_indexlist(self,shelf):
        indexlist = []
        if shelf == 0:
            for i in range(0,len(self.voclist)):
                if self.voclist[i]['shelf'] != 0:
                    indexlist.append(i)
        else:
            for i in range(0,len(self.voclist)):
                if self.voclist[i]['shelf'] == shelf:
                    indexlist.append(i)
        return indexlist

    def make_short_indexlist(self,shelf):
        indexlist = []
        if shelf == 0:
            for i in range(0,len(self.voclist)):
                if self.voclist[i]['shelf'] != 0:
                    indexlist.append(i)
        else:
            for i in range(0,len(self.voclist)):
                if self.voclist[i]['shelf'] == shelf:
                    indexlist.append(i)
        shuffle(indexlist)
        del indexlist[10:]
        return indexlist

#=====================
# Fuer den Home-Screen (und About-Screen und LernView-Screens)
#=====================

    def go_to_about(self):
        self.transition.duration = 0.35
        self.transition.direction = 'left'
        self.root.current = 'about'

    def go_back_to_home_from_about(self):
        self.transition.direction = 'right'
        self.root.current = 'home'

    def go_back_to_home(self):
        self.save_words()
        for i in self.act_indexlist:
            alter_screen = 'word{}'.format(i)
            if self.root.has_screen(alter_screen) == True:
                self.root.remove_widget(self.root.get_screen(alter_screen))
        self.make_indexlists()
        self.act_show_index = 0
        self.act_word_index = 0
        self.transition.direction = 'right'
        self.root.current = 'home'

    def go_to_manage_overview(self):
        self.act_indexlist = self.indexlist0
        self.transition.duration = 0.2
        self.transition.direction = 'left'
        self.root.current = 'manage'

#==============================================
# Fuer die Manage-Screens und den Lernen-Screen
#==============================================
    def save_words(self):
        with open(self.vocabulary_fn, 'w') as fd:
            json.dump(self.voclist, fd)

#========================
# Fuer die Manage-Screens
#========================
    def go_back_to_manage(self):
        self.save_words()
        self.act_indexlist = self.indexlist0
        self.act_shelf_index = 0
        self.set_next_index()
        self.transition.duration = 0.2
        self.transition.direction = 'left'
        self.root.current = 'manage'

    def import_pictures(self):
        list_of_files = listdir('pic')
        for x in list_of_files:
            if any(x==y['file'] for y in self.voclist):
                pass
            else:
                self.voclist.append({'file': x, 'shelf':1,'cap':'links'})
                self.voclist.append({'file': x, 'shelf':1,'cap':'rechts'})
        self.save_words()
        self.make_indexlists()

    def set_next_index(self):
        self.act_show_index += 1
        self.act_word_index = self.act_indexlist[self.act_show_index%len(self.act_indexlist)]

    def set_prev_index(self):
        self.act_show_index -= 1
        self.act_word_index = self.act_indexlist[self.act_show_index%len(self.act_indexlist)]

    def manage_words(self):
        if self.indexlist0 == []:
            return
        else:
            self.act_show_index = 0
            self.act_word_index = self.indexlist0[0]
            self.transition.direction = 'left'
            self.transition.duration = 0.1
            self.load_words_to_manage()

    def load_words_to_manage(self):
        for i in range(0,len(self.indexlist0)):
            name = 'manage{}'.format(self.act_word_index)
            if self.root.has_screen(name):
                self.root.remove_widget(self.root.get_screen(name))
            if self.voclist[self.act_word_index].get('cap') == "links":
                cap_x_1 = 0
                cap_x_2 = 0
                cap_x_3 = .5
                cap_x_4 = 1
            elif self.voclist[self.act_word_index].get('cap') == "rechts":
                cap_x_1 = .5
                cap_x_2 = 0
                cap_x_3 = .5
                cap_x_4 = 1
            elif self.voclist[self.act_word_index].get('cap') == "unten":
                cap_x_1 = 0
                cap_x_2 = 0
                cap_x_3 = 1
                cap_x_4 = .5
            elif self.voclist[self.act_word_index].get('cap') == "oben":
                cap_x_1 = 0
                cap_x_2 = .5
                cap_x_3 = 1
                cap_x_4 = .5
            else:
                print('Es fehlt der cap-Eintrag.')
            view = ManageWordView(
                name = name,
                cap_x_1 = cap_x_1,
                cap_x_2 = cap_x_2,
                cap_x_3 = cap_x_3,
                cap_x_4 = cap_x_4,
                file = self.voclist[self.act_word_index].get('file')
                )
            self.root.add_widget(view)
            self.set_next_index()
            i += 1
        name = 'manage{}'.format(self.act_word_index)
        self.root.current = view.name

    def del_word(self):
        self.voclist[self.act_word_index]['shelf'] = 0
        self.set_next_index()
        self.show_next_word()

    def set_cap(self,cap_neu):
        self.voclist[self.act_word_index]['cap'] = cap_neu
        self.show_next_word()
        # self.ids["cap"].pos_hint = {'x':0, 'y':0}
        # self.ids["cap"].size_hint = 1,.5
        # self.set_next_index()
        # self.manage_words()

    def duplicate_word(self):
        cap_act = self.voclist[self.act_word_index]['cap']
        if cap_act == 'links':
            cap_neu = 'rechts'
        elif cap_act == 'rechts':
            cap_neu = 'links'
        elif cap_act == 'oben':
            cap_neu = 'unten'
        elif cap_act == 'unten':
            cap_neu = 'oben'
        duplikat = self.voclist[self.act_word_index].copy()
        duplikat['cap'] = cap_neu
        self.voclist.append(duplikat)
        self.manage_words()

    def go_to_next_word(self):
        '''...beim Bearbeiten.
        '''
        self.set_next_index()
        screenname = 'manage{}'.format(self.act_word_index)
        self.root.current = screenname

    def go_to_prev_word(self):
        '''...beim Bearbeiten.
        '''
        self.set_prev_index()
        screenname = 'manage{}'.format(self.act_word_index)
        self.root.current = screenname

#=======================
# Fuer den Lernen-Screen
#=======================

    def load_shelf(self,shelf):
        self.act_shelf_index = shelf
        self.act_indexlist = self.make_short_indexlist(shelf)
        if self.act_indexlist == []:
            return
        else:
            self.add_word_screens(self.act_indexlist)
            self.transition.direction = 'left'
            self.transition.duration = 0.1
            screenname = 'word{}'.format(self.act_indexlist[0])
            self.root.current = screenname
    def add_word_screens(self,indexlist):
        self.act_word_index = indexlist[0]
        for i in indexlist:
            name = 'word{}'.format(i)
            if self.root.has_screen(name):
                self.root.remove_widget(self.root.get_screen(name))
            if self.voclist[self.act_word_index].get('cap') == "links":
                cap_x_1 = 0
                cap_x_2 = 0
                cap_x_3 = .5
                cap_x_4 = 1
            elif self.voclist[self.act_word_index].get('cap') == "rechts":
                cap_x_1 = .5
                cap_x_2 = 0
                cap_x_3 = .5
                cap_x_4 = 1
            elif self.voclist[self.act_word_index].get('cap') == "unten":
                cap_x_1 = 0
                cap_x_2 = 0
                cap_x_3 = 1
                cap_x_4 = .5
            elif self.voclist[self.act_word_index].get('cap') == "oben":
                cap_x_1 = 0
                cap_x_2 = .5
                cap_x_3 = 1
                cap_x_4 = .5
            else:
                print('Es fehlt der cap-Eintrag.')
            view = LearnView(
                name = name,
                cap_x_1 = cap_x_1,
                cap_x_2 = cap_x_2,
                cap_x_3 = cap_x_3,
                cap_x_4 = cap_x_4,
                file = self.voclist[self.act_word_index].get('file'),
                shelf = self.voclist[self.act_word_index].get('shelf')
                )
            self.root.add_widget(view)
            # print(view)
            self.set_next_index()

    def show_next_word(self):
        '''...beim Lernen.
        '''
        self.set_next_index()
        screenname = 'word{}'.format(self.act_word_index)
        self.root.current = screenname

    def show_prev_word(self):
        '''...beim Lernen.
        '''
        self.set_prev_index()
        screenname = 'word{}'.format(self.act_word_index)
        self.root.current = screenname

    def shelf_up(self,shelf_old):
        if shelf_old == 1:
            self.voclist[self.act_word_index]['shelf'] = 2
            self.show_next_word()
        elif shelf_old == 2:
            self.voclist[self.act_word_index]['shelf'] = 3
            self.show_next_word()
        else:
            self.show_next_word()

    def shelf_down(self,shelf_old):
        if shelf_old == 2:
            self.voclist[self.act_word_index]['shelf'] = 1
            self.show_next_word()
        elif shelf_old == 3:
            self.voclist[self.act_word_index]['shelf'] = 2
            self.show_next_word()
        else:
            self.show_next_word()

    @property
    def vocabulary_fn(self):
        return join('data/', 'vocabulary.json')

if __name__ == '__main__':
    BananaLearnerApp().run()
                                                                       
