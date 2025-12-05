# Opportunity Hub

This is a simple web application designed to facilitate communication between organizers and students for volunteer opportunities. Organizers can post new opportunities, and both organizers and students can view opportunities and engage in discussions related to each opportunity.

## Features

-   **User Roles**: Basic login for Organizer and Student roles.
-   **Opportunity Management**: Organizers can post volunteer opportunities with a title and description.
-   **Messaging System**: Users can view and send messages within the context of specific volunteer opportunities.

## How to Run

1.  **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Flask application**:
    ```bash
    python app.py
    ```

6.  **Access the application**:
    Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

-   **Login**: On the homepage, you can select to log in as an 'Organizer' or a 'Student' to switch roles for demonstration purposes.
-   **View Opportunities**: Once logged in, navigate to "View Opportunities" to see available postings.
-   **Post Opportunity (Organizer)**: If logged in as an organizer, you will see a "Post New Opportunity" button on the opportunities page.
-   **Message System**: Click "Message Organizer / View Discussion" on an opportunity to access the messaging interface for that specific opportunity. You can send messages and see the ongoing discussion.
