URL = {
    'realm': {
        'base': 'https://pc.realms.minecraft.net{url}',
        'mco-available': 'https://pc.realms.minecraft.net',
        'worlds': '/worlds',
        'world-players': '/worlds/{world_id}',
        'live-players': '/activities/liveplayerlist',
        'TOS': '/worlds/v1/{world_id}/join/pc',
        'world-backups': '/worlds/{world_id}/backups',
        'world-backups-download': '/worlds/{world_id}/slot/{map_idx}/download'
        
    },
    'auth': {
        'base': 'https://authserver.mojang.com{url}',
        'authenticate': '/authenticate'
    }
}