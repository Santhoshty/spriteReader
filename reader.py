


import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def get_text_from_item(item):
    """Helper function to extract clean text from an EpubHtml item."""
    soup = BeautifulSoup(item.get_body_content(), 'lxml')
    return soup.get_text(separator='\n', strip=True)

def get_specific_item_by_index(file_path, item_index):
    """
    Reads an EPUB file and returns the text of a specific item in the reading spine.
    Index 0 is typically the start of the book's main content.
    """
    try:
        book = epub.read_epub(file_path)
        
        # The 'spine' contains the ordered list of items in the reading order
        spine_items = [item[0] for item in book.spine]
        
        if item_index < 0 or item_index >= len(spine_items):
            print(f"Error: Item index {item_index} is out of range.")
            return None

        # Get the specific item reference (its ID) from the spine list
        item_id = spine_items[item_index]
        # Fetch the actual EpubHtml object using its ID
        target_item = book.get_item_with_id(item_id)
        
        if target_item:
            print(f"--- Extracting content from item ID: {item_id}, Name: {target_item.get_name()} ---")
            text_content = get_text_from_item(target_item)
            return text_content
        else:
            print(f"Item with ID {item_id} not found.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def parseText(file_path, index, trim_start, trim_end):
        # Call the function from your reader module
        book_content = get_specific_item_by_index(file_path, index)

        if book_content is None:
            book_content_trim = "Error: Could not load book content. Check your EPUB file or index number."
        else:
            book_content_trim = book_content[trim_start:trim_end] + "..."

        return book_content_trim