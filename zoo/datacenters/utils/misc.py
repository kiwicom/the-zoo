def email_to_full_name(email):
    """Convert email to full name of the owner."""
    return " ".join([part.title() for part in email.split("@")[0].split(".")])
