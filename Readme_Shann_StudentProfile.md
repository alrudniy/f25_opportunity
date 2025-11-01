# Student Profile Feature Breakdown

This document outlines the features and changes implemented for the Student Profile functionality. It is intended to assist with merging this feature branch into the main branch.

## 1. Feature Overview

A comprehensive, minimalistic, and functional Student Profile page has been created. This feature allows students to manage their personal information, academic details, and professional experiences.

### Key Features Implemented:
- **Profile Viewing:** A dedicated page for students to view their profile, including personal details, an "About Me" section, and a profile picture.
- **Experience Management:** Students can add their professional experiences (e.g., volunteer work, internships, career positions) through a dedicated form.
- **Profile Editing:** Students can edit their first name, last name, university, class year, "About Me" section, and upload a profile picture.
- **Logout Fix:** The logout functionality was corrected to use the required POST method, ensuring users can securely log out.
- **UI/UX:** The design is minimalistic, with a clean layout, generous whitespace, and a single-column, mobile-first approach.

## 2. Technical Implementation Details

### New Models (`pages/models.py`):
- `StudentProfile`: A one-to-one model linked to the `User` model. It stores the student's profile picture, university, class year, and an "About Me" text field.
- `Experience`: A model linked to `StudentProfile` to store professional experiences, including organization name, role, dates, description, and type.

### Forms (`pages/forms.py`):
- `StudentProfileForm`: For editing the student's profile information and uploading a profile picture.
- `ExperienceForm`: For adding or editing professional experiences, with built-in validation for required fields and date logic.

### Views & URLs (`pages/views.py`, `pages/urls.py`):
- New views and corresponding URL patterns were created to handle:
  - Viewing the student profile (`profile_student`).
  - Editing the student profile (`edit_profile_student`).
  - Adding a new experience (`add_experience`).

### Media File Handling:
- The project is now configured to handle user-uploaded media (like profile pictures).
- `MEDIA_URL` and `MEDIA_ROOT` have been configured in `opportunity_app/settings.py`.
- URL patterns in `opportunity_app/urls.py` have been updated to serve media files during development.

### Helper Scripts:
- `manage.sh`: A new shell script that simplifies running `manage.py` commands by automatically activating the virtual environment.
- `run-server.sh`: A shell script to easily start the Django development server within the virtual environment.

## 3. Instructions for Merging to Main Branch

When merging this branch, the following steps must be taken to ensure the application runs correctly.

### Step 1: Install New Dependencies
A new Python package, `Pillow`, was added to handle image uploads. Update the environment's dependencies by running:
```bash
# Activate your virtual environment first if not using a script
pip install -r requirements.txt
```

### Step 2: Apply Database Migrations
The `pages` app has new models and model changes that require database migrations. Run the following command:
```bash
./manage.sh migrate
```
This command will create the `pages_studentprofile` and `pages_experience` tables and add the new fields to the database.

### Step 3: Check Media Directory
The configuration expects a `media` directory in the project's root for storing uploaded files. Django will create this directory automatically when the first file is uploaded. Ensure your production environment has the correct permissions for this directory.

After completing these steps, the student profile feature will be fully integrated and functional.

## 4. Future Development & Next Steps

This section provides guidance for developers who may continue working on the student profile feature.

### Suggested Enhancements:
- **Edit/Delete Experiences:** Implement the functionality for students to edit and delete their existing experiences. This will require:
  - New views and URL patterns for editing and deleting an `Experience` object.
  - "Edit" and "Delete" buttons on each experience item in the profile template.
  - A confirmation step for the delete action to prevent accidental data loss.

- **Responsive Design:** While the current design is functional, it can be improved for tablet and desktop views. Consider implementing a multi-column layout on larger screens.

- **UI Feedback:** Enhance the user experience by adding toast notifications or on-page messages to confirm successful actions (e.g., "Profile updated successfully," "Experience added") or to display errors.

- **Advanced Experience Management:**
  - Add filtering or sorting options for experiences on the profile page (e.g., by type or date).
  - Implement the "auto-add" feature, where experiences are automatically created when a student completes an opportunity through the app.

- **Accessibility (a11y):** Conduct a full accessibility audit and implement ARIA attributes to ensure the profile page and forms are fully compliant with WCAG AA standards. This includes managing focus, announcing dynamic content changes to screen readers, and ensuring proper color contrast.
