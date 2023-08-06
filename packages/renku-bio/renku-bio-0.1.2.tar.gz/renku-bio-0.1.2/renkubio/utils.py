import csv
import functools
import json
from io import StringIO
from typing import Any, Dict, Iterable, List, Optional

import click
from renku.command.command_builder.command import Command
from renku.command.dataset import edit_dataset, show_dataset
from renku.command.project import _edit_project, _show_project
from renku.core.management.client import LocalClient
from renku.core.management.repository import DATABASE_METADATA_PATH
from renku.core.util.util import NO_VALUE
from renku.domain_model.provenance.annotation import Annotation
from tabulate import tabulate

style_key = functools.partial(click.style, bold=True, fg="magenta")
style_value = functools.partial(click.style, bold=True)


def nest_dict_items(dic: Dict, src_keys: Iterable[Any], to_key: Any):
    """Given dictionary dic containing keys listed in src_keys, nest
    these keys into a dictionary inside arr_key. dic is modified in place

    Examples
    --------
    >>> d = {'a': 1, 'b': 2, 'c': 3}
    >>> nest_dict_items(d, src_keys=['b', 'c'], to_key='consonants')
    >>> d
    {'a': 1, 'consonants': {'b': 2, 'c': 3}}
    """
    sub_dict = {k: dic.pop(k) for k in src_keys if k in dic}
    dic[to_key] = sub_dict


def prettify_csv(csv_str: str, has_headers=True, **kwargs) -> str:
    r"""Given an input string representing a csv table,
    return the prettified table. Keyword arguments are
    passed to tabulate.tabulate

    Examples
    --------
    >>> prettify_csv("a,b,c\nd,e,f", has_headers=False)
    '-  -  -\na  b  c\nd  e  f\n-  -  -'
    """

    table = list(csv.reader(StringIO(csv_str)))
    if has_headers:
        kwargs["headers"] = table.pop(0)

    return tabulate(table, **kwargs)


def print_key_value(key, value, print_empty: bool = True):
    if print_empty or value:
        click.echo(style_key(key) + style_value(value))


def prettyprint_dict(dic: Dict, prefix=""):
    """Colored and capitalized printing of input dictionary."""
    for k, v in dic.items():
        nice_key = f"{prefix}{k.capitalize()}: "
        # Recurse in case of nested dictionaries and
        # increase indentation level
        if isinstance(v, dict):
            print_key_value(nice_key, "")
            prettyprint_dict(v, prefix=prefix + "  ")
        else:
            print_key_value(nice_key, v)


def get_project_url():
    """Use localclient to build the full Renku project URL."""
    client = LocalClient(path=".", external_storage_requested=False)
    host, owner, name = [client.remote[key] for key in ["host", "owner", "name"]]
    return f"https://{host}/{owner}/{name}"


def get_renku_project() -> Dict:
    """Gets the metadata of the renku project in the current working directory."""

    client = LocalClient(path=".", external_storage_requested=False)
    # Current annotations
    project = (
        Command()
        .command(_show_project)
        .with_client(client)
        .lock_project()
        .with_database()
        .require_migration()
        .build()
        .execute()
        .output.__dict__
    )
    return project


def get_renku_dataset(name: str) -> Dict:
    client = LocalClient(path=".", external_storage_requested=False)
    # Current annotations
    ds = (
        Command()
        .command(show_dataset)
        .with_client(client)
        .lock_project()
        .with_database()
        .require_migration()
        .build()
        .execute(name)
        .output
    )
    return ds


def load_annotations(entity: Dict) -> List[Dict]:
    """Loads custom annotations from project or dataset metadata into a dictionary."""
    # Initialize annotations if needed
    if entity["annotations"] in ([], None):
        annotations = [dict(id=Annotation.generate_id(), body=[], source="renku")]
    else:
        annotations = json.loads(entity["annotations"])

    return annotations


def find_sample_in_annot(annot: List[Dict], name: str) -> int:
    """Returns the index of the annotation body corresponding to input sample name. Returns -1 if sample is not found"""
    body = annot[0]["body"]
    # For each biosample annotation in the body, check if it has the input name.
    for sample_idx, sample in enumerate(body):
        # Malformed samples
        if isinstance(sample, list):
            sample = sample[0]
        if (
            name in sample["http://schema.org/name"][0].values()
            and "http://bioschemas.org/BioSample" in sample["@type"]
        ):
            return sample_idx

    return -1


def edit_annotations(annotations: Dict, dataset: Optional[str] = None):
    """Replace annotations for target dataset. If no dataset name is
    specified, edit project annotations instead. The keyword 'renku-bio'
    is also added automatically if not present."""

    client = LocalClient(path=".", external_storage_requested=False)

    if dataset:
        keywords = get_renku_dataset(dataset)["keywords"]
        edit_cmd = edit_dataset
        # BUG: Renku <=1.6.0 can only parse annotations as dict and
        # not list. This means only 1 biosample/dataset. When this is
        # Fixed, we can remove the limitation (see TODO below.)
        edit_args = dict(
            name=dataset,
            description=NO_VALUE,
            creators=NO_VALUE,
            images=NO_VALUE,
            keywords=NO_VALUE,
            title=NO_VALUE,
            custom_metadata=annotations[0]["body"][
                0
            ],  # TODO: rm last [0] for multisample
        )
    else:
        keywords = get_renku_project()["keywords"]
        edit_cmd = _edit_project
        edit_args = dict(
            description=NO_VALUE,
            creator=NO_VALUE,
            keywords=NO_VALUE,
            custom_metadata=annotations[0]["body"],
        )
    if "renku-bio" not in keywords:
        edit_args["keywords"] = keywords + ["renku-bio"]

    command = (
        Command()
        .command(edit_cmd)
        .with_client(client)
        .lock_project()
        .with_database(write=True)
        .require_migration()
        .with_commit(commit_only=DATABASE_METADATA_PATH)
    )
    command.build().execute(**edit_args)
