from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button


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
        return layout


if __name__ == '__main__':
    ETLApp().run()
