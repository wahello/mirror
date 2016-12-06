import unittest
import json
import transaction

from pyramid import testing
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.database.discussion_model import User
from dbas.helper.tests import add_settings_to_appconfig
from dbas.handler.password import get_hashed_password
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))
DBNewsSession.configure(bind=engine_from_config(settings, 'sqlalchemy-news.'))


class AjaxTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.include('pyramid_mailer.testing')
        # self.config.testing_securitypolicy(userid='Tobias', permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_user_login_wrong_nick(self):
        from dbas.views import user_login as ajax
        request = testing.DummyRequest(params={
            'user': 'Tobiass',
            'password': 'tobias',
            'keep_login': 'false',
            'url': ''
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_user_login_wrong_password(self):
        from dbas.views import user_login as ajax
        request = testing.DummyRequest(params={
            'user': 'Tobias',
            'password': 'tobiass',
            'keep_login': 'false',
            'url': ''
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_user_login(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        db_user.password = get_hashed_password('tobias')
        transaction.commit()
        from dbas.views import user_login as ajax
        request = testing.DummyRequest(params={
            'user': 'Tobias',
            'password': 'tobias',
            'keep_login': 'false',
            'url': ''
        }, matchdict={})
        response = ajax(request)
        self.assertTrue(type(response) is HTTPFound)

    def test_user_logout(self):
        from dbas.views import user_logout as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = ajax(request)
        self.assertTrue(type(response) is Response)
        self.assertTrue(type(response) is not HTTPFound)

    # cannot be testted, because we have no request.session['antispamanswer']
    # def test_user_registration(self):
    #     from dbas.views import user_registration as ajax
    #     request = testing.DummyRequest(params={
    #         'firstname': 'ThisIsAWebTestAndSoItIsNotSpam',
    #         'lastname': 'Allo',
    #         'nickname': 'SomeoneNew',
    #         'email': 'tobias.krauthoff@web.de',
    #         'gender': 'm',
    #         'password': 'somepassword',
    #         'passwordconfirm': 'somepassword',
    #         'spamanswer': ''
    #     }, matchdict={})
    #     response = json.loads(ajax(request))
    #     self.assertIsNotNone(response)
    #     self.assertTrue(len(response['success']) != 0)
    #     self.assertTrue(len(response['error']) == 0)
    #     self.assertTrue(len(response['info']) == 0)
    #     self.assertTrue(len(response['spamquestion']) != 0)

    def test_user_password_request_failure1(self):
        from dbas.views import user_password_request as ajax
        request = testing.DummyRequest(params={'email': 'krauthof@cs.uni-duesseldorf.de'}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['success']) == 0)
        self.assertTrue(len(response['error']) == 0)
        self.assertTrue(len(response['info']) != 0)

    def test_user_password_request_failure2(self):
        from dbas.views import user_password_request as ajax
        request = testing.DummyRequest(params={'emai': 'krauthoff@cs.uni-duesseldorf.de'}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['success']) == 0)
        self.assertTrue(len(response['error']) != 0)
        self.assertTrue(len(response['info']) == 0)

    def test_user_password_request(self):
        db_user = DBDiscussionSession.query(User).filter_by(nickname='Tobias').first()
        from dbas.views import user_password_request as ajax
        request = testing.DummyRequest(params={'email': 'krauthoff@cs.uni-duesseldorf.de'}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(db_user.password != get_hashed_password('tobias'))
        db_user.password = get_hashed_password('tobias')
        transaction.commit()

    def test_fuzzy_search_mode_0(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(params={'value': 'cat', 'type': 0}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertNotIn('error', response)

    def test_fuzzy_search_mode_1(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(params={'value': 'cat', 'type': 1, 'extra': 1}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertNotIn('error', response)

    def test_fuzzy_search_mode_2(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(params={'value': 'cat', 'type': 2}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertNotIn('error', response)

    def test_fuzzy_search_mode_3(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(params={'value': 'cat', 'type': 3}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertNotIn('error', response)

    def test_fuzzy_search_mode_4(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(params={'value': 'cat', 'type': 4}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertNotIn('error', response)

    def test_fuzzy_search_mode_5(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(params={'value': 'cat', 'type': 5}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertNotIn('error', response)

    def test_fuzzy_search_failure_mode(self):
        from dbas.views import fuzzy_search as ajax
        request = testing.DummyRequest(params={'value': 'cat', 'type': 6}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)

    def test_switch_language_de(self):
        from dbas.views import switch_language as ajax
        request = testing.DummyRequest(params={'lang': 'de'}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(response['ui_locales'] == 'de')

    def test_switch_language_en(self):
        from dbas.views import switch_language as ajax
        request = testing.DummyRequest(params={'lang': 'en'}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(response['ui_locales'] == 'en')

    def test_switch_language_failure(self):
        from dbas.views import switch_language as ajax
        request = testing.DummyRequest(params={'lang': 'sw'}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(response['ui_locales'] != 'sw')

    def test_additional_service(self):
        from dbas.views import additional_service as ajax
        request = testing.DummyRequest(params={}, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)

    def test_set_user_language(self):
        from dbas.views import set_user_language as ajax
        request = testing.DummyRequest(params={'ui_locales': 'en'})
        response = json.loads(ajax(request))
        self.assertTrue(len(response['error']) > 0)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(params={'ui_locales': 'en'})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['ui_locales'] == 'en')
        self.assertTrue(response['current_lang'] == 'English')
        request = testing.DummyRequest(params={'ui_locales': 'de'})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['ui_locales'] == 'de')
        self.assertTrue(response['current_lang'] == 'Deutsch')
        request = testing.DummyRequest(params={'ui_locales': 'li'})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('ui_locales', response)
        self.assertIn('current_lang', response)
        self.assertTrue(response['error'] != '')
        self.assertTrue(response['ui_locales'] == 'li')
        self.assertTrue(response['current_lang'] == '')

    def test_set_user_setting_mail(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(params={'ui_locales': 'en'})
        response = json.loads(ajax(request))
        self.assertTrue(len(response['error']) > 0)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(params={'service': 'mail', 'settings_value': False})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')

    def test_set_user_setting_notification(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(params={'ui_locales': 'en'})
        response = json.loads(ajax(request))
        self.assertTrue(len(response['error']) > 0)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(params={'service': 'notification', 'settings_value': True})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')

    def test_set_user_setting_nick(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(params={'ui_locales': 'en'})
        response = json.loads(ajax(request))
        self.assertTrue(len(response['error']) > 0)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(params={'service': 'public_nick', 'settings_value': False})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] == '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')

    def test_set_user_setting_no_service(self):
        from dbas.views import set_user_settings as ajax
        request = testing.DummyRequest(params={'ui_locales': 'en'})
        response = json.loads(ajax(request))
        self.assertTrue(len(response['error']) > 0)

        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        request = testing.DummyRequest(params={'service': 'oha', 'settings_value': False})
        response = json.loads(ajax(request))
        self.assertIn('error', response)
        self.assertIn('public_nick', response)
        self.assertIn('public_page_url', response)
        self.assertIn('gravatar_url', response)
        self.assertTrue(response['error'] != '')
        self.assertTrue(response['public_nick'] != '')
        self.assertTrue(response['public_page_url'] != '')
        self.assertTrue(response['gravatar_url'] != '')