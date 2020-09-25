import mongoengine as me
from decolators import auth_check
from .collections.models import Collection


class ApiRoot(me.Document):
    name = me.StringField(required=True, primary_key=True)
    title = me.StringField(required=True)
    description = me.StringField(default='')
    versions = me.ListField(required=True)
    max_content_length = me.IntField(required=True)
    collections = me.ListField(me.ReferenceField(Collection))
    stip_meta = me.DictField(default={})

    meta = {
        'db_alias': 'taxii21_alias'
    }

    @staticmethod
    def update_or_create(name, title, description, versions, max_content_length):
        try:
            doc = ApiRoot.objects.get(name=name)
        except me.DoesNotExist:
            doc = ApiRoot()
        doc.name = name
        doc.title = title
        doc.description = description
        if versions:
            doc.versions = versions
        doc.max_content_length = max_content_length
        doc.save()
        return doc

    @staticmethod
    def get_api_root(api_root_name):
        doc = ApiRoot.objects.get(name=api_root_name)
        return doc.get_api_info()

    @staticmethod
    def get_max_content_length(api_root_name):
        doc = ApiRoot.objects.get(name=api_root_name)
        return doc.max_content_length

    @staticmethod
    def get_collections(api_root_name):
        doc = ApiRoot.objects.get(name=api_root_name)
        collections = []
        for col in doc.collections:
            collections.append(col.get_collection_info())
        return collections

    @staticmethod
    def get_collection(api_root_name, col_id):
        doc = ApiRoot.objects.get(name=api_root_name)
        for col in doc.collections:
            if col.col_id == col_id:
                return col
            if col.alias == col_id:
                return col
        return None

    @staticmethod
    def auth_check(request, api_root_name):
        doc = ApiRoot.objects.get(name=api_root_name)
        try:
            allowed_users = doc.stip_meta['users']
        except Exception:
            allowed_users = None
        return auth_check(request, allowed_users)

    def get_api_info(self):
        resp = {}
        resp['title'] = self.title
        resp['description'] = self.description
        resp['versions'] = self.versions
        resp['max_content_length'] = self.max_content_length
        return resp

    def append_collection(self, collection):
        if collection not in self.collections:
            self.collections.append(collection)
        self.save()

    def set_collections(self, col_ids):
        self.collections = []
        for col_id in col_ids:
            collection = Collection.objects.get(col_id=col_id)
            self.append_collection(collection)

    def set_users(self, users):
        self.stip_meta['users'] = users
        self.save()
