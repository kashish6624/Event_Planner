from flask import Flask, render_template, request, send_file, make_response
import os
import sys
import re
from weasyprint import HTML

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from event_planner.crew import EventPlanner

app = Flask(__name__)

OUTPUT_FILE = "event_plan.md"

# --- Helper function to parse Markdown into sections ---
def parse_md_to_sections(md_text):
    """
    Split markdown text into sections based on headings.
    Each section becomes a dict with 'title' and 'content'.
    """
    sections = []
    current_section = {"title": "Introduction", "content": ""}
    for line in md_text.splitlines():
        line = line.strip()
        # Detect headings (Day 1, ## Phase, # etc.)
        if re.match(r'^(#|##|Day\s+\d+)', line):
            if current_section["content"]:
                sections.append(current_section)
            current_section = {"title": line, "content": ""}
        else:
            if line:
                # Optionally add emoji/icons based on keywords
                emoji_line = line
                if "DJ" in line or "music" in line: emoji_line = "🎤 " + line
                elif "cater" in line or "food" in line: emoji_line = "🍴 " + line
                elif "venue" in line: emoji_line = "🏢 " + line
                elif "decor" in line or "theme" in line: emoji_line = "🎨 " + line
                elif "invite" in line or "guests" in line: emoji_line = "✉️ " + line
                elif "photograph" in line or "photo" in line: emoji_line = "📸 " + line
                current_section["content"] += emoji_line + "\n"
    if current_section["content"]:
        sections.append(current_section)
    return sections

# --- Home route ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        topic = request.form.get("topic")
        year = request.form.get("year")
        location = request.form.get("location")
        budget = request.form.get("budget")
        attendees = request.form.get("attendees")
        theme = request.form.get("theme")

        inputs = {
            "topic": topic,
            "current_year": year,
            "location": location,
            "budget": budget,
            "attendees": attendees,
            "theme": theme
        }

        # Run CrewAI
        try:
            EventPlanner().crew().kickoff(inputs=inputs)
        except Exception as e:
            return f"An error occurred: {e}"

        # Read output file
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                md_text = f.read()
                sections = parse_md_to_sections(md_text)
        else:
            sections = [{"title": "No output", "content": "No plan generated."}]

        return render_template("result.html",
                               topic=topic,
                               year=year,
                               sections=sections,
                               download_link=OUTPUT_FILE)
    else:
        return render_template("index.html")

# --- Markdown download ---
@app.route("/download")
def download():
    if os.path.exists(OUTPUT_FILE):
        return send_file(OUTPUT_FILE, as_attachment=True)
    else:
        return "File not found."

# --- PDF download route ---
@app.route("/download_pdf")
def download_pdf():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            md_text = f.read()
            sections = parse_md_to_sections(md_text)

        # Generate simple HTML for PDF
        html_content = "<html><head><style>"
        html_content += """
            body { font-family: Arial; padding: 20px; }
            h2 { color: #4e73df; }
            .section { border-left: 6px solid #4e73df; padding: 10px; margin-bottom: 15px; }
            .section h3 { margin: 0; }
            .section p { white-space: pre-line; }
        """
        html_content += "</style></head><body>"
        html_content += f"<h2>Event Plan</h2>"
        for sec in sections:
            html_content += f"<div class='section'><h3>{sec['title']}</h3><p>{sec['content']}</p></div>"
        html_content += "</body></html>"

        pdf_file = HTML(string=html_content).write_pdf()
        response = make_response(pdf_file)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=event_plan.pdf'
        return response
    else:
        return "No plan generated."

# --- Run Flask app ---
if __name__ == "__main__":
    app.run(debug=True)

