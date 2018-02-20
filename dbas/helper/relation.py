"""
Class for handling relations of arguments

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import random
from typing import Tuple, Union

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, Premise, PremiseGroup, User, Issue
from dbas.input_validator import is_integer
from dbas.lib import get_text_for_premisesgroup_uid
from dbas.query_wrapper import get_not_disabled_arguments_as_query, get_not_disabled_premises_as_query


def get_undermines_for_argument_uid(argument_uid, is_supportive=False):
    """
    Returns all uid's of undermines for the argument.

    :return argument_uid: UID of the argument
    :return is_supportive: Boolean
    :return: array with dict() with id (of argument) and text.
    """
    # logger('RelationHelper', 'get_undermines_for_argument_uid', 'main with argument_uid ' + str(self.argument_uid))
    if not is_integer(argument_uid):
        return None

    if int(argument_uid) < 1:
        return None

    db_arguments = get_not_disabled_arguments_as_query()
    db_attacked_argument = db_arguments.filter_by(uid=argument_uid).first()
    if not db_attacked_argument:
        return []

    db_premises = get_not_disabled_premises_as_query()
    db_attacked_premises = db_premises \
        .filter_by(premisesgroup_uid=db_attacked_argument.premisesgroup_uid) \
        .order_by(Premise.premisesgroup_uid.desc()).all()

    premises_as_statements_uid = set()
    for premise in db_attacked_premises:
        premises_as_statements_uid.add(premise.statement_uid)

    if len(premises_as_statements_uid) == 0:
        return []

    return __get_undermines_for_premises(premises_as_statements_uid, is_supportive)


def get_undercuts_for_argument_uid(argument_uid):
    """
    Calls self.__get_attack_or_support_for_justification_of_argument_uid(key, argument_uid, False)

    :return argument_uid: UID of the argument
    :return: array with dict() with id (of argumet) and text.
    """
    # logger('RelationHelper', 'get_undercuts_for_argument_uid', 'main ' + str(self.argument_uid))
    if not is_integer(argument_uid):
        return None

    if int(argument_uid) < 1:
        return None

    return __get_attack_or_support_for_justification_of_argument_uid(argument_uid, False)


def get_rebuts_for_argument_uid(argument_uid):
    """
    Returns all uid's of rebuts for the argument.

    :return argument_uid: UID of the argument
    :return: array with dict() with id (of argumet) and text.
    """
    if not is_integer(argument_uid):
        return None

    if int(argument_uid) < 1:
        return None

    # logger('RelationHelper', 'get_rebuts_for_argument_uid', 'main ' + str(self.argument_uid))
    db_arguments = get_not_disabled_arguments_as_query()
    db_argument = db_arguments.filter_by(uid=int(argument_uid)).first()
    if not db_argument:
        return None

    if db_argument.conclusion_uid is not None:
        return __get_rebuts_for_arguments_conclusion_uid(db_argument)
    else:
        return get_undercuts_for_argument_uid(argument_uid)


def __get_rebuts_for_arguments_conclusion_uid(db_argument):
    """
    Returns a list with dict(). They contain id and text of the rebuttal's pgroups

    :return argument_uid: UID of the argument
    :param db_argument: Argument
    :return: [dict()]
    """
    return_array = []
    given_rebuts = set()
    db_arguments = get_not_disabled_arguments_as_query()
    db_rebut = db_arguments.filter(Argument.is_supportive == (not db_argument.is_supportive),
                                   Argument.conclusion_uid == db_argument.conclusion_uid).all()
    for rebut in db_rebut:

        if rebut.premisesgroup_uid not in given_rebuts:
            given_rebuts.add(rebut.premisesgroup_uid)
            tmp_dict = dict()
            tmp_dict['id'] = rebut.uid
            text, trash = get_text_for_premisesgroup_uid(rebut.premisesgroup_uid)
            tmp_dict['text'] = text[0:1].upper() + text[1:]
            return_array.append(tmp_dict)
    return return_array


def get_supports_for_argument_uid(argument_uid):
    """
    Returns all uid's of supports for the argument.

    :return argument_uid: UID of the argument
    :return: array with dict() with id (of argumet) and text
    """
    if not is_integer(argument_uid):
        return None

    if int(argument_uid) < 1:
        return None

    return_array = []
    given_supports = set()
    db_arguments = get_not_disabled_arguments_as_query()
    db_argument = db_arguments.filter_by(uid=argument_uid).join(PremiseGroup).first()
    if not db_argument:
        return []

    db_arguments_premises = DBDiscussionSession.query(Premise).filter_by(
        premisesgroup_uid=db_argument.premisesgroup_uid).all()

    for arguments_premises in db_arguments_premises:
        db_arguments = get_not_disabled_arguments_as_query()
        db_supports = db_arguments.filter(Argument.conclusion_uid == arguments_premises.statement_uid,
                                          Argument.is_supportive == True).join(PremiseGroup).all()
        if not db_supports:
            continue

        for support in db_supports:
            if support.premisesgroup_uid not in given_supports:
                tmp_dict = dict()
                tmp_dict['id'] = support.uid
                tmp_dict['text'], trash = get_text_for_premisesgroup_uid(support.premisesgroup_uid)
                return_array.append(tmp_dict)
                given_supports.add(support.premisesgroup_uid)

    return [] if len(return_array) == 0 else return_array


def set_new_undermine_or_support_for_pgroup(premisegroup_uid: int, current_argument: Argument, is_supportive: bool,
                                            db_user: User, db_issue: Issue):
    """
    Inserts a new undermine or support with the given parameters.

    :param premisegroup_uid: premisesgroup_uid
    :param current_argument: Argument
    :param is_supportive: Boolean
    :param db_user: User
    :param issue: Issue.uid
    :return: Argument, Boolean if the argument is a duplicate
    """
    already_in = []

    # all premises out of current pgroup
    db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=current_argument.premisesgroup_uid).all()
    for premise in db_premises:
        new_arguments = []
        db_arguments = get_not_disabled_arguments_as_query()
        db_argument = db_arguments.filter(Argument.premisesgroup_uid == premisegroup_uid,
                                          Argument.is_supportive == True,
                                          Argument.conclusion_uid == premise.statement_uid).first()
        if db_argument:
            continue

        db_tmp = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=premisegroup_uid).all()
        if any([p.statement_uid == premise.statement_uid for p in db_tmp]):
            return False

        new_arguments.append(Argument(premisegroup=premisegroup_uid,
                                      issupportive=is_supportive,
                                      author=db_user.uid,
                                      conclusion=premise.statement_uid,
                                      issue=db_issue.uid))

        if len(new_arguments) > 0:
            DBDiscussionSession.add_all(new_arguments)
            DBDiscussionSession.flush()
            transaction.commit()

            already_in += new_arguments

    rnd = random.randint(0, len(already_in) - 1)
    return already_in[rnd]


def set_new_undercut(premisegroup_uid, current_argument: Argument, db_user: User, issue: Issue) \
        -> Tuple[Argument, bool]:
    """
    Inserts a new undercut or overbid with the given parameters.

    :param premisegroup_uid: premisesgroup_uid
    :param current_argument: Argument
    :param db_user: User
    :param issue: Issue.uid
    :return: Argument, Boolean if the argument is a duplicate
    """
    # duplicate?
    db_argument = DBDiscussionSession.query(Argument).filter(Argument.premisesgroup_uid == premisegroup_uid,
                                                             Argument.is_supportive == False,
                                                             Argument.argument_uid == current_argument.uid).first()
    if db_argument:
        return db_argument, True
    else:
        new_argument = Argument(premisegroup=premisegroup_uid,
                                issupportive=False,
                                author=db_user.uid,
                                issue=issue.uid)
        new_argument.set_conclusions_argument(current_argument.uid)
        DBDiscussionSession.add(new_argument)
        DBDiscussionSession.flush()
        transaction.commit()
        return new_argument, False


def set_new_rebut(premisegroup_uid, current_argument: Argument, db_user: User, db_issue: Issue) \
        -> Tuple[Union[Argument, bool], bool]:
    """
    Inserts a new rebut with the given parameters.

    :param premisegroup_uid: premisesgroup_uid
    :param current_argument: Argument
    :param db_user: User
    :return: Argument, Boolean if the argument is a duplicate
    """
    # duplicate?
    db_arguments = get_not_disabled_arguments_as_query()
    db_argument = db_arguments.filter(Argument.premisesgroup_uid == premisegroup_uid,
                                      Argument.is_supportive == True,
                                      Argument.conclusion_uid == current_argument.conclusion_uid).first()
    if db_argument:
        return db_argument, True
    else:
        db_tmp = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=premisegroup_uid).all()
        if any([p.statement_uid == current_argument.conclusion_uid for p in db_tmp]):
            return False, False
        new_argument = Argument(premisegroup=premisegroup_uid,
                                issupportive=False,
                                author=db_user.uid,
                                conclusion=current_argument.conclusion_uid,
                                issue=db_issue.uid)
        DBDiscussionSession.add(new_argument)
        DBDiscussionSession.flush()
        transaction.commit()
        return new_argument, False


def set_new_support(premisegroup_uid: int, current_argument: Argument, db_user: User, db_issue: Issue) \
        -> Tuple[Union[Argument, bool], bool]:
    """
    Inserts a new support with the given parameters.

    :param premisegroup_uid: premisesgroup_uid
    :param current_argument: Argument
    :param db_user: User
    :param db_issue: Issue
    :return: Argument, Boolean if the argument is a duplicate
    """
    # duplicate?
    db_arguments = get_not_disabled_arguments_as_query()
    db_argument = db_arguments.filter(Argument.premisesgroup_uid == premisegroup_uid,
                                      Argument.is_supportive == True,
                                      Argument.conclusion_uid == current_argument.conclusion_uid).first()
    if db_argument:
        return db_argument, True
    else:
        db_tmp = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=premisegroup_uid).all()
        if any([p.statement_uid == current_argument.conclusion_uid for p in db_tmp]):
            return False, False

        new_argument = Argument(premisegroup=premisegroup_uid,
                                issupportive=True,
                                author=db_user.uid,
                                conclusion=current_argument.conclusion_uid,
                                issue=db_issue.uid)
        DBDiscussionSession.add(new_argument)
        DBDiscussionSession.flush()
        transaction.commit()
        return new_argument, False


def __get_attack_or_support_for_justification_of_argument_uid(argument_uid, is_supportive):
    """
    Querys all

    :param argument_uid: Argument.uid
    :param is_supportive: Boolean
    :return: [{id, text}] or 0
    """
    return_array = []
    db_arguments = get_not_disabled_arguments_as_query()
    db_related_arguments = db_arguments.filter(Argument.is_supportive == is_supportive,
                                               Argument.argument_uid == argument_uid).all()
    given_relations = set()

    if not db_related_arguments:
        return None

    for relation in db_related_arguments:
        if relation.premisesgroup_uid not in given_relations:
            given_relations.add(relation.premisesgroup_uid)
            tmp_dict = dict()
            tmp_dict['id'] = relation.uid
            tmp_dict['text'], trash = get_text_for_premisesgroup_uid(relation.premisesgroup_uid)
            return_array.append(tmp_dict)

    return return_array


def __get_undermines_for_premises(premises_as_statements_uid, is_supportive=False):
    """
    Querys all undermines for the given statements

    :param premises_as_statements_uid:
    :param is_supportive
    :return: [{id, text}]
    """
    return_array = []
    given_undermines = set()
    for s_uid in premises_as_statements_uid:
        db_arguments = get_not_disabled_arguments_as_query()
        db_undermine = db_arguments.filter(Argument.is_supportive == is_supportive,
                                           Argument.conclusion_uid == s_uid).all()
        for undermine in db_undermine:
            if undermine.premisesgroup_uid not in given_undermines:
                given_undermines.add(undermine.premisesgroup_uid)
                tmp_dict = dict()
                tmp_dict['id'] = undermine.uid
                tmp_dict['text'], uids = get_text_for_premisesgroup_uid(undermine.premisesgroup_uid)
                return_array.append(tmp_dict)
    return return_array
