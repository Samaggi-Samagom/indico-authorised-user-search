# from indico.core import signals
# See https://github.com/indico/indico/blob/master/indico/core/plugins/__init__.py#L48 for details
# about the IndicoPlugin class.
from indico.core.plugins import IndicoPlugin  # , IndicoPluginBlueprint, url_for_plugin
# from indico.core.logger import Logger
from indico.modules.groups.core import GroupProxy
import indico.modules.users.util

from flask import session

from indico.web.forms.base import IndicoForm
from wtforms.fields import IntegerField
from wtforms.validators import InputRequired, NumberRange


def add_monkey_patch():

    def get_user_search_permission():
        """Check whether the current user is allowed to search users or not"""

        group_id = AuthorisedUserSearchPlugin.settings.get('group_id')
        if group_id is None:
            return True

        group_id = int(group_id)
        if 0 == group_id:
            return True
        elif group_id > 0:
            group_proxy = GroupProxy(group_id)
            return session.user in group_proxy
        else:
            return False

    def authorised_search_users(**kwargs):
        # logger = Logger.get("search_users")
        # logger.info("Session: {}".format(session))
        # raise Exception("Just wanna see the traceback")
        if get_user_search_permission():
            return old_search_users(**kwargs)
        else:
            return set(session.user)

    AuthorisedUserSearchPlugin.logger.info("adding monkey patch")
    old_search_users = indico.modules.users.util.search_users
    indico.modules.users.util.search_users = authorised_search_users


class AuthorisedGroupSettings(IndicoForm):
    group_id = IntegerField('Local Group Id', [InputRequired(), NumberRange(min=-1)])


class AuthorisedUserSearchPlugin(IndicoPlugin):
    """Authorised User Search

    Only allow users in the specified local group to use the 'user search' functionality.
    Users who are not in the specified group will only see themselves when they perform user
    searching.

    Specifying group_id=0 to allow everyone to search, and group_id=-1 to block everyone.
    """

    configurable = True
    settings_form = AuthorisedGroupSettings
    default_settings = {
        'group_id': None
    }

    def init(self):
        super(AuthorisedUserSearchPlugin, self).init()
        AuthorisedUserSearchPlugin.logger.info("New5 Plugin Init")
        add_monkey_patch()
