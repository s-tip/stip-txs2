import mongoengine as me
from api_root.models import ApiRoot


class Discovery(me.Document):
    title = me.StringField(required=True)
    description = me.StringField(default='')
    contact = me.StringField(default='')
    default = me.ReferenceField(ApiRoot)
    api_roots = me.ListField(me.ReferenceField(ApiRoot))

    meta = {
        'db_alias': 'taxii21_alias'
    }

    @staticmethod
    def _get_api_root(name):
        taxii_root = ''
        return '%s/%s/' % (taxii_root, name)

    @staticmethod
    def get_discovery_response():
        doc = Discovery.objects.get()
        resp = {}
        resp['title'] = doc.title
        resp['description'] = doc.description
        resp['contact'] = doc.contact
        if doc.default:
            resp['default'] = Discovery._get_api_root(doc.default.name)
        resp['api_roots'] = []
        for api_root in doc.api_roots:
            resp['api_roots'].append(Discovery._get_api_root(api_root.name))
        return resp

    @staticmethod
    def update_or_create(title, description, contact, default_api_root_name=None):
        try:
            doc = Discovery.objects.get()
        except me.DoesNotExist:
            doc = Discovery()
        doc.title = title
        doc.description = description
        doc.contact = contact
        if default_api_root_name:
            default_api_root = ApiRoot.objects.get(name=default_api_root_name)
            doc.default = default_api_root
        else:
            doc.default = None
        doc.save()
        return doc

    @staticmethod
    def append_api_root(api_root, default=False):
        doc = Discovery.objects.get()
        if api_root not in doc.api_roots:
            doc.api_roots.append(api_root)
        if len(api_root) == 1:
            doc.default = api_root
        else:
            if default:
                doc.default = api_root
        doc.save()
