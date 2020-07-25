# from indico.core import signals
# See https://github.com/indico/indico/blob/master/indico/core/plugins/__init__.py#L48 for details
# about the IndicoPlugin class.
from indico.core.plugins import IndicoPlugin  # , IndicoPluginBlueprint, url_for_plugin


class AuthorisedUserSearchPlugin(IndicoPlugin):
    """Authorised User Search

    Require the users to be authorised to use the user search functionality before they can perform
    user searching
    """

    def init(self):
        super(AuthorisedUserSearchPlugin, self).init()
        AuthorisedUserSearchPlugin.logger.info("New3 Plugin Init")

