"""
This module implements a command-line dialog with the user.
Its goal is to configure a UserInput object with users specifications.
Optionally, values can be passed from the command-line when jina-now is launched. In that case,
the dialog won't ask for the value.
"""
from __future__ import annotations, print_function, unicode_literals

import importlib
import os
import pathlib
from typing import Dict, List, Optional, Union

import cowsay
from hubble import AuthenticationRequiredError
from kubernetes import client, config
from pyfiglet import Figlet

from now.apps.base.app import JinaNOWApp
from now.constants import AVAILABLE_DATASET, Apps, DatasetTypes
from now.deployment.deployment import cmd
from now.log import yaspin_extended
from now.now_dataclasses import UserInput
from now.thirdparty.PyInquirer import Separator
from now.thirdparty.PyInquirer.prompt import prompt
from now.utils import _get_info_hubble, jina_auth_login, sigmap, to_camel_case

cur_dir = pathlib.Path(__file__).parent.resolve()
NEW_CLUSTER = {'name': '🐣 create new', 'value': 'new'}
AVAILABLE_SOON = 'will be available in upcoming versions'


def _configure_app_options(app_instance: JinaNOWApp, user_input, **kwargs):
    for option in app_instance.options:
        val = _prompt_value(
            **option,
            **kwargs,
        )
        setattr(user_input, option['name'], val)
    # _configure_quality(user_input, **kwargs)


def _construct_app(app: Apps) -> JinaNOWApp:
    return getattr(
        importlib.import_module(f'now.apps.{app}.app'),
        f'{to_camel_case(app)}',
    )()


def configure_user_input(**kwargs) -> [JinaNOWApp, UserInput]:
    print_headline()

    user_input = UserInput()
    _configure_app(user_input, **kwargs)
    app_instance = _construct_app(user_input.app)
    _configure_app_options(app_instance, user_input, **kwargs)
    _configure_dataset(app_instance, user_input, **kwargs)
    _configure_cluster(user_input, **kwargs)
    app_instance.run_checks(user_input)
    if user_input.deployment_type == 'remote':
        if _configure_security(user_input, **kwargs):
            if _configure_additional_user(user_input, **kwargs):
                _configure_user_emails(user_input, **kwargs)
    return app_instance, user_input


def print_headline():
    f = Figlet(font='slant')
    print('Welcome to:')
    print(f.renderText('Jina NOW'))
    print('Get your search case up and running - end to end.\n')
    print(
        'You can choose between image and text search. \nJina NOW trains a model, pushes it to Jina Hub '
        'and deploys a Flow and a playground app in the cloud or locally. \nCheck out one of our demos or bring '
        'your own data.\n'
    )
    print('If you want learn more about our framework please visit docs.jina.ai')
    print(
        '💡 Make sure you give enough memory to your Docker daemon. '
        '5GB - 8GB should be okay.'
    )
    print()


def _configure_app(user_input: UserInput, **kwargs) -> None:
    """Asks user questions to set output_modality in user_input"""
    user_input.app = _prompt_value(
        name='app',
        choices=[
            {'name': '📝 ▶ 🏞 text to image search', 'value': Apps.TEXT_TO_IMAGE},
            {'name': '🏞 ▶ 📝 image to text search', 'value': Apps.IMAGE_TO_TEXT},
            {'name': '🏞 ▶ 🏞 image to image search', 'value': Apps.IMAGE_TO_IMAGE},
            {'name': '📝 ▶ 📝 text to text search', 'value': Apps.TEXT_TO_TEXT},
            {
                'name': '📝 ▶ 🎦 text to video search (gif only at the moment)',
                'value': Apps.TEXT_TO_VIDEO,
            },
            {
                'name': '🥁 ▶ 🥁 music to music search',
                'value': Apps.MUSIC_TO_MUSIC,
            },
        ],
        prompt_message='What sort of search engine would you like to build?',
        prompt_type='list',
        **kwargs,
    )


def _configure_dataset(
    app_instance: JinaNOWApp, user_input: UserInput, **kwargs
) -> None:
    """Asks user to set dataset attribute of user_input"""
    _configure_app_dataset(app_instance, user_input, **kwargs)

    if user_input.data in [
        name for name, _ in AVAILABLE_DATASET[app_instance.output_modality]
    ]:
        user_input.is_custom_dataset = False
    else:
        user_input.is_custom_dataset = True
        if user_input.data == 'custom':
            _configure_custom_dataset(user_input, **kwargs)
        else:
            _parse_custom_data_from_cli(user_input)


def _parse_custom_data_from_cli(user_input: UserInput):
    data = user_input.data
    try:
        data = os.path.expanduser(data)
    except Exception:
        pass
    if os.path.exists(data):
        user_input.custom_dataset_type = DatasetTypes.PATH
        user_input.dataset_path = data
    elif 'http' in data:
        user_input.custom_dataset_type = DatasetTypes.URL
        user_input.dataset_url = data
    else:
        user_input.custom_dataset_type = DatasetTypes.DOCARRAY
        user_input.dataset_name = data


def _configure_custom_dataset(user_input: UserInput, **kwargs) -> None:
    """Asks user questions to setup custom dataset in user_input."""
    user_input.custom_dataset_type = _prompt_value(
        name='custom_dataset_type',
        prompt_message='How do you want to provide input? (format: https://docarray.jina.ai/)',
        choices=[
            {
                'name': 'DocArray name (recommended)',
                'value': DatasetTypes.DOCARRAY,
            },
            {
                'name': 'DocArray URL',
                'value': DatasetTypes.URL,
            },
            {
                'name': 'Local path',
                'value': DatasetTypes.PATH,
            },
            {'name': 'Download from S3 bucket', 'value': DatasetTypes.S3_BUCKET},
        ],
        **kwargs,
    )
    if user_input.custom_dataset_type == DatasetTypes.DOCARRAY:
        user_input.dataset_name = _prompt_value(
            name='dataset_name',
            prompt_message='Please enter your DocArray name:',
            **kwargs,
        )

    elif user_input.custom_dataset_type == DatasetTypes.URL:
        user_input.dataset_url = _prompt_value(
            name='dataset_url',
            prompt_message='Please paste in the URL to download your DocArray from:',
            prompt_type='input',
            **kwargs,
        )

    elif user_input.custom_dataset_type == DatasetTypes.PATH:
        user_input.dataset_path = _prompt_value(
            name='dataset_path',
            prompt_message='Please enter the path to the local folder:',
            prompt_type='input',
            **kwargs,
        )

    elif user_input.custom_dataset_type == DatasetTypes.S3_BUCKET:
        user_input.dataset_path = _prompt_value(
            name='dataset_path',
            prompt_message='Please enter the S3 URI to the folder:',
            prompt_type='input',
            **kwargs,
        )
        user_input.aws_access_key_id = _prompt_value(
            name='aws_access_key_id',
            prompt_message='Please enter the AWS access key ID:',
            prompt_type='input',
            **kwargs,
        )
        user_input.aws_secret_access_key = _prompt_value(
            name='aws_secret_access_key',
            prompt_message='Please enter the AWS secret access key:',
            prompt_type='input',
            **kwargs,
        )
        user_input.aws_region_name = _prompt_value(
            name='aws_region_name',
            prompt_message='Please enter the AWS region:',
            prompt_type='input',
            **kwargs,
        )


def _configure_app_dataset(
    app_instance: JinaNOWApp, user_input: UserInput, **kwargs
) -> None:
    user_input.data = _prompt_value(
        name='data',
        prompt_message='What dataset do you want to use?',
        choices=[
            {'name': name, 'value': value}
            for value, name in AVAILABLE_DATASET[app_instance.output_modality]
        ]
        + [
            Separator(),
            {
                'name': '✨ custom',
                'value': 'custom',
            },
        ],
        **kwargs,
    )


def _configure_cluster(user_input: UserInput, skip=False, **kwargs):
    """Asks user question to determine cluster for user_input object"""

    def ask_deployment():
        user_input.deployment_type = _prompt_value(
            name='deployment_type',
            choices=[
                {
                    'name': '⛅️ Jina Cloud',
                    'value': 'remote',
                },
                {
                    'name': '📍 Local',
                    'value': 'local',
                },
            ],
            prompt_message='Where do you want to deploy your search engine?',
            prompt_type='list',
            **kwargs,
        )

    if not skip:
        ask_deployment()

    if user_input.deployment_type == 'remote':
        try:
            jina_auth_login()
        except AuthenticationRequiredError:
            with yaspin_extended(
                sigmap=sigmap, text='Log in to JCloud', color='green'
            ) as spinner:
                cmd('jina auth login')
            spinner.ok('🛠️')

        _get_info_hubble(user_input)
        os.environ['JCLOUD_NO_SURVEY'] = '1'
    else:
        # get all local cluster contexts
        choices = _construct_local_cluster_choices(
            active_context=kwargs.get('active_context'), contexts=kwargs.get('contexts')
        )
        # prompt the local cluster context choices to the user
        user_input.cluster = _prompt_value(
            name='cluster',
            choices=choices,
            prompt_message='On which cluster do you want to deploy your search engine?',
            prompt_type='list',
            **kwargs,
        )
        if user_input.cluster != NEW_CLUSTER['value']:
            if not _cluster_running(user_input.cluster):
                print(
                    f'Cluster {user_input.cluster} is not running. Please select a different one.'
                )
                _configure_cluster(user_input, skip=True, **kwargs)
        else:
            user_input.create_new_cluster = True


def _configure_security(user_input: UserInput, **kwargs):
    user_input.secured = _prompt_value(
        name='secured',
        prompt_message='Do you want to secure the flow?',
        choices=[
            {'name': '✅ yes', 'value': True},
            {'name': '⛔ no', 'value': False},
        ],
        **kwargs,
    )
    return user_input.secured


def _configure_additional_user(user_input: UserInput, **kwargs):
    user_input.additional_user = _prompt_value(
        name='additional_user',
        prompt_message='Do you want to provide additional users access to this flow?',
        choices=[
            {'name': '✅ yes', 'value': True},
            {'name': '⛔ no', 'value': False},
        ],
        **kwargs,
    )
    return user_input.additional_user


def _configure_user_emails(user_input: UserInput, **kwargs):
    user_emails_string = _prompt_value(
        name='user_emails',
        prompt_message='Please enter the comma separated Email IDs'
        ' who will have access to this flow:',
        prompt_type='input',
        **kwargs,
    )
    user_emails = user_emails_string.split(',')
    user_input.user_emails = user_emails


def _construct_local_cluster_choices(active_context, contexts):
    context_names = _get_context_names(contexts, active_context)
    choices = [NEW_CLUSTER]
    # filter contexts with `gke`
    if len(context_names) > 0 and len(context_names[0]) > 0:
        context_names = [context for context in context_names if 'gke' not in context]
        choices = context_names + choices
    return choices


def maybe_prompt_user(questions, attribute, **kwargs):
    """
    Checks the `kwargs` for the `attribute` name. If present, the value is returned directly.
    If not, the user is prompted via the cmd-line using the `questions` argument.

    :param questions: A dictionary that is passed to `PyInquirer.prompt`
        See docs: https://github.com/CITGuru/PyInquirer#documentation
    :param attribute: Name of the value to get. Make sure this matches the name in `kwargs`

    :return: A single value of either from `kwargs` or the user cli input.
    """
    if kwargs and kwargs.get(attribute) is not None:
        return kwargs[attribute]
    else:
        answer = prompt(questions)
        if attribute in answer:
            return answer[attribute]
        else:
            print("\n" * 10)
            cowsay.cow('see you soon 👋')
            exit(0)


def _prompt_value(
    name: str,
    prompt_message: str,
    prompt_type: str = 'input',
    choices: Optional[List[Union[Dict, str]]] = None,
    **kwargs: Dict,
):
    qs = {'name': name, 'type': prompt_type, 'message': prompt_message}

    if choices is not None:
        qs['choices'] = choices
        qs['type'] = 'list'
    return maybe_prompt_user(qs, name, **kwargs)


def _get_context_names(contexts, active_context=None):
    names = [c for c in contexts] if contexts is not None else []
    if active_context is not None:
        names.remove(active_context)
        names = [active_context] + names
    return names


def _cluster_running(cluster):
    config.load_kube_config(context=cluster)
    v1 = client.CoreV1Api()
    try:
        v1.list_namespace()
    except Exception as e:
        return False
    return True
