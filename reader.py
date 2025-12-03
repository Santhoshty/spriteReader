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
epub_file = 'theKingInYellow.epub' # Replace with your EPUB file path
read_epub_content(epub_file)