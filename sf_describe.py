import requests
import json
import re
import datetime
import xlsxwriter
import os
from sf_authentication import SfAuth
from getpass import getpass

AUTH = SfAuth()
API_VERSION = '52.0'
OBJ_DETAIL_KEYS = [
    'name',
    'label',
    'labelPlural',
    'networkScopeFieldName',
    'keyPrefix',
    'custom',
    'customSetting',
    'hasSubtypes',
    'isSubtype',
    'activateable',
    'createable',
    'updateable',
    'deletable',
    'undeletable',
    'queryable',
    'searchable',
    'mergeable',
    'triggerable',
    'layoutable',
    'compactLayoutable',
    'lookupLayoutable',
    'searchLayoutable',
    'listviewable',
    'replicateable',
    'retrieveable',
    'deprecatedAndHidden',
    'feedEnabled',
    'mruEnabled'
]
OBJ_FIELD_KEYS = [
    'label',
    'name',
    'type',
    'soapType',
    'custom',
    'length',
    'scale',
    'precision',
    'digits',
    'byteLength',
    'picklistValues',
    'defaultValue',
    'defaultValueFormula',
    'defaultedOnCreate',
    'htmlFormatted',
    'calculated',
    'calculatedFormula',
    'idLookup',
    'unique',
    'caseSensitive',
    'encrypted',
    'externalId',
    'autoNumber',
    'inlineHelpText',
    'controllerName',
    'dependentPicklist',
    'restrictedPicklist',
    'mask',
    'maskType',
    'nillable',
    'sortable',
    'createable',
    'updateable',
    'aggregatable',
    'searchPrefilterable',
    'filterable',
    'groupable',
    'permissionable',
    'aiPredictionField',
    'cascadeDelete',
    'compoundFieldName',
    'deprecatedAndHidden',
    'displayLocationInDecimal',
    'extraTypeInfo',
    'filteredLookupInfo',
    'formulaTreatNullNumberAsZero',
    'highScaleNumber',
    'nameField',
    'namePointing',
    'polymorphicForeignKey',
    'queryByDistance',
    'referenceTargetField',
    'referenceTo',
    'relationshipName',
    'relationshipOrder',
    'restrictedDelete',
    'writeRequiresMasterRead'
]

def prompt_user_for_credentials():
    environment = {}
    print('\nWhat is the Login URL?')
    print('  Type 1 for Production (https://login.salesforce.com)')
    print('  Type 2 for a Sandbox (https://test.salesforce.com)')
    print('  Or enter a custom domain such as "https://MYDOMAIN.my.salesforce.com"')
    environmentType = input()
    if environmentType == '1':
        environment['login_url'] = 'https://login.salesforce.com'
    elif environmentType == '2':
        environment['login_url'] = 'https://test.salesforce.com'
    else:
        environment['login_url'] = environmentType
    environment['username'] = input('\nEnter the Username\n')
    environment['password'] = getpass('\nEnter the Password\n')
    environment['client_id'] = input('\nEnter the Client Id\n')
    environment['client_secret'] = input('\nEnter the Client Secret\n')
    return environment



def create_sub_folder(root_path):
    dt_string = datetime.datetime.now().strftime("%Y-%m-%d--%I-%M-%S-%p")
    folder_name = root_path + '/Salesforce Schema ' + dt_string
    os.mkdir(folder_name)
    return folder_name


def get_active_picvals(picvals):
    values = []

    if picvals:
        for picval in picvals:
            if picval['active']:
                values.append(picval["label"])

    return values


def get_filtered_lookups(data):
    items = []

    if data:
        for item in data:
            fields = ", ".join(data["controllingFields"])
            items.append(
                "Dependent: {} | Optional Filter: {} | Controlling Fields: {}".format(data["dependent"], data["optionalFilter"], fields))

    return items


def get_object_details(data):
    details = {}
    for key in OBJ_DETAIL_KEYS:
        details[convert_to_title_case(key)] = data[key]
    return details


def get_object_fields(data):
    fields = []

    for field in data["fields"]:
        details = {}
        for key in OBJ_FIELD_KEYS:
            if key == 'picklistValues':
                details[convert_to_title_case(key)] = '\n'.join(
                    get_active_picvals(field[key])) if field[key] else ''
            elif key == 'filteredLookupInfo':
                details[convert_to_title_case(key)] = '\n'.join(
                    get_filtered_lookups(field[key]))
            elif key == 'referenceTo':
                details[convert_to_title_case(key)] = '\n'.join(
                    field[key]) if field[key] else ''
            else:
                details[convert_to_title_case(key)] = field[key]

        fields.append(details)

    return fields


def get_credentials():
    if os.path.exists(".credentials.json"):
        with open('.credentials.json') as json_file:
            cred_data = json.load(json_file)
        print('Which environment?')
        env_id = 1
        for env in cred_data['environments']:
            print('  Type {} for {}'.format(env_id, env['name']))
            env_id = env_id + 1
        print('  Type {} to use custom credentials'.format(env_id))
        selected_env_id = int(input())
        if selected_env_id == env_id:
            return get_custom_credentials()
        else:
            return cred_data['environments'][selected_env_id - 1]
    else:
        return get_custom_credentials()

def get_custom_credentials():
    new_env = prompt_user_for_credentials()
    print('\nSave Environment?')
    save_creds = input('  y = yes,\n  n = no\n')
    if save_creds.lower() == 'y':
        save_credentials(new_env)
    return new_env


def save_credentials(env):
    print('┌───────────────────────────────────────────────────────┐')
    print('│                      ▲ WARNING ▲                      │')
    print('├───────────────────────────────────────────────────────┤')
    print('│ Passwords and keys will be stored in plain text. Make │')
    print('│ sure that the .credentials.json is not accessable by  │')
    print('│ untrusted users and will not be tracked by git. By    │')
    print('│ default, the .gitignore file should be set to not     │')
    print('│ this file                                             │')
    print('└───────────────────────────────────────────────────────┘')
    env_name = input('\nEnter a name for this environment\n')
    env['name'] = env_name
    envs = {}
    if os.path.exists(".credentials.json"):
        with open('.credentials.json', 'r') as json_file:
            envs = json.load(json_file)
        envs['environments'].append(env)
        with open('.credentials.json', 'w') as json_file:
            json.dump(envs, json_file, indent=4)
    else:
        envs['environments'] = []
        envs['environments'].append(env)
        with open('.credentials.json', 'w') as json_file:
            json.dump(envs, json_file, indent=4)

def save_setting(key, value):
    settings = {}
    if os.path.exists(".settings.json"):
        with open('.settings.json', 'r') as json_file:
            settings = json.load(json_file)
    settings[key] = value
    with open('.settings.json', 'w') as json_file:
        json.dump(settings, json_file, indent=4)

    print('...saved')

def get_setting(key):
    value = None
    if os.path.exists(".settings.json"):
        with open('.settings.json', 'r') as json_file:
            settings = json.load(json_file)
            if key in settings:
                value = settings[key]

    return value

def get_custom_path():
    print('\nEnter the path where the files will be saved')
    selected_path = input()

    while not os.path.exists(selected_path) and not os.path.isdir(selected_path):
        print('\nThis does not appear to be a valid directory. Please try again')
        selected_path = input()
    
    return selected_path


def prompt_for_file_path():
    default_path = get_setting('defaultPath')
    if default_path is not None:
        print('\nSave the files in the Default Path?')
        print('  Enter y to use: ' + default_path)
        print('  Enter n to senter a new path')
        use_default = input()
        if use_default.lower() == 'y':
            if os.path.exists(default_path) and os.path.isdir(default_path):
                return default_path
            else:
                print('\nThis does not appear to be a valid directory. Please enter a new one')
                return get_custom_path()
        else:
            return get_custom_path()
    else:
        return get_custom_path()

def convert_to_title_case(camel_case_string):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub(' ', camel_case_string).title()


def describe(sObjectName, api_version, token_data):
    base_path = token_data['instance_url']
    resource_path = '/services/data/v' + api_version + '/sobjects/'
    endpoint = base_path + resource_path + sObjectName + '/describe'
    headers = {
        'Authorization': token_data['token_type'] + ' ' + token_data['access_token']}

    resp = requests.get(endpoint, headers=headers)
    return resp.json()


def write_excel(subfolder, details, fields):
    workbook = xlsxwriter.Workbook(
        subfolder + '/' + details['Label'] + '.xlsx')

    cell_format_justify = workbook.add_format()
    cell_format_justify.set_align('justify')

    cell_format_wrap = workbook.add_format()
    cell_format_wrap.set_text_wrap()

    details_sheet = workbook.add_worksheet("Details")
    details_sheet.set_column("A:A", 26)
    details_sheet.write_column("A1", details.keys())
    details_sheet.write_column("B1", details.values())

    fields_sheet = workbook.add_worksheet("Fields")
    fields_sheet.write_row("A1", fields[0].keys())
    row = 1
    for field in fields:
        fields_sheet.write_row(row, 0, field.values())
        row += 1

    # fields_sheet.write(0, 0, None, cell_format_justify)
    fields_sheet.autofilter(0, 0, 1, len(fields[0].values()))

    workbook.close()


creds = get_credentials()
token_data = AUTH.get_session_id_conn_app(username=creds['username'], password=creds['password'],
                                          client_id=creds['client_id'], client_secret=creds['client_secret'], base_path=creds['login_url'])

if 'access_token' in token_data: 
    print('\nWhich Objects? (comma seperated)')
    obj_string = input()
    objects_to_describe = obj_string.split(',')

    file_path = prompt_for_file_path()

    if(file_path != get_setting('defaultPath')):
        print('\nSave this path as the default output location?')
        print('  y = yes')
        print('  n = n')
        save_path = input()
        if save_path.lower() == 'y':
            print('saving settings...')
            save_setting('defaultPath', file_path)

    describe_results = []
    print('\nFetching the data from Salesforce...')
    for sObjectName in objects_to_describe:
        describe_results.append(
            describe(sObjectName.strip(), API_VERSION, token_data))

    output_folder = create_sub_folder(file_path)
    for result in describe_results:
        details = get_object_details(result)
        fields = get_object_fields(result)
        write_excel(output_folder, details, fields)

    print('\nDONE! The output was saved to ' + output_folder)
else:
    if 'error' in token_data:
        print('\nERROR:' + token_data['error'])
        if 'error_description' in token_data:
            print('\nERROR DESCRIPTION:' + token_data['error_description'])
    else:
        print('\nERROR: Unable to authenticate')
