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
        group_proxy = GroupProxy(AuthorisedUserSearchPlugin.settings.get('group_id'))
        return session.user in group_proxy

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
    group_id = IntegerField('Local Group Id', [InputRequired(), NumberRange(min=1)])


class AuthorisedUserSearchPlugin(IndicoPlugin):
    """Authorised User Search

    Require the users to be authorised to use the user search functionality before they can perform
    user searching
    """

    configurable = True
    settings_form = AuthorisedGroupSettings
    default_settings = {
        'group_id': None
    }

    def init(self):
        super(AuthorisedUserSearchPlugin, self).init()
        AuthorisedUserSearchPlugin.logger.info("New4 Plugin Init")
        add_monkey_patch()
