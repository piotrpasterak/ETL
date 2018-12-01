from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from functools import partial
import threading
from extract import scrapper
from transform.transformer import Transformer


class ETLApp(App):
    title = "ETL Project"
    extract_list = []
    close_button = False

    def build(self):
        button_extract = Button(text="Extract", size_hint = (.2,.1), pos_hint ={'x': .1, 'y': .7})
        button_transform = Button(text="Transform",size_hint = (.2,.1), pos_hint ={'x': .4, 'y': .7})
        button_load = Button(text="Load", size_hint = (.2,.1), pos_hint ={'x': .7, 'y': .7})
        button_complete = Button(text="Whole Process", size_hint = (.2,.1), pos_hint ={'x': .4, 'y': .5})

        button_show_database_content = Button(text="Show Database", size_hint=(.2, .1), pos_hint={'x': .2, 'y': .3})

        layout = FloatLayout()
        layout.add_widget(button_extract)
        layout.add_widget(button_transform)
        layout.add_widget(button_load)
        layout.add_widget(button_complete)

        layout.add_widget(button_show_database_content)

        button_complete.bind(on_press=self.on_complete)
        button_extract.bind(on_press=self.on_extract)
        button_load.bind(on_press=self.on_load)
        button_transform.bind(on_press=self.on_transform)
        return layout

    def on_complete(self, button):
        self.show_popup('Starting Extract & Transform & Load ...', 'Info')

    def on_extract(self, button):
        self.show_popup('Starting Extract ...', 'Info')
        thr = threading.Thread(target=self.extract_thread)
        thr.start()
        Clock.schedule_interval(partial(self.check_job, thr), 1)

    def check_job(self, a_thread, what):
        if not a_thread.isAlive():
            self.close_button.disabled = False
            return False

    def on_transform(self, button):
        if not self.extract_list:
            self.show_popup('Empty result from Extract, please extract first!', 'Error')
            self.close_button.disabled = False
        else:
            self.show_popup('Starting Transform ...', 'Info')
            thr = threading.Thread(target=self.transform_thread)
            thr.start()
            Clock.schedule_interval(partial(self.check_job, thr), 1)

    def on_load(self, button):
        self.show_popup('Starting Load ...', 'Info')

    def extract_thread(self):
        self.extract_list = scrapper.scrap("http://www.booking.com/reviews/pl/hotel/cracowdayskrakow.html")

    def transform_thread(self):
        Transformer.transform_all(self.extract_list)

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


if __name__ == '__main__':
    ETLApp().run()
