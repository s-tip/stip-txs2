import mongoengine as me


class Collection(me.Document):
    col_id = me.StringField(required=True)
    title = me.StringField(requierd=True)
    description = me.StringField(default='')
    alias = me.StringField(default='')
    can_read = me.BooleanField(required=True)
    can_write = me.BooleanField(required=True)
    media_types = me.ListField()
    stip_meta = me.DictField(default={})

    meta = {
        'db_alias': 'taxii21_alias'
    }

    @staticmethod
    def update_or_create(
        col_id,
        title,
        description,
        alias,
        can_read,
        can_write,
        media_types,
        can_read_communities=None,
        can_write_community=None
    ):

        try:
            doc = Collection.objects.get(col_id=col_id)
        except me.DoesNotExist:
            doc = Collection()
        doc.col_id = col_id
        doc.title = title
        doc.description = description
        if Collection._is_duplicate_alias(doc.alias, alias):
            raise Exception('This alias (%s) is already in use.' % (alias))
        doc.alias = alias
        doc.can_read = can_read
        doc.can_write = can_write
        if media_types:
            doc.media_types = media_types
        if can_read_communities:
            doc.stip_meta['can_read_communities'] = can_read_communities
        if can_write_community:
            doc.stip_meta['can_write_community'] = can_write_community
        doc.save()
        return doc

    @staticmethod
    def _is_duplicate_alias(origin_alias, alias):
        if origin_alias == alias:
            return False
        for collection in Collection.objects:
            if collection.alias == alias:
                return True
        return False

    def get_collection_info(self):
        resp = {}
        resp['id'] = self.col_id
        resp['title'] = self.title
        resp['description'] = self.description
        resp['alias'] = self.alias
        resp['can_read'] = self.can_read
        resp['can_write'] = self.can_write
        resp['media_types'] = self.media_types
        return resp
