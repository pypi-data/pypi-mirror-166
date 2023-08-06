'''
This module stores custom runtime variables
'''

# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=no-self-argument

import typing

class ArtemisRuntimeManager:
    '''
    This class stores custom runtime information
    '''

    # Custom runtime info
    fields = {}
    runtime_information = {}
    runtime_settings = {}

    # Register fields
    def register_fields(fields : typing.Dict):
        '''
        Register custom fields
        '''
        for key, value in fields.items():
            ArtemisRuntimeManager.fields[key] = value

    # Register run information
    def register_run_information(run_information : typing.Dict):
        '''
        Register run information
        '''
        for key, value in run_information.items():
            ArtemisRuntimeManager.runtime_information[key] = value

    # Register runtime settings
    def register_runtime_settings(runtime_settings : typing.Dict):
        '''
        Register runtime settings
        '''
        ArtemisRuntimeManager.runtime_settings = runtime_settings

    # Get fields
    def get_fields() -> typing.Dict:
        '''
        Get custom fields
        '''
        return ArtemisRuntimeManager.fields
    
    # Get run information
    def get_run_information() -> typing.Dict:
        '''
        Get run information
        '''
        return ArtemisRuntimeManager.runtime_information

    # Get runtime settings
    def get_runtime_settings() -> typing.Dict:
        '''
        Get runtime settings
        '''
        return ArtemisRuntimeManager.runtime_settings