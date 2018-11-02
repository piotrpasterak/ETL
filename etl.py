from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from extract import scrapper


class ETLApp(App):
    title = "ETL Project"

    def build(self):
        button_extract = Button(text="Extract", size_hint = (.2,.1), pos_hint ={'x': .1, 'y': .7})
        button_transform = Button(text="Transform",size_hint = (.2,.1), pos_hint ={'x': .4, 'y': .7})
        button_load = Button(text="Load", size_hint = (.2,.1), pos_hint ={'x': .7, 'y': .7})
        button_complete = Button(text="Complete Process", size_hint = (.2,.1), pos_hint ={'x': .4, 'y': .5})
        layout = FloatLayout()
        layout.add_widget(button_extract)
        layout.add_widget(button_transform)
        layout.add_widget(button_load)
        layout.add_widget(button_complete)

        button_complete.bind(on_press=self.onButtonPress)
        button_extract.bind(on_press=self.on_extract)
        return layout

    def onButtonPress(self, button):
        layout = GridLayout(cols=1, padding=10)

        popupLabel = Label(text="Click for pop-up")
        closeButton = Button(text="Close the pop-up", size_hint = (.2,.1))

        layout.add_widget(popupLabel)

        layout.add_widget(closeButton)

        # Instantiate the modal popup and display

        popup = Popup(title='Confirmation', content=layout, )

        # content=(Label(text='This is a demo pop-up')))

        popup.open()

        # Attach close button press with popup.dismiss action

        closeButton.bind(on_press=popup.dismiss)

    def on_extract(self, button):
        scrapper.get_content("http://www.booking.com/reviews/pl/hotel/cracowdayskrakow.html")


if __name__ == '__main__':
    ETLApp().run()
