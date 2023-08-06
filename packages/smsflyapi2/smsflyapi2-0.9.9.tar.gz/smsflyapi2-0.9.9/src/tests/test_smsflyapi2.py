from unittest import TestCase
from src.smsfluapi2.smsflyapi2 import SMSFlyAPI2


class TestSMSFlyAPI2(TestCase):
    API_KEY = "Your API KEY"
    api = SMSFlyAPI2(API_KEY)

    def test_api_key(self):
        assert self.api.API_KEY != "! Set this your API KEY !", "Не задан API KEY!"

    def test_get_balance(self):
        r = self.api.get_balance()
        assert r.ok, "Нет информации о балансе"

    def test_get_balance_ext(self):
        r = self.api.get_balance_ext()
        assert r.ok, "Нет информации о балансе"

    # def test_send_message(self):
    #     self.fail()

    # def test_send_sms_message(self):
    #     r = self.api.send_sms_message("380675788007", "Test")
    #     assert r.ok, ""
    #     self.fail()

    # def test_send_viber_message(self):
    #     self.fail()

    # def test_get_message_status(self):
    #     self.fail()
