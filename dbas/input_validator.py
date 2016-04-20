"""
Methods for validating input params given via url or ajax

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from .database import DBDiscussionSession
from .database.discussion_model import Argument, Statement, Premise, PremiseGroup
from sqlalchemy import and_


class Validator:
	"""
	Methods for saving or reading data out of current session. Additionally these values can be aligned.
	"""

	@staticmethod
	def save_params_in_session(session, user_arg_uid, sys_arg_uid, mood, reaction):
		"""
		Saves values in session

		:param session: request.session
		:param user_arg_uid: Argument.uid
		:param sys_arg_uid: Argument.uid
		:param mood: Srting
		:param reaction: String
		:return:
		"""
		session['user_arg_uid'] = user_arg_uid
		session['sys_arg_uid'] = sys_arg_uid
		session['mood'] = mood
		session['reaction'] = reaction

	@staticmethod
	def validate_params_with_session(session=None, user_arg_uid=None, sys_arg_uid=None, mood=None, reaction=None):
		"""
		Compares given values with the values in current session

		:param session: request.session
		:param user_arg_uid: Argument.uid
		:param sys_arg_uid: Argument.uid
		:param mood: String
		:param reaction: String
		:return: True, 0, 0 if everything is fine or False, !=0 and the stored value.
		:return: False, -1, stored value if user_arg_uid is wrong
		:return: False, -2, stored value if sys_arg_uid is wrong
		:return: False, -3, stored value if mood is wrong
		:return: False, -4, stored value if reaction is wrong

		"""
		if user_arg_uid and session['user_arg_uid'] != user_arg_uid:
			return False, -1, session['user_arg_uid']
		if sys_arg_uid and session['sys_arg_uid'] != sys_arg_uid:
			return False, -2, session['sys_arg_uid']
		if mood and session['mood'] != mood:
			return False, -3, session['mood']
		if reaction and session['reaction'] != reaction:
			return False, -4, session['reaction']
		return True, 0, 0

	@staticmethod
	def check_reaction(attacked_arg_uid, attacking_arg_uid, relation):
		"""
		Checks whether the attacked argument uid and the attacking argument uid are connected via the given relation

		:param attacking_arg_uid: Argument.uid
		:param relation: String
		:return: Boolean
		"""
		if relation == 'undermine':
			db_attacking_arg = DBDiscussionSession.query(Argument).filter_by(uid=attacking_arg_uid).join(Statement).first()
			if not db_attacking_arg:
				return False

			db_attacked_premise = DBDiscussionSession.query(Premise).filter_by(statement_uid=db_attacking_arg.statements.uid).first()
			if not db_attacked_premise:
				return False

			db_attacked_pgroup = DBDiscussionSession.query(PremiseGroup).filter_by(uid=db_attacked_premise.premisesgroup_uid).join(Statement).first()
			if not db_attacked_pgroup:
				return False

			db_premises_in_attacked_pgroup = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=db_attacked_premise.premisesgroup_uid).first()
			if len(db_premises_in_attacked_pgroup) != 1:
				return False

			db_attacked_arg = DBDiscussionSession.query(Argument).filter(and_(Argument.uid == attacked_arg_uid,
			                                                                  Argument.premisesgroup_uid == db_attacked_premise.premisesgroup_uid)).first()
			return True if db_attacked_arg else False

		elif relation == 'undercut':
			db_attacking_arg = DBDiscussionSession.query(Argument).filter(and_(Argument.uid == attacking_arg_uid,
			                                                                   Argument.argument_uid == attacked_arg_uid)).first()
			return True if db_attacking_arg else False
		elif relation == 'rebut':
			db_attacking_arg = DBDiscussionSession.query(Argument).filter_by(uid=attacking_arg_uid).join(Statement).first()
			if not db_attacking_arg:
				return False

			db_attacked_arg = DBDiscussionSession.query(Argument).filter_by(uid=attacked_arg_uid).join(Statement).first()
			if not db_attacked_arg:
				return False

			return True if db_attacking_arg.conclusion_uid == db_attacked_arg.conclusion_uid and db_attacked_arg.conclusion_uid is not None else False
		else:
			return False
