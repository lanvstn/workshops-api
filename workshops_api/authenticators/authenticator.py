class Authenticator():
    # Identifies the auth method to the client
    _method = "default"

    def auth(self, credential, is_admin_login):
        """ Returns a user object

        Credential object can be anything and is validated only here.
        Can be user/pass, a key, etc...
        """
        raise NotImplementedError
