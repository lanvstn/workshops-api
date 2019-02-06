import yaml

from workshops_api.models.event import EventModel
from workshops_api.models.workshop import WorkshopModel
from workshops_api.models.workshop_link import WorkshopLinkModel
from workshops_api.models.user import UserModel
from workshops_api.models.registration import RegistrationModel

with open('testdata.yml', 'r') as f:
    data = yaml.safe_load(f)

testdata = []

for event in data['events']:
    testdata.append(
        EventModel(
            name=event['name'],
            available=event['available']
        )
    )

    for workshop in event['workshops']:
        testdata.append(
            WorkshopModel(
                id=workshop['id'],
                title=workshop['title'],
                description=workshop['description'],
                moment=workshop['moment'],
                limit=workshop['limit'],
                targetGroup=workshop['targetGroup'],
                event_id=event['id']
            )
        )

        for user_id in workshop['registrations']:
            testdata.append(
                RegistrationModel(
                    workshop_id=workshop['id'],
                    user_id=user_id
                )
            )

    for workshop_link in event['workshop_links']:
        testdata.append(
            WorkshopLinkModel(
                workshop1_id=workshop_link['workshop1_id'],
                workshop2_id=workshop_link['workshop2_id'],
                link_type=workshop_link['link_type'],
                event_id=event['id']
            )
        )

    for user in event['users']:
        testdata.append(
            UserModel(
                id=user['id'],
                full_name=user['full_name'],
                targetGroup=user['targetGroup'],
                user_class=user['user_class'],
                event_id=event['id'],
                identity=user['full_name']
            )
        )
