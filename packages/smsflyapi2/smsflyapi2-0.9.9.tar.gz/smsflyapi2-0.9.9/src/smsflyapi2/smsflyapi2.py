from typing import Dict, List, Optional
import requests
import logging


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        # logging.FileHandler('sms-fly-api2.log'),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger()


class SMSFlyAPI2:
    API_URL = 'https://sms-fly.ua/api/v2/api.php'
    API_KEY = None
    SMS_SOURCE = 'InfoCenter'
    VIBER_SOURCE = None
    CHANNELS = ['sms']
    TTL = 5

    def __init__(self, api_key: str,
                 sms_source: Optional[str] = None,
                 viber_source: Optional[str] = None,
                 channels: Optional[List[str]] = None,
                 api_url: Optional[str] = None):
        self._session = requests.Session()
        self.API_KEY = api_key

        if sms_source:
            self.SMS_SOURCE = sms_source

        if viber_source:
            self.VIBER_SOURCE = viber_source

        if channels:
            self.CHANNELS = channels

        if api_url:
            self.API_URL = api_url

    def _post(self, action: str, data: Dict = None) -> requests.Response:
        json = {
            "auth": {
                "key": self.API_KEY
            },
            "action": action,
            "data": data
        }
        r = self._session.post(url=self.API_URL, json=json)
        if not r.ok:
            logger.error(r.text)
        return r

    def get_balance(self) -> requests.Response:
        """
        Запрос баланса СМС

        :return: requests.Response
        """
        return self._post(action='GETBALANCE')

    def get_balance_ext(self) -> requests.Response:
        """
        Запрос расширенного баланса

        :return: requests.Response
        """
        return self._post(action='GETBALANCEEXT')

    def send_message(self, recipient: str, message: str,
                     button_caption: Optional[str] = None,
                     button_url: Optional[str] = None,
                     image: Optional[str] = None,
                     channels: Optional[List[str]] = None) -> requests.Response:
        """
        Отправить Viber или SMS сообщение

        :param recipient: Номер телефона 380ххххххххх
        :param message:
        :param button_caption:
        :param button_url:
        :param image:
        :param channels:
        :return: requests.Response
        """
        if not channels:
            channels = self.CHANNELS

        data = {
            "recipient": recipient,
            "channels": channels
        }

        if 'sms' in channels and self.SMS_SOURCE:
            data['sms'] = {
                "source": self.SMS_SOURCE,
                "ttl": self.TTL,
                "text": message
            }

        if 'viber' in channels and self.VIBER_SOURCE:
            data['viber'] = {
                "source": self.VIBER_SOURCE,
                "ttl": self.TTL,
                "text": message
            }

            if image is not None:
                data['viber']['image'] = image

            if button_caption is not None and button_url is not None:
                data['viber']['button'] = {
                    "caption": button_caption,
                    "url": button_url
                }

        r = self._post(action='SENDMESSAGE', data=data)
        return r

    def send_sms_message(self, recipient: str, message: str) -> requests.Response:
        """
        Отправка SMS сообщения

        :param recipient:
        :param message:
        :return: requests.Response

        :200:
        {
            "success": 1,
            "date": "2022-08-26 00:14:20 +0300",
            "data": {
                "messageID": "FAPI0009390725000001",
                "sms": {
                    "status": "ACCEPTD",
                    "date": "2022-08-26 00:14:20 +0300",
                    "cost": "0.479"
                }
            }
        }
        """
        return self.send_message(recipient=recipient, message=message, channels=['sms'])

    def send_viber_message(self, recipient: str, message: str, button_caption: Optional[str] = None,
                           button_url: Optional[str] = None, image: Optional[str] = None) -> requests.Response:
        """
        Отправка Viber сообщения

        :param recipient:
        :param message:
        :param button_caption:
        :param button_url:
        :param image:
        :return: requests.Response
        """
        return self.send_message(
            recipient=recipient,
            message=message,
            button_url=button_url,
            button_caption=button_caption,
            image=image,
            channels=['viber'])

    def get_message_status(self, message_id: str) -> requests.Response:
        """
        Получение статуса сообщения

        :param message_id:
        :return: requests.Response
        """
        data = {
            "messageID": message_id
        }
        return self._post(action='GETMESSAGESTATUS', data=data)
