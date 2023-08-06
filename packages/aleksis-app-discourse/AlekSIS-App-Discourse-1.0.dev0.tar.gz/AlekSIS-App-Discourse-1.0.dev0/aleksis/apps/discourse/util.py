from pydiscourse import DiscourseClient

from aleksis.core.util.core_helpers import get_site_preferences


def get_client():
    """Get a Discourse API client from preferences."""
    prefs = get_site_preferences()

    client = DiscourseClient(prefs["discourse__base_url"], api_username=prefs["discourse__api_user"], api_key=prefs["discourse__api_key"])
    return client


def is_oidc_enabled():
    """Determine if we have an OIDC application redirecting to Discourse."""
    from aleksis.core.models import OAuthApplication

    prefs = get_site_preferences()

    return OAuthApplication.objects.filter(redirect_uris__startswith=prefs["discourse__base_url"]).exists()
