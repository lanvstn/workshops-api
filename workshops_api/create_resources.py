from workshops_api.app import api

from workshops_api.resources.event import EventResource
from workshops_api.resources.event_list import EventListResource
from workshops_api.resources.event_user_list import EventUserListResource, \
                                                    UnregisteredEventUserListResource
from workshops_api.resources.auth import AuthConfigResource, \
                                         AuthLoginResource, \
                                         AuthAdminPasswordChangeResource
from workshops_api.resources.registration_user import RegistrationUserResource
from workshops_api.resources.workshop_link import WorkshopLinkResource
from workshops_api.resources.event_registration_export import EventRegistrationExportResource

# Events
api.add_resource(EventListResource, '/events')
api.add_resource(EventResource, '/events/<string:event_id>')
api.add_resource(WorkshopLinkResource, '/events/<string:event_id>/workshop_links')

# Users
api.add_resource(EventUserListResource, '/events/<string:event_id>/users')
api.add_resource(UnregisteredEventUserListResource, '/events/<string:event_id>/unregistered_users')

# Authentication
api.add_resource(AuthConfigResource, '/auth/config')
api.add_resource(AuthLoginResource, '/auth/login')
api.add_resource(AuthAdminPasswordChangeResource, '/auth/change_admin_password')

# Registration
api.add_resource(EventRegistrationExportResource, '/export/event_registrations/<string:event_id>')
api.add_resource(RegistrationUserResource, '/registrations/user/<string:user_id>',
                 '/registrations/user/<string:user_id>/<string:workshop_id>')
