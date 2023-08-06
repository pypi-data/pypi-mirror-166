import os
import base64
from sendgrid import SendGridAPIClient, Attachment, FileContent, FileType, FileName, Disposition, ContentId
from sendgrid.helpers.mail import Mail

class SendEmail(object):
    """
    :sender: string
    :recipient: string
    :subject: string
    :html_content: string
    :base64_file: string
    :file_name: string
    :file_extension: string
    """
    def __init__(self, sender, recipient, subject, html_content, base64_file, file_name, file_extension):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.html_content = html_content
        self.base64_file = base64_file
        self.file_name = file_name
        self.file_extension = file_extension

    def send_email(self):
        """Ensure that the Mail object is valid and send it.

        :from_email (string): The email address of the sender.
        :to_emails: list(obj)
        :subject: string
        :html_content: string
        """
        msg = Mail(from_email=self.sender,
               to_emails=self.recipient,
               subject=self.subject,
               html_content=self.html_content)

        message_byte = self.base64_file.encode('ascii')

        with open("{}.{}".format(self.file_name,self.file_extension), "wb") as fh:
            fh.write(base64.decodebytes(message_byte))

        with open("{}.{}".format(self.file_name,self.file_extension), 'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('application/{}'.format(self.file_extension))
        attachment.file_name = FileName("{}.{}".format(self.file_name,self.file_extension))
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('Example Content ID')
        msg.attachment = attachment

        sendgrid_client = SendGridAPIClient(os.environ.get("KEY"))
        response = sendgrid_client.send(msg)
        if response.status_code == 202:
            os.remove("{}.{}".format(self.file_name,self.file_extension))
            print("Email sent successfully")
        else:
            print("Email not sent")

    
    def __str__(self):
        """A JSON-ready string representation of this Mail object.

        :returns: A JSON-ready string representation of this Mail object.
        :rtype: string
        """
        return str(self.get())
