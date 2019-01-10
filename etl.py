"""Application and Ux module.

This module implements application graphics and logic. Kivy has been chosen as graphic framework.

.. Kivy site:
   https://kivy.org/#home
"""
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
    """Represent Hotel Button graphical element.

    """
    pass


class HotelsDropDown(DropDown):
    """Represent Hotel DropDown (aka combobox) graphical element.

    """
    def create_hotels_list(self):
        """Creation Hotel list for DropDown.

        """
        hotels = load.loader.get_all_hotels()

        for hotel in hotels:
            btn = HotelButton(text=hotel.name)
            self.add_widget(btn)
            btn.bind(on_release=lambda bt: self.select(bt.text))


class ScrollLabel(ScrollView):
    """Represent Scrolling Label graphical element

    """
    text = StringProperty('')


class SelectableButton(RecycleDataViewBehavior, ScrollLabel):
    """Adding selection support to the Button.

    """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes.

        """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """Add selection on touch down .

        """
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view.
        """
        self.selected = is_selected


class SelectableLabel(RecycleDataViewBehavior, Label):
    """Add selection support to the Label.
    """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    selected_hotel= ""

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes.
        """
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down.

        """
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_node(self.index)

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view..

        """
        self.selected = is_selected
        if is_selected:
            SelectableLabel.selected_hotel = rv.data[index]['text']


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view.

    """


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    """ Adds selection and focus behaviour to the view.

    """


class TableView(RecycleView):
    """Table selectable View.

    """
    data_items = ListProperty([])
    hotel_name = ''
    row_number = StringProperty()

    def __init__(self, **kwargs):
        super(TableView, self).__init__(**kwargs)

    def get_reviews(self, name):
        """Extracting review for given Hotel name and update attribute.

        Args:
            name (str): The Hotel name.
        """
        data = load.loader.get_data_for_hotel(name)

        self.hotel_name = name

        self.data_items = []

        if data:
            for row in data:
                for col in row:
                    self.data_items.append(col)
        self.row_number = str(self.get_row_number())

    def get_row_number(self):
        """Extracting number or rows of data.

        Returns:
            Rows number.

        """
        return int(len(self.data_items)/9)

    def delete_all_reviews(self):
        """deleting all reviews from given hotel.

        """
        load.loader.clear_data_for_hotel(self.hotel_name)
        self.data_items = []

        self.row_number = str(self.get_row_number())


class CityListView(RecycleView):
    """City List selectable View.

    """
    city = ""

    def __init__(self, **kwargs):
        super(CityListView, self).__init__(**kwargs)

    def update_data(self):
        """Update City list from database.

        """
        CityListView.hotels_data = Transformer.transform_hotels((scrapper.get_hotels_from_city(CityListView.city)))
        self.data = [{'text': name} for name
                     in CityListView.hotels_data.keys()]


class ETLApp(App):
    """Main application.

    """
    title = "ETL Project"
    extract_list = []
    transform_result = {}
    close_button = False
    text_city = None
    count_funct = classmethod
    load_count = 0

    def build(self):
        """Build all graphical elements.

        Returns:
            Build layout.

        """
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
        """Handler for "Whole Process" button.

        Args:
            _: Ignored argument, Button (Button is not needed).

        """
        self.count_funct = lambda: self.load_count
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
        """Handler for "Extract" button.

        Args:
            _: Ignored argument, Button (Button is not needed).

        """
        self.count_funct = lambda: len(self.extract_list)
        self.show_popup('Extracting ongoing ...', 'Info')
        thr = threading.Thread(target=self.extract_thread)
        thr.start()
        Clock.schedule_interval(partial(self.check_job, thr), 1)

    def check_job(self, a_thread, _):
        """Checker if log term processing is finished now.

        Args:
            a_thread (object): The target thread for monitoring.

        Returns:
            False if thread fished.

        """
        if not a_thread.isAlive():
            self.close_button.disabled = False
            self.popup_label.text = "Process finished. Processed records:" + str(self.count_funct())
            return False

    def on_transform(self, _):
        """Handler for "Transform" button.

        Args:
            _: Ignored argument, Button (Button is not needed).

        """
        if not self.extract_list:
            self.show_popup('Empty result from Extract, please extract first!', 'Error')
            self.close_button.disabled = False
        else:
            self.count_funct = lambda: len(self.transform_result['review']) if len(self.transform_result) > 0 else 0
            self.show_popup('Transforming ongoing ...', 'Info')
            thr = threading.Thread(target=self.transform_thread)
            thr.start()
            Clock.schedule_interval(partial(self.check_job, thr), 1)

    def on_load(self, _):
        """Handler for "Load" button.

        Args:
            _: Ignored argument, Button (Button is not needed).

        """
        if not self.transform_result:
            self.show_popup('Empty result from Transform, please transform first!', 'Error')
            self.close_button.disabled = False
        else:
            self.count_funct = lambda: self.load_count
            self.show_popup('Loading ongoing...', 'Info')
            thr = threading.Thread(target=self.load_thread)
            thr.start()
            Clock.schedule_interval(partial(self.check_job, thr), 1)

    def extract_thread(self):
        """worker "extract" thread function.

        """
        "TODO: check if hotel seletecd"
        hotel_name = SelectableLabel.selected_hotel
        hlink = CityListView.hotels_data[hotel_name]
        self.extract_list = scrapper.scrap("http://www.booking.com/" + hlink)

    def transform_thread(self):
        """worker "transform" thread function.

        """
        self.transform_result = Transformer.transform_all(self.extract_list, SelectableLabel.selected_hotel)

    def load_thread(self):
        """worker "load" thread function.

        """
        self.load_count = load.loader.update_hotel_with_data(self.transform_result)
        self.clear_temporary_data()

    def show_popup(self, process_info, label_info):
        """Extracting review positive opinion from raw HTML.

        Args:
            process_info (str): info displayed inside popup.
            label_info (str): popup header.

        """
        layout = FloatLayout()

        self.popup_label = Label(text= process_info)
        self.close_button = Button(text="OK", size_hint=(.2,.1), pos_hint={'x': .4, 'y': .1})

        layout.add_widget(self.popup_label)

        layout.add_widget(self.close_button)

        # Instantiate the modal popup and display

        popup = Popup(title=label_info, content=layout)

        popup.open()

        # Attach close button press with popup.dismiss action
        self.close_button.disabled = True
        self.close_button.bind(on_press=popup.dismiss)

    def is_default_city_name(self):
        """Checks if city name is not default.

        Returns:
            True if city name is default, false if not.

        """
        if len(self.text_city.text) == 0 or self.text_city.text == "Please enter city":
            return True
        return False

    def on_city_find(self, _):
        """City find handler.

        Args:
            _: Ignored argument, Button (Button is not needed).

        """
        CityListView.city = self.text_city.text

        if self.is_default_city_name():
            self.show_popup("Please enter correct city name!", "Info")
            self.close_button.disabled = False
            return

        if self.citypopup:
            self.citypopup.open()

    def on_show_database(self, _):
        """Start show database popup handler.

        Args:
            _: Ignored argument, Button (Button is not needed).

        """
        if self.tablepopup:
            self.tablepopup.open()

    def clear_temporary_data(self):
        """Clear all data temporary stored in this class.

        """
        self.extract_list = []
        self.transform_result = {}
        self.text_city = None


if __name__ == '__main__':
    """Main application loop.

    """
    ETLApp().run()
