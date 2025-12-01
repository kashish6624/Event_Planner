from flask import Flask, render_template, request, send_file
from datetime import datetime
import os
import sys
import markdown

from crewai.crew import Crew
from crewai.crew import Agent

# Include src folder
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from event_planner.crew import EventPlanner

app = Flask(__name__)

OUTPUT_FILE = "event_plan.md"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
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
            return render_template("error.html", error=str(e))

        # Read generated file
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                markdown_text = f.read()
                html_text = markdown.markdown(markdown_text)
        else:
            html_text = "<p>No output generated.</p>"

        return render_template(
            "result.html",
            topic=topic,
            year=year,
            plan_html=html_text,
            download_link=OUTPUT_FILE
        )
    else:
        return render_template("index.html")


@app.route("/download")
def download():
    if os.path.exists(OUTPUT_FILE):
        return send_file(OUTPUT_FILE, as_attachment=True)
    else:
        return "File not found."


if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask, render_template, request, send_file
# import os
# import sys
# import re

# sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# from event_planner.crew import EventPlanner

# app = Flask(__name__)

# OUTPUT_FILE = "event_plan.md"

# def parse_md_to_sections(md_text):
#     """
#     Split markdown text into sections based on headings.
#     Each section becomes a dict with 'title' and 'content'.
#     """
#     sections = []
#     current_section = {"title": "Introduction", "content": ""}
#     for line in md_text.splitlines():
#         line = line.strip()
#         # Detect headings (Day 1, ## Phase, # etc.)
#         if re.match(r'^(#|##|Day\s+\d+)', line):
#             if current_section["content"]:
#                 sections.append(current_section)
#             current_section = {"title": line, "content": ""}
#         else:
#             if line:
#                 current_section["content"] += line + "\n"
#     if current_section["content"]:
#         sections.append(current_section)
#     return sections

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         # Get form data
#         topic = request.form.get("topic")
#         year = request.form.get("year")
#         location = request.form.get("location")
#         budget = request.form.get("budget")
#         attendees = request.form.get("attendees")
#         theme = request.form.get("theme")

#         inputs = {
#             "topic": topic,
#             "current_year": year,
#             "location": location,
#             "budget": budget,
#             "attendees": attendees,
#             "theme": theme
#         }

#         # Run CrewAI
#         try:
#             EventPlanner().crew().kickoff(inputs=inputs)
#         except Exception as e:
#             return f"An error occurred: {e}"

#         # Read output file
#         if os.path.exists(OUTPUT_FILE):
#             with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
#                 md_text = f.read()
#                 sections = parse_md_to_sections(md_text)
#         else:
#             sections = [{"title": "No output", "content": "No plan generated."}]

#         return render_template("result.html",
#                                topic=topic,
#                                year=year,
#                                sections=sections,
#                                download_link=OUTPUT_FILE)
#     else:
#         return render_template("index.html")


# @app.route("/download")
# def download():
#     if os.path.exists(OUTPUT_FILE):
#         return send_file(OUTPUT_FILE, as_attachment=True)
#     else:
#         return "File not found."


# if __name__ == "__main__":
#     app.run(debug=True)
