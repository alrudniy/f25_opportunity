import uuid
import datetime

# In a real application, this would be your user database.
USERS = {
    "user@example.com": {"password": "old_password_hash"}
}

# In a real application, this would be a database table for password reset tokens.
RESET_TOKENS = {}


def request_password_reset(email):
    """
    Handles a user's request to reset their password.
    Generates a token and simulates sending an email.
    """
    if email not in USERS:
        return "Error: Email address not found."

    token = str(uuid.uuid4())
    expiry_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    RESET_TOKENS[token] = {"email": email, "expires": expiry_time}

    # In a real application, you would send an email here.
    reset_link = f"https://yourapp.com/reset-password?token={token}"
    print(f"Simulating email to {email}:")
    print(f"Please click this link to reset your password: {reset_link}")
    
    return "Password reset link has been sent to your email."


def reset_password(token, new_password):
    """
    Resets a user's password if a valid token is provided.
    """
    if token not in RESET_TOKENS:
        return "Error: Invalid or expired reset token."

    token_data = RESET_TOKENS[token]
    if datetime.datetime.now() > token_data["expires"]:
        del RESET_TOKENS[token]  # Clean up expired token
        return "Error: Invalid or expired reset token."

    user_email = token_data["email"]
    
    # In a real app, you would hash the new_password before saving.
    USERS[user_email]["password"] = new_password
    
    # Invalidate the token after use.
    del RESET_TOKENS[token]
    
    return "Your password has been reset successfully."


# --- Example Usage ---
if __name__ == "__main__":
    user_email_address = "user@example.com"
    
    # 1. User requests a password reset
    print(f"--- Step 1: Requesting password reset for {user_email_address} ---")
    print(request_password_reset(user_email_address))
    print("\n")
    
    # For demonstration, we'll grab the token that was "sent".
    # In a real app, the user would click a link in their email.
    reset_token = None
    for token, data in RESET_TOKENS.items():
        if data["email"] == user_email_address:
            reset_token = token
            break
            
    if reset_token:
        # 2. User provides the token and a new password
        print(f"--- Step 2: User uses the token to set a new password ---")
        new_user_password = "a_new_secure_password"
        print(reset_password(reset_token, new_user_password))
        print(f"User's password is now: {USERS[user_email_address]['password']}")
    else:
        print("Could not find reset token for demonstration.")
