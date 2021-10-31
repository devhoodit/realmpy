import asyncio
import json

import endpoint
import aiohttp
import msmcauth


async def login(username, id, password, platform='Mojang', version='1.17.1'):
    a = Realm(username, id, password, platform, version)
    await a.auth()
    return a

class Request():
    def __init__(self) -> None:
        pass
    
    async def post(self, endpoint, header={'content-type': 'application/json'}, cookie={}, data={}):
        async with aiohttp.ClientSession(headers=header) as session:
            resp = await session.post(endpoint, json=data)
            return await resp.json(), resp.status
    
    async def get(self, endpoint, header={'content-type': 'application/json'}):
        async with aiohttp.ClientSession(headers=header) as session:
            resp = await session.get(endpoint)
            return await resp.json(), resp.status
   
class Converter:
    def _realmConverter(self, form):
        url = endpoint.URL['realm']['base'].format(
            url=form
        )
        cookie='sid=token:{token}:{uuid};user={username};version={version}'.format(
            token=self.access_token,
            uuid=self.uuid,
            username=self.username,
            version=self.version
        )
        header = {
            'Cookie': cookie,
            'User-Agent': 'Java/1.6.0_27',
            'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2'
        }
        
        return {'endpoint': url, 'header': header}

class Mojang():
    pass

class Realm(Request, Converter):
    
    def __init__(self, username, id, password, platform, version):
        self.id = id
        self.password = password
        self.username = username
        self.version = version
        if platform != 'Mojang' and platform != 'Microsoft':
            raise ValueError
        else:
            self.platform = platform
            
    async def auth(self):
        if self.platform == 'Mojang':
            data = {
                "agent": {
                    "name": "Minecraft",
                    "version": 1    
                },
                "username": self.id,
                "password": self.password,
            }
            url = endpoint.URL['auth']['base'].format(
                url=endpoint.URL['auth']['authenticate']
            )
            player, status = await self.post(url, data=data)
            if status == 200:
                self.access_token = player['accessToken']
                self.uuid = player['selectedProfile']['id']
        
        elif self.platform == 'Microsoft':
            player = msmcauth.login(self.id, self.password)
            
            self.access_token = player.access_token
            self.uuid = player.uuid
    
    async def livePlayers(self):
        resp, status = await self.get(**self._realmConverter(endpoint.URL['realm']['live-players']))
        return resp, status
    
    async def worlds(self):
        resp, status = await self.get(**self._realmConverter(endpoint.URL['realm']['worlds']))
        return resp, status
    
    async def worldId(self, world_id):
        resp, status = await self.get(**self._realmConverter(endpoint.URL['realm']['world-players'].format(
            world_id=world_id
        )))
        return resp, status
    
    async def world_backups(self, world_id):
        resp, status = await self.get(**self._realmConverter(endpoint.URL['realm']['world-backups'].format(
            world_id = world_id
        )))
        return resp, status
    
    async def world_backups_download(self, world_id, map_idx):
        resp, status = await self.get(**self._realmConverter(endpoint.URL['realm']['world-backups-download'].format(
            world_id = world_id,
            map_idx=map_idx
        )))
        return resp, status
    
    async def TOS(self, world_id):
        resp, status = await self.get(**self._realmConverter(endpoint.URL['realm']['TOS'].format(
            world_id=world_id
        )))
        return resp, status 
    
        