import os
import base64
from sendgrid import SendGridAPIClient, Attachment, FileContent, FileType, FileName, Disposition, ContentId
from sendgrid.helpers.mail import Mail


def send_email(sender, recipient, subject, html_content, base64_file, file_name, file_extension):
    """
    :sender: string
    :recipient: string
    :subject: string
    :html_content: string
    :base64_file: string
    :file_name: string
    :file_extension: string
    """
    msg = Mail(from_email=sender,
        to_emails=recipient,
        subject=subject,
        html_content=html_content)

    message_byte = base64_file.encode('ascii')

    with open("{}.{}".format(file_name,file_extension), "wb") as fh:
        fh.write(base64.decodebytes(message_byte))

    with open("{}.{}".format(file_name,file_extension), 'rb') as f:
        data = f.read()
        f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('application/{}'.format(file_extension))
        attachment.file_name = FileName("{}.{}".format(file_name,file_extension))
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('Example Content ID')
        msg.attachment = attachment

        sendgrid_client = SendGridAPIClient("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")
        response = sendgrid_client.send(msg)
    if response.status_code == 202:
        os.remove("{}.{}".format(file_name,file_extension))
        print("Email sent successfully")
    else:
        print("Email not sent")
