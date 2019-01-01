from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
import threading
from functools import partial
from extract import scrapper
from transform.transformer import Transformer
import load.loader
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown


class HotelButton(Button):
    pass


class HotelsDropDown(DropDown):
    def create_hotels_list(self):
        hotels = load.loader.get_all_hotels()

        for hotel in hotels:
            btn = HotelButton(text=hotel.name)
            self.add_widget(btn)
            btn.bind(on_release=lambda bt: self.select(bt.text))

class ScrollLabel(ScrollView):
    text = StringProperty('')


class SelectableButton(RecycleDataViewBehavior, ScrollLabel):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    selected_hotel= ""

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_node(self.index)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            SelectableLabel.selected_hotel = rv.data[index]['text']


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class TableView(RecycleView):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(TableView, self).__init__(**kwargs)

    def get_reviews(self, name):
        data = load.loader.get_data_for_hotel(name)

        self.data_items = []

        if data:
            for row in data:
                for col in row:
                    self.data_items.append(col)

    def get_row_number(self):
        return int(len(self.data_items)/9)

    def delete_all_reviews(self):
        load.loader.clear_data_for_hotel("Armon Residence")
        self.data_items = []


class RV(RecycleView):
    city = ""

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def updatedata(self):
        RV.hotels_data = Transformer.transfom_hotels((scrapper.get_hotels_from_city(RV.city)))
        self.data = [{'text': name} for name
                     in RV.hotels_data.keys()]


class ETLApp(App):
    title = "ETL Project"
    extract_list = []
    transfrom_result={}
    close_button = False
    text_city = None

    def build(self):
        self.text_city = TextInput(text='Please enter city', multiline=False, size_hint = (.6,.1), pos_hint ={'x': .1, 'y': .8})
        button_city_input = Button(text="Enter", size_hint=(.2, .1), pos_hint={'x': .7, 'y': .8})

        button_extract = Button(text="Extract", size_hint = (.2,.1), pos_hint ={'x': .1, 'y': .6})
        button_transform = Button(text="Transform",size_hint = (.2,.1), pos_hint ={'x': .4, 'y': .6})
        button_load = Button(text="Load", size_hint = (.2,.1), pos_hint ={'x': .7, 'y': .6})

        button_complete = Button(text="Whole Process", size_hint = (.2,.1), pos_hint ={'x': .4, 'y': .4})

        button_show_database_content = Button(text="Show Database", size_hint=(.2, .1), pos_hint={'x': .4, 'y': .2})

        layout = FloatLayout()
        layout.add_widget(self.text_city)
        layout.add_widget(button_city_input)
        layout.add_widget(button_extract)
        layout.add_widget(button_transform)
        layout.add_widget(button_load)
        layout.add_widget(button_complete)

        layout.add_widget(button_show_database_content)

        button_complete.bind(on_press=self.on_complete)
        button_extract.bind(on_press=self.on_extract)
        button_load.bind(on_press=self.on_load)
        button_transform.bind(on_press=self.on_transform)
        button_city_input.bind(on_press=self.on_city_find)
        button_show_database_content.bind(on_press=self.on_show_database)

        load.loader.init_connection()
        self.tablepopup = Builder.load_file('ux/tablepopup.kv')
        self.citypopup = Builder.load_file('ux/citespopup.kv')
        return layout

    def on_complete(self, _):
        self.show_popup('Starting Extract & Transform & Load ...', 'Info')
        threxecute = threading.Thread(target=self.extract_thread)
        thrtransform = threading.Thread(target=self.transform_thread)
        thrload = threading.Thread(target=self.load_thread)

        threxecute.start()
        threxecute.join()
        thrtransform.start()
        thrtransform.join()
        thrload.start()

        Clock.schedule_interval(partial(self.check_job, thrload), 1)

    def on_extract(self, _):
        self.show_popup('Starting Extract ...', 'Info')
        thr = threading.Thread(target=self.extract_thread)
        thr.start()
        Clock.schedule_interval(partial(self.check_job, thr), 1)

    def check_job(self, a_thread, _):
        if not a_thread.isAlive():
            self.close_button.disabled = False
            return False

    def on_transform(self, _):
        if not self.extract_list:
            self.show_popup('Empty result from Extract, please extract first!', 'Error')
            self.close_button.disabled = False
        else:
            self.show_popup('Starting Transform ...', 'Info')
            thr = threading.Thread(target=self.transform_thread)
            thr.start()
            Clock.schedule_interval(partial(self.check_job, thr), 1)

    def on_load(self, _):
        if not self.transfrom_result:
            self.show_popup('Empty result from Transform, please transform first!', 'Error')
            self.close_button.disabled = False
        else:
            self.show_popup('Starting Load ...', 'Info')
            thr = threading.Thread(target=self.load_thread)
            thr.start()
            Clock.schedule_interval(partial(self.check_job, thr), 1)

    def extract_thread(self):
        "TODO: check if hotel seletecd"
        hotel_name = SelectableLabel.selected_hotel
        hlink = RV.hotels_data[hotel_name]
        self.extract_list = scrapper.scrap("http://www.booking.com/" + hlink)

    def transform_thread(self):
        self.transfrom_result = Transformer.transform_all(self.extract_list, SelectableLabel.selected_hotel)

    def load_thread(self):
        load.loader.update_hotel_with_data(self.transfrom_result)

    def show_popup(self, process_info, label_info):
        layout = FloatLayout()

        popup_label = Label(text= process_info)
        self.close_button = Button(text="OK", size_hint=(.2,.1), pos_hint={'x': .4, 'y': .1})

        layout.add_widget(popup_label)

        layout.add_widget(self.close_button)

        # Instantiate the modal popup and display

        popup = Popup(title=label_info, content=layout)

        popup.open()

        # Attach close button press with popup.dismiss action
        self.close_button.disabled = True
        self.close_button.bind(on_press=popup.dismiss)

    def on_city_find(self, _):
        RV.city = self.text_city.text
        if self.citypopup:
            self.citypopup.open()

    def on_show_database(self, _):
        if self.tablepopup:
            self.tablepopup.open()


if __name__ == '__main__':
    ETLApp().run()
