class AuthenticityMessage:
    def __init__(self, certificate, slmp_payload):
        self.certificate = certificate
        self.slmp_payload = slmp_payload
