# Email Automation

A Python project for automating bulk email sending using Gmail SMTP, HTML templates, and recipient data from Excel/CSV files. Supports inline image embedding and personalized workshop registration emails.

## Features
- Load recipient data from `.xlsx` or `.csv`
- Use HTML templates with placeholders (`{name}`, `{date}`, `{time}`)
- Validate email addresses before sending
- Embed local images inline in the email body
- Send personalized bulk emails via Gmail SMTP

## Requirements
- Python 3.x
- pandas
- smtplib
- email.mime


