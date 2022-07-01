import smtplib, ssl
import streamlit as st
from contextlib import contextmanager
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import wedding_utils
from wedding_utils import WeddingException


def get_google_credentials():
    """Get the username and password."""
    username = st.sidebar.text_input("Username", "adrien.g.treuille@gmail.com")
    is_valid = valid_email(username)
    WeddingException.assertion(is_valid, "Please enter a valid username.")
    password = st.sidebar.text_input("Password", type="password")
    WeddingException.assertion(password, "Please input a password.")
    return username, password


def valid_email(email: str) -> bool:
    """Returns true if this string represents a valid email address."""
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    return bool(re.fullmatch(regex, email))


@contextmanager
def gmail_service(username, password):
    port = 465
    smtp_server_domain_name = "smtp.gmail.com"

    ssl_context = ssl.create_default_context()
    service = smtplib.SMTP_SSL(smtp_server_domain_name, port, context=ssl_context)

    try:
        service.login(username, password)
        yield service

    finally:
        service.quit()


def main():
    username, password = get_google_credentials()

    recipient = st.text_input("To")
    is_valid = valid_email(recipient)
    WeddingException.assertion(is_valid, "Please enter a valid recipient email.")

    subject = st.text_input("Subject", key="subject")
    WeddingException.assertion(subject, "Subject cannot be empty")

    text_content = MIMEText(wedding_utils.get_email_text(), "plain")
    html_content = MIMEText(wedding_utils.get_email_html(), "html")

    with st.expander("Show text content"):
        st.code(text_content)

    with st.expander("Show HTML content"):
        st.code(html_content)

    if st.button("Send email"):
        with gmail_service(username, password) as service:
            mail = MIMEMultipart("alternative")
            mail["Subject"] = subject
            mail["From"] = username
            mail["To"] = recipient

            mail.attach(text_content)
            mail.attach(html_content)

            # # text_template = """
            # # Geekflare

            # # Hi {0},
            # # We are delighted announce that our website hits 10 Million views this month.
            # # """
            # # # html_template = """
            # # # <h1>Geekflare</h1>

            # # # <p>Hi {0},</p>
            # # # <p>We are delighted announce that our website hits <b>10 Million</b> views last month.</p>
            # # # """

            service.sendmail(username, recipient, mail.as_string())

            total_content = len(text_content) + len(html_content)
            st.success(f"Send mesage of len `{total_content}`b to `{recipient}`.")

    # mails = input("Enter emails: ").split()
    # subject = input("Enter subject: ")
    # content = input("Enter content: ")

    # mail = Mail()
    # mail.send(mails, subject, content)


if __name__ == "__main__":
    wedding_utils.run_main(main)
