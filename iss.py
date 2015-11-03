import requests
from redis import Redis
from rq_scheduler import Scheduler

from twilio.rest import TwilioRestClient
from datetime import datetime

# Open a connection to your Redis server.
redis_server = Redis()

# Create a scheduler object with your Redis server.
scheduler = Scheduler(connection=redis_server)

client = TwilioRestClient()


def get_next_pass(lat, lon):
    iss_url = 'http://api.open-notify.org/iss-pass.json'
    location = {'lat': lat, 'lon': lon}
    response = requests.get(iss_url, params=location).json()

    next_pass = response['response'][0]['risetime']

    print('Next pass is: {}'.format(datetime.fromtimestamp(next_pass)))
    return datetime.fromtimestamp(next_pass)


def add_to_queue(phone_number, lat, lon):
    # Add this phone number to Redis associated with "lat,lon"
    redis_server.set(phone_number, '{},{}'.format(lat, lon))

    # Get the timestamp of the next ISS flyby for this number.
    next_pass_timestamp = get_next_pass(lat, lon)

    # Schedule a text to be sent at the time of the next flyby.
    scheduler.enqueue_at(next_pass_timestamp, notify_subscriber, phone_number)

    print('{} will be notified when ISS passes by {}, {}'
          .format(phone_number, lat, lon))


def notify_subscriber(phone_number):
    msg_body = 'Look up! You may not be able to see it, but the International' \
               ' Space Station is passing above you right now!'

    # Retrieve the latitude and longitude associated with this number.
    lat, lon = redis_server.get(phone_number).split(',')

    # Send a message to the number alerting them of an ISS flyby.
    client.messages.create(to=phone_number,
                           messaging_service_sid='MESSAGING_SERVICE_SID',
                           body=msg_body)

    # Add the subscriber back to the queue to receive their next flyby message.
    add_to_queue(phone_number, lat, lon)

    print('Message has been sent to {}'.format(phone_number))
