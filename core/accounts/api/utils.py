from threading import Thread
from mail_templated import EmailMessage


class SendEmailAsThread(Thread):
    def __init__(self, mail_obj: EmailMessage):
        Thread.__init__(self)
        self.mail_obj = mail_obj

    def run(self):
        self.mail_obj.send()
