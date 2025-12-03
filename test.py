from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from reader import read_epub_content

class MyKivyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text=read_epub_content("theKingInYellow.epub"), font_size='30sp')
        layout.add_widget(label)
        return layout

if __name__ == '__main__':
    MyKivyApp().run()