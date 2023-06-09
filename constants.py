# GLOBAL
AUTHORIZATION_HEADER_KEY = 'Authorization'
AUTHORIZATION_HEADER_VALUE = 'Bearer {}'
SEARCH_REQUEST_KEY = 'searchRequest'
ID_KEY = 'id'
DATA_KEY = 'data'
FILTER_KEY = 'filter'
NAME_KEY = 'name'
IN_KEY = 'in'
FROM_KEY = 'from'
TO_KEY = 'to'
MEASUREMENTS_DATA_TYPE = 'measurements'
HTTP_OK = 200
HTTP_CREATED = 201


# LOGIN
USER_LOGIN_PATH = '/ums/v2/users/login'
REFRESH_TOKEN_LOGIN_PATH = '/ums/v2/users/token/login'
USER_LOGIN_URL_FORMAT = '{}' + USER_LOGIN_PATH
REFRESH_TOKEN_LOGIN_URL_FORMAT = '{}' + REFRESH_TOKEN_LOGIN_PATH
ACCESS_JWT_KEY = 'accessJwt'
REFRESH_JWT_KEY = 'refreshJwt'
TOKEN_KEY = 'token'
REFRESH_TOKEN_KEY = 'refreshToken'
USERNAME_KEY = 'username'
PW_KEY = 'password'


# EXPORT
REPORT_BASE_PATH = '/dms/v1/data/reports'
EXPORT_PATH = '/export'
ID_PATH = '/{}'
CREATE_REPORT_PATH = REPORT_BASE_PATH + EXPORT_PATH
CREATE_REPORT_URL_FORMAT = '{}' + CREATE_REPORT_PATH
GET_REPORT_PATH = REPORT_BASE_PATH + ID_PATH
GET_REPORT_URL_FORMAT = '{}' + GET_REPORT_PATH
HEALTH_CHECK_PATH = '/dms/system/healthCheck'
HEALTH_CHECK_URL_FORMAT = '{}' + HEALTH_CHECK_PATH

REPORT_STATUS_KEY = 'status'
REPORT_STATUS_COMPLETED = 'COMPLETED'
REPORT_STATUS_IN_PROGRESS = 'IN_PROGRESS'
REPORT_STATUS_FAILED = 'FAILED'

REPORT_FILE_OUTPUT_KEY = 'fileOutput'
REPORT_FILES_LOCATION_KEY = 'filesLocation'
REPORT_FILES_PATHS_KEY = 'paths'

DATA_OUTPUT_DIR_NAME_FORMAT = '{}/{}/{}/{}'
OUTPUTS_DIR_NAME = 'outputs'

CREATION_TIME_KEY = '_creationTime'
LAST_MODIFIED_TIME_KEY = '_lastModifiedTime'
TEMPLATE_ID_KEY = '_templateId'
OUTPUT_METADATA_KEY = 'outputMetadata'
MAX_FILE_SIZE_IN_BYTES_KEY = 'maxFileSizeInBytes'
MAX_FILE_SIZE_IN_BYTES_VALUE = 100000
EXPORT_FORMAT_KEY = 'exportFormat'
EXPORT_FORMAT_VALUE = 'CSV'
CALLBACK_ENDPOINT_KEY = 'callbackEndpoint'
CALLBACK_ENDPOINT_DUMMY_VALUE = 'http://dummy.com'
QUERIES_KEY = 'queries'
DEFAULT_DOWNLOAD_DIR = '.'


# ARGUMENTS
ARG_FORMAT = '--{}'
DATA_TYPE_ARG_KEY = 'dataType'
TEMPLATE_NAMES_ARG_KEY = 'templateNames'
TEMPLATE_IDS_ARG_KEY = 'templateIds'
CREATION_FROM_ARG_KEY = 'creationTimeFrom'
CREATION_TO_ARG_KEY = 'creationTimeTo'
MODIFIED_FROM_ARG_KEY = 'lastModifiedFrom'
MODIFIED_TO_ARG_KEY = 'lastModifiedTo'
USERNAME_ARG_KEY = 'username'
PASSWORD_ARG_KEY = 'password'
BASE_URL_ARG_KEY = 'baseUrl'
OUTPUT_PATH_ARG_KEY = 'outputPath'


#  SETTINGS
SEARCH_MINIMIZED_TEMPLATES_PATH = '/settings/v1/templates/minimized'
SEARCH_MINIMIZED_TEMPLATES_URL_FORMAT = '{}' + SEARCH_MINIMIZED_TEMPLATES_PATH


# VALIDATION
VALID_DATA_TYPES = ['device', 'device-alert', 'usage-session', 'command', 'organization', 'patient', 'organization-user', 'caregiver', 'patient-alert', 'generic-entity', 'measurements']

