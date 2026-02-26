import uuid
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch
from reportlab.lib.units import inch as inch_unit

def validate_trim_size(width, height):
    allowed = [(5, 8), (5.5, 8.5), (6, 9), (7, 10), (8, 10), (8.5, 11)]
    return (float(width), float(height)) in allowed

def generate_pdf(filename, pages, header, trim_width, trim_height, layout='lines', prompts=None, show_page_numbers=True):
    width = float(trim_width) * inch_unit
    height = float(trim_height) * inch_unit
    
    c = canvas.Canvas(filename, pagesize=(width, height))
    
    margin = 0.5 * inch_unit
    line_spacing = 0.25 * inch_unit
    
    for p in range(1, int(pages) + 1):
        # Header
        if header:
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(width / 2, height - 0.75 * inch_unit, header)
            
        # Prompt
        if prompts and (p-1) < len(prompts):
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(margin, height - 1.25 * inch_unit, f"Prompt: {prompts[p-1]}")
            top_y = height - 1.5 * inch_unit
        else:
            top_y = height - 1.0 * inch_unit
            
        # Layout
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        bottom_y = margin
        
        if layout == 'lines':
            y = top_y
            while y > bottom_y:
                c.line(margin, y, width - margin, y)
                y -= line_spacing
        elif layout == 'dot_grid':
            dot_spacing = 0.25 * inch_unit
            y = top_y
            while y > bottom_y:
                x = margin
                while x < width - margin:
                    c.circle(x, y, 0.5, fill=1)
                    x += dot_spacing
                y -= dot_spacing
        elif layout == 'graph':
            grid_spacing = 0.125 * inch_unit
            y = top_y
            while y > bottom_y:
                c.line(margin, y, width - margin, y)
                y -= grid_spacing
            x = margin
            while x < width - margin:
                c.line(x, top_y, x, bottom_y)
                x += grid_spacing

        # Page Numbering
        if show_page_numbers:
            c.setFont("Helvetica", 8)
            c.drawCentredString(width / 2, 0.3 * inch_unit, str(p))
            
        c.showPage()
        
    c.save()

from PIL import Image, ImageOps, ImageFilter

def process_coloring_image(image_path, output_path, outline=True):
    with Image.open(image_path) as img:
        img = img.convert('L') # Grayscale
        if outline:
            # Simple edge detection for coloring book effect
            img = img.filter(ImageFilter.FIND_EDGES)
            img = ImageOps.invert(img)
            # Enhance contrast
            img = ImageOps.autocontrast(img, cutoff=2)
        img.save(output_path)

def generate_coloring_pdf(filename, image_paths, trim_width, trim_height):
    width = float(trim_width) * inch_unit
    height = float(trim_height) * inch_unit
    c = canvas.Canvas(filename, pagesize=(width, height))
    
    for img_path in image_paths:
        # Calculate aspect ratio to fit image on page
        with Image.open(img_path) as img:
            img_w, img_h = img.size
            img_aspect = img_w / img_h
            page_aspect = width / height
            
            if img_aspect > page_aspect:
                draw_w = width - 1 * inch_unit
                draw_h = draw_w / img_aspect
            else:
                draw_h = height - 1 * inch_unit
                draw_w = draw_h * img_aspect
                
            x = (width - draw_w) / 2
            y = (height - draw_h) / 2
            c.drawImage(img_path, x, y, width=draw_w, height=draw_h)
            c.showPage()
    c.save()
