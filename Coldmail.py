import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import yaml
import json
import openai

# Load configuration from config.yml
def load_config():
    with open("config.yml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

# Email credentials from config
username = config['email_credentials']['username']
password = config['email_credentials']['password']
imap_server = config['email_credentials']['imap_server']
smtp_server = config['email_credentials']['smtp_server']
imap_port = config['email_credentials']['imap_port']
smtp_port = config['email_credentials']['smtp_port']
gmail_address = config['email_credentials']['gmail_address']

# OpenAI API key from config
api_key = config['openai']['api_key']

# Connect to the IMAP server for University of Tehran
def connect_imap():
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(username, password)
    print("Connected to IMAP server.")
    return imap

# Connect to the University of Tehran SMTP
def connect_smtp():
    smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    smtp.login(username, password)
    return smtp

# Fetch emails from the inbox
def fetch_emails(imap):
    imap.select("inbox")
    result, data = imap.search(None, "ALL")  # Get all emails
    email_ids = data[0].split()
    emails = []
    
    for eid in email_ids[-10:]:  # Fetch the last 10 emails
        result, msg_data = imap.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        decoded_email = raw_email.decode('utf-8', errors='replace')
        msg = email.message_from_string(decoded_email)
        emails.append(msg)
    return emails

# Simple email classifier
def classify_email(subject, body):
    prompt_template = config['classification']['prompt_template']
    prompt = prompt_template.format(subject=subject, body=body)
    
    client = openai.OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that classifies emails as either 'cold mail' or 'not cold mail' based on the criteria. Return a JSON with a key 'cold_mail' with true or false value."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )
    
    answer = response.choices[0].message.content
    print(answer)
    return json.loads(answer)

# Forward email to Gmail
def forward_email(smtp, msg, category):
    forwarded_msg = MIMEMultipart()
    forwarded_msg["From"] = username
    forwarded_msg["To"] = gmail_address
    forwarded_msg["Subject"] = f"FWD: {msg['subject']} - {'Cold' if category['cold_mail'] else 'Not Cold'}"

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                forwarded_msg.attach(MIMEText(body, "plain"))
    else:
        body = msg.get_payload(decode=True).decode()
        forwarded_msg.attach(MIMEText(body, "plain"))

    smtp.sendmail(username, gmail_address, forwarded_msg.as_string())
    print("Email forwarded.")

# Main script
def main():
    imap = connect_imap()
    smtp = connect_smtp()

    try:
        while True:
            emails = fetch_emails(imap)
            for msg in emails:
                subject = decode_header(msg["subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                category = classify_email(subject, body)
                print(f"Classified '{subject}' as '{category}'")
                
                if category["cold_mail"] == False:
                    forward_email(smtp, msg, category)
                else:
                    print(config['classification']['cold_response'])

            print("Waiting for new emails...")
            time.sleep(60)  # Wait for 60 seconds before checking again

    except KeyboardInterrupt:
        print("Stopping email checker.")
    finally:
        # Close connections
        imap.logout()
        smtp.quit()

if __name__ == "__main__":
    main()
