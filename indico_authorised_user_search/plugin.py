# from indico.core import signals
# See https://github.com/indico/indico/blob/master/indico/core/plugins/__init__.py#L48 for details
# about the IndicoPlugin class.
from indico.core.plugins import IndicoPlugin  # , IndicoPluginBlueprint, url_for_plugin
from indico.core.logger import Logger
import indico.modules.users.util
from flask import session


def add_monkey_patch():

    def authorised_search_users(**kwargs):
        logger = Logger.get("search_users")
        logger.info("Session: {}".format(session))
        # raise Exception("Just wanna see the traceback")
        return old_search_users(**kwargs)

    AuthorisedUserSearchPlugin.logger.info("adding monkey patch")
    old_search_users = indico.modules.users.util.search_users
    indico.modules.users.util.search_users = authorised_search_users


class AuthorisedUserSearchPlugin(IndicoPlugin):
    """Authorised User Search

    Require the users to be authorised to use the user search functionality before they can perform
    user searching
    """

    def init(self):
        super(AuthorisedUserSearchPlugin, self).init()
        AuthorisedUserSearchPlugin.logger.info("New3 Plugin Init")
        add_monkey_patch()
