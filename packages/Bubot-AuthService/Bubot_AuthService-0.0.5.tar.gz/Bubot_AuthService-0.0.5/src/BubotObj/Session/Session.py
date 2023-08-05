from datetime import datetime

from aiohttp_session import get_session, new_session
from bson import ObjectId
from bson.errors import InvalidId

from Bubot.Core.DocumentObj import DocumentObj
from Bubot.Helpers.ActionDecorator import async_action
from Bubot.Helpers.ExtException import ExtException, KeyNotFound


class Session(DocumentObj):
    name = 'Session'

    @property
    def db(self):
        return 'AuthService'

    def init(self):
        self.data = dict(
            title=''
        )

    @classmethod
    @async_action
    async def init_from_request(cls, view, **kwargs):
        action = kwargs['_action']
        _session = await get_session(view.request)
        if not _session or not _session.identity:  # если авторизация происходит под чужой живой сессией грохаем её
            raise KeyNotFound(detail='session')
        self = cls(view.storage)
        action.add_stat(await self.find_by_id(_session.identity, _form=None))
        return action.set_end(self)

    @classmethod
    @async_action
    async def create_from_request(cls, user, view, **kwargs):
        action = kwargs['_action']
        try:
            old_session = action.add_stat(await cls.init_from_request(view))
            if not old_session.data['end']:
                if user.get_link()['_id'] == old_session.data['user']['_id']:
                    return old_session
                action.add_stat(await old_session.close())
        except KeyNotFound:
            pass

        self = cls(view.storage)

        self.data = {
            "user": user.get_link(),
            "account": user.get_default_account(),
            "date": datetime.now(),
            "end": None
        }
        action.add_stat(await self.update())
        _session = await new_session(view.request)
        identity = self.get_identity()
        _session.set_new_identity(identity)
        _session['user'] = self.data['user']
        _session['account'] = self.data['account']
        _session['_id'] = identity
        return self

    @async_action
    async def close(self, **kwargs):
        self.data['end'] = datetime.now()
        await self.update()

    def get_identity(self):
        return str(self.obj_id)
        # return {
        #     "user": str(self.data["user"]["_id"]),
        #     "_id": str(self.obj_id),
        # }
