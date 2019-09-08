def sendmail(sender, receiver, subject, body, attachments=None):
    pass


def sharelinkbymail(user1, user2, link):
    subject: "share link from" + user1
    body = link

    sender = user1.email
    receiver = user1.email

    try:
        sendmail(sender, receiver, subject, body)
    except:
        pass
