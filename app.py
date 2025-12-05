from flask import Flask, render_template, request, redirect, url_for, session
import os
import uuid # For generating unique IDs for messages and opportunities

app = Flask(__name__)
app.secret_key = os.urandom(24) # A secret key for session management

# In-memory data stores (for simplicity; in a real app, this would be a database)
opportunities = []
messages = [] # Format: {'id': 'uuid', 'sender': 'user_role', 'recipient': 'user_role', 'opportunity_id': 'uuid', 'text': 'message_text'}
users = {
    'organizer1': {'role': 'organizer', 'name': 'Organizer One'},
    'student1': {'role': 'student', 'name': 'Student One'},
    'student2': {'role': 'student', 'name': 'Student Two'},
}
# A simple way to track current logged-in user for demonstration
current_user = None

@app.route('/')
def index():
    global current_user
    # Default to organizer for demonstration, or pick first student
    if not current_user:
        current_user = 'organizer1' # Or choose 'student1' to start as student

    user_role = users[current_user]['role']
    user_name = users[current_user]['name']
    return render_template('index.html', user_name=user_name, user_role=user_role, users=users)

@app.route('/login', methods=['POST'])
def login():
    global current_user
    username = request.form.get('username')
    if username in users:
        current_user = username
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('index'))


@app.route('/opportunities')
def list_opportunities():
    if not current_user:
        return redirect(url_for('index'))
    user_role = users[current_user]['role']
    return render_template('opportunities.html', opportunities=opportunities, user_role=user_role, current_user_id=current_user)

@app.route('/opportunities/new', methods=['GET', 'POST'])
def new_opportunity():
    if not current_user or users[current_user]['role'] != 'organizer':
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        opportunity_id = str(uuid.uuid4())
        opportunities.append({'id': opportunity_id, 'title': title, 'description': description, 'organizer_id': current_user})
        return redirect(url_for('list_opportunities'))
    return render_template('new_opportunity.html')

@app.route('/messages/<opportunity_id>', methods=['GET', 'POST'])
def view_messages(opportunity_id):
    if not current_user:
        return redirect(url_for('index'))

    related_opportunity = next((o for o in opportunities if o['id'] == opportunity_id), None)
    if not related_opportunity:
        return "Opportunity not found", 404

    # Filter messages relevant to this opportunity
    opportunity_messages = [m for m in messages if m.get('opportunity_id') == opportunity_id]

    if request.method == 'POST':
        message_text = request.form['message_text']
        sender_id = current_user
        sender_role = users[sender_id]['role']

        # Determine recipient based on who the other party for this opportunity is
        if sender_id == related_opportunity['organizer_id']:
            # Organizer is sending, so student(s) who showed interest would be recipients
            # For simplicity, we'll make this a general conversation for the opportunity.
            # In a real app, you'd target specific students.
            recipient_id = 'all_students_for_opp' # Placeholder for group chat or specific student in future
        else: # A student is sending
            recipient_id = related_opportunity['organizer_id']

        messages.append({
            'id': str(uuid.uuid4()),
            'sender_id': sender_id,
            'sender_name': users[sender_id]['name'],
            'recipient_id': recipient_id,
            'opportunity_id': opportunity_id,
            'text': message_text
        })
        return redirect(url_for('view_messages', opportunity_id=opportunity_id))

    return render_template('messages.html',
                           opportunity=related_opportunity,
                           messages=opportunity_messages,
                           current_user_id=current_user,
                           users=users)

if __name__ == '__main__':
    # Add some dummy data for testing
    opportunities.append({'id': str(uuid.uuid4()), 'title': 'Food Bank Volunteering', 'description': 'Help organize donations at the local food bank.', 'organizer_id': 'organizer1'})
    opportunities.append({'id': str(uuid.uuid4()), 'title': 'Park Cleanup', 'description': 'Spend a day cleaning up our community park.', 'organizer_id': 'organizer1'})

    app.run(debug=True)
