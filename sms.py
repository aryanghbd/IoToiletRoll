from twilio.rest import Client
def dispatch_text(client, number, content):
    message = client.messages \
        .create(
        body=content,
        from_='+447897016821',
        to=number
    )
    return 0