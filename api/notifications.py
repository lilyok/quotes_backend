import os

from datetime import datetime, timedelta

from gobiko.apns import APNsClient

# TODO make in db

USER_DEVICES = [{
    'user_id': 'sdsfds',
    'device_token': 'sfdesf'
}]

NOTIFIIONS = [{
    'device_token': 'awdadawd',  # required
    'start_time': '11:00',
    'stop_time': '23:00',
    'number': 3,
    'seconds_offset': 0,  # required
    'start_time_utc': '11:00',
    'stop_time_utc': '23:00',
    'notification_times': '14:00,17:00,20:00'
}]

CATEGORIES = {  # name: id
    'Common Sense': 0,
    'Favourite': 1,
    'Popular': 2
}

CATEGORY_USERS = [  # many to many
    {
        'user_id': 'sdeded',
        'category_id': 0
    }
]


#. venv/bin/postactivate  

class NotificationClient:

    def __init__(self):
        print(os.environ['USE_SANDBOX'], type(os.environ['USE_SANDBOX']))
        self.client = APNsClient(  # TODO move parameters to enviroment
            team_id=os.environ['TEAM_ID'],
            bundle_id=os.environ['BUNDLE_ID'],
            auth_key_id=os.environ['AUTH_KEY_ID'],
            auth_key=os.environ['AUTH_KEY'],
            use_sandbox=os.environ['USE_SANDBOX'],
            wrap_key=True,
            force_proto='h2'
        )


    def send(self, message='All your base are belong to us'):
        device_token = os.environ['DEVICE_TOKEN']  # TODO get from database for each
        self.client.send_message(
            device_token,
            message,  # TODO add quote here
            # badge=1,
            sound='default',
            category='User Action',
            content_available=True
        )


    def update_settings(self, **kwargs):
        self.create_or_update_notifications(**kwargs)
        self.select_categories(kwargs['userID'], kwargs['categories'])


    def select_categories(self, user_id, categories):
        for category, category_id in CATEGORIES.items():
            is_category_users_exists = False or category not in categories
            row_for_delete = None
            for row in CATEGORY_USERS:
                if row['category_id'] == category_id and row['user_id'] == user_id:
                    if category not in categories:
                        row_for_delete = row
                    is_category_users_exists = True
                    break
            if not is_category_users_exists:
                CATEGORY_USERS.append({'user_id': user_id, 'category_id': category_id})
            if row_for_delete:
                CATEGORY_USERS.remove(row_for_delete)
        # print(CATEGORY_USERS)


    def __get_utc_hours_minutes(self, d, seconds_offset=0):
        if d is None:
            return None, None
        t = datetime.strptime(d, "%H:%M") if isinstance(d, str) else d
        if seconds_offset == 0:
            return t, datetime.strftime(t, '%H:%M') 

        t -= timedelta(seconds=seconds_offset)
        return t, datetime.strftime(t, '%H:%M') 


    def __create_notification_times(self, start_time, stop_time, number):
        if start_time is None or stop_time is None or number is None:
            return None
        min_delta = (stop_time - start_time).seconds / (number + 1)

        notification_times = []
        for i in range(number):
            _, time_str = self.__get_utc_hours_minutes(start_time + timedelta(seconds=(i + 1) * min_delta))
            notification_times.append(time_str)
        return ','.join(notification_times)


    def __create_if_not_exists_user_devices(self, user_id, device_token):
        is_user_device_exists = False
        for row in USER_DEVICES:
            if row['user_id']!= user_id and row['device_token']!= device_token:  # where
                continue
            is_user_device_exists = True
        if not is_user_device_exists:
            USER_DEVICES.append({'user_id': user_id, 'device_token': device_token})
        # print(USER_DEVICES)


    def __update_notification_settings(self, row, start_time_field, stop_time_field, number, seconds_offset, start_time, stop_time, start_time_str, stop_time_str):
        row['start_time'] = start_time_field
        row['stop_time'] = stop_time_field
        row['number'] = number
        row['seconds_offset'] = seconds_offset
        row['start_time_utc'] = start_time_str
        row['stop_time_utc'] = stop_time_str
        row['notification_times'] = self.__create_notification_times(start_time, stop_time, number)


    def create_or_update_notifications(self, userID, deviceToken, secondsOffset, currentStartTime=None, currentStopTime=None, numberOfQuotes=None, isExpanded=None, **kwargs):
        self.__create_if_not_exists_user_devices(userID, deviceToken)

        if not isExpanded:
            currentStartTime, currentStopTime, numberOfQuotes = None, None, None


        start_time, start_time_str = self.__get_utc_hours_minutes(currentStartTime, secondsOffset)
        stop_time, stop_time_str = self.__get_utc_hours_minutes(currentStopTime, secondsOffset)
        # print('start_time=', start_time, ' stop_time=', stop_time)

        is_updated = False

        for row in NOTIFIIONS:  # TODO
            # for all users, get from db table notifications start_time("11:00"), stop_time("23:00"), number
            if row['device_token']!= deviceToken:  # where
                continue
            is_updated = True
            # update
            self.__update_notification_settings(row, currentStartTime, currentStopTime, numberOfQuotes, secondsOffset, start_time, stop_time, start_time_str, stop_time_str)
        
        # insert
        if not is_updated:
            NOTIFIIONS.append({
                'device_token': deviceToken,
                'start_time': currentStartTime,
                'stop_time': currentStopTime,
                'number': numberOfQuotes,
                'seconds_offset': secondsOffset,
                'start_time_utc':start_time_str,
                'stop_time_utc': stop_time_str,
                'notification_times': self.__create_notification_times(start_time, stop_time, numberOfQuotes)
            })
        # print(NOTIFIIONS)


    def notify(self):
        local_utc_hours_minutes = self.__get_utc_hours_minutes(datetime.now(datetime.timezone.utc))  # '16:28'
        # print('local_utc_hours_minutes=', local_utc_hours_minutes)

        for row in NOTIFIIONS:  # TODO
            # for all users, get from db table notifications start_time("11:00"), stop_time("23:00"), number

            if row['notification_times'] is None or row['start_time_utc'] > local_utc_hours_minutes or row['stop_time_utc'] < local_utc_hours_minutes:  # move to where
                continue  # user doesn't want notification at the current time

            for t in row['notification_times'].split(','):
                if t != local_utc_hours_minutes:
                    continue

                self.client.send()
                break






























