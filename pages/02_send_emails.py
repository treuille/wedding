import smtplib, ssl
import streamlit as st
from contextlib import contextmanager
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class WeddingException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    @classmethod
    def run_main(cls, func):
        """Runs a function, extracting WeddingExceptions
        and displaying them specially."""
        try:
            func()
        except cls as wedding_exception:
            st.error(wedding_exception.msg)

    @classmethod
    def assertion(cls, condition: bool, msg: str):
        if not condition:
            raise cls(msg)


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
    message = st.text_area("Message")
    WeddingException.assertion(message, "Please enter a message.")

    if st.button("Send email"):
        with gmail_service(username, password) as service:
            mail = MIMEMultipart("alternative")
            mail["Subject"] = "this is a test"
            mail["From"] = username
            mail["To"] = recipient

            text_content = MIMEText(message, "plain")

            # text_template = """
            # Geekflare

            # Hi {0},
            # We are delighted announce that our website hits 10 Million views this month.
            # """
            # # html_template = """
            # # <h1>Geekflare</h1>

            # # <p>Hi {0},</p>
            # # <p>We are delighted announce that our website hits <b>10 Million</b> views last month.</p>
            # # """

            # html_content = MIMEText(html_template.format(email.split("@")[0]), "html")

            mail.attach(text_content)

            # mail.attach(html_content)

            service.sendmail(username, recipient, mail.as_string())
            st.success(f"Send mesage of len `{len(message)}` to `{recipient}`.")

            # st.write(type(service))
            # st.write(dir(service))
            # st.help(service.sendmail)

    # mails = input("Enter emails: ").split()
    # subject = input("Enter subject: ")
    # content = input("Enter content: ")

    # mail = Mail()
    # mail.send(mails, subject, content)


if __name__ == "__main__":
    WeddingException.run_main(main)
