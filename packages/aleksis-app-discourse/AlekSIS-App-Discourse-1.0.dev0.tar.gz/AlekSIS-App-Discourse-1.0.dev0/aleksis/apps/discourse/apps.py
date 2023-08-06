from aleksis.core.util.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "aleksis.apps.discourse"
    verbose_name = "AlekSIS — Discourse"
    dist_name = "AlekSIS-App-Discourse"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Discourse",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2022], "Dominik George", "dominik.george@teckids.org"),
    )
