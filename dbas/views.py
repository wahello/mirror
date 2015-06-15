import transaction

import time

import smtplib
from socket import error as socket_error

from validate_email import validate_email
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from pyramid.security import remember, forget
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from .database import DBSession
from .database.model import User, Group, Issue, Position, Argument, RelationArgPos
from .helper import PasswordHandler, PasswordGenerator, logger, QueryHelper, DictionaryHelper

class Dbas(object):
	def __init__(self, request):
		"""
		Object initialization
		:param request: init http request
		:return:
		"""
		self.request = request

	# main page
	@view_config(route_name='main_page', renderer='templates/index.pt', permission='everybody')
	def main_page(self):
		logger('main_page', 'def', 'main page')
		"""
		View configuration for the main page
		:return:
		"""
		return dict(
			title='Main',
			project='DBAS',
			logged_in=self.request.authenticated_userid
		)

	# login page
	@view_config(route_name='main_login', renderer='templates/login.pt', permission='everybody')
	@forbidden_view_config(renderer='templates/login.pt')
	def main_login(self):
		"""
		View-configuration for the login template
		:return:
		"""
		# check for already logged in users
		logger('main_login', 'def', 'login page')
		if self.request.authenticated_userid:
			return HTTPFound(location=self.request.route_url('main_content'))

		login_url = self.request.route_url('main_login')
		referrer = self.request.url

		if referrer == login_url:
			referrer = self.request.route_url('main_page')  # never use the login form itself as came_from
		came_from = self.request.params.get('came_from', referrer)

		# some variables
		message = ''
		password = ''
		passwordconfirm = ''
		firstname = ''
		surname = ''
		nickname = ''
		email = ''
		reg_failed = False
		log_failed = False
		reg_success = False
		password_handler = PasswordHandler()
		password_generator = PasswordGenerator()

		# case: user login
		if 'form.login.submitted' in self.request.params:
			logger('main_login', 'form.login.submitted', 'requesting params')

			# requesting parameters
			nickname = self.request.params['nickname']
			password = self.request.params['password']
			db_user = DBSession.query(User).filter_by(nickname=nickname).first()

			# check for user and password validations
			if not db_user:
				logger('main_login', 'form.login.submitted', 'user \'' + nickname + '\' does not exists')
				message = 'User does not exists'
			elif not db_user.validate_password(password):  # dbUser.validate_password(password)
				logger('main_login', 'form.login.submitted', 'wrong password')
				message = 'Wrong password'
			else:
				logger('main_login', 'form.login.submitted', 'login successful')
				headers = remember(self.request, nickname)

				# update timestamp
				logger('main_login', 'form.login.submitted', 'update login timestamp')
				db_user.update_last_logged()
				transaction.commit()

				return HTTPFound(
					location=self.request.route_url('main_content'),
					headers=headers
				)
			log_failed = True

		# case: user registration
		if 'form.registration.submitted' in self.request.params:
			logger('main_login', 'form.registration.submitted', 'Requesting params')

			# getting parameter
			firstname = self.request.params['firstname']
			surname = self.request.params['surname']
			nickname = self.request.params['nickname']
			email = self.request.params['email']
			password = self.request.params['password']
			passwordconfirm = self.request.params['passwordconfirm']

			# database queries mail verification
			db_nick = DBSession.query(User).filter_by(nickname=nickname).first()
			db_mail = DBSession.query(User).filter_by(email=email).first()
			logger('main_login', 'form.registration.submitted', 'Validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			# are the password equal?
			if not password == passwordconfirm:
				logger('main_login', 'form.registration.submitted', 'Passwords are not equal')
				message = 'Passwords are not equal'
				password = ''
				passwordconfirm = ''
				reg_failed = True
			# is the nick already taken?
			elif db_nick:
				logger('main_login', 'form.registration.submitted', 'Nickname \'' + nickname + '\' is taken')
				message = 'Nickname is taken'
				nickname = ''
				reg_failed = True
			# is the email already taken?
			elif db_mail:
				logger('main_login', 'form.registration.submitted', 'E-Mail \'' + email + '\' is taken')
				message = 'E-Mail is taken'
				email = ''
				reg_failed = True
			# is the email valid?
			elif not is_mail_valid:
				logger('main_login', 'form.registration.submitted', 'E-Mail \'' + email + '\' is not valid')
				message = 'E-Mail is not valid'
				email = ''
				reg_failed = True
			else:
				# getting the editors group
				group = DBSession.query(Group).filter_by(name='editors').first()

				# does the group exists?
				if not group:
					message = 'An error occured, please try again later or contact the author'
					reg_failed = True
					logger('main_login', 'form.registration.submitted', 'Error occured')
				else:
					# creating a new user with hased password
					logger('main_login', 'form.registration.submitted', 'Adding user')
					hashedPassword = password_handler.get_hashed_password(self, password)
					newuser = User(firstname=firstname, surname=surname, email=email,
					               nickname=nickname, password=hashedPassword)
					newuser.group = group.uid
					DBSession.add(newuser)
					transaction.commit()

					# sanity check, whether the user exists
					checknewuser = DBSession.query(User).filter_by(nickname=nickname).first()
					if checknewuser:
						logger('main_login', 'form.registration.submitted', 'New data was added with uid ' + str(checknewuser.uid))
						message = 'Your account was added and you are able to login now'
						reg_success = True
					else:
						logger('main_login', 'form.registration.submitted', 'New data was not added')
						message = 'Your account with the nick could not be added. Please try again or contact the author'
						reg_failed = True

		# case: user password request
		if 'form.passwordrequest.submitted' in self.request.params:
			logger('main_login', 'form.passwordrequest.submitted', 'requesting params')
			email = self.request.params['email']
			logger('main_login', 'form.passwordrequest.submitted', 'email is ' + email)
			db_user = DBSession.query(User).filter_by(email=email).first()

			# does the user exists?
			if db_user:
				# get password and hashed password
				pwd = password_generator.get_rnd_passwd()
				logger('main_login', 'form.passwordrequest.submitted', 'New password is ' + pwd)
				hashedpwd = password_handler.get_hashed_password(pwd)
				logger('main_login', 'form.passwordrequest.submitted', 'New hashed password is ' + hashedpwd)

				# set the hased one
				db_user.password = hashedpwd
				DBSession.add(db_user)
				transaction.commit()
				message, reg_success, reg_failed = password_handler.send_password_to_email(self.request, pwd)

				# logger
				if reg_success:
					logger('main_login', 'form.passwordrequest.submitted', 'New password was sent')
				elif reg_failed:
					logger('main_login', 'form.passwordrequest.submitted', 'Error occured')
			else:
				logger('main_login', 'form.passwordrequest.submitted', 'Mail unknown')
				message = 'The given e-mail address is unkown'
				reg_failed = True

		return dict(
			title='Login', 
			project='DBAS', 
			message=message, 
			url=self.request.application_url + '/login', 
			came_from=came_from, 
			password=password, 
			passwordconfirm=passwordconfirm, 
			firstname=firstname, 
			surname=surname, 
			nickname=nickname, 
			email=email, 
			login_failed=log_failed, 
			registration_failed=reg_failed, 
			registration_success=reg_success, 
			logged_in=self.request.authenticated_userid 
		)

	# logout page
	@view_config(route_name='main_logout', renderer='templates/logout.pt', permission='use')
	def main_logout(self):
		"""
		View configuration for the logout view. This will will automatically redirect to main_logout_redirect via JS
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_logout', 'def', 'user will be logged out')
		return dict(
			title='Logout',
			project='DBAS',
			logged_in=self.request.authenticated_userid
		)

	# logout redirect page
	@view_config(route_name='main_logout_redirect', permission='use')
	def main_logout_redirect(self):
		"""
		View configuration for the redirect logout view. This method will forget the headers of self.request
		:return: HTTPFound with location for the main page
		"""
		logger('main_logout_redirect', 'def', 'headers are now forgotten')
		logger('main_logout_redirect', 'def', 'redirecting to the main_page')
		headers = forget(self.request)
		return HTTPFound(
			location=self.request.route_url('main_page'),
			headers=headers
		)

	# contact page
	@view_config(route_name='main_contact', renderer='templates/contact.pt', permission='everybody')
	def main_contact(self):
		"""
		View configuration for the contact view.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_contact', 'def', 'contact page')
		contact_error = False
		send_message = False
		message = ''
		name = ''
		email = ''
		phone = ''
		content = ''
		spam = ''
		if 'form.contact.submitted' in self.request.params:
			logger('main_contact', 'form.contact.submitted', 'requesting params')
			name = self.request.params['name']
			email = self.request.params['mail']
			phone = self.request.params['phone']
			content = self.request.params['content']
			spam = self.request.params['spam']

			logger('main_contact', 'form.contact.submitted', 'validating email')
			is_mail_valid = validate_email(email, check_mx=True)

			## sanity checks
			# check for empty name
			if not name:
				logger('main_contact', 'form.contact.submitted', 'name empty')
				contact_error = True
				message = "Your name is empty!"

			# check for non valid mail
			elif not is_mail_valid:
				logger('main_contact', 'form.contact.submitted', 'mail is not valid')
				contact_error = True
				message = "Your e-mail is empty!"

			# check for empty content
			elif not content:
				logger('main_contact', 'form.contact.submitted', 'content is empty')
				contact_error = True
				message = "Your content is empty!"

			# check for empty name
			elif (not spam) or (not spam.isdigit()) or (not int(spam) == 4):
				logger('main_contact', 'form.contact.submitted', 'empty or wrong anti-spam answer')
				contact_error = True
				message = "Your anti-spam message is empty or wrong!"

			else:
				subject = 'Contact D-BAS'
				systemmail = 'krauthoff@cs.uni-duesseldorf.de'
				body = 'Name: ' + name + '\n' + 'Mail: ' + email + '\n' + 'Phone: ' + phone + '\n' + 'Message:\n' + content
				logger('main_contact', 'form.contact.submitted', 'sending mail')
				mailer = get_mailer(self.request)
				message = Message(subject = subject,
			   					  sender = systemmail,
			   					  recipients = ["krauthoff@cs.uni-duesseldorf.de",email],
			   					  body = body
			   					)
				# try sending an catching errors
				try:
					mailer.send_immediately(message, fail_silently=False)
					send_message = True
				except smtplib.SMTPConnectError as exception:
					logger('main_contact', 'form.contact.submitted', 'error while sending')
					logger('main_contact', 'exception smtplib.SMTPConnectError smtp_code', str(exception.smtp_code))
					logger('main_contact', 'exception smtplib.SMTPConnectError smtp_error', str(exception.smtp_error))
					contact_error = True
					message = 'Your message could not be send due to a system error! (' + 'smtp_code '\
							  + str(exception.smtp_code) + ' || smtp_error ' + str(exception.smtp_error) + ')'
				except socket_error as serr:
					logger('main_contact', 'form.contact.submitted', 'error while sending')
					logger('main_contact', 'form.contact.submitted', 'socket_error ' + str(serr))
					contact_error = True
					message = 'Your message could not be send due to a system error! (' + 'socket_error ' + str(serr) + ')'

		return dict(
			title='Contact',
			project='DBAS',
			logged_in=self.request.authenticated_userid,
			was_message_send=send_message,
			contact_error=contact_error,
			message=message,
			name=name,
			mail=email,
			phone=phone,
			content=content,
			spam=spam
		)

	# content page, after login
	@view_config(route_name='main_content', renderer='templates/content.pt', permission='use')
	def main_content(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_content', 'def', 'main')
		db_issue = DBSession.query(Issue).filter_by(uid=1).first()
		issue = 'none'
		date = 'empty'
		logger('main_content', 'def', 'check for an issue')
		statement_inserted = False
		msg = ''

		# get the current issue
		if db_issue:
			logger('main_content', 'def', 'issue exists')
			issue = db_issue.text
			date = db_issue.date
		else:
			logger('main_content', 'def', 'issue does not exists')

		# adding a statement
		# if 'form.contact.submitted' in self.request.params:
		# msg = 'Statement could not be added (not implemented yet)!'
		# statement_inserted = False

		# checks whether the current user is admin
		is_admin = QueryHelper().is_user_admin(self.request.authenticated_userid)

		return dict(
			title='Content',
			project='DBAS',
			logged_in=self.request.authenticated_userid,
			message=msg,
			issue=issue,
			date=date,
			is_admin=is_admin,
			was_statement_inserted=statement_inserted,
		)

	# settings page, when logged in
	@view_config(route_name='main_settings', renderer='templates/settings.pt', permission='use')
	def main_settings(self):
		"""
		View configuration for the content view. Only logged in user can reach this page.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_settings', 'def', 'main')
		
		oldpw = ''
		newpw = ''
		confirmpw = ''
		message = ''
		error = False
		success = False

		db_user_firstname = 'unknown'
		db_user_surname = 'unknown'
		db_user_nickname = 'unknown'
		db_user_mail = 'unknown'
		db_user_group = 'unknown'

		db_user = DBSession.query(User).filter_by(nickname=str(self.request.authenticated_userid)).first()
		if db_user:
			db_user_firstname = db_user.firstname
			db_user_surname = db_user.surname
			db_user_nickname = db_user.nickname
			db_user_mail = db_user.email
			db_user_group = DBSession.query(Group).filter_by(uid=db_user.group).first()
			if db_user_group:
				db_user_group = db_user_group.name

		if 'form.passwordchange.submitted' in self.request.params:
			logger('main_settings', 'form.changepassword.submitted', 'requesting params')
			old_pw = self.request.params['passwordold']
			new_pw = self.request.params['password']
			confirmpw = self.request.params['passwordconfirm']

			# is the old password given?
			if not old_pw:
				logger('main_settings', 'form.changepassword.submitted', 'old pwd is empty')
				message = 'The old password field is empty.'
				error = True
			# is the new password given?
			elif not new_pw:
				logger('main_settings', 'form.changepassword.submitted', 'new pwd is empty')
				message = 'The new password field is empty.'
				error = True
			# is the cofnrimation password given?
			elif not confirmpw:
				logger('main_settings', 'form.changepassword.submitted', 'confirm pwd is empty')
				message = 'The password confirmation field is empty.'
				error = True
			# is new password equals the confirmation?
			elif not new_pw == confirmpw:
				logger('main_settings', 'form.changepassword.submitted', 'new pwds not equal')
				message = 'The new passwords are not equal'
				error = True
			# is new old password equals the new one?
			elif oldpw == new_pw:
				logger('main_settings', 'form.changepassword.submitted', 'pwds are the same')
				message = 'The new and old password are the same'
				error = True
			else:
				# is the old password valid?
				if not db_user.validate_password(oldpw):
					logger('main_settings', 'form.changepassword.submitted', 'old password is wrong')
					message = 'Your old password is wrong.'
					error = True
				else:
					logger('main_login', 'form.passwordrequest.submitted', 'new password is ' + new_pw)
					password_handler = PasswordHandler()
					hashed_pw = password_handler.get_hashed_password(self, new_pw)
					logger('main_login', 'form.passwordrequest.submitted', 'New hashed password is ' + hashed_pw)

					# set the hased one
					db_user.password = hashed_pw
					DBSession.add(db_user)
					transaction.commit()

					logger('main_settings', 'form.changepassword.submitted', 'password was changed')
					message = 'Your password was changed'
					success = True

		return dict(
			title='Settings',
			project='DBAS',
			logged_in=self.request.authenticated_userid,
			passwordold=oldpw,
			password=newpw,
			passwordconfirm=confirmpw,
			change_error=error,
			change_success=success,
			message=message,
			db_firstname=db_user_firstname,
			db_surname=db_user_surname,
			db_nickname=db_user_nickname,
			db_mail=db_user_mail,
			db_group=db_user_group
		)

	# news page for everybody
	@view_config(route_name='main_news', renderer='templates/news.pt', permission='everybody')
	def main_news(self):
		"""
		View configuration for the news.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_news', 'def', 'main')
		return dict(
			title='News',
			project='DBAS',
			logged_in=self.request.authenticated_userid
		)

	# impressum
	@view_config(route_name='main_impressum', renderer='templates/impressum.pt', permission='everybody')
	def main_impressum(self):
		"""
		View configuration for the impressum.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('main_impressum', 'def', 'main')
		return dict(
			title='Impressum',
			project='DBAS',
			logged_in=self.request.authenticated_userid
		)

	# 404 page
	@notfound_view_config(renderer='templates/404.pt')
	def notfound(self):
		"""
		View configuration for the impressum.
		:return: dictionary with title and project name as well as a value, weather the user is logged in
		"""
		logger('notfound', 'def', 'view \'' + self.request.view_name + '\' not found')
		self.request.response.status = 404
		return dict(
			title='Error',
			project='DBAS',
			page_notfound_viewname=self.request.view_name,
			logged_in=self.request.authenticated_userid
		)

	# ajax - getting all positions
	@view_config(route_name='ajax_all_positions', renderer='json')
	def get_ajax_all_positions(self):
		"""
		Returns all positions as dictionary with uid <-> value
		:return: list of all positions
		"""
		logger('ajax_all_positions', 'def', 'main')
		db_positions = DBSession.query(Position).all()
		logger('ajax_all_positions', 'def', 'get all positions')

		return_dict = {}

		if db_positions:
			logger('ajax_all_positions', 'def', 'iterate all positions')
			# get every position
			for pos in db_positions:
				logger('ajax_all_positions', 'position iterator ' + str(pos.uid) + ' of ' + str(len(db_positions)-1),
				       "uid: " + str(pos.uid) + "   val: " + pos.text)
				return_dict[str(pos.uid)] = pos.text

		dictionaryHelper = DictionaryHelper()
		return_json = dictionaryHelper.dictionarty_to_json_array(return_dict, True)

		return return_json

	# ajax - getting every user, and returns dicts with name <-> group
	@view_config(route_name='ajax_all_users', renderer='json')
	def get_ajax_all_users(self):
		"""
		Returns all users as dictionary with name <-> group
		:return: list of all positions
		"""
		logger('get_ajax_users', 'def', 'main')
		logger('get_ajax_users', 'def', 'get all users')
		db_users = DBSession.query(User).all()
		logger('get_ajax_users', 'def', 'get all groups')

		db_groups = DBSession.query(Group).all()
		groups = {}
		for g in db_groups:
			logger('get_ajax_users', 'def', str(g.uid) + " - " + g.name)
			groups[str(g.uid)] = g.name

		return_dict = {}

		if db_users:
			logger('get_ajax_users', 'def', 'iterate all users')
			for user in db_users:
				return_user = {}
				return_user['uid']         = user.uid
				return_user['firstname']   = user.firstname
				return_user['surname']     = user.surname
				return_user['nickname']    = user.nickname
				return_user['email']       = user.email
				return_user['group']       = groups.get(str(user.group))
				return_user['last_logged'] = str(user.last_logged)
				return_user['registered']  = str(user.registered)
				logger('get_ajax_users', 'user iterator ' + str(user.uid) + ' of ' + str(len(db_users)),
							"uid: " + str(user.uid)
							+ ", firstname: " + user.firstname
							+ ", surname: " + user.surname
							+ ", nickname: " + user.nickname
							+ ", email: " + user.email
							+ ", group: " + groups.get(str(user.group))
							+ ", last_logged: " + str(user.last_logged)
							+ ", registered: " + str(user.registered)
				       )
				return_dict[user.uid] = return_user

		logger('get_ajax_users', 'def', 'SLEEEEEPING')
		time.sleep(1)

		dictionaryHelper = DictionaryHelper()
		return_json = dictionaryHelper.dictionarty_to_json_array(return_dict, True)

		return return_json

	# ajax - getting complete track of the user
	@view_config(route_name='ajax_manage_user_track', renderer='json')
	def ajax_manage_user_track(self):
		"""
		Request the complete user track
		:return:
		"""
		logger('ajax_manage_user_track', 'def', 'main')

		nickname = 'unknown'
		get_data = ''
		try:
			logger('ajax_manage_user_track', 'def', 'read params')
			nickname = str(self.request.authenticated_userid)
			get_data = self.request.params['get_data']
			logger('ajax_manage_user_track', 'def', 'nickname ' + nickname + ', get ' + get_data)
		except KeyError as e:
			logger('ajax_manage_user_track', 'error', repr(e))

		return_dict = {}
		if get_data == '1':
			logger('ajax_manage_user_track', 'def', 'get track data')
			return_dict = QueryHelper().get_track_for_user(DBSession, nickname)
		else:
			logger('ajax_manage_user_track', 'def', 'remove track data')
			return_dict['removed data'] = 'true'
			QueryHelper().del_track_for_user(DBSession, transaction, nickname)

		dictionary_helper = DictionaryHelper()
		return_json = dictionary_helper.dictionarty_to_json_array(return_dict, True)

		return return_json

	# ajax - getting every argument, which is connected to the given position uid
	@view_config(route_name='ajax_arguments_connected_to_position_uid', renderer='json')
	def get_ajax_arguments_by_pos(self):
		logger('ajax_arguments_connected_to_position_uid', 'def', 'main')

		# get every relation from current argument to an position with uid send
		uid = ''
		try:
			uid = self.request.params['uid']
		except KeyError as e:
			logger('ajax_arguments_connected_to_position_uid', 'error', repr(e))

		logger('ajax_arguments_connected_to_position_uid', 'def', 'uid: ' + uid)

		# get all arguments
		query_helper = QueryHelper()
		return_list = QueryHelper().get_argument_list_in_relation_to_statement(uid, True, True)
		return_dict = {}
		for entry in return_list:
			return_dict[entry['uid']] = entry

		# save track, because the given uid is a position uid
		logger('ajax_arguments_connected_to_position_uid', 'def', 'saving track: position id ' + str(uid))
		query_helper.save_track_position_for_user(DBSession, transaction, self.request.authenticated_userid, uid)

		# get return count of arguments
		return_json = DictionaryHelper().dictionarty_to_json_array(return_dict, True)

		return return_json

	# ajax - getting next argument for confrontation
	@view_config(route_name='ajax_args_for_new_discussion_round', renderer='json')
	def get_ajax_args_for_new_round(self):
		logger('get_args_for_new_round', 'def', 'main')

		# TODO: FINISHED; BUT NOT DEBUGGED:
		uid = ''
		is_argument = ''
		try:
			uid = self.request.params['uid']
			is_argument = True if self.request.params['is_argument'] == 'argument' else False
			logger('get_args_for_new_round', 'def', 'request data: uid ' + str(uid) + ', isArgument '
			       + str(is_argument) + '(' + str(self.request.params['is_argument']) + ')')
		except KeyError as e:
			logger('get_args_for_new_round', 'error', repr(e))

		# saving track
		query_helper = QueryHelper()
		if is_argument:
			logger('ajax_arguments_connected_to_position_uid', 'def', 'saving track: argument id ' + str(uid))
			query_helper.save_track_argument_for_user(DBSession, transaction, self.request.authenticated_userid, uid)
		else:
			logger('ajax_arguments_connected_to_position_uid', 'def', 'saving track: position id ' + str(uid))
			query_helper.save_track_position_for_user(DBSession, transaction, self.request.authenticated_userid, uid)

		# get data
		return_dict = query_helper.get_args_for_new_round(self.request.authenticated_userid, uid, is_argument)
		return_json = DictionaryHelper().dictionarty_to_json_array(return_dict, True)

		return return_json
