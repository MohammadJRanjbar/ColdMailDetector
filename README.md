# ColdMailDetector
We all know that faculty members are often bombarded with emails, making it tough to keep up with important messages amidst the noise. To help ease this burden, I created a smart email classification tool designed specifically for academics.

This tool acts like a trusty assistant, sorting through incoming emails to identify which ones are genuinely important and which ones can be considered "cold mail." It checks if the sender is familiar with the recipient's work and whether they share research interests, giving faculty members a clearer picture of what deserves their attention.

By automatically forwarding the relevant emails to a dedicated inbox, this project saves valuable time and energy, allowing professors to focus more on what they love—teaching and research—without getting lost in their overflowing inboxes.
# Email Classifier and Forwarder

This script connects to your email account, fetches the latest emails, classifies them as "cold mail" or "not cold mail," and forwards the non-cold emails to your specified Gmail address. It uses OpenAI's API to classify the emails based on their subject and body content.

## Prerequisites

- Python 3.x
- Required libraries:
  - `imaplib`
  - `smtplib`
  - `email`
  - `yaml`
  - `json`
  - `openai`
  
You can install any missing packages using pip:

```bash
pip install openai pyyaml
```

## Configuration

Before running the script, you need to set up the `config.yml` file with your email credentials and OpenAI API key. Below is a sample configuration:

```yaml
email_credentials:
  username: "your_email@domain.com"  # Your email address
  password: "your_password"            # Your email password
  imap_server: "your_imap_server"      # IMAP server (e.g., mail.ut.ac.ir)
  smtp_server: "your_smtp_server"      # SMTP server (e.g., mail.ut.ac.ir)
  imap_port: 993                       # IMAP port (usually 993 for SSL)
  smtp_port: 465                       # SMTP port (usually 465 for SSL)
  gmail_address: "your_gmail_address@gmail.com"  # Your Gmail address for forwarding

openai:
  api_key: "your_openai_api_key"      # Your OpenAI API key

classification:
  prompt_template: "Classify the following email. Subject: {subject}. Body: {body}."  # Template for classification
  cold_response: "This email is classified as cold mail."  # Response if classified as cold mail
```

### Fill in the following placeholders:
- Replace `your_email@domain.com` with your actual email address.
- Replace `your_password` with your actual email password.
- Replace `your_imap_server` and `your_smtp_server` with the appropriate server addresses (e.g., `mail.ut.ac.ir`).
- Replace `your_gmail_address@gmail.com` with the Gmail address to which you want to forward the emails.
- Replace `your_openai_api_key` with your actual OpenAI API key.

## Running the Script

1. Ensure your Python environment is set up and the required libraries are installed.
2. Fill out the `config.yml` file with your credentials.
3. Run the script using the command:

   ```bash
   python your_script_name.py
   ```

The script will connect to your email account, check for new emails every 60 seconds, classify them, and forward non-cold emails to your specified Gmail address.

## Disclaimer

If you have any questions, need assistance, or would like to request updates to this script, please feel free to reach out. Your feedback is appreciated!

---

Thank you for using this Email Classifier and Forwarder!

