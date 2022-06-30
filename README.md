# wedding

Code supporting our wedding

### Objective

1. Send beautifully formatted wedding inviations
2. That aren't classified as spam

### Todo

- New architecture
    - Parameters are stored in the sesso
    - Get each files to work in succession
        - `./wedding_utils.py`
        - `./pages/03_test.py`
        - `./pages/02_send_emails.py`
        - `./pages/01_create_html.py`
        - `./wedding.py`
- Send a test html email
    - Load the image in
    - Send the email to that test email website
    - Send some test emails to various people
    - Verify that it's not going ot people's spam folders
- Send out all the emails
    - Create a CSV of all the emails
    - Send them out proplery

### Utility Functions

- `get_email_text()`
- `get_email_html()`

### Session State Parameters

- `image_input`
- `google_username`
- `google_password`
