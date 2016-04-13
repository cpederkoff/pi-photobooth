# Import smtplib for the actual sending function

# Here are the email package modules we'll need
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

import time
import picamera
import smtplib

from os.path import basename

GOOGLE_USERNAME = 'replace with gmail username'
GOOGLE_PASSWORD = 'replace with application-specific password for gmail'

def do_main():
    while True:
        take_picture()
        email = raw_input("Please enter email: ")
        send_email(email, "foo.png")


def take_picture():
    with picamera.PiCamera(sensor_mode=2) as camera:
        camera.resolution = (2592, 1944)
        # The following is equivalent
        # camera.resolution = camera.MAX_IMAGE_RESOLUTION
        camera.hflip = True
        camera.start_preview()
        time.sleep(15)
        # camera.stop_preview()
        camera.capture('foo.jpg')
    print("Taking picture")


def send_email(to_address, filename):
    from_address = GOOGLE_USERNAME + "@gmail.com"
    msg = MIMEMultipart(
        From=from_address,
        To=to_address,
        Date=formatdate(localtime=True),
        Subject="subject"
    )
    with open(filename, "rb") as fil:
        msg.attach(MIMEApplication(
            fil.read(),
            Content_Disposition='attachment; filename="%s"' % basename(filename),
            Name=basename(filename)
        ))

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(GOOGLE_USERNAME, GOOGLE_PASSWORD)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()


if __name__ == '__main__':
    do_main()
