#메일 관련 라이브러리 임포트
#gmail을 사용해 보낼 경우
#msgRoot 안에 만들어진 대로 메일 폼이 전송
import smtplib,ssl

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

class SendEmail:
    def __init__(self):
        pass
    
    def email_send_message(self, sender, receiver_list, msgRoot):
        
        #print(msgRoot, type(msgRoot))
        #print(msgRoot.as_string())
        
        smtp=smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #아이디와 비밀번호를 넣으면 해당 아이디로 메일 발송 
        #아이디와 다른 사용자로 보내기는 불가능
        smtp.login("ID", "PW")
        smtp.sendmail(sender, receiver_list, msgRoot.as_string() )
        smtp.quit()