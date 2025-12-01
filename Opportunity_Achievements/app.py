from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def achievements():
    # Example data – you can later pull this from a database
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
            "description": "Hit 50 total volunteer hours.",
            "completed": False
        },
        {
            "title": "Volunteer at 3 organizations",
            "description": "Help out at three different organizations.",
            "completed": False
        },
        {
            "title": "Lead an event",
            "description": "Organize or lead at least one volunteer event.",
            "completed": False
        },
    ]

    total_milestones = 100   # your target number
    completed_milestones = sum(1 for m in milestones if m["completed"])

    return render_template(
        "achievements.html",
        total_hours=total_hours,
        total_orgs=total_orgs,
        milestones=milestones,
        completed_milestones=completed_milestones,
        total_milestones=total_milestones,
    )


if __name__ == "__main__":
    app.run(debug=True)
