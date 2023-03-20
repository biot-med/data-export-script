# README

# BIOT's export data script

This script can be used in order to export data from the BioT environment and download the exported files on to the user local computer.

## Requirements
- Python 3.9 or above

## How To Use
- Clone this repository to your computer
- Open a new terminal window
- Navigate to the repository directory you've just cloned
- Run the script with the needed arguments (explanation will follow)
- The script will run and when finished the exported data will be stored locally on your computer

## Commands and arguments
- In order to run the script we will use the 'python3 main.py' command with the following arguments.


- [-d | --dataType] **Mandatory: true** The data type for which the export will be performed. While exporting data using this script, only one data type can be exported each time.
  Valid input: {device, device-alert, usage-session, command, organization, patient, organization-user, caregiver, patient-alert, generic-entity, measurements}.
- [-t | --templateNames] **Mandatory: false** When exporting a template base data, it is possible to filter the exported entities to a specific template based entities. 
  To do so pass this argument followed by a list of the template names of which you want to filter the result
  Note: this argument is not relevant for measurement data type.
- [--creationTimeFrom] **Mandatory: false** Limits the data export to only data created after this date. Example: 2023-03-16T10:11:46.612Z. 
  Note: A valid time range constructed either from [--creationTimeFrom and --creationTimeTo] or from [--lastModifiedFrom and lastModifiedTo] or from both.
- [--creationTimeTo] **Mandatory: false** Limits the data export to only data created before this date. Example: 2023-03-16T10:11:46.612Z. 
  Note: A valid time range constructed either from [--creationTimeFrom and --creationTimeTo] or from [--lastModifiedFrom and lastModifiedTo] or from both.
- [--lastModifiedFrom] **Mandatory: false** Limits the data export to only data modified after this date. Example: 2023-03-16T10:11:46.612Z. 
  Note: A valid time range constructed either from [--creationTimeFrom and --creationTimeTo] or from [--lastModifiedFrom and lastModifiedTo] or from both.
  Note: this argument is not relevant for measurement data type.
- [--lastModifiedTo] **Mandatory: false** Limits the data export to only data modified before this date. Example: 2023-03-16T10:11:46.612Z. 
  Note: A valid time range constructed either from [--creationTimeFrom and --creationTimeTo] or from [--lastModifiedFrom and lastModifiedTo] or from both.
  Note: this argument is not relevant for measurement data type.
- [-u | --username] **Mandatory: true** The username of the user that performs the export. Needed in order to login to the system. 
  Note: this user must have permissions to access the exported data
- [-p | --password] **Mandatory: true** The Password of the user that performs the export. Needed in order to login to the system.
- [-b | --baseUrl] **Mandatory: true** The base url for making api calls to the BioT platform. Example: https://api.dev.biot-med.com.
- [-o | --outputPath] **Mandatory: false** The location on the local computer output files should be downloaded to. 
  If this argument is not provided by the user, the output files will be downloaded to a new directory inside this repository directory.


- For help and more information run: 'python3 main.py --help' or 'python3 main.py -h' 

## Run Examples
python3 main.py -d device -u my-name@biot-med.com -p 123456789 -b https://api.dev.biot-med.com --creationTimeFrom 2000-02-07T08:00:18.860Z --creationTimeTo 2023-02-07T08:00:18.860Z -t template1 template2 -o ./my/path 

python3 main.py -d organization -u my-name@biot-med.com -p 123456789 -b https://api.dev.biot-med.com --creationTimeFrom 2000-02-07T08:00:18.860Z --creationTimeTo 2023-02-07T08:00:18.860Z  --lastModifiedFrom 2000-02-07T08:00:18.860Z --lastModifiedTo 2023-02-07T08:00:18.860Z 