"""
TODO

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
import re
from datetime import datetime

from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Statement, User, TextVersion, Premise, Issue, Bubble, VoteArgument, VoteStatement, Breadcrumb
from dbas.helper.notification_helper import NotificationHelper
from dbas.helper.query_helper import QueryHelper
from dbas.lib import get_text_for_argument_uid, get_text_for_statement_uid, get_text_for_premisesgroup_uid, get_text_for_conclusion
from dbas.logger import logger
from dbas.recommender_system import RecommenderHelper
from dbas.strings import Translator, TextGenerator
from dbas.url_manager import UrlManager
from dbas.user_management import UserHandler


class DictionaryHelper(object):
	"""

	"""

	def __init__(self, lang=''):
		"""
		Initialize default values

		:param lang: ui_locales
		:return:
		"""
		self.lang = lang

	def get_random_subdict_out_of_orderer_dict(self, ordered_dict, count):
		"""
		Creates a random subdictionary with given count out of the given ordered_dict.
		With a count of <2 the dictionary itself will be returned
		.
		:param ordered_dict: dictionary for the function
		:param count: count of entries for the new dictionary
		:return: dictionary
		"""
		return_dict = dict()
		logger('DictionaryHelper', 'get_subdictionary_out_of_orderer_dict', 'count: ' + str(count))
		items = list(ordered_dict.items())

		if count < 0:
			return ordered_dict
		elif count == 1:
			if len(items) > 1:
				rnd = random.randint(0, len(items) - 1)
				return_dict[items[rnd][0]] = items[rnd][1]
			else:
				return ordered_dict
		else:

			for i in range(0, count):
				rnd = random.randint(0, len(items) - 1)
				return_dict[items[rnd][0]] = items[rnd][1]
				items.pop(rnd)

		return return_dict

	def prepare_discussion_dict_for_start(self, breadcrumbs, nickname, session_id):
		"""

		:param breadcrumbs:
		:param nickname:
		:param session_id:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_start', 'at_start')
		_tn			        = Translator(self.lang)
		bubbles_array       = self.__create_speechbubble_history(breadcrumbs, nickname, session_id)
		add_premise_text    = ''
		intro               = _tn.get(_tn.initialPositionInterest)
		save_statement_url  = 'ajax_set_new_start_premise'

		start_bubble = self.__create_speechbubble_dict(False, True, False, 'start', '', intro, True)
		self.__append_bubble(bubbles_array, start_bubble)

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_discussion_dict_for_attitude(self, uid, breadcrumbs, nickname, session_id):
		"""

		:param uid:
		:param breadcrumbs:
		:param nickname:
		:param session_id:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_attitude', 'at_attitude')
		_tn			        = Translator(self.lang)
		bubbles_array       = self.__create_speechbubble_history(breadcrumbs, nickname, session_id)
		add_premise_text    = ''
		save_statement_url  = 'ajax_set_new_start_statement'
		statement_text      = get_text_for_statement_uid(uid)
		if not statement_text:
			return None
		text                = _tn.get(_tn.whatDoYouThinkAbout) + ' <strong>' + statement_text[0:1].lower() + statement_text[1:] + '</strong>?'
		# select_bubble = self.__create_speechbubble_dict(True, False, False, '', '', _tn.get(_tn.youAreInterestedIn) + ': <strong>' + statement_text + '</strong>')
		bubble = self.__create_speechbubble_dict(False, True, False, '', '', text, True)

		# if save_crumb:
		# 	self.__append_bubble(bubbles_array, select_bubble)
		# 	self.__save_speechbubble(select_bubble, db_user, session_id, breadcrumbs[-1], transaction, statement_uid=uid)
		self.__append_bubble(bubbles_array, bubble)

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_discussion_dict_for_justify_statement(self, nickname, transaction, uid, breadcrumbs, save_crumb, application_url,
	                                                  slug, is_supportive, logged_in, count_of_items, session_id):
		"""

		:param nickname:
		:param transaction:
		:param uid:
		:param breadcrumbs:
		:param save_crumb:
		:param application_url:
		:param slug:
		:param is_supportive:
		:param logged_in:
		:param count_of_items:
		:param session_id:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_justify_statement', 'at_justify')
		_tn			        = Translator(self.lang)
		if not nickname:
			nickname = 'anonymous'
		db_user             = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		bubbles_array       = self.__create_speechbubble_history(breadcrumbs, nickname, session_id)
		add_premise_text    = ''
		save_statement_url  = 'ajax_set_new_start_statement'
		text				= get_text_for_statement_uid(uid)
		text                = text[0:1].upper() + text[1:]
		if not text:
			return None
		question            = _tn.get(_tn.whatIsYourMostImportantReasonWhy) + ' <strong>' + text[0:1].lower() + text[1:] + '</strong> '
		question            += _tn.get(_tn.holds if is_supportive else _tn.isNotAGoodIdea) + '?'
		because			    = _tn.get(_tn.because)[0:1].upper() + _tn.get(_tn.because)[1:].lower() + '...'
		add_premise_text	+= text + ' ' + (_tn.get(_tn.holds) if is_supportive else _tn.get(_tn.isNotAGoodIdea))

		# intro = _tn.get(_tn.youAgreeWith) if is_supportive else _tn.get(_tn.youDisagreeWith) + ': '
		intro = '' if is_supportive else _tn.get(_tn.youDisagreeWith) + ': '
		intro_rev = '' if not is_supportive else _tn.get(_tn.youDisagreeWith) + ': '
		url = UrlManager(application_url, slug).get_slug_url(False)
		question_bubble = self.__create_speechbubble_dict(False, True, False, '', '', question + ' <br>' + because, True)
		if text[:-1] != '.':
			text += '.'
		select_bubble = self.__create_speechbubble_dict(True, False, False, '', url, intro + '<strong>' + text + '</strong>', False, statement_uid=uid, nickname=nickname, is_up_vote=is_supportive)

		if save_crumb:
			self.__save_speechbubble(select_bubble, db_user, session_id, breadcrumbs[-1], transaction, statement_uid=uid)

		# check for double bubbles
		should_append = True
		if len(bubbles_array) > 0:
			should_append = bubbles_array[-1]['message'] != select_bubble['message']
			if bubbles_array[-1]['message'] == intro_rev + '<strong>' + text + '</strong>':
				bubbles_array.remove(bubbles_array[-1])
		if len(bubbles_array) > 1:
			if bubbles_array[-2]['message'] == intro_rev + '<strong>' + text + '</strong>':
				bubbles_array.remove(bubbles_array[-2])

		if should_append:
			self.__append_bubble(bubbles_array, select_bubble)

		self.__append_bubble(bubbles_array, self.__create_speechbubble_dict(False, False, True, 'now', '', _tn.get(_tn.now), True))
		self.__append_bubble(bubbles_array, question_bubble)

		if not logged_in and count_of_items == 1:
			self.__append_bubble(bubbles_array, self.__create_speechbubble_dict(False, False, True, 'now', '', _tn.get(_tn.onlyOneItemWithLink), True))

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': '', 'is_supportive': is_supportive}

	def prepare_discussion_dict_for_justify_argument(self, nickname, uid, is_supportive, attack, logged_in, breadcrumbs, save_crumb, count_of_items, session_id, transaction):
		"""

		:param nickname:
		:param uid:
		:param is_supportive:
		:param attack:
		:param logged_in:
		:param breadcrumbs:
		:param save_crumb:
		:param count_of_items:
		:param session_id:
		:param transaction:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict', 'prepare_discussion_dict_for_justify_argument')
		_tn			       = Translator(self.lang)
		_tg                = TextGenerator(self.lang)
		bubbles_array      = self.__create_speechbubble_history(breadcrumbs, nickname, session_id)
		add_premise_text   = ''
		save_statement_url = 'ajax_set_new_premises_for_argument'

		db_argument		= DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		if not db_argument:
			return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

		confr	       = get_text_for_argument_uid(uid, self.lang, True)
		premise, tmp   = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, self.lang)
		conclusion     = get_text_for_conclusion(db_argument, self.lang)

		user_msg, sys_msg = _tg.get_header_for_users_confrontation_response(premise, attack, conclusion, False, is_supportive, logged_in)

		if attack == 'undermine':
			add_premise_text = _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion,
																	  db_argument.is_supportive)
			add_premise_text = add_premise_text[0:1].upper() + add_premise_text[1:]

		elif attack == 'support':
			is_supportive = not is_supportive
			# when the user rebuts a system confrontation, he attacks his own negated premise, therefore he supports
			# is own premise. so his premise is the conclusion and we need new premises ;-)
			add_premise_text += _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion, is_supportive)
		elif attack == 'undercut':
			add_premise_text += _tg.get_text_for_add_premise_container(premise, premise, attack, conclusion,
																	   db_argument.is_supportive)
		else:
			add_premise_text += _tg.get_text_for_add_premise_container(confr, premise, attack, conclusion,
																	   db_argument.is_supportive)

		sys_msg  = _tn.get(_tn.whatIsYourMostImportantReasonFor) + ': ' + user_msg[:-1] + '?<br>' + _tn.get(_tn.because) + '...'
		# bubble_user = self.__create_speechbubble_dict(True, False, False, '', '', user_msg[0:1].upper() + user_msg[1:], True)
		bubble_question = self.__create_speechbubble_dict(False, True, False, '', '', sys_msg, True)

		self.__append_bubble(bubbles_array, self.__create_speechbubble_dict(False, False, True, 'now', '', _tn.get(_tn.now), True))
		# self.__append_bubble(bubbles_array, bubble_user)
		self.__append_bubble(bubbles_array, bubble_question)

		# if save_crumb:
		# 	db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		# 	self.__save_speechbubble(bubble_user, db_user, session_id, breadcrumbs[-1], transaction, argument_uid=uid)
		# 	self.__save_speechbubble(bubble_question, db_user, session_id, breadcrumbs[-1], transaction)

		# if not logged_in and count_of_items == 1:
		# 	self.__append_bubble(bubbles_array, self.__create_speechbubble_dict(False, False, True, 'now', '', _tn.get(_tn.onlyOneItemWithLink), True))

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': '', 'attack_type': attack, 'arg_uid': uid}

	def prepare_discussion_dict_for_dont_know_reaction(self, nickname, transaction, uid, breadcrumbs, save_crumb, session_id):
		"""

		:param nickname:
		:param transaction:
		:param uid:
		:param breadcrumbs:
		:param save_crumb:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_dont_know_reaction', 'at_dont_know')
		_tn			   = Translator(self.lang)
		db_user        = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		bubbles_array  = self.__create_speechbubble_history(breadcrumbs, nickname, session_id)
		add_premise_text = ''
		save_statement_url = 'ajax_set_new_start_statement'

		if uid != 0:
			text			= get_text_for_argument_uid(uid, self.lang)
			text			= text.replace(_tn.get(_tn.because).lower(), '</strong>' + _tn.get(_tn.because).lower() + '<strong>')
			sys_text    	= _tn.get(_tn.otherParticipantsThinkThat) + ' <strong>' + text[0:1].lower() + text[1:]  + '</strong>. '

			bubble_sys_save = self.__create_speechbubble_dict(False, True, False, '', '', sys_text)
			bubble_sys = self.__create_speechbubble_dict(False, True, False, '', '', sys_text + '<br><br>' + _tn.get(_tn.whatDoYouThinkAboutThat) + '?')
			self.__append_bubble(bubbles_array, bubble_sys)

			if save_crumb:
				self.__save_speechbubble(bubble_sys_save, db_user, session_id, breadcrumbs[-1], transaction, argument_uid=uid)

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_discussion_dict_for_argumentation(self, nickname, transaction, uid, breadcrumbs, save_crumb, is_supportive, additional_id, attack, session_id):
		"""

		:param nickname:
		:param transaction:
		:param uid:
		:param breadcrumbs:
		:param save_crumb:
		:param is_supportive:
		:param additional_id:
		:param attack:
		:param session_id:
		:param changed_opinion:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_discussion_dict_for_argumentation', 'at_argumentation')
		_tn			        = Translator(self.lang)
		db_user             = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		bubbles_array       = self.__create_speechbubble_history(breadcrumbs, nickname, session_id)
		add_premise_text    = ''
		save_statement_url  = 'ajax_set_new_start_statement'
		mid_text            = ''
		bubble_mid          = ''

		_tg					 = TextGenerator(self.lang)
		db_argument			 = DBDiscussionSession.query(Argument).filter_by(uid=uid).first()
		if attack == 'end':
			#  user_text        = _tn.get(_tn.soYourOpinionIsThat) + ': '
			text             = get_text_for_argument_uid(uid, self.lang, True)
			user_text        = '<strong>' + text[0:1].upper() + text[1:] + '</strong>.'
			sys_text         = _tn.get(_tn.otherParticipantsDontHaveCounterForThat) + '.'
			mid_text         = _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.discussionEndLinkText)
		else:
			premise, tmp	 = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, self.lang)
			conclusion       = get_text_for_conclusion(db_argument, self.lang)
			db_confrontation = DBDiscussionSession.query(Argument).filter_by(uid=additional_id).first()
			confr, tmp       = get_text_for_premisesgroup_uid(db_confrontation.premisesgroup_uid, self.lang)
			sys_conclusion   = get_text_for_conclusion(db_confrontation, self.lang)
			if attack == 'undermine':
				premise = get_text_for_statement_uid(db_confrontation.conclusion_uid) if db_confrontation.conclusion_uid != 0 \
					else get_text_for_argument_uid(db_confrontation.argument_uid, self.lang, True)

			# did the user changed his opinion?
			user_changed_opinion = len(breadcrumbs) > 1 and '/undercut/' in breadcrumbs[-2]['url']

			# argumentation is a reply for an argument, if the arguments conclusion of the user is no position
			db_statement		= DBDiscussionSession.query(Statement).filter_by(uid=db_argument.conclusion_uid).first()
			reply_for_argument  = not (db_statement and db_statement.is_startpoint)
			current_argument	= get_text_for_argument_uid(uid, self.lang, with_strong_html_tag=True,
			                                                    start_with_intro=True, user_changed_opinion=user_changed_opinion)
			user_is_attacking   = not db_argument.is_supportive

			# fix
			prefix = '</strong>' + _tn.get(_tn.soYourOpinionIsThat) + ': <strong>'
			if conclusion.startswith(prefix):
				conclusion = conclusion[len(prefix):]

			if current_argument.startswith(prefix):
				current_argument = current_argument[len(prefix):]

			current_argument = current_argument[0:1].upper() + current_argument[1:]
			premise = premise[0:1].lower() + premise[1:]

			user_text = '<strong>'
			user_text += current_argument if current_argument != '' else premise
			user_text += '</strong>.'

			sys_text = _tg.get_text_for_confrontation(premise, conclusion, sys_conclusion, is_supportive, attack, confr,
			                                          reply_for_argument, user_is_attacking, db_argument)
		if attack == 'end':
			bubble_user = self.__create_speechbubble_dict(True, False, False, '', '', user_text, True, argument_uid=uid, nickname=nickname, is_up_vote=is_supportive)
			bubble_sys  = self.__create_speechbubble_dict(False, True, False, '', '', sys_text, True)
			bubble_mid  = self.__create_speechbubble_dict(False, False, True, '', '', mid_text, True)
		else:
			bubble_user = self.__create_speechbubble_dict(True, False, False, '', '', user_text, True, argument_uid=uid, nickname=nickname, is_up_vote=is_supportive)
			bubble_sys  = self.__create_speechbubble_dict(False, True, False, 'question-bubble', '', sys_text, True)

		# dirty fixes
		if len(bubbles_array) > 0 and bubbles_array[-1]['message'] == bubble_user['message']:
			bubbles_array.remove(bubbles_array[-1])

		self.__append_bubble(bubbles_array, self.__create_speechbubble_dict(False, False, True, 'now', '', _tn.get(_tn.now)))
		self.__append_bubble(bubbles_array, bubble_user)
		self.__append_bubble(bubbles_array, bubble_sys)

		if attack == 'end':
			self.__append_bubble(bubbles_array, bubble_mid)

		if save_crumb:
			self.__save_speechbubble(bubble_user, db_user, session_id, breadcrumbs[-1], transaction, argument_uid=uid)
			self.__save_speechbubble(bubble_sys, db_user, session_id, breadcrumbs[-1], transaction)

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_discussion_dict_for_choosing(self, uid, is_uid_argument, is_supportive, breadcrumbs, nickname, session_id):
		"""

		:param uid:
		:param is_uid_argument:
		:param is_supportive:
		:param breadcrumbs:
		:return:
		"""
		_tn			   = Translator(self.lang)
		bubbles_array  = self.__create_speechbubble_history(breadcrumbs, nickname, session_id)
		add_premise_text = ''
		save_statement_url = 'ajax_set_new_start_statement'

		logger('DictionaryHelper', 'prepare_discussion_dict', 'at_choosing')
		text = _tn.get(_tn.soYouEnteredMultipleReasons) + '.'
		text += _tn.get(_tn.whyAreYouAgreeingWith) if is_supportive else _tn.get(_tn.whyAreYouDisagreeingWith)
		text += ':<br><strong>'
		text += get_text_for_argument_uid(uid, self.lang, True) if is_uid_argument else get_text_for_statement_uid(uid)
		text += '</strong>?<br>' + _tn.get(_tn.because) + '...'

		self.__append_bubble(bubbles_array, self.__create_speechbubble_dict(False, False, True, 'now', '', 'Now', True))
		self.__append_bubble(bubbles_array, self.__create_speechbubble_dict(True, False, False, 'question-bubble', '', text, True))

		return {'bubbles': bubbles_array, 'add_premise_text': add_premise_text, 'save_statement_url': save_statement_url, 'mode': ''}

	def prepare_item_dict_for_start(self, issue_uid, logged_in, application_url, for_api):
		"""

		:param issue_uid:
		:param logged_in:
		:param application_url:
		:param for_api:
		:return:
		"""
		db_statements = DBDiscussionSession.query(Statement)\
			.filter(and_(Statement.is_startpoint == True, Statement.issue_uid == issue_uid))\
			.join(TextVersion, TextVersion.uid == Statement.textversion_uid).all()
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()

		statements_array = []
		_um = UrlManager(application_url, slug, for_api)

		if db_statements:
			for statement in db_statements:
				statements_array.append(self.__create_statement_dict(statement.uid,
				                                                     [{'title': get_text_for_statement_uid(statement.uid), 'id': statement.uid}],
																     'start',
																     _um.get_url_for_statement_attitude(True, statement.uid)))
			_tn = Translator(self.lang)
			if logged_in:
				statements_array.append(self.__create_statement_dict('start_statement',
				                                                     [{'title': _tn.get(_tn.newConclusionRadioButtonText), 'id': 0}],
																	 'start',
																	 'add'))
			else:
				statements_array.append(self.__create_statement_dict('login', [{'id': '0', 'title': _tn.get(_tn.wantToStateNewPosition)}], 'justify', 'login'))

		return statements_array

	def prepare_item_dict_for_attitude(self, statement_uid, issue_uid, application_url, for_api):
		"""

		:param statement_uid:
		:param issue_uid:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_attitude', 'def')
		_tn = Translator(self.lang)

		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		text = get_text_for_statement_uid(statement_uid)
		statements_array = []

		_um = UrlManager(application_url, slug, for_api)

		statements_array.append(self.__create_statement_dict('agree',
		                                                     [{'title': _tn.get(_tn.iAgreeWithInColor) + ': ' + text, 'id': 'agree'}],
															 'agree', _um.get_url_for_justifying_statement(True, statement_uid, 't')))
		statements_array.append(self.__create_statement_dict('disagree',
		                                                     [{'title': _tn.get(_tn.iDisagreeWithInColor) + ': ' + text, 'id': 'disagree'}],
															 'disagree', _um.get_url_for_justifying_statement(True, statement_uid, 'f')))
		statements_array.append(self.__create_statement_dict('dontknow',
		                                                     [{'title': _tn.get(_tn.iHaveNoOpinionYetInColor) + ': ' + text, 'id': 'dontknow'}],
															 'dontknow', _um.get_url_for_justifying_statement(True, statement_uid, 'd')))

		return statements_array

	def prepare_item_dict_for_justify_statement(self, statement_uid, nickname, issue_uid, is_supportive, application_url, for_api):
		"""

		:param statement_uid:
		:param nickname:
		:param issue_uid:
		:param is_supportive:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_justify_statement', 'def')
		statements_array = []
		_tn = Translator(self.lang)
		_rh = RecommenderHelper()
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		db_arguments = RecommenderHelper.get_arguments_by_conclusion(statement_uid, is_supportive)

		_um = UrlManager(application_url, slug, for_api)

		if db_arguments:
			for argument in db_arguments:
				# get all premises in the premisegroup of this argument
				db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
				premise_array = []
				for premise in db_premises:
					text = get_text_for_statement_uid(premise.statement_uid)
					text = text[0:1].upper() + text[1:]
					premise_array.append({'title': text, 'id': premise.statement_uid})

				# get attack for each premise, so the urls will be unique
				arg_id_sys, attack = _rh.get_attack_for_argument(argument.uid, issue_uid, self.lang)
				statements_array.append(self.__create_statement_dict(str(argument.uid),
				                                                     premise_array,
				                                                     'justify',
																     _um.get_url_for_reaction_on_argument(True, argument.uid, attack, arg_id_sys)))

		if nickname:
			statements_array.append(self.__create_statement_dict('start_premise',
			                                                     [{'title': _tn.get(_tn.newPremiseRadioButtonText), 'id': 0}],
																  'justify',
																  'add'))
		else:
			# elif len(statements_array) == 1:
			statements_array.append(self.__create_statement_dict('login', [{'id': '0', 'title': _tn.get(_tn.onlyOneItem)}], 'justify', 'login'))

		return statements_array

	def prepare_item_dict_for_justify_argument(self, argument_uid, attack_type, issue_uid, application_url, for_api, logged_in):
		"""

		:param argument_uid:
		:param attack_type:
		:param issue_uid:
		:param application_url:
		:param for_api:
		:param logged_in:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_justify_argument', 'def')
		statements_array = []
		_tn = Translator(self.lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()

		db_arguments = []
		# description in docs: dbas/logic
		if attack_type == 'undermine':
			db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_argument.premisesgroup_uid).all()
			for premise in db_premises:
				arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == premise.statement_uid,
																			Argument.is_supportive == False,
				                                                            Argument.issue_uid == issue_uid)).all()
				db_arguments = db_arguments + arguments

		elif attack_type == 'undercut':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.argument_uid == argument_uid,
																		   Argument.is_supportive == False,
				                                                           Argument.issue_uid == issue_uid)).all()

		elif attack_type == 'overbid':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.argument_uid == argument_uid,
																		   Argument.is_supportive == True,
				                                                           Argument.issue_uid == issue_uid)).all()

		elif attack_type == 'rebut':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == db_argument.conclusion_uid,
																		   Argument.argument_uid == db_argument.argument_uid,
																		   Argument.is_supportive == False,
				                                                           Argument.issue_uid == issue_uid)).all()
		elif attack_type == 'support':
			db_arguments = DBDiscussionSession.query(Argument).filter(and_(Argument.conclusion_uid == db_argument.conclusion_uid,
																		   Argument.argument_uid == db_argument.argument_uid,
																		   Argument.is_supportive == db_argument.is_supportive,
				                                                           Argument.issue_uid == issue_uid)).all()

		_um = UrlManager(application_url, slug, for_api)

		if db_arguments:
			for argument in db_arguments:
				# get alles premises in this group
				db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=argument.premisesgroup_uid).all()
				premises_array = []
				for premise in db_premises:
					premise_dict = dict()
					premise_dict['id'] = premise.statement_uid
					text = get_text_for_statement_uid(premise.statement_uid)
					text = text[0:1].upper() + text[1:]
					premise_dict['title'] = text
					premises_array.append(premise_dict)

				# for each justifying premise, we need a new confrontation:
				arg_id_sys, attack = RecommenderHelper().get_attack_for_argument(argument_uid, issue_uid, self.lang)

				url = _um.get_url_for_reaction_on_argument(True, argument.uid, attack, arg_id_sys)
				statements_array.append(self.__create_statement_dict(argument.uid, premises_array, 'justify', url))

		if logged_in:
			if len(statements_array) == 0:
				text = _tn.get(_tn.newPremisesRadioButtonTextAsFirstOne)
			else:
				text = _tn.get(_tn.newPremiseRadioButtonText)
			statements_array.append(self.__create_statement_dict('justify_premise', [{'id': '0', 'title': text}], 'justify', 'add'))
		else:
			# elif len(statements_array) == 1:
			statements_array.append(self.__create_statement_dict('login', [{'id': '0', 'title': _tn.get(_tn.onlyOneItem)}], 'justify', 'login'))

		return statements_array

	def prepare_item_dict_for_dont_know_reaction(self, argument_uid, is_supportive, issue_uid, application_url, for_api):
		"""

		:param argument_uid:
		:param is_supportive:
		:param issue_uid:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_dont_know_reaction', 'def')
		_tg = TextGenerator(self.lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		_um = UrlManager(application_url, slug, for_api)
		statements_array = []

		db_argument  = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid).first()
		if not db_argument:
			return statements_array

		conclusion   = get_text_for_conclusion(db_argument, self.lang)
		premise, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, self.lang)
		conclusion   = conclusion[0:1].lower() + conclusion[1:]
		premise	     = premise[0:1].lower() + premise[1:]
		rel_dict	 = _tg.get_relation_text_dict(premise, conclusion, False, False, False, is_dont_know=True)
		mode		 = 't' if is_supportive else 't'
		counter_mode = 'f' if is_supportive else 't'

		# relations = ['undermine', 'support', 'undercut', 'overbid', 'rebut'] # TODO 'overbid'
		relations = ['undermine', 'support', 'undercut', 'rebut']
		for relation in relations:
			if relation == 'support':
				arg_id_sys, sys_attack = RecommenderHelper().get_attack_for_argument(argument_uid, issue_uid, self.lang)
				url = _um.get_url_for_reaction_on_argument(True, argument_uid, sys_attack, arg_id_sys)

			else:
				current_mode = mode if relation == 'overbid' else counter_mode
				url = _um.get_url_for_justifying_argument(True, argument_uid, current_mode, relation)

			statements_array.append(self.__create_statement_dict(relation, [{'title': rel_dict[relation + '_text'], 'id':relation}], relation, url))

		return statements_array

	def prepare_item_dict_for_reaction(self, argument_uid_sys, argument_uid_user, is_supportive, issue_uid, attack, application_url, for_api):
		"""

		:param argument_uid_sys:
		:param argument_uid_user:
		:param is_supportive:
		:param issue_uid:
		:param attack:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_reaction', 'def')
		_tg  = TextGenerator(self.lang)
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()

		db_sys_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid_sys).first()
		db_user_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_uid_user).first()
		statements_array = []
		if not db_sys_argument or not db_user_argument:
			return statements_array

		conclusion   = get_text_for_conclusion(db_sys_argument, self.lang)
		premise, tmp = get_text_for_premisesgroup_uid(db_sys_argument.premisesgroup_uid, self.lang)
		conclusion	 = conclusion[0:1].lower() + conclusion[1:]
		premise		 = premise[0:1].lower() + premise[1:]

		rel_dict	 = _tg.get_relation_text_dict(premise, conclusion, False, True, not db_sys_argument.is_supportive)
		mode		 = 't' if is_supportive else 'f'
		_um			 = UrlManager(application_url, slug, for_api)
		_rh          = RecommenderHelper()

		# based in the relation, we will fetch different url's for the items
		# relations = ['undermine', 'support', 'undercut', 'overbid', 'rebut'] # TODO overbid
		# TODO COMMA16 Special Case (forbid: undercuts of undercuts)
		# if attack == 'undercut':
		# 	relations = ['undermine', 'support', 'rebut']
		# else:
		relations = ['undermine', 'support', 'undercut', 'rebut']
		for relation in relations:
			url = ''

			# special case, when the user selectes the support, because this does not need to be justified!
			if relation == 'support':
				arg_id_sys, sys_attack = _rh.get_attack_for_argument(argument_uid_sys, issue_uid, self.lang)
				if sys_attack == 'rebut' and attack == 'undercut':
					# case: system makes an undercut and the user supports this
					# new attack can be an rebut, so another undercut for the users argument
					# therefore now the users opininion is the new undercut (e.g. rebut)
					# because he supported it!
					url = _um.get_url_for_reaction_on_argument(True, arg_id_sys, sys_attack, db_sys_argument.argument_uid)
				else:
					url = _um.get_url_for_reaction_on_argument(True, argument_uid_sys, sys_attack, arg_id_sys)

			# easy cases
			elif relation == 'undermine' or relation == 'undercut':

				url = _um.get_url_for_justifying_argument(True, argument_uid_sys, mode, relation)

			elif relation == 'overbid':
				# if overbid is the 'overbid', it's easy
				#  url = _um.get_url_for_justifying_argument(True, argument_uid_sys, mode, relation)
				# otherwise it will be the attack again
				url = _um.get_url_for_justifying_argument(True, argument_uid_user, mode, attack)

			elif relation == 'rebut':  # if we are having an rebut, everything seems different
				if attack == 'undermine':  # rebutting an undermine will be a support for the initial argument
					url = _um.get_url_for_justifying_statement(True, db_sys_argument.conclusion_uid, mode)
				# rebutting an undercut will be a overbid for the initial argument
				elif attack == 'undercut':
					url = _um.get_url_for_justifying_argument(True, argument_uid_user, mode, 'overbid')
				# rebutting an rebut will be a justify for the initial argument
				elif attack == 'rebut':
					url = _um.get_url_for_justifying_statement(True, db_user_argument.conclusion_uid, mode)

			else:
				url = _um.get_url_for_justifying_argument(True, argument_uid_sys, mode, relation)

			statements_array.append(self.__create_statement_dict(relation, [{'title': rel_dict[relation + '_text'], 'id':relation}], relation, url))

		# last item is the change attack button or step back, if we have bno other attack
		arg_id_sys, new_attack = _rh.get_attack_for_argument(argument_uid_user, issue_uid, self.lang, restriction_on_attacks=attack, restriction_on_arg_uid=argument_uid_sys)
		if new_attack == 'no_other_attack' or new_attack == 'end':
			relation = 'step_back'
			url = 'back' if for_api else 'window.history.go(-1)'
		else:
			relation = 'no_opinion'
			url = _um.get_url_for_reaction_on_argument(True, argument_uid_user, new_attack, arg_id_sys)
			url = url[0:len(url) - 1] + '?rm_bubble=' + str(argument_uid_user) + '/' + attack + '/' + str(argument_uid_sys) + '"'
		statements_array.append(self.__create_statement_dict(relation, [{'title': rel_dict[relation + '_text'], 'id':relation}], relation, url))

		return statements_array

	def prepare_item_dict_for_choosing(self, argument_or_statement_id, pgroup_ids, is_argument, is_supportive, application_url, issue_uid, for_api):
		"""

		:param argument_or_statement_id:
		:param pgroup_ids:
		:param is_argument:
		:param is_supportive:
		:param application_url:
		:param issue_uid:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_item_dict_for_choosing', 'def')
		statements_array = []
		slug = DBDiscussionSession.query(Issue).filter_by(uid=issue_uid).first().get_slug()
		_um = UrlManager(application_url, slug, for_api)
		conclusion = argument_or_statement_id if not is_argument else None
		argument = argument_or_statement_id if is_argument else None

		for group_id in pgroup_ids:
			db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=group_id).all()
			premise_array = []
			for premise in db_premises:
				text = get_text_for_statement_uid(premise.statement_uid)
				premise_array.append({'title': text, 'id': premise.statement_uid})

			# get attack for each premise, so the urls will be unique
			logger('DictionaryHelper', 'prepare_item_dict_for_choosing', 'premisesgroup_uid: ' + str(group_id) +
			       ', conclusion_uid: ' + str(conclusion) +
			       ', argument_uid: ' + str(argument) +
			       ', is_supportive: ' + str(is_supportive))
			db_argument = DBDiscussionSession.query(Argument).filter(and_(Argument.premisesgroup_uid == group_id,
																		  Argument.conclusion_uid == conclusion,
																		  Argument.argument_uid == argument,
																		  Argument.is_supportive == is_supportive)).first()
			arg_id_sys, attack = RecommenderHelper().get_attack_for_argument(db_argument.uid, issue_uid, self.lang)
			url = _um.get_url_for_reaction_on_argument(True, db_argument.uid, attack, arg_id_sys)

			statements_array.append(self.__create_statement_dict(str(db_argument.uid), premise_array, 'choose', url))
		# url = 'back' if for_api else 'window.history.go(-1)'
		# text = _t.get(_t.iHaveNoOpinion) + '. ' + _t.get(_t.goStepBack) + '.'
		# statements_array.append(self.__create_statement_dict('no_opinion', text, [{'title': text, 'id': 'no_opinion'}], 'no_opinion', url))
		return statements_array

	def prepare_extras_dict_for_normal_page(self, nickname):
		"""

		:param nickname:
		:return:
		"""
		return self.prepare_extras_dict('', False, False, False, False, False, nickname)

	def prepare_extras_dict(self, current_slug, is_editable, is_reportable, show_bar_icon,
	                        show_display_styles, show_expert_icon, authenticated_userid, argument_id=0,
	                        application_url='', for_api=False,):
		"""

		:param current_slug:
		:param is_editable:
		:param is_reportable:
		:param show_bar_icon:
		:param show_display_styles:
		:param show_expert_icon:
		:param authenticated_userid:
		:param argument_id:
		:param application_url:
		:param for_api:
		:return:
		"""
		logger('DictionaryHelper', 'prepare_extras_dict', 'def')
		_uh = UserHandler()
		_tn = Translator(self.lang)
		_qh = QueryHelper()
		_nh = NotificationHelper()
		is_logged_in = _uh.is_user_logged_in(authenticated_userid)
		nickname = authenticated_userid if authenticated_userid else 'anonymous'
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

		return_dict = dict()
		return_dict['restart_url']		             = UrlManager(application_url, current_slug, for_api).get_slug_url(True)
		return_dict['logged_in']		             = is_logged_in
		return_dict['nickname']		                 = nickname
		return_dict['users_name']		             = str(authenticated_userid)
		return_dict['add_premise_container_style']   = 'display: none'
		return_dict['add_statement_container_style'] = 'display: none'
		return_dict['users_avatar']                  = _uh.get_profile_picture(db_user)
		return_dict['is_user_male']                  = db_user.gender == 'm' if db_user else False
		return_dict['is_user_female']                = db_user.gender == 'f' if db_user else False
		return_dict['is_user_neutral']               = not return_dict['is_user_male'] and not return_dict['is_user_female']
		self.add_language_options_for_extra_dict(return_dict)

		if not for_api:
			return_dict['is_editable']                   = is_editable and is_logged_in
			return_dict['is_reportable']	             = is_reportable
			return_dict['is_admin']			             = _uh.is_user_in_group(authenticated_userid, 'admins')
			return_dict['is_author']			         = _uh.is_user_in_group(authenticated_userid, 'authors')
			return_dict['show_bar_icon']	             = show_bar_icon and False
			return_dict['show_display_style']            = show_display_styles and False
			return_dict['show_expert_icon']              = show_expert_icon and False
			return_dict['close_premise_container']	     = True
			return_dict['close_statement_container']	 = True
			return_dict['date']	                         = datetime.strftime(datetime.now(), '%d.%m.%Y')
			return_dict['title']						 = {'barometer': _tn.get(_tn.opinionBarometer),
															'guided_view': _tn.get(_tn.displayControlDialogGuidedBody),
															'island_view': _tn.get(_tn.displayControlDialogIslandBody),
															'expert_view': _tn.get(_tn.displayControlDialogExpertBody)}
			return_dict['buttons']					     = {'report': _tn.get(_tn.report),
															'report_title': _tn.get(_tn.reportTitle),
															'finish_title': _tn.get(_tn.finishTitle),
															'question_title': _tn.get(_tn.questionTitle),
															'show_all_arguments': _tn.get(_tn.showAllArguments),
															'show_all_users': _tn.get(_tn.showAllUsers),
															'delete_track': _tn.get(_tn.deleteTrack),
															'request_track': _tn.get(_tn.requestTrack),
															'delete_history': _tn.get(_tn.deleteHistory),
															'request_history': _tn.get(_tn.requestHistory),
															'password_submit': _tn.get(_tn.passwordSubmit),
															'contact_submit': _tn.get(_tn.contactSubmit),
															'lets_go': _tn.get(_tn.letsGo),
															'opinion_barometer': _tn.get(_tn.opinionBarometer),
															'edit_statement': _tn.get(_tn.editTitle),
															'more_title': _tn.get(_tn.more),
															'previous': _tn.get(_tn.previous),
															'next': _tn.get(_tn.next),
															'save_my_statement': _tn.get(_tn.saveMyStatement),
															'add_statement_row_title': _tn.get(_tn.addStatementRow),
															'rem_statement_row_title': _tn.get(_tn.remStatementRow),
															'clear_statistics': _tn.get(_tn.clearStatistics),
															'user_options': _tn.get(_tn.userOptions),
															'switch_language': _tn.get(_tn.switchLanguage),
															'login': _tn.get(_tn.login),
															'news_about_dbas': _tn.get(_tn.newsAboutDbas),
															'share_url': _tn.get(_tn.shareUrl),
			                                                'go_back': _tn.get(_tn.letsGoBack),
			                                                'go_home': _tn.get(_tn.letsGoHome),
			                                                'count_of_posts': _tn.get(_tn.countOfPosts),
			                                                'default_view': _tn.get(_tn.defaultView),
			                                                'wide_node_view': _tn.get(_tn.wideView),
			                                                'tight_node_view': _tn.get(_tn.tightView),
			                                                'show_content': _tn.get(_tn.showContent),
			                                                'hide_content': _tn.get(_tn.hideContent)}
			# /return_dict['breadcrumbs']   = breadcrumbs
			message_dict = dict()
			message_dict['new_count']    = _nh.count_of_new_notifications(authenticated_userid)
			message_dict['has_unread']   = (message_dict['new_count'] > 0)
			message_dict['all']		     = _nh.get_notification_for(authenticated_userid)
			message_dict['total']		 = len(message_dict['all'])
			return_dict['notifications'] = message_dict

			# add everything for the island view
			if return_dict['show_display_style']:
				# does an argumente exists?
				db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_id).first()
				if db_argument:
					island_dict = _qh.get_every_attack_for_island_view(argument_id, self.lang)

					db_argument = DBDiscussionSession.query(Argument).filter_by(uid=argument_id).first()
					premise, tmp = get_text_for_premisesgroup_uid(db_argument.premisesgroup_uid, self.lang)
					conclusion = get_text_for_conclusion(db_argument, self.lang)
					island_dict['heading'] = get_text_for_argument_uid(argument_id, self.lang, True)

					island_dict['premise'] = premise[0:1].lower() + premise[1:]
					island_dict['conclusion'] = conclusion[0:1].lower() + conclusion[1:]
					island_dict.update(TextGenerator(self.lang).get_relation_text_dict(island_dict['premise'],
																				  island_dict['conclusion'],
																				  False, False, not db_argument.is_supportive))
					return_dict['island'] = island_dict
				else:
					return_dict['is_editable']		  = False
					return_dict['is_reportable']	  = False
					return_dict['show_bar_icon']	  = False
					return_dict['show_display_style'] = False
					return_dict['title']			  = {'barometer': _tn.get(_tn.opinionBarometer),
					                                     'guided_view': _tn.get(_tn.displayControlDialogGuidedBody),
					                                     'island_view': _tn.get(_tn.displayControlDialogIslandBody),
					                                     'expert_view': _tn.get(_tn.displayControlDialogExpertBody),
					                                     'edit_statement': _tn.get(_tn.editTitle),
					                                     'report_statement': _tn.get(_tn.reportTitle)}
		return return_dict

	def add_discussion_end_text(self, discussion_dict, extras_dict, logged_in, at_start=False, at_dont_know=False,
								at_justify_argumentation=False, at_justify=False, current_premise='', supportive=False):
		"""

		:param discussion_dict: dict()
		:param extras_dict: dict()
		:param logged_in: Boolean
		:param at_start: Boolean
		:param at_dont_know: Boolean
		:param at_justify_argumentation: Boolean
		:param at_justify: Boolean
		:param current_premise: id
		:param supportive: supportive
		:return: None
		"""
		logger('DictionaryHelper', 'add_discussion_end_text', 'main')
		_tn = Translator(self.lang)
		current_premise = current_premise[0:1].lower() + current_premise[1:]

		if at_start:
			discussion_dict['mode'] = 'start'
			user_text = _tn.get(_tn.firstPositionText) + '<br>'
			user_text += _tn.get(_tn.pleaseAddYourSuggestion) if logged_in else (_tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.feelFreeToLogin))
			discussion_dict['bubbles'].append(self.__create_speechbubble_dict(False, False, True, 'end', '', user_text))
			if logged_in:
				extras_dict['add_statement_container_style'] = ''  # this will remove the 'display: none;'-style
				extras_dict['close_statement_container'] = False
			extras_dict['show_display_style']	= False
			extras_dict['show_bar_icon']	    = False
			extras_dict['is_editable']		    = False
			extras_dict['is_reportable']		= False

		elif at_justify_argumentation:
			discussion_dict['mode'] = 'justify_argumentation'
			if logged_in:
				extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
			extras_dict['close_premise_container'] = False
			extras_dict['show_display_style'] = False
			if logged_in:
				mid_text = _tn.get(_tn.firstOneReason)
				discussion_dict['bubbles'].append(self.__create_speechbubble_dict(False, False, True, 'end', '', mid_text))
			# else:
			# 	mid_text = _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.feelFreeToLogin)


		elif at_dont_know:
			discussion_dict['mode'] = 'dont_know'
			sys_text  = _tn.get(_tn.firstOneInformationText) + ' <strong>' + current_premise + '</strong>, '
			sys_text += _tn.get(_tn.soThatOtherParticipantsDontHaveOpinionRegardingYourOpinion) + '.'
			mid_text  = _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.discussionEndLinkText)
			discussion_dict['bubbles'].append(self.__create_speechbubble_dict(False, True, False, 'end', '', sys_text))
			discussion_dict['bubbles'].append(self.__create_speechbubble_dict(False, False, True, 'end', '', mid_text))

		elif at_justify:
			discussion_dict['mode'] = 'justify'
			mid_text = _tn.get(_tn.firstPremiseText1) + ' <strong>' + current_premise + '</strong>'
			if not supportive:
				mid_text += ' ' + _tn.get(_tn.doesNotHold)
			mid_text += '.<br>'
			# pretty prints
			if discussion_dict['bubbles'][-1]['is_system'] and discussion_dict['bubbles'][-2]['message'] == _tn.get(_tn.now):
				discussion_dict['bubbles'].remove(discussion_dict['bubbles'][-1])
				discussion_dict['bubbles'].remove(discussion_dict['bubbles'][-1])
			if logged_in:
				extras_dict['add_premise_container_style'] = ''  # this will remove the 'display: none;'-style
				mid_text += _tn.get(_tn.firstPremiseText2)
			else:
				mid_text += _tn.get(_tn.discussionEnd) + ' ' + _tn.get(_tn.discussionEndLinkText)

			discussion_dict['bubbles'].append(self.__create_speechbubble_dict(False, False, True, 'end', '', mid_text))
			extras_dict['close_premise_container'] = False
			extras_dict['show_display_style']	   = False
			extras_dict['show_bar_icon']		   = False
			extras_dict['is_editable']			   = False
			extras_dict['is_reportable']		   = False

		else:
			mid_text = _tn.get(_tn.discussionEnd) + ' ' + (_tn.get(_tn.discussionEndLinkText) if logged_in else _tn.get(_tn.feelFreeToLogin))
			discussion_dict['bubbles'].append(self.__create_speechbubble_dict(False, True, False, '', '', mid_text))

	def add_language_options_for_extra_dict(self, extras_dict):
		"""

		:param extras_dict:
		:return:
		"""
		logger('DictionaryHelper', 'add_language_options_for_extra_dict', 'def')
		lang_is_en = (self.lang != 'de')
		lang_is_de = (self.lang == 'de')
		extras_dict.update({
			'lang_is_de': lang_is_de,
			'lang_is_en': lang_is_en,
			'link_de_class': ('active' if lang_is_de else ''),
			'link_en_class': ('active' if lang_is_en else '')
		})

	@staticmethod
	def __create_statement_dict(uid, premises, attitude, url):
		"""

		:param uid:
		:param premises:
		:param attitude:
		:param url:
		:return:
		"""
		return {
			'id': 'item_' + str(uid),
			'premises': premises,
			'attitude': attitude,
			'url': url}

	def __create_speechbubble_dict(self, is_user, is_system, is_status, uid, url, message, omit_url=False, argument_uid=None, statement_uid=None, nickname=None, is_up_vote=True):
		"""

		:param is_user:
		:param is_system:
		:param is_status:
		:param uid:
		:param url:
		:param message:
		:param omit_url:
		:param argument_uid:
		:param statement_uid:
		:param nickname:
		:param is_up_vote:
		:return:
		"""
		speech = dict()
		speech['is_user']            = is_user
		speech['is_system']          = is_system
		speech['is_status']          = is_status
		speech['id']                 = uid if len(str(uid)) > 0 else 'None'
		speech['url']                = url if len(str(url)) > 0 else 'None'
		speech['message']            = message
		speech['omit_url']           = omit_url
		speech['data_type']          = 'argument' if argument_uid else 'statement' if statement_uid else 'None'
		speech['data_argument_uid']  = str(argument_uid)
		speech['data_statement_uid'] = str(statement_uid)
		db_votecounts                = None

		if argument_uid:
			db_votecounts = DBDiscussionSession.query(VoteArgument).filter(and_(VoteArgument.argument_uid == argument_uid,
			                                                                    VoteArgument.is_up_vote == is_up_vote,
			                                                                    VoteArgument.is_valid == True)).all()
		elif statement_uid:
			db_votecounts = DBDiscussionSession.query(VoteStatement).filter(and_(VoteStatement.statement_uid == statement_uid,
			                                                                     VoteStatement.is_up_vote == is_up_vote,
			                                                                     VoteStatement.is_valid == True)).all()

		_t = Translator(self.lang)
		diff = 0
		if nickname:
			diff = 1 if nickname != 'anonymous' else 0
		votecounts = len(db_votecounts) - diff if db_votecounts else 0

		if votecounts == 0:
			speech['votecounts_message'] = _t.get(_t.voteCountTextFirst) + '.'
		elif votecounts == 1:
			speech['votecounts_message'] = _t.get(_t.voteCountTextOneOther) + '.'
		else:
			speech['votecounts_message'] = str(votecounts) + ' ' + _t.get(_t.voteCountTextMore) + '.'
		speech['votecounts'] = votecounts

		return speech

	@staticmethod
	def __save_speechbubble(bubble_dict, db_user, session_id, related_breadcrumb, transaction, argument_uid=None, statement_uid=None):
		"""

		:param bubble_dict:
		:param db_user:
		:param session_id:
		:param related_breadcrumb:
		:param transaction:
		:param argument_uid:
		:param statement_uid:
		:return:
		"""
		if not db_user:
			user = 'anonymous'
			db_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
			if not db_user:
				return False

		is_user   = bubble_dict['is_user']
		is_system = bubble_dict['is_system']
		is_status = bubble_dict['is_status']
		latest_bubble = DBDiscussionSession.query(Bubble).filter(and_(Bubble.breadcrumb_uid == related_breadcrumb['uid'],
		                                                              Bubble.author_uid == db_user.uid)).order_by(Bubble.uid.desc()).first()
		latest_specific_bubble = DBDiscussionSession.query(Bubble).filter(and_(Bubble.author_uid == db_user.uid,
		                                                                       Bubble.is_user == is_user,
																			   Bubble.is_system == is_system,
																			   Bubble.is_status == is_status)).order_by(Bubble.uid.desc()).first()
		if latest_bubble and latest_bubble.content == bubble_dict['message'] or \
						latest_specific_bubble and latest_specific_bubble.content == bubble_dict['message']:
				return False

		logger('DictionaryHelper', '__save_speechbubble', 'bubble_id = ' + str(bubble_dict['id']) +
		       ', user=' + str(db_user.uid) +
		       ', content=' + str(bubble_dict['message']) +
		       ', is_user=' + str(bubble_dict['is_user']) +
		       ', is_system=' + str(bubble_dict['is_system']) +
		       ', is_status=' + str(bubble_dict['is_status']) +
		       ', session_id=' + str(session_id) +
		       ', breadcrumb_uid=' + str(related_breadcrumb['uid']) +
		       ', argument_uid=' + str(argument_uid) +
		       ', statement_uid=' + str(statement_uid))
		DBDiscussionSession.add(Bubble(bubble_id=bubble_dict['id'],
		                               user=str(db_user.uid),
		                               content=bubble_dict['message'],
		                               is_user=bubble_dict['is_user'],
		                               is_system=bubble_dict['is_system'],
		                               is_status=bubble_dict['is_status'],
		                               session_id=session_id,
		                               breadcrumb_uid=str(related_breadcrumb['uid']),
		                               related_argument_uid=argument_uid,
									   related_statement_uid=statement_uid))
		transaction.commit()
		return True

	def __create_speechbubble_history(self, breadcrumbs, nickname, session_id):
		"""

		:param breadcrumbs:
		:param nickname:
		:param session_id:
		:return:
		"""
		logger('DictionaryHelper', '__create_speechbubble_history', 'main')
		bubble_history = []
		is_user_anonym = not nickname
		if is_user_anonym:
			nickname = 'anonymous'
		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()
		for crumb in breadcrumbs:
			if is_user_anonym:
				history = DBDiscussionSession.query(Bubble).filter(and_(Bubble.breadcrumb_uid == crumb['uid'],
				                                                        Bubble.author_uid == db_user.uid,
				                                                        Bubble.session_id == session_id)).all()
			else:
				history = DBDiscussionSession.query(Bubble).filter(and_(Bubble.breadcrumb_uid == crumb['uid'],
				                                                        Bubble.author_uid == db_user.uid)).all()
			for h in history:
				is_user   = h.is_user
				is_system = h.is_system
				is_status = h.is_status
				uid       = crumb['uid']
				url       = crumb['url']
				content   = h.content
				rel_arg   = h.related_argument_uid
				rel_stat  = h.related_statement_uid
				expr0     = re.search(re.compile(r"/t/"), url)
				expr1     = re.search(re.compile(r"/t$"), url)
				group0    = expr0.group(0) if expr0 else None
				group1    = expr1.group(0) if expr1 else None
				is_supp   = True if group0 or group1 else False
				bubble_history.append(self.__create_speechbubble_dict(is_user, is_system, is_status, uid, url, content, False, rel_arg, rel_stat, nickname, is_supp))

		return bubble_history

	@staticmethod
	def __append_bubble(bubbles_array, bubble):
		"""
		
		:param bubbles_array: 
		:param bubble: 
		:return: 
		"""
		# sanity check
		if len(bubbles_array) > 2:
			for i in range(-3, 0):
				if bubbles_array[i]['message'] == bubble['message']:
					bubbles_array.remove(bubbles_array[i])

		bubbles_array.append(bubble)

	@staticmethod
	def remove_last_bubble_for_discussion_reaction(nickname, session_id, bubble_param):
		"""
		Removes the last Bubble of the user if the linked url ends with the bubble params

		:param nickname:
		:param session_id:
		:param bubble_param:
		:return:
		"""
		logger('DictionaryHelper', 'remove_last_bubble_for_discussion_reaction', 'nickname: ' + str(nickname) + ', session: ' + str(session_id))
		if not nickname:
			nickname = 'anonymous'

		db_user = DBDiscussionSession.query(User).filter_by(nickname=nickname).first()

		if nickname == 'anonymous':
			bubble = DBDiscussionSession.query(Bubble).filter(and_(Bubble.author_uid == db_user.uid,
			                                                       Bubble.session_id == session_id)).order_by(Bubble.uid.desc()).first()
		else:
			bubble = DBDiscussionSession.query(Bubble).filter_by(author_uid=db_user.uid).order_by(Bubble.uid.desc()).first()

		if bubble and DBDiscussionSession.query(Breadcrumb).filter_by(uid=bubble.breadcrumb_uid).first().url.endswith(bubble_param):
			DBDiscussionSession.query(Bubble).filter_by(uid=bubble.uid).delete()
			return True
		return False