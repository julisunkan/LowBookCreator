# Low-Content Book Creator

A Flask web application for generating KDP-ready low-content book PDFs (notebooks, planners, etc.).

## Features
- Single book PDF generation (custom header, page numbering, various layouts)
- Random journal prompts from SQLite
- KDP trim size validation
- Bulk PDF generation via CSV
- Random title generator
- PDF preview in browser
- Spine width calculator

## Tech Stack
- Backend: Flask
- PDF Generation: ReportLab
- Data Handling: Pandas
- Styling: Tailwind CSS

## Getting Started
The application is ready to run. Use the "Run App" button or execute:
```bash
python3 app.py
```
Visit `http://localhost:5000` to start creating your books.
