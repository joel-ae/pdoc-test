"""
This module contains the RallyAsset class, which is used to represent an asset in Rally.
"""


class RallyAsset:
    def __init__(self, name, asset_type, asset_id, asset_url):
        self.name = name
        self.asset_type = asset_type
        self.asset_id = asset_id
        self.asset_url = asset_url

    def __str__(self):
        return f'{self.name} ({self.asset_type})'

    def __repr__(self):
        return f'{self.name} ({self.asset_type})'
