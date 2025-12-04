from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
# Import the Button widget
from kivy.uix.button import Button

from kivy.lang import Builder
from kivy.metrics import dp

from reader import parseText, get_specific_item_by_index



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
        self.current_end = 800
        self.offset_step = 800
        self.epub_file_name = 'theKingInYellow.epub'
        self.item_index = 3 
        # Calculate the total size of the current book item
        self.size = len(get_specific_item_by_index(self.epub_file_name, self.item_index))

        # 1. Create the main layout (Vertical for overall app structure)
        main_layout = BoxLayout(orientation='vertical')
        
        # 2. Setup the content Label and ScrollView
        initial_text = parseText(self.epub_file_name, self.item_index, self.current_start, self.current_end)

        self.label = ScrollableLabel(
            text=initial_text, 
            font_size='24sp'
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
        self.left_button = Button(text='Previous Page', on_press=self.prev_page)
        # Right Button
        self.right_button = Button(text='Next Page', on_press=self.next_page)
        
        button_layout.add_widget(self.left_button)
        button_layout.add_widget(self.right_button)

        # Initially disable the 'Previous Page' button since we start at page 1
        self.left_button.disabled = True

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
        if self.root: # Ensure root is available (it is after build finishes)
             # Accessing root children by index can be fragile. A better way 
             # is to store a reference to the scroll_view itself: self.scroll_view = scroll_view
            pass # Skipping scroll reset for brevity, focus on buttons

        # *** This is the core logic change ***
        # Re-evaluate the state of BOTH buttons after ANY text update

        # Enable the 'Previous' button if we are past the start point
        self.left_button.disabled = self.current_start == 0

        # Enable the 'Next' button if we haven't reached the end yet
        # Using >= size check is safer when dealing with partial pages
        self.right_button.disabled = self.current_end >= self.size


    def next_page(self, instance):
        """Handler for the Right (Next) button."""
        # Only proceed if we are not at the very end (extra safety check)
        if self.current_end < self.size:
            # Increment the offsets
            self.current_start += self.offset_step
            self.current_end += self.offset_step
            self.update_text_display()
        
        # Note: The disabling logic is now consolidated in update_text_display()


    def prev_page(self, instance):
        """Handler for the Left (Previous) button."""
        # Only proceed if we are not at the beginning
        if self.current_start > 0:
            # Decrement the offsets
            self.current_start -= self.offset_step
            self.current_end -= self.offset_step
            # Ensure start doesn't become negative
            if self.current_start < 0:
                self.current_start = 0
            self.update_text_display()


if __name__ == '__main__':
    Reader().run()