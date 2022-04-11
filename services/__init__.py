from . import const
import logging
import os

# get a logger for the package.
logging.basicConfig(format='%(asctime)-10s %(levelname)-10s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('journeySharing')

# define some constants for the aws
const.default_region = "us-west-2"
const.default_profile = None
const.AWS_PROFILE = None
const.REDIS_JOURNEY_KEY = "current_journey"
# const.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# const.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
const.AWS_ACCESS_KEY_ID = None 
const.AWS_SECRET_ACCESS_KEY = None
