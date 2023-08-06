from django.utils.translation import gettext as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import BooleanPreference, StringPreference

from aleksis.core.registries import site_preferences_registry

discourse = Section("discourse", verbose_name=_("Discourse"))


@site_preferences_registry.register
class BaseURL(StringPreference):
    section = discourse
    name = "base_url"
    verbose_name = _("Base URL of Discourse instance")
    default = ""
    help_text = _("Base URL for all Discourse API endpoints")


@site_preferences_registry.register
class APIUser(StringPreference):
    section = discourse
    name = "api_user"
    verbose_name = _("Discourse API username")
    help_text = _("The username to authenticate as")
    default = "system"


@site_preferences_registry.register
class APIKey(StringPreference):
    section = discourse
    name = "api_key"
    verbose_name = _("Discourse API key")
    help_text = _("The API key from Discourse to authenticate requests")
    default = ""


@site_preferences_registry.register
class SyncExistingGroups(BooleanPreference):
    section = discourse
    name = "sync_existing_groups"
    verbose_name = _("Synchronise users in existing groups")
    help_text = _("Members and owners of existing Discourse groups with a matching short name will be synchronised")
    default = True


@site_preferences_registry.register
class SyncNewGroups(BooleanPreference):
    section = discourse
    name = "sync_new_groups"
    verbose_name = _("Create new groups in Discourse")
    help_text = _("New groups will be created in Discourse for groups in AlekSIS")
    default = False


@site_preferences_registry.register
class SyncExistingUsers(BooleanPreference):
    section = discourse
    name = "sync_existing_users"
    verbose_name = _("Synchronise existing users")
    help_text = _("Update existing users in Discourse")
    default = False


@site_preferences_registry.register
class SyncExistingUsersName(BooleanPreference):
    section = discourse
    name = "sync_existing_users_name"
    verbose_name = _("Synchronise existing users' name")
    help_text = _("Foce update of users' names in Discourse")
    default = False


@site_preferences_registry.register
class SyncExistingUsersEmail(BooleanPreference):
    section = discourse
    name = "sync_existing_users_email"
    verbose_name = _("Synchronise existing users' e-mail address")
    help_text = _("Foce update of users' e-mail addresses in Discourse")
    default = False


@site_preferences_registry.register
class SyncNewUsers(BooleanPreference):
    section = discourse
    name = "sync_new_users"
    verbose_name = _("Create new users in Discourse")
    help_text = _("New users will be created in Discourse")
    default = True
