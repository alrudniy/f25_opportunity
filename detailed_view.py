from flask import Flask, render_template_string

app = Flask(__name__)

# -----------------------------
# Combined backend + frontend
# -----------------------------

@app.route("/")
def organization_detail():
    # Example organization data
    org = {
        "name": "Heritage Storytellers Club",
        "category": "Cultural Heritage",
        "description": (
            "The Heritage Storytellers Club is a student-run volunteer organization "
            "dedicated to preserving and celebrating local cultural traditions. "
            "Members partner with local community centers, libraries, and senior groups "
            "to gather oral histories, record narratives, and publish stories from elders and cultural leaders."
        ),
    }

    # Example events data
    events = [
        {
            "title": "Community Storytelling Night",
            "description": "Join us for an evening of storytelling and shared memories at the town library.",
            "start_time": "Oct 31, 2025, 6:00 PM",
            "hours_value": 2,
        },
        {
            "title": "Oral History Workshop",
            "description": "Learn how to interview local elders and record their stories.",
            "start_time": "Nov 7, 2025, 4:00 PM",
            "hours_value": 3,
        },
    ]

    # Render everything inline (no templates folder needed)
    html = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>{{ org.name }} - Opportunity App</title>
        <style>
          body {
            font-family: 'Segoe UI', Roboto, sans-serif;
            background-color: #00BCD4;
            margin: 0;
            padding: 0;
          }
          .page {
            max-width: 900px;
            margin: 40px auto;
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            overflow: hidden;
          }
          .header {
            display: flex;
            align-items: center;
            gap: 20px;
            padding: 30px;
            border-bottom: 1px solid #eee;
          }
          .header img {
            width: 120px;
            height: 120px;
            border-radius: 12px;
            object-fit: cover;
          }
          h1 { margin: 0; font-size: 1.8rem; color: #006064; }
          .category { color: #00838f; margin: 6px 0; font-weight: 600; }
          .description { color: #37474f; }
          .btn {
            background: #0097A7;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            cursor: pointer;
            margin-top: 10px;
          }
          .btn:hover { background: #00796B; }
          section {
            padding: 30px;
            border-bottom: 1px solid #eee;
          }
          section:last-child { border-bottom: none; }
          h2 {
            color: #004d40;
            margin-top: 0;
          }
          .mission {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
          }
          .mission-icon {
            width: 36px;
            height: 36px;
            background: #e0f2f1;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            color: #00796B;
          }
          .event {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 15px;
          }
          .event-icon {
            width: 36px;
            height: 36px;
            background: #e0f7fa;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            color: #00838F;
          }
          footer {
            text-align: center;
            color: #004d40;
            padding: 20px;
            font-size: 0.9rem;
          }
        </style>
      </head>
      <body>
        <div class="page">

          <!-- Header Section -->
          <div class="header">
            <img src="" alt="Club">
            <div>
              <h1>{{ org.name }}</h1>
              <div class="category">{{ org.category }}</div>
              <p class="description">{{ org.description }}</p>
              <button class="btn">Sign Up</button>
              <button class="btn" style="background:#00796B;">Follow</button>
            </div>
          </div>

          <!-- About Section -->
          <section>
            <h2>About Club</h2>
            <div class="mission">
              <div class="mission-icon">📖</div>
              <div>
                <strong>Club’s Mission</strong>
                <p>Dedicated to preserving local heritage through storytelling and creative projects.</p>
              </div>
            </div>
          </section>

          <!-- Events Section -->
          <section>
            <h2>Meeting Information / Events</h2>
            {% for e in events %}
              <div class="event">
                <div class="event-icon">👥</div>
                <div>
                  <strong>{{ e.title }}</strong>
                  <p>{{ e.description }}</p>
                  <p style="color:#607d8b;">📅 {{ e.start_time }} • ⏱ {{ e.hours_value }} hrs</p>
                </div>
              </div>
            {% endfor %}
          </section>

        </div>
        <footer>Opportunity App • © 2025</footer>
      </body>
    </html>
    """

    return render_template_string(html, org=org, events=events)


if __name__ == "__main__":
    app.run(debug=True)
