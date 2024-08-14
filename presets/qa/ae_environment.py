ENVIRONMENT = 'qa'

MEDIA_CONVERT_QUEUE = 'arn:aws:mediaconvert:us-east-1:849505200098:queues/Default'
MEDIA_CONVERT_ROLE_ARN = 'arn:aws:iam::849505200098:role/mediaconvert-test'
MEDIA_CONVERT_ROLE_ID = '7d1102e3-84f5-11e6-9bcf-3c15c2c86b26'

AEUID_SERVICE_BASE = 'https://qnh3p6zbqi.execute-api.us-east-1.amazonaws.com/prod/rally_ids/'
META_EXCHANGE_API_BASE = 'https://pv27xaw4xc.execute-api.us-east-1.amazonaws.com/' + \
    'prod/transform/'
MEDIA_ENTRY_API_BASE = 'https://k0glevemwd.execute-api.us-east-1.amazonaws.com/prod/metadata/core'

BRANDING_INSERTION_LENGTH = 2  # seconds

DELIVERY_ERROR_EMAILS = {
    'tubi': [],
    'pluto': [],
    }

DELIVERY_SUCCESS_EMAILS = {
    'tubi': [],
    'pluto': [],
    }
LOG_LEVEL = 'INFO'