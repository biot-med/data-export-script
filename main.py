import sys
import subprocess
import time
from datetime import datetime
from threading import Thread
import argparse
from utils import *

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'wget'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'certifi'])

time.sleep(3)

import requests
import wget

token = ''
refreshToken = ''
baseUrl = ''


# ==================================== LOGIN LOGIC ==================================== #
def userLogin(userName: str, pw: str):
    print('login to {}'.format(userName))
    loginBody = {
        USERNAME_KEY: userName,
        PW_KEY: pw
    }
    login(USER_LOGIN_URL_FORMAT.format(baseUrl), loginBody)


def tokenRefresher():
    while True:
        time.sleep(300)
        print('refreshing token')

        refreshTokenLoginBody = {
            REFRESH_TOKEN_KEY: refreshToken
        }
        login(REFRESH_TOKEN_LOGIN_URL_FORMAT.format(baseUrl), refreshTokenLoginBody)


def login(loginUrl: str, loginBody: json):
    global token
    global refreshToken

    loginResponse = requests.post(loginUrl, json=loginBody)
    if loginResponse.status_code != HTTP_OK:
        print('login failed')
        exit()

    print('login succeeded')
    token = loginResponse.json()[ACCESS_JWT_KEY][TOKEN_KEY]
    refreshToken = loginResponse.json()[REFRESH_JWT_KEY][TOKEN_KEY]


# ==================================== EXPORT LOGIC ==================================== #
def createReport(createReportRequest: json) -> str:
    createReportResponse = requests.post(CREATE_REPORT_URL_FORMAT.format(baseUrl), headers=getHttpHeaders(token), json=createReportRequest)

    if createReportResponse.status_code != HTTP_CREATED:
        print('report creation failed, status code: [{}]. error: {}'
              .format(createReportResponse.status_code, createReportResponse.json()))
        exit()

    return createReportResponse.json()[ID_KEY]


def waitOnExport(reportId: str) -> json:
    checkCounter = 1

    while True:
        time.sleep(15)
        print('checking for report status for the {} time...'.format(checkCounter))
        checkCounter += 1

        getReportResponse = requests.get(GET_REPORT_URL_FORMAT.format(baseUrl, reportId), headers=getHttpHeaders(token))

        if getReportResponse.status_code != HTTP_OK:
            print('can not get report with id: [{}]'.format(reportId))
            exit()

        responseBody = getReportResponse.json()
        print('report status is: [{}]'.format(responseBody[REPORT_STATUS_KEY]))
        if responseBody[REPORT_STATUS_KEY] == REPORT_STATUS_IN_PROGRESS:
            continue
        elif responseBody[REPORT_STATUS_KEY] == REPORT_STATUS_FAILED:
            print('export failed for report with id: [{}]'.format(reportId))
            exit()
        else:
            break
    return responseBody


def downloadExportedData(reportToDownload: json, baseOutputPath: str):
    reportId = reportToDownload[ID_KEY]
    print('start downloading output files for report: [{}]'.format(reportId))

    filesLocations: dict = reportToDownload[REPORT_FILE_OUTPUT_KEY][REPORT_FILES_LOCATION_KEY]

    for dataTypeKey, dataTypeValue in filesLocations.items():
        print('start downloading output files for [{}] data type'.format(dataTypeKey))
        outputDirPath = DATA_OUTPUT_DIR_NAME_FORMAT.format(baseOutputPath, OUTPUTS_DIR_NAME, reportId, dataTypeKey)
        openDirIfNotExist(outputDirPath)

        paths: list[str] = dataTypeValue[REPORT_FILES_PATHS_KEY]
        for index, path in enumerate(paths):
            print('start download {} file out of {} files for [{}] data type'
                  .format(index + 1, len(paths), dataTypeKey))
            wget.download(path, out=outputDirPath)


# ==================================== SETTINGS ==================================== #
def getTemplateIdsWithTemplateNames(argumentsDict: dict):
    if argumentsDict[TEMPLATE_NAMES_ARG_KEY] is None:
        return

    searchTemplateRequest: json = {FILTER_KEY: {NAME_KEY: {IN_KEY: argumentsDict[TEMPLATE_NAMES_ARG_KEY]}}}
    url = SEARCH_MINIMIZED_TEMPLATES_URL_FORMAT.format(baseUrl)

    searchTemplatesResponse = requests.get(url, headers=getHttpHeaders(token), params={SEARCH_REQUEST_KEY: json.dumps(searchTemplateRequest)})

    if searchTemplatesResponse.status_code != HTTP_OK:
        print('getting templates failed for request [{}] with status: {}. \nerror: {}'.format(searchTemplatesResponse.url, searchTemplatesResponse.status_code, searchTemplatesResponse.json()))
        exit()

    data: list[dict] = searchTemplatesResponse.json()[DATA_KEY]
    templateIds: list[str] = list(map(lambda template: template[ID_KEY], data))
    argumentsDict[TEMPLATE_IDS_ARG_KEY] = templateIds


# ==================================== ARGUMENTS ==================================== #
def parseArgs(argumentsDict: dict):
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', ARG_FORMAT.format(DATA_TYPE_ARG_KEY), dest=DATA_TYPE_ARG_KEY, required=True,
                        help='Data type to be exported', choices=VALID_DATA_TYPES)
    parser.add_argument('-t', ARG_FORMAT.format(TEMPLATE_NAMES_ARG_KEY), dest=TEMPLATE_NAMES_ARG_KEY, nargs='*', required=False,
                        help='Template names to be exported. if more than one is given write without spaces and separate with comma. Example: template1,template2')
    parser.add_argument(ARG_FORMAT.format(CREATION_FROM_ARG_KEY), dest=CREATION_FROM_ARG_KEY, required=False,
                        help='Limit the data export to only data created after this date. Example: 2023-03-16T10:11:46.612Z')
    parser.add_argument(ARG_FORMAT.format(CREATION_TO_ARG_KEY), dest=CREATION_TO_ARG_KEY, required=False,
                        help='Limit the data export to only data created before this date. Example: 2023-03-16T10:11:46.612Z')
    parser.add_argument(ARG_FORMAT.format(MODIFIED_FROM_ARG_KEY), dest=MODIFIED_FROM_ARG_KEY, required=False,
                        help='Limit the data export to only data modified after this date. Example: 2023-03-16T10:11:46.612Z')
    parser.add_argument(ARG_FORMAT.format(MODIFIED_TO_ARG_KEY), dest=MODIFIED_TO_ARG_KEY, required=False,
                        help='Limit the data export to only data modified before this date. Example: 2023-03-16T10:11:46.612Z')
    parser.add_argument('-u', ARG_FORMAT.format(USERNAME_ARG_KEY), dest=USERNAME_ARG_KEY, required=True,
                        help='The username of the user that performs the export. Needed in order to login to the system')
    parser.add_argument('-p', ARG_FORMAT.format(PASSWORD_ARG_KEY), dest=PASSWORD_ARG_KEY, required=True,
                        help='The Password of the user that performs the export. Needed in order to login to the system.')
    parser.add_argument('-b', ARG_FORMAT.format(BASE_URL_ARG_KEY), dest=BASE_URL_ARG_KEY, required=True,
                        help='Base url for API calls. Example: https://api.dev.biot-med.com')
    parser.add_argument('-o', ARG_FORMAT.format(OUTPUT_PATH_ARG_KEY), dest=OUTPUT_PATH_ARG_KEY, required=False,
                        help='The location on the local computer output files should be downloaded to. If this argument is not provided by the user, the output files will be downloaded to a new directory inside this repository directory.')

    args = parser.parse_known_args().__getitem__(0)

    for key, value in vars(args).items():
        argumentsDict[key] = value


# ==================================== VALIDATION ==================================== #
def validateArguments(argumentsToValidate: dict):
    validateDataType(argumentsToValidate[DATA_TYPE_ARG_KEY])
    validateTimeRange(argumentsToValidate[CREATION_FROM_ARG_KEY], argumentsToValidate[CREATION_TO_ARG_KEY],
                      argumentsToValidate[MODIFIED_FROM_ARG_KEY], argumentsToValidate[MODIFIED_TO_ARG_KEY])
    validateBaseUrl(argumentsToValidate[BASE_URL_ARG_KEY])
    validateOutputPath(argumentsToValidate[OUTPUT_PATH_ARG_KEY])

    if MEASUREMENTS_DATA_TYPE.__eq__(argumentsToValidate[DATA_TYPE_ARG_KEY]):
        validateSpecificToMeasurements(argumentsToValidate)


def validateDataType(dataType: str):
    if dataType not in VALID_DATA_TYPES:
        print('[{}] is not a valid data type. valid date types are: [{}]'.format(dataType, VALID_DATA_TYPES))


def validateTimeRange(creationFrom: str, creationTo: str, modifiedFrom: str, modifiedTo: str):
    validateIsoString(creationFrom)
    validateIsoString(creationTo)
    validateIsoString(modifiedFrom)
    validateIsoString(modifiedTo)

    if (creationFrom is None or creationTo is None) and (modifiedFrom is None or modifiedTo is None):
        print('valid time range must be provided, either [{} and {}] or [{} and {}]'
              .format(CREATION_FROM_ARG_KEY, CREATION_TO_ARG_KEY, MODIFIED_FROM_ARG_KEY, MODIFIED_TO_ARG_KEY))
        exit()


def validateBaseUrl(baseUrlToValidate: str):
    try:
        healthResponse = requests.get(HEALTH_CHECK_URL_FORMAT.format(baseUrlToValidate))
        if healthResponse.status_code != HTTP_OK:
            print('[{}] is not valid base url'.format(baseUrlToValidate))
            exit()
    except:
        print('an error occurred while trying to access: [{}]'.format(baseUrlToValidate))
        exit()


def validateOutputPath(outputPath: str or None):
    if outputPath is None:
        return

    try:
        openDirIfNotExist(outputPath)
    except:
        print('you do not have permissions to write output files at the chosen directory: {}'.format(outputPath))
        exit()

    if not checkForPermission(outputPath, os.W_OK):
        print('you do not have permissions to write output files at the chosen directory: {}'.format(outputPath))
        exit()



def validateSpecificToMeasurements(argumentsToValidate: dict):
    if argumentsToValidate[TEMPLATE_NAMES_ARG_KEY] is not None \
            or argumentsToValidate[MODIFIED_FROM_ARG_KEY] is not None \
            or argumentsToValidate[MODIFIED_TO_ARG_KEY] is not None:
        print('[{}, {}, {}] must not be provided for [measurements] data type'.format(TEMPLATE_NAMES_ARG_KEY, MODIFIED_FROM_ARG_KEY, MODIFIED_TO_ARG_KEY))
        exit()


def validateIsoString(isoString: str):
    if isoString is None:
        return

    try:
        isoStringToCheck = isoString.upper().removesuffix('Z')
        datetime.fromisoformat(isoStringToCheck)
    except:
        print('[{}] is not a valid timestamp. example to valid timestamp: 2023-03-16T10:11:46.612Z'.format(isoString))
        exit()


# ==================================== MAIN ==================================== #
if __name__ == '__main__':
    arguments: dict = {}
    parseArgs(arguments)
    validateArguments(arguments)

    baseUrl = arguments[BASE_URL_ARG_KEY]

    userLogin(arguments[USERNAME_KEY], arguments[PASSWORD_ARG_KEY])
    refreshTokenThread = Thread(target=tokenRefresher)
    refreshTokenThread.daemon = True
    refreshTokenThread.start()

    getTemplateIdsWithTemplateNames(arguments)

    exportRequest = buildCreateReportRequest(arguments)
    print('export request: {}'.format(exportRequest))

    createdReportId = createReport(exportRequest)
    print('created new report with id: [{}]'.format(createdReportId))

    report = waitOnExport(createdReportId)
    downloadExportedData(report, arguments[OUTPUT_PATH_ARG_KEY] if arguments[OUTPUT_PATH_ARG_KEY] is not None else DEFAULT_DOWNLOAD_DIR)

