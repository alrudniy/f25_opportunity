from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def achievements():
    # Example data — replace with database later
    total_hours = 120
    total_orgs = 8

    milestones = [
        {
            "title": "Sign up for your first club",
            "description": "Join any school or community club and attend at least one meeting.",
            "completed": True
        },
        {
            "title": "Volunteer 10 hours",
            "description": "Reach a total of 10 hours of volunteering.",
            "completed": True
        },
        {
            "title": "Volunteer 25 hours",
            "description": "Hit 25 total volunteer hours.",
            "completed": True
        },
        {
            "title": "Volunteer 50 hours",
            "description": "Hit 50 volunteer hours.",
            "completed": False
        },
        {
            "title": "Volunteer 100 hours",
            "description": "Hit 100 volunteer hours.",
            "completed": False
        }
    ]

    return render_template(
        "achievements.html",
        total_hours=total_hours,
        total_orgs=total_orgs,
        milestones=milestones
    )

if __name__ == "__main__":
    app.run(debug=True)
