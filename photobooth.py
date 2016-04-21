# Import smtplib for the actual sending function

# Here are the email package modules we'll need
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import time

import datetime
from os.path import basename

import picamera
import smtplib
import os


import os
import time
import picamera # http://picamera.readthedocs.org/en/release-1.4/install2.html
import pygame
from signal import alarm, signal, SIGALRM, SIGKILL



GOOGLE_USERNAME = 'replace with gmail username'
GOOGLE_PASSWORD = 'replace with application-specific password for gmail'

transform_x = 640
transform_y = 480
offset_x = 80
offset_y = 0
def init_pygame():
    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.display.set_caption('Photo Booth Pics')
    pygame.mouse.set_visible(False) #hide the mouse cursor
    return pygame.display.set_mode(size, pygame.FULLSCREEN)

def show_image(image_path):
    screen = init_pygame()
    img=pygame.image.load(image_path)
    img = pygame.transform.scale(img,(transform_x,transform_y))
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()


def do_main():
    init_pygame()
    while True:
        email = raw_input("Please enter email: ")
        filename = str(datetime.datetime.now()) + "-" + email + ".jpg"
        take_picture(filename)
        try:
            send_email(email, filename)
        except:
            print "Bad email"
        os.system('clear')


def take_picture(filename):
    with picamera.PiCamera(sensor_mode=2) as camera:
        camera.resolution = (2592, 1944)
        # The following is equivalent
        # camera.resolution = camera.MAX_IMAGE_RESOLUTION
        camera.hflip = True
        camera.start_preview()
        time.sleep(5)
        camera.capture(filename)
        camera.stop_preview()

    print("Taking picture")


def send_email(to_address, filename):
    from_address = GOOGLE_USERNAME + "@gmail.com"
    msg = MIMEMultipart('mixed')
    msg['Subject'] = "Your photobooth pictures"
    msg['From'] = GOOGLE_USERNAME + "@gmail.com"
    msg['To'] = to_address
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




