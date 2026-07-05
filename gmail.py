import os
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

sender = "ahamedairf251@gmail.com"
password = "ztjr ospi akch bmcp"   # App password

# Detect the input data file

if os.path.exists("email.csv"):
    data_file = "email.csv"

else:
    raise FileNotFoundError(
        "Missing data file. Expected registrations.xlsx, email.xlsx or email.csv in the current directory."
    )

# Load data
if data_file.lower().endswith(".csv"):
    try:
        data = pd.read_csv(data_file)
    except Exception:
        data = pd.read_excel(data_file)
else:
    data = pd.read_excel(data_file)

if data.empty:
    raise ValueError("The data file is empty.")

# Detect the HTML template file
if os.path.exists("template.html"):
    template_file = "template.html"
elif os.path.exists("content.html"):
    template_file = "content.html"
else:
    raise FileNotFoundError(
        "Missing HTML template. Expected template.html or content.html in the current directory."
    )

with open(template_file, "r", encoding="utf-8") as f:
    template = f.read()

columns = [str(col).strip().lower() for col in data.columns]

def find_column(names):
    for candidate in names:
        for idx, col in enumerate(columns):
            if candidate in col:
                return data.columns[idx]
    raise KeyError(f"Could not find a column for: {names}")

name_col = find_column(["name"])
email_col = find_column(["email", "e-mail"])
date_col = find_column(["date", "day", "workshop day", "workshopdate"])
time_col = find_column(["time", "workshop time", "workshoptime"])

def is_valid_email(address):
    if not address or address.lower() == "nan":
        return False
    if "@" not in address or "," in address or address.count("@") != 1:
        return False
    local, domain = address.split("@", 1)
    return bool(local.strip()) and bool(domain.strip()) and "." in domain

# Send emails
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)

    for _, row in data.iterrows():
        name = str(row[name_col]).strip()
        receiver = str(row[email_col]).strip()
        date_val = row[date_col]
        time_val = row[time_col]

        # Format date nicely
        if pd.api.types.is_datetime64_any_dtype(data[date_col]):
            date = pd.to_datetime(date_val).strftime("%Y-%m-%d")
        else:
            date = str(date_val).split()[0]

        # Format time nicely
        if pd.api.types.is_datetime64_any_dtype(data[time_col]):
            time = pd.to_datetime(time_val).strftime("%I:%M %p")
        else:
            time = str(time_val).split()[0]

        if not is_valid_email(receiver):
            print(f"Skipping invalid email: {receiver}")
            continue

        # HTML content with inline image reference
        html_content = template.format(
            name=name,
            date=date,
            time=time
        ) + """
        <p>You are enrolled in the <b>Cyber Security Fundamentals Course</b>. Please be on time!</p>
        
        """

        # Create multipart message
        msg = MIMEMultipart("related")
        msg["Subject"] = "Cyber Security Workshop Registration"
        msg["From"] = sender
        msg["To"] = receiver

        # Attach HTML
        msg.attach(MIMEText(html_content, "html"))

        # Attach local image
        with open("cyber.png", "rb") as img_file:   # replace with your image file
            img = MIMEImage(img_file.read())
            img.add_header("Content-ID", "<cyber_image>")
            msg.attach(img)
 
        # Send email
        server.sendmail(sender, receiver, msg.as_string())
        print(f"Mail sent successfully to {receiver}")
