from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
# Import the Button widget
from kivy.uix.button import Button

from kivy.lang import Builder
from kivy.metrics import dp

from reader import parseText


# Optional: Configuration for multi-line text wrapping in the Label
Builder.load_string('''
<ScrollableLabel>:
    # Ensure text wraps within the width of the ScrollView/parent container
    text_size: self.width, None 
    size_hint_y: None
    height: self.texture_size[1]
    padding: dp(10), dp(10)
    # Added vertical alignment top for better display in a scroll view
    valign: 'top' 
''')

class ScrollableLabel(Label):
    pass

class Reader(App):
    def build(self):
        # Initialize navigation state variables
        self.current_start = 0
        self.current_end = 1000
        self.offset_step = 1000
        self.epub_file_name = 'theKingInYellow.epub'
        self.item_index = 3 # The second argument to parseText

        # 1. Create the main layout (Vertical for overall app structure)
        main_layout = BoxLayout(orientation='vertical')
        
        # 2. Setup the content Label and ScrollView
        initial_text = parseText(self.epub_file_name, self.item_index, self.current_start, self.current_end)

        self.label = ScrollableLabel(
            text=initial_text, 
            font_size='24sp' # Adjusted font size to fit more text on a mobile screen
        )
        
        scroll_view = ScrollView(
            size_hint=(1, 1), 
            do_scroll_y=True, 
            do_scroll_x=False
        )
        scroll_view.add_widget(self.label)
        
        # 3. Create the navigation buttons layout (Horizontal)
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        # Left Button
        left_button = Button(text='Previous (-1000)', on_press=self.prev_page)
        # Right Button
        right_button = Button(text='Next (+1000)', on_press=self.next_page)
        
        button_layout.add_widget(left_button)
        button_layout.add_widget(right_button)

        # 4. Add widgets to the main layout
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(button_layout)

        return main_layout
    
    def update_text_display(self):
        """Fetches new text and updates the label."""
        new_text = parseText(
            self.epub_file_name, 
            self.item_index, 
            self.current_start, 
            self.current_end
        )
        self.label.text = new_text
        # Optional: Reset scroll position to the top for the new page
        self.root.children[1].scroll_y = 1 

    def next_page(self, instance):
        """Handler for the Right (Next) button."""
        # Increment the offsets
        self.current_start += self.offset_step
        self.current_end += self.offset_step
        self.update_text_display()

    def prev_page(self, instance):
        """Handler for the Left (Previous) button."""
        # Decrement the offsets, ensuring start doesn't go below zero
        if self.current_start > 0:
            self.current_start -= self.offset_step
            self.current_end -= self.offset_step
            # Ensure start doesn't become negative if it was less than 1000 previously
            if self.current_start < 0:
                self.current_start = 0
            self.update_text_display()


if __name__ == '__main__':
    Reader().run()