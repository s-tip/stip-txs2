import uuid
import core.const as txs_const

from mongoengine import connect
from django.apps import AppConfig
from django.core.management import call_command
from discovery.models import Discovery
from api_root.models import ApiRoot
from api_root.collections.models import Collection
from stip.common.boot import is_skip_sequence


def _init_mongo():
    MONGO_DEFAULT_DB_NAME = 'ctirs'
    MONGO_DEFAULT_TXS21_DB_NAME = 'taxii21'
    MONGO_DEFAULT_HOST_NAME = 'localhost'
    MONGO_DEFAULT_PORT = 27017

    from ctirs.models.rs.models import MongoConfig
    config = MongoConfig.objects.get()
    try:
        connect(config.db, host=config.host, port=int(config.port))
        connect(MONGO_DEFAULT_TXS21_DB_NAME, host=config.host, port=int(config.port), alias='taxii21_alias')
    except BaseException:
        connect(MONGO_DEFAULT_DB_NAME, host=MONGO_DEFAULT_HOST_NAME, port=MONGO_DEFAULT_PORT)
        connect(MONGO_DEFAULT_TXS21_DB_NAME, host=MONGO_DEFAULT_HOST_NAME, port=MONGO_DEFAULT_PORT, alias='taxii21_alias')
    return


class TXS21Boot(AppConfig):
    name = 'core.boot'

    def ready(self):
        _init_mongo()


class TXS21ConsoleBoot(AppConfig):
    name = 'core.boot'

    def ready(self):
        _init_mongo()
        is_skip_sequnece = is_skip_sequence()
        if not is_skip_sequnece:
            print('>>> Start Auto Deploy')
            print('>>> Start collcect static --noinput')
            call_command('collectstatic', '--noinput')
            call_command('makemigrations')
            call_command('migrate')

        if Discovery.objects.count() == 0:
            col = Collection.update_or_create(
                str(uuid.uuid4()),
                'Test Collection',
                'This Collection is temporary.',
                'Test_Collection_Alias',
                False,
                False,
                txs_const.DEFAULT_MEDIA_TYPES
            )

            api_root = ApiRoot.update_or_create(
                'api_test',
                'Test_APIRoot',
                'This API Root is temporary.',
                txs_const.DEFAULT_VERSIONS,
                txs_const.DEFAULT_MAX_CONTENT_LENGTH
            )
            api_root.append_collection(col)

            discovery = Discovery.update_or_create(
                'S-TIP TAXII2 Server',
                'This service is not a production version.',
                'Please change this contact information.'
            )
            discovery.append_api_root(api_root, default=True)
            return
