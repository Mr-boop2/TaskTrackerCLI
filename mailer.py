from email.message import EmailMessage
import smtplib

def autoMail(emailContent): 
    testMsg = EmailMessage()
    testMsg.set_content(emailContent)
    testMsg["Subject"] = "Mailed Via Python"


    #Put the SMTP server for the desired domain  EX: outlook, gmail 
    host = "smtp.gmail.com"
    port = 587

    #Initiate your own FROM and TO emails 
    fromEmail = "******"
    toEmail = "*****"


    #Must be password app token for the FROM Email if using gmail. 
    password = "*****" 
    smtp = smtplib.SMTP(host,port)

    status_code, response = smtp.ehlo()
    print(f"[*] Echoing the server: {status_code} {response}")

    status_code, response = smtp.starttls()
    print(f"[*] Starting TLS connection: {status_code} {response}")

    status_code, response = smtp.login(fromEmail,password)
    print(f"[*] Logging in: {status_code} {response}")

    smtp.send_message(testMsg,fromEmail, toEmail)
    smtp.quit()
