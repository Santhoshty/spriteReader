import ebooklib
from ebooklib import epub

def read_epub_content(file_path):
    """
    Reads an EPUB file and extracts its text content.
    """
    try:
        # Read the EPUB file
        book = epub.read_epub(file_path)

        # Iterate through the items in the book to find document content
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Get the content of the document item (e.g., a chapter)
                content = item.get_content()
                # You can then process this content (e.g., print it, parse it with BeautifulSoup)
                print(f"Content from item '{item.get_id()}':")
                print(content.decode('utf-8')) # Decode bytes to string
                print("-" * 30)

    except Exception as e:
        print(f"Error reading EPUB file: {e}")

# Example usage:
#epub_file = 'theKingInYellow.epub' # Replace with your EPUB file path
#read_epub_content(epub_file)


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

# Example usage: Get the content of the first main chapter (index might vary, often starts at 0 or 1 for content)
epub_file = 'theKingInYellow.epub'
# You might need to experiment with the index. Some books start useful content at index 0, others later.
page_text = get_specific_item_by_index(epub_file, 1) 

if page_text:
    print(page_text[:1000] + "...") 
else:
    # If index 1 didn't work, try index 2
    page_text = get_specific_item_by_index(epub_file, 2)
    if page_text:
        print(page_text[:1000] + "...")
