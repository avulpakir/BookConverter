import fitz  # PyMuPDF
import PyPDF2

def split_pdf_by_pages(input_pdf, output_pdf_odd, output_pdf_even):
    """
    Splits the input PDF into two PDFs: one with odd pages and another with even pages.
    """
    with open(input_pdf, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)

        # Create PDF writers for odd and even pages
        odd_writer = PyPDF2.PdfWriter()
        even_writer = PyPDF2.PdfWriter()

        # Loop through the pages and separate them into odd and even
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            if (i + 1) % 2 != 0:
                # Odd page (1, 3, 5, ...)
                odd_writer.add_page(page)
            else:
                # Even page (2, 4, 6, ...)
                even_writer.add_page(page)

        # Save the odd pages to a new PDF
        with open(output_pdf_odd, 'wb') as odd_outfile:
            odd_writer.write(odd_outfile)

        # Save the even pages to a new PDF
        with open(output_pdf_even, 'wb') as even_outfile:
            even_writer.write(even_outfile)

def merge_pdf_pages_left_to_right(input_pdf_path, output_pdf_path, outer_margin=10, inner_margin=5):
    """
    Merges PDF pages left to right with borders and margins.
    """
    doc = fitz.open(input_pdf_path)
    new_doc = fitz.open()

    for i in range(0, len(doc), 2):
        first_page_width = doc[0].rect.width
        first_page_height = doc[0].rect.height
        
        # Calculate width and height considering outer margins
        new_page_width = (first_page_width * 2) + outer_margin * 2 + inner_margin
        new_page_height = first_page_height + outer_margin * 2
        
        # Create a new page with the calculated dimensions
        new_page = new_doc.new_page(width=new_page_width, height=new_page_height)

        # Calculate positions for inserting pages considering margins
        left_x = outer_margin  # Left page starts after the outer margin
        right_x = left_x + first_page_width + inner_margin  # Right page starts after left page and inner margin

        # Insert first page on the left considering margins
        if i < len(doc):
            new_page.show_pdf_page(fitz.Rect(left_x, outer_margin, left_x + first_page_width, outer_margin + first_page_height), doc, i)

            # Draw border around the left page
            new_page.draw_rect(fitz.Rect(left_x, outer_margin, left_x + first_page_width, outer_margin + first_page_height), 
                               color=(0, 0, 0), width=2)  # Black border with thickness of 2

        # Insert second page on the right considering margins
        if i + 1 < len(doc):
            new_page.show_pdf_page(fitz.Rect(right_x, outer_margin, right_x + first_page_width, outer_margin + first_page_height), doc, i + 1)

            # Draw border around the right page
            new_page.draw_rect(fitz.Rect(right_x, outer_margin, right_x + first_page_width, outer_margin + first_page_height), 
                               color=(0, 0, 0), width=2)  # Black border with thickness of 2

    new_doc.save(output_pdf_path)
    new_doc.close()

def merge_pdf_pages_right_to_left(input_pdf_path, output_pdf_path, outer_margin=10, inner_margin=5):
    """
    Merges PDF pages right to left with borders and margins.
    """
    doc = fitz.open(input_pdf_path)
    new_doc = fitz.open()

    for i in range(0, len(doc), 2):
        first_page_width = doc[0].rect.width
        first_page_height = doc[0].rect.height
        
        # Calculate width and height considering outer margins
        new_page_width = (first_page_width * 2) + outer_margin * 2 + inner_margin
        new_page_height = first_page_height + outer_margin * 2
        
        # Create a new page with the calculated dimensions
        new_page = new_doc.new_page(width=new_page_width, height=new_page_height)

        # Calculate positions for inserting pages considering margins
        right_x = outer_margin  # Right page starts after the outer margin
        left_x = right_x + first_page_width + inner_margin  # Left page starts after right page and inner margin

        # Insert second page on the right considering margins (Right-to-Left)
        if i + 1 < len(doc):
            new_page.show_pdf_page(fitz.Rect(right_x, outer_margin, right_x + first_page_width, outer_margin + first_page_height), doc, i + 1)

            # Draw border around the right page
            new_page.draw_rect(fitz.Rect(right_x, outer_margin, right_x + first_page_width, outer_margin + first_page_height), 
                               color=(0, 0, 0), width=2)  # Black border with thickness of 2

        # Insert first page on the left considering margins (Right-to-Left)
        if i < len(doc):
            new_page.show_pdf_page(fitz.Rect(left_x, outer_margin, left_x + first_page_width, outer_margin + first_page_height), doc, i)

            # Draw border around the left page
            new_page.draw_rect(fitz.Rect(left_x, outer_margin, left_x + first_page_width, outer_margin + first_page_height), 
                               color=(0, 0, 0), width=2)  # Black border with thickness of 2

    new_doc.save(output_pdf_path)
    new_doc.close()

def merge_alternating_pages(pdf1_path, pdf2_path, output_path):
    """
    Merges two PDF files alternately.
    """
    reader1 = PyPDF2.PdfReader(pdf1_path)
    reader2 = PyPDF2.PdfReader(pdf2_path)
    writer = PyPDF2.PdfWriter()

    num_pages_pdf1 = len(reader1.pages)
    num_pages_pdf2 = len(reader2.pages)

    for i in range(max(num_pages_pdf1, num_pages_pdf2)):
        if i < num_pages_pdf1:
            writer.add_page(reader1.pages[i])  # Add a page from the first PDF (odd)
        if i < num_pages_pdf2:
            writer.add_page(reader2.pages[i])  # Add a page from the second PDF (even)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

def main():
    input_pdf = 'input.pdf'           # Input PDF file path
    output_pdf_odd = 'odd_pages.pdf'   # Output file for odd pages
    output_pdf_even = 'even_pages.pdf'  # Output file for even pages
    merged_output_path = 'merged.pdf'   # Final merged output path

    # Step 1: Split input PDF into odd and even pages
    split_pdf_by_pages(input_pdf, output_pdf_odd, output_pdf_even)

    # Step 2: Merge odd pages into a single PDF (left to right)
    merge_pdf_pages_left_to_right(output_pdf_odd, 'merged_odd.pdf')

    # Step 3: Merge even pages into a single PDF (right to left)
    merge_pdf_pages_right_to_left(output_pdf_even, 'merged_even.pdf')

    # Step 4: Merge the two resulting PDFs alternately starting with odd pages
    merge_alternating_pages('merged_odd.pdf', 'merged_even.pdf', merged_output_path)

if __name__ == "__main__":
    main()
