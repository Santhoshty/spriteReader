from kivy.app import App
# Import ScrollView to handle large text
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
# Assuming 'reader' is the name of your file containing the get_specific_item_by_index function
from reader import get_specific_item_by_index
# Kivy usually requires you to import the Builder if you start touching default configurations
from kivy.lang import Builder

# Optional: Configuration for multi-line text wrapping in the Label
Builder.load_string('''
<ScrollableLabel>:
    text_size: self.width, None
    size_hint_y: None
    height: self.texture_size[1]
    padding: dp(10), dp(10)
''')

class ScrollableLabel(Label):
    pass

class MyKivyApp(App):
    def build(self):
        # Call the function from your reader module
        book_content = get_specific_item_by_index('theKingInYellow.epub', 2)
        
        # --- FIX 1: Ensure the content is a string, even if the index failed ---
        if book_content is None:
            text_to_display = "Error: Could not load book content. Check your EPUB file or index number."
        else:
            text_to_display = book_content

        # --- FIX 2: Use ScrollView for long text ---
        # 1. Create the main layout
        layout = BoxLayout(orientation='vertical')
        
        # 2. Create the label *inside* the ScrollView
        # Use our custom ScrollableLabel class which handles wrapping and height
        label = ScrollableLabel(
            text=text_to_display, 
            font_size='2sp' # Reduced font size to make more text fit initially
        )
        
        # 3. Create the ScrollView and add the label to it
        scroll_view = ScrollView(
            size_hint=(1, 1), 
            do_scroll_y=True, 
            do_scroll_x=False
        )
        scroll_view.add_widget(label)
        
        # 4. Add the ScrollView to the main layout
        layout.add_widget(scroll_view)
        
        return layout

if __name__ == '__main__':
    MyKivyApp().run()