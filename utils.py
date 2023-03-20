import json
import os
from constants import *


def getHttpHeaders(token: str) -> json:
    return {AUTHORIZATION_HEADER_KEY: AUTHORIZATION_HEADER_VALUE.format(token)}


def openDirIfNotExist(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def checkForPermission(directory: str, permissions) -> bool:
    return os.access(directory, permissions)


def buildCreateReportRequest(argumentsDict: dict) -> dict:
    queryFilter: dict = {}

    if argumentsDict[CREATION_FROM_ARG_KEY] is not None:
        queryFilter[CREATION_TIME_KEY] = {
            FROM_KEY: argumentsDict[CREATION_FROM_ARG_KEY],
            TO_KEY: argumentsDict[CREATION_TO_ARG_KEY]
        }

    if argumentsDict[MODIFIED_FROM_ARG_KEY] is not None:
        queryFilter[LAST_MODIFIED_TIME_KEY] = {
            FROM_KEY: argumentsDict[MODIFIED_FROM_ARG_KEY],
            TO_KEY: argumentsDict[MODIFIED_TO_ARG_KEY]
        }

    if argumentsDict[TEMPLATE_NAMES_ARG_KEY] is not None:
        queryFilter[TEMPLATE_ID_KEY] = {
            IN_KEY: argumentsDict[TEMPLATE_IDS_ARG_KEY]
        }

    query: dict = {
        DATA_TYPE_ARG_KEY: argumentsDict[DATA_TYPE_ARG_KEY],
        FILTER_KEY: queryFilter
    }

    outputMetadata: dict = {
        MAX_FILE_SIZE_IN_BYTES_KEY: MAX_FILE_SIZE_IN_BYTES_VALUE,
        EXPORT_FORMAT_KEY: EXPORT_FORMAT_VALUE
    }

    return {
        QUERIES_KEY: [query],
        OUTPUT_METADATA_KEY: outputMetadata,
        CALLBACK_ENDPOINT_KEY: CALLBACK_ENDPOINT_DUMMY_VALUE
    }
