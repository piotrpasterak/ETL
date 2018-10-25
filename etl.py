from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class ETLApp(App):
    title = "ETL Project"

    def build(self):
        buttonextract = Button(text="Extract", size_hint = (.2,.1), pos_hint ={'x': .1, 'y': .7})
        buttontransform = Button(text="Transform",size_hint = (.2,.1), pos_hint ={'x': .4, 'y': .7})
        buttonload = Button(text="Load", size_hint = (.2,.1), pos_hint ={'x': .7, 'y': .7})
        buttoncomplete = Button(text="Complete Process", size_hint = (.2,.1), pos_hint ={'x': .4, 'y': .5})
        layout = FloatLayout()
        layout.add_widget(buttonextract)
        layout.add_widget(buttontransform)
        layout.add_widget(buttonload)
        layout.add_widget(buttoncomplete)

        buttoncomplete.bind(on_press=self.onButtonPress)
        return layout

    def onButtonPress(self, button):
        layout = GridLayout(cols=1, padding=10)

        popupLabel = Label(text="Click for pop-up")
        closeButton = Button(text="Close the pop-up", size_hint = (.2,.1))

        layout.add_widget(popupLabel)

        layout.add_widget(closeButton)

        # Instantiate the modal popup and display

        popup = Popup(title='Confirmation', content=layout)

        # content=(Label(text='This is a demo pop-up')))

        popup.open()

        # Attach close button press with popup.dismiss action

        closeButton.bind(on_press=popup.dismiss)


if __name__ == '__main__':
    ETLApp().run()
