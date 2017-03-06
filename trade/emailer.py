## sends email notifications
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Emailer():

	def __init__(self):
		self.server = smtplib.SMTP('smtp.gmail.com', 587)
		self.server.starttls()
		self.email = ""
		with open('./trade/email.key', 'r') as myfile:
			self.email = myfile.readline().rstrip()
			email_pass = myfile.readline().rstrip()
		self.server.login(self.email, email_pass)

	##emails signal
	def email_signal(self, signal):
		#Send the mail
		msg = MIMEMultipart()
		msg['From'] = self.email 
		msg['To'] = self.email
		msg['Subject'] = signal.type 
		 
		body = signal.summary() 
		msg.attach(MIMEText(body, 'plain'))
		self.server.sendmail(self.email, self.email, msg.as_string())
		
		print("Sent Email:")
		print(msg)

	def __del__(self):
		self.server.quit()


