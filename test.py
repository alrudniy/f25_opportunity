import os

# Define the folder path
base_path = "templates/pages/partials"

# Define the files to create
files = [
    "s1_student.html",
    "s1_organization.html",
    "s1_administrator.html",
    "s2_student.html",
    "s2_organization.html",
    "s2_administrator.html",
    "s3_student.html",
    "s3_organization.html",
    "s3_administrator.html"
]

# Create the directory structure if it doesn't exist
os.makedirs(base_path, exist_ok=True)

# Create each file with a basic placeholder content
for file_name in files:
    file_path = os.path.join(base_path, file_name)
    with open(file_path, "w") as f:
        f.write(f"<h1>{file_name.replace('.html', '').replace('_', ' ').title()}</h1>\n")
        f.write("<p>This is a placeholder page.</p>\n")
    print(f"Created: {file_path}")

print("All files created successfully.")
