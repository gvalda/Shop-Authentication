from string import Template


class TemplateParser:
    d = {
        'logo_uri': 'https://cdn.logo.com/hotlink-ok/logo-social.png',
        'name': 'Unknown stranger',
        'company_name': 'Unknown company',
        'company_uri': 'https://www.unknown.com',
        'confirmation_uri': 'https://www.unknown.com/confirm',
        'unsubscribe_uri': 'https://www.unknown.com/unsubscribe',
    }

    @classmethod
    def verification_email_template(cls, **kwargs):
        with open('./authentication/templates/email/verification.txt') as f:
            template = Template(f.read())
            return template.substitute(cls.d | kwargs)
