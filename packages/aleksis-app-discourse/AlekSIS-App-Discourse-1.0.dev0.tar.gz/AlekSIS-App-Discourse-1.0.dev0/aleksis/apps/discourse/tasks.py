from celery.utils.log import get_task_logger
from pydiscourse.exceptions import DiscourseClientError

from aleksis.core.celery import app
from aleksis.core.models import Group, Person
from aleksis.core.util.core_helpers import get_site_preferences, generate_random_code, has_person

from .util import get_client, is_oidc_enabled


@app.task
def sync_user(person_pk: int):
    logger = get_task_logger("sync_user")
    prefs = get_site_preferences()
    client = get_client()

    person = Person.objects.get(pk=person_pk)

    # Try to get existing user
    try:
        client.user(person.user.username)
        logger.info(f"Syncing existing user {person.user.username}")
    except DiscourseClientError:
        # Create new user
        password = generate_random_code(3, 5)
        client.create_user(person.full_name, person.user.username, person.email, password, active=True)
        logger.info(f"Syncing new user {person.user.username}")

    payload = {}
    if prefs["discourse__sync_existing_users_name"]:
        payload["name"] = person.full_name
    if prefs["discourse__sync_existing_users_email"]:
        payload["name"] = person.email
    if is_oidc_enabled():
        # Write our user ID as external ID if we have an OAuth application for Discourse
        payload["external_ids"] = {"oidc": str(person.user.pk)}

    if payload:
        logger.debug(f"Syncing user {person.user.username} with payload {payload}")
        client.update_user(person.user.username, **payload)


@app.task
def sync_users():
    logger = get_task_logger("sync_users")
    prefs = get_site_preferences()
    client = get_client()

    # Get all usernames known to Discourse
    usernames = [u["username"] for u in client.users()]
    logger.debug(f"Discourse knows {len(usernames)} users")

    persons_q = Person.objects.filter(user__isnull=False)
    if not prefs["discourse__sync_new_users"]:
        logger.info("Not syncing new users")
        persons_q = persons_q.filter(user__username__in=usernames)
    if not prefs["discourse__sync_existing_users"]:
        logger.info("Not syncing existing users")
        persons_q = persons_q.exclude(user__username__in=usernames)
    pks = persons_q.values_list("pk", flat=True)

    for pk in pks:
        sync_user.delay(pk)


@app.task
def sync_group(pk: int):
    logger = get_task_logger("sync_group")
    prefs = get_site_preferences()
    client = get_client()

    group = Group.objects.get(pk=pk)
    if not group.short_name:
        raise ValueError(f"Group {group.name} does not have a hort name.")

    # Does the group already exist in Discourse?
    try:
        group_id = client.group(group.short_name)["group"]["id"]
        logger.info(f"Syncing existing group {group.short_name}")
    except DiscourseClientError:
        # Try to create the group
        group_id = client.create_group(group.short_name, full_name=group.name)["basic_group"]["id"]
        logger.info(f"Syncing new group {group.short_name}")

    # Synchronise group owners
    existing_owners = {u["username"] for u in client.group_owners(group.short_name)}
    wanted_owners = set(group.owners.values_list("user__username", flat=True))
    if wanted_owners != existing_owners:
        try:
            logger.info("Group owners differ, adding new owners")
            client.add_group_owners(group_id, wanted_owners-existing_owners)
        except DiscourseClientError:
            # Ignore this error; some users were probably unknown
            logger.warning("Failed to add some owners")
            pass

        for username in existing_owners-wanted_owners:
            logger.info(f"{username} is group owner in Discourse but not AlekSIS, removing")
            try:
                user_id = client.user(username)["id"]
                client.delete_group_owner(group_id, user_id)
            except DiscourseClientError:
                # Ignore this error; user is probably unknown
                logger.warning(f"Failed to remove {username} as group owner")
                continue

    # Synchronise group members
    existing_members = {u["username"] for u in client.group_members(group.short_name)}
    wanted_members = set(group.members.values_list("user__username", flat=True))
    if wanted_members != existing_members:
        try:
            logger.info("Group members differ, adding new members")
            client.add_group_members(group_id, wanted_members-existing_members)
        except DiscourseClientError:
            # Ignore this error; some users were probably unknown
            logger.warning("Failed to add some members")
            pass

        for username in existing_members-wanted_members:
            logger.info(f"{username} is group member in Discourse but not AlekSIS, removing")
            try:
                # Get user ID because Discourse API is stupid
                user_id = client.user(username)["id"]
                client.delete_group_member(group_id, user_id)
            except DiscourseClientError:
                # Ignore this error; user is probably unknown
                logger.warning(f"Failed to remove {username} as group member")
                continue


@app.task
def sync_groups():
    logger = get_task_logger("sync_groups")
    prefs = get_site_preferences()
    client = get_client()

    # Get all group names known to Discourse
    names = [u["name"] for u in client.groups()]

    groups_q = Group.objects.all()
    if not prefs["discourse__sync_new_groups"]:
        logger.info("Not syncing new groups")
        groups_q = groups_q.filter(short_name__in=names)
    if not prefs["discourse__sync_existing_groups"]:
        logger.info("Not syncing existing groups")
        groups_q = groups_q.exclude(short_name__in=groups)
    pks = groups_q.values_list("pk", flat=True)

    for pk in pks:
        sync_group.delay(pk)
