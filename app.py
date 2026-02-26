import os
import uuid
import pandas as pd
from flask import Flask, render_template, request, send_from_directory, jsonify, redirect, url_for
from database import get_db_connection, init_db
from utils import generate_pdf, validate_trim_size, calculate_spine_width, process_coloring_image, generate_coloring_pdf
from models import generate_random_title
import zipfile

app = Flask(__name__)
EXPORTS_DIR = 'exports'

if not os.path.exists(EXPORTS_DIR):
    os.makedirs(EXPORTS_DIR)

# Initialize DB on start
init_db()

@app.route('/coloring', methods=['GET', 'POST'])
def coloring():
    if request.method == 'POST':
        images = request.files.getlist('images')
        trim = request.form.get('trim', '8.5x11').split('x')
        width, height = float(trim[0]), float(trim[1])
        outline = 'outline_effect' in request.form
        
        processed_paths = []
        for img in images:
            if img.filename == '': continue
            ext = os.path.splitext(img.filename)[1]
            temp_name = f"temp_{uuid.uuid4()}{ext}"
            temp_path = os.path.join(EXPORTS_DIR, temp_name)
            img.save(temp_path)
            
            proc_name = f"proc_{uuid.uuid4()}.png"
            proc_path = os.path.join(EXPORTS_DIR, proc_name)
            process_coloring_image(temp_path, proc_path, outline=outline)
            processed_paths.append(proc_path)
            os.remove(temp_path)
            
        if processed_paths:
            filename = f"coloring_{uuid.uuid4()}.pdf"
            filepath = os.path.join(EXPORTS_DIR, filename)
            generate_coloring_pdf(filepath, processed_paths, width, height)
            
            # Cleanup processed images
            for p in processed_paths:
                try: os.remove(p)
                except: pass
                
            return redirect(url_for('preview', filename=filename))
            
    return render_template('coloring.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notebook', methods=['GET', 'POST'])
def notebook():
    if request.method == 'POST':
        pages = request.form.get('pages', 100)
        header = request.form.get('header', '')
        trim = request.form.get('trim', '6x9').split('x')
        width, height = float(trim[0]), float(trim[1])
        layout = request.form.get('layout', 'lines')
        show_nums = 'show_page_numbers' in request.form
        category = request.form.get('category', 'None')
        
        prompts = []
        if category != 'None':
            conn = get_db_connection()
            rows = conn.execute('SELECT prompt FROM prompts WHERE category = ? ORDER BY RANDOM() LIMIT ?', (category, pages)).fetchall()
            prompts = [row['prompt'] for row in rows]
            conn.close()
            
        filename = f"{uuid.uuid4()}.pdf"
        filepath = os.path.join(EXPORTS_DIR, filename)
        
        generate_pdf(filepath, pages, header, width, height, layout, prompts, show_nums)
        return redirect(url_for('preview', filename=filename))
        
    return render_template('notebook.html')

@app.route('/planner', methods=['GET', 'POST'])
def planner():
    # Similar to notebook for this starter, can be customized further
    return notebook()

@app.route('/bulk', methods=['GET', 'POST'])
def bulk():
    if request.method == 'POST':
        file = request.files.get('csv_file')
        if file and file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            zip_filename = f"bulk_{uuid.uuid4()}.zip"
            zip_path = os.path.join(EXPORTS_DIR, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for _, row in df.iterrows():
                    pdf_name = f"{uuid.uuid4()}.pdf"
                    pdf_path = os.path.join(EXPORTS_DIR, pdf_name)
                    generate_pdf(
                        pdf_path, 
                        row.get('pages', 100), 
                        row.get('header', ''), 
                        row.get('trim_width', 6), 
                        row.get('trim_height', 9)
                    )
                    zipf.write(pdf_path, arcname=f"{row.get('title', 'book')}_{pdf_name}")
            
            return redirect(url_for('download_file', filename=zip_filename))
    return render_template('bulk.html')

@app.route('/preview/<filename>')
def preview(filename):
    return render_template('preview.html', filename=filename)

@app.route('/exports/<filename>')
def download_file(filename):
    return send_from_directory(EXPORTS_DIR, filename)

@app.route('/generate-title')
def api_generate_title():
    return jsonify({'title': generate_random_title()})

@app.route('/generate-prompts')
def api_generate_prompts():
    category = request.args.get('category', 'Gratitude')
    limit = int(request.args.get('limit', 5))
    conn = get_db_connection()
    rows = conn.execute('SELECT prompt FROM prompts WHERE category = ? ORDER BY RANDOM() LIMIT ?', (category, limit)).fetchall()
    prompts = [row['prompt'] for row in rows]
    conn.close()
    return jsonify({'prompts': prompts})

@app.route('/spine-calculator')
def spine_calculator():
    pages = request.args.get('pages', 0)
    width = calculate_spine_width(pages)
    return jsonify({'spine_width': width})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
