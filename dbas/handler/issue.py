"""
Provides helping function for issues.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

from math import ceil

import arrow
import transaction
from slugify import slugify
from sqlalchemy import and_

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, User, Issue, Language, Statement, sql_timestamp_pretty_print, \
    ClickedStatement
from dbas.database.initializedb import nick_of_anonymous_user
from dbas.handler import user
from dbas.handler.language import get_language_from_header
from dbas.helper.query import get_short_url
from dbas.logger import logger
from dbas.query_wrapper import get_not_disabled_issues_as_query, get_visible_issues_for_user_as_query
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from dbas.url_manager import UrlManager

rep_limit_to_open_issues = 10


def set_issue(db_user: User, info: str, long_info: str, title: str, db_lang: Language, is_public: bool,
              is_read_only: bool, application_url: str) -> dict:
    """
    Sets new issue, which will be a new discussion

    :param db_user: User
    :param info: Short information about the new issue
    :param long_info: Long information about the new issue
    :param title: Title of the new issue
    :param db_lang: Language
    :param application_url: Url of the app itself
    :param is_public: Boolean
    :param is_read_only: Boolean
    :rtype: dict
    :return: Collection with information about the new issue
    """
    user.update_last_action(db_user)

    logger('setter', 'set_new_issue', 'main')
    DBDiscussionSession.add(Issue(title=title,
                                  info=info,
                                  long_info=long_info,
                                  author_uid=db_user.uid,
                                  is_read_only=is_read_only,
                                  is_private=not is_public,
                                  lang_uid=db_lang.uid))
    DBDiscussionSession.flush()
    transaction.commit()
    db_issue = DBDiscussionSession.query(Issue).filter(and_(Issue.title == title,
                                                            Issue.info == info)).first()

    return {'issue': get_issue_dict_for(db_issue, application_url, False, 0, db_lang.ui_locales)}


def prepare_json_of_issue(uid, application_url, lang, for_api, nickname):
    """
    Prepares slug, info, argument count and the date of the issue as dict

    :param uid: Issue.uid
    :param application_url: application_url
    :param lang: ui_locales
    :param for_api: Boolean
    :param nickname: Nickname of current user
    :return: Issue-dict()
    """
    logger('issueHelper', 'prepare_json_of_issue', 'main')
    db_issue = DBDiscussionSession.query(Issue).get(uid)

    slug = slugify(db_issue.title) if db_issue else 'none'
    title = db_issue.title if db_issue else 'none'
    info = db_issue.info if db_issue else 'none'
    long_info = db_issue.long_info if db_issue else 'none'
    stat_count = get_number_of_statements(uid)
    date_pretty = sql_timestamp_pretty_print(db_issue.date, lang) if db_issue else 'none'
    duration = (arrow.utcnow() - db_issue.date) if db_issue else 0
    days, seconds = (duration.days, duration.seconds) if db_issue else (0, 0)
    duration = ceil(days * 24 + seconds / 3600)
    date_ms = int(db_issue.date.format('X') if db_issue else arrow.utcnow().format('X')) * 1000
    date = db_issue.date.format('DD.MM. HH:mm') if db_issue else 'none'

    db_user = DBDiscussionSession.query(User).filter_by(
        nickname=nickname if nickname else nick_of_anonymous_user).first()
    db_issues = get_visible_issues_for_user_as_query(db_user.uid).all()
    all_array = []
    for issue in db_issues:
        issue_dict = get_issue_dict_for(issue, application_url, for_api, uid, lang)
        all_array.append(issue_dict)

    _t = Translator(lang)
    t1 = _t.get(_.discussionInfoTooltip1)
    t2 = _t.get(_.discussionInfoTooltip2)
    t3 = _t.get(_.discussionInfoTooltip3sg if stat_count == 1 else _.discussionInfoTooltip3pl)
    tooltip = '{} {} {} {} {}'.format(t1, date, t2, stat_count, t3)

    return {
        'slug': slug,
        'info': info,
        'long_info': long_info,
        'title': title,
        'uid': uid,
        'stat_count': stat_count,
        'date': date,
        'date_ms': date_ms,
        'date_pretty': date_pretty,
        'all': all_array,
        'tooltip': tooltip,
        'intro': _t.get(_.currentDiscussion),
        'duration': duration,
        'read_only': db_issue.is_read_only
    }


def get_number_of_arguments(issue_uid):
    """
    Returns number of arguments for the issue

    :param issue_uid: Issue Issue.uid
    :return: Integer
    """
    return len(DBDiscussionSession.query(Argument).filter_by(issue_uid=issue_uid).all())


def get_number_of_statements(issue_uid):
    """
    Returns number of statements for the issue

    :param issue_uid: Issue Issue.uid
    :return: Integer
    """
    return len(DBDiscussionSession.query(Statement).filter_by(issue_uid=issue_uid).all())


def get_issue_dict_for(issue, application_url, for_api, uid, lang):
    """
    Creates an dictionary for the issue

    :param issue: Issue
    :param application_url:
    :param for_api: Boolean
    :param uid: current selected Issue.uid
    :param lang: ui_locales
    :return: dict()
    """
    if str(type(issue)) != str(Issue):
        return {'uid': '', 'slug': '', 'title': '', 'url': '', 'review_url': '', 'info': '', 'stat_count': '',
                'date': '', 'author': '', 'author_url': '', 'enabled': '', 'error': 'true'}

    _um = UrlManager(application_url, issue.slug, for_api)
    issue_dict = dict()
    issue_dict['uid'] = str(issue.uid)
    issue_dict['slug'] = issue.slug
    issue_dict['title'] = issue.title
    issue_dict['url'] = _um.get_slug_url(False) if str(uid) != str(issue.uid) else ''
    issue_dict['review_url'] = _um.get_review_url(False) if str(uid) != str(issue.uid) else ''
    issue_dict['info'] = issue.info
    issue_dict['stat_count'] = get_number_of_statements(issue.uid)
    issue_dict['date'] = sql_timestamp_pretty_print(issue.date, lang)
    issue_dict['author'] = issue.users.public_nickname
    issue_dict['error'] = ''
    issue_dict['author_url'] = '{}/user/{}'.format(application_url, issue.users.public_nickname)
    issue_dict['enabled'] = 'disabled' if str(uid) == str(issue.uid) else 'enabled'
    return issue_dict


def get_id_of_slug(slug: str, request, save_id_in_session: bool):
    """
    Returns the uid of the issue with given slug

    :param slug: slug
    :param request: self.request for a fallback
    :param save_id_in_session: Boolean
    :return: uid
    """
    logger('IssueHelper', 'get_id_of_slug', 'slug: {}'.format(slug))
    db_issue = get_not_disabled_issues_as_query().filter(Issue.slug == slug).first()
    if db_issue:
        if save_id_in_session:
            request.session['issue'] = db_issue.uid
        return db_issue.uid
    return None


def get_issue_id(request):
    """
    Returns issue uid saved in request. If there is no uid, we will choose an
    issue based on the language from the requests header

    :param request: self.request
    :return: uid
    """
    # logger('IssueHelper', 'get_issue_id', 'def')
    # first matchdict, then params, then session
    issue_uid = request.matchdict['issue'] if 'issue' in request.matchdict \
        else request.params['issue'] if 'issue' in request.params \
        else request.session['issue'] if 'issue' in request.session \
        else None

    # no issue found
    if not issue_uid:
        issue_uid = get_issue_based_on_header(request)

    # save issue in session
    request.session['issue'] = issue_uid
    return issue_uid


def get_issue_based_on_header(request):
    """

    :param request:
    :return:
    """
    # logger('IssueHelper', 'get_issue_based_on_header', 'no saved issue found')
    ui_locales = get_language_from_header(request)
    db_issues = get_not_disabled_issues_as_query()
    db_lang = DBDiscussionSession.query(Language).filter_by(ui_locales=ui_locales).first()
    db_issue = db_issues.filter_by(lang_uid=db_lang.uid).first()
    if not db_issue:
        db_issue = db_issues.first()

    return db_issue.uid


def get_title_for_slug(slug):
    """
    Returns the issues title for a given slug

    :param slug: String
    :return: String
    """
    db_issues = DBDiscussionSession.query(Issue).all()
    for issue in db_issues:
        if str(slugify(issue.title)) == str(slug):
            return issue.title
    return None


def get_issues_overiew(nickname, application_url) -> dict:
    """
    Returns dictionary with keywords 'user' and 'others', which got lists with dicts with infos

    :param nickname: Users.nickname
    :param application_url: current applications url
    :return: dict
    """
    logger('IssueHelper', 'get_issues_overiew', 'def')
    user.update_last_action(nickname)
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(nickname)).first()
    if not db_user:
        return {
            'user': [],
            'other': []
        }

    is_admin = user.is_admin(nickname)
    if is_admin:
        db_issues_other_users = DBDiscussionSession.query(Issue).filter(Issue.author_uid != db_user.uid).all()
    else:
        db_issues_other_users = get_visible_issues_for_user_as_query(db_user.uid).filter(
            Issue.author_uid != db_user.uid).all()

    db_issues_of_user = DBDiscussionSession.query(Issue).filter_by(author_uid=db_user.uid).all()

    return {
        'user': [__create_issue_dict(issue, application_url) for issue in db_issues_of_user],
        'other': [__create_issue_dict(issue, application_url) for issue in db_issues_other_users]
    }


def set_discussions_properties(db_user: User, db_issue: Issue, value, property, translator) -> dict:
    """

    :param db_user: User
    :param db_issue: Issue
    :param value: The value which should be assigned to property
    :param property: Property of Issue, e.g. is_disabled
    :param translator:
    :return:
    """
    logger('IssueHelper', 'set_discussions_properties',
           'issue: {}, key: {}, checked: {}'.format(db_issue.slug, property, value))

    if db_issue.author_uid != db_user.uid and not user.is_admin(db_user.nickname):
        return {'error': translator.get(_.noRights)}

    if property == 'enable':
        db_issue.set_disable(not value)
    elif property == 'public':
        db_issue.set_private(not value)
    elif property == 'writable':
        db_issue.set_read_only(not value)
    else:
        return {'error': translator.get(_.internalKeyError)}

    DBDiscussionSession.add(db_issue)
    DBDiscussionSession.flush()
    transaction.commit()

    return {'error': ''}


def __create_issue_dict(issue, application_url) -> dict:
    """
    Returns dictionary with several informationa bout the given issue

    :param issue: database row of issue
    :param application_url: current applications url
    :return: dict()
    """
    short_url_dict = get_short_url(application_url + '/' + issue.slug, 'en')
    url = short_url_dict['url'] if len(short_url_dict['error']) == 0 else application_url + '/' + issue.slug

    # we do nto have to check for clicked arguments, cause arguments consist out of statements
    statements = [s.uid for s in DBDiscussionSession.query(Statement).filter_by(issue_uid=issue.uid).all()]
    db_clicked_statements = DBDiscussionSession.query(ClickedStatement).filter(
        ClickedStatement.statement_uid.in_(statements)).all()
    authors_clicked_statement = [click.author_uid for click in db_clicked_statements]
    db_authors = DBDiscussionSession.query(User).filter(User.uid.in_(authors_clicked_statement)).all()
    involved_users = str(len(db_authors))

    prepared_dict = {
        'uid': issue.uid,
        'title': issue.title,
        'url': application_url + '/' + issue.slug,
        'short_url': url,
        'date': issue.date.format('DD.MM. HH:mm'),
        'count_of_statements': str(get_number_of_statements(issue.uid)),
        'is_enabled': not issue.is_disabled,
        'is_public': not issue.is_private,
        'is_writable': not issue.is_read_only,
        'involved_users': involved_users,
        'lang': DBDiscussionSession.query(Language).get(issue.lang_uid).ui_locales,
        'toggle_on': "<i class='fa fa-check'></i>",
        'toggle_off': "<i class='fa fa-times'></i>",
    }
    return prepared_dict
