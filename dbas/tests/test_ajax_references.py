import unittest
import json
import transaction
from pyramid import testing

from dbas.database import DBDiscussionSession, DBNewsSession
from dbas.database.discussion_model import StatementReferences
from dbas.helper.tests import add_settings_to_appconfig
from sqlalchemy import engine_from_config

settings = add_settings_to_appconfig()
DBDiscussionSession.configure(bind=engine_from_config(settings, 'sqlalchemy-discussion.'))
DBNewsSession.configure(bind=engine_from_config(settings, 'sqlalchemy-news.'))


class AjaxReferencesTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)

        # test every ajax method, which is not used in other classes

    def tearDown(self):
        testing.tearDown()

    def test_get_references_empty(self):
        from dbas.views import get_references as ajax
        request = testing.DummyRequest(params={
            'uid': json.dumps([14]),
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        for uid in response['data']:
            self.assertTrue(len(response['data'][uid]) == 0)
            self.assertTrue(len(response['text'][uid]) != 0)

    def test_get_references(self):
        from dbas.views import get_references as ajax
        request = testing.DummyRequest(params={
            'uid': json.dumps([15]),
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        for uid in response['data']:
            self.assertTrue(len(response['data'][uid]) != 0)
            self.assertTrue(len(response['text'][uid]) != 0)

    def test_get_references_failure(self):
        from dbas.views import get_references as ajax
        request = testing.DummyRequest(params={
            'uid': json.dumps('ab'),
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) != 0)
        self.assertTrue(len(response['data']) == 0)
        self.assertTrue(len(response['text']) == 0)

    def test_set_references(self):
        self.config.testing_securitypolicy(userid='Tobias', permissive=True)
        from dbas.views import set_references as ajax
        request = testing.DummyRequest(params={
            'uid': 17,
            'reference': json.dumps('This is a source'),
            'ref_source': json.dumps('http://www.google.de/some_source'),
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)

        from dbas.views import get_references as ajax
        request = testing.DummyRequest(params={
            'uid': json.dumps([17]),
            'is_argument': 'false'
        }, matchdict={})
        response = json.loads(ajax(request))
        self.assertIsNotNone(response)
        self.assertTrue(len(response['error']) == 0)
        for uid in response['data']:
            self.assertTrue(17, uid)
            self.assertTrue(len(response['data'][uid]) != 0)
            self.assertTrue(len(response['text'][uid]) != 0)

        DBDiscussionSession.query(StatementReferences).filter_by(statement_uid=17).delete()
        transaction.commit()