import uuid
import datetime
import mongoengine as me
from ctirs.core.mongo.documents_taxii21_objects import get_modified_from_object
from core.response import get_taxii_date_str


class Status(me.Document):
    added = me.DateTimeField(default=datetime.datetime.utcnow, required=True)
    status_id = me.StringField(required=True, primary_key=True)
    status = me.StringField(requierd=True)
    request_timestamp = me.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'db_alias': 'taxii21_alias'
    }

    @staticmethod
    def create(objects):
        status = Status()
        status.status_id = str(uuid.uuid4())
        status.status = 'pending'
        for object_ in objects:
            StatusDetail.create(object_, status)
        status.save()
        return status

    def modify_detail_status(self, object_id, version, status, message=None):
        if version:
            status_detail = StatusDetail.objects.get(
                taxii_status=self,
                object_id=object_id,
                version=version)
        else:
            status_detail = StatusDetail.objects.get(
                taxii_status=self,
                object_id=object_id)
        status_detail.status = status
        if message:
            status_detail.message = message
        status_detail.save()

    def success(self, object_id, version, message=None):
        self.modify_detail_status(object_id, version, 'success', message)

    def failure(self, object_id, version, message):
        self.modify_detail_status(object_id, version, 'failure', message)

    def get_status_list(self, status):
        ret = []
        cursor = StatusDetail.objects.filter(
            taxii_status=self,
            status=status)
        for status_detail in cursor:
            ret.append(status_detail.get_detail_status())
        return ret

    def get_status(self):
        status_list = [
            ('success', 'successes'),
            ('failure', 'failures'),
            ('pending', 'pendings'),
        ]

        resp = {}
        resp['id'] = self.status_id
        resp['status'] = self.status
        resp['request_timestamp'] = get_taxii_date_str(self.request_timestamp)
        resp['total_count'] = 0
        for status, list_key in status_list:
            resp[list_key] = self.get_status_list(status)
            count_key = status + '_count'
            resp[count_key] = len(resp[list_key])
            resp['total_count'] += len(resp[list_key])
        if resp['pending_count'] == 0:
            resp['status'] = 'complete'
        return resp


class StatusDetail(me.Document):
    added = me.DateTimeField(default=datetime.datetime.utcnow, required=True)
    object_id = me.StringField(required=True)
    version = me.StringField(required=True)
    message = me.StringField()
    status = me.StringField(required=True, deafult='pending')
    taxii_status = me.ReferenceField(Status)

    meta = {
        'db_alias': 'taxii21_alias'
    }

    @staticmethod
    def create(object_, taxii_status, message=None):
        status_detail = StatusDetail()
        status_detail.object_id = object_['id']
        status_detail.version = get_modified_from_object(object_)
        if message:
            status_detail.message = message
        status_detail.status = 'pending'
        status_detail.taxii_status = taxii_status
        status_detail.save()
        return status_detail

    def get_detail_status(self):
        resp = {}
        resp['id'] = self.object_id
        resp['version'] = self.version
        if self.message:
            resp['message'] = self.message
        return resp
