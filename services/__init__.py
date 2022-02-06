from . import const
import logging
import os

# get a logger for the package.
logging.basicConfig(format='%(asctime)-15s  %(message)s')
logger = logging.getLogger('journeySharing')

# define some constants for the aws
const.default_region = "us-west-2"
const.default_role = "operator"
const.default_profile = None
const.AWS_PROFILE = None
# const.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# const.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
const.AWS_ACCESS_KEY_ID = None
const.AWS_SECRET_ACCESS_KEY = None
