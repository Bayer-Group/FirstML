import getpass

from typing import Optional


def create_parameters(
    base_url: str,
    base_path: str,
    data_home: str,
    nodebook_path: str,
    dev_usr: Optional[str] = None,
):
    """Create key-value-store containing global parameters.

    Parameters
    ----------
    base_url : str
        url to open notebooks (e.g., "https://jupyter-us-east-1.xxx.ez.sats.cloud/hub/user-redirect/lab/tree")
    base_path : str
        full path to home folder of jupyterlab (e.g., "/home/dev_usr_folder/")
    data_home : str
        relative path to the folder where to store data outputs, nodebook runs, etc.
        (e.g., "workspace/test/firstml-example/data")
    nodebook_path : str
        relative path to the folder where the nodebooks are stored (nodebooks can be up to one level lower)
        (e.g., "workspace/test/firstml-example/nodebooks")
    dev_usr : str, optional
        name of current user, is retrieved automatically, you can force the named here

    Returns
    -------
    dict
        global parameters encoded as dict
    """

    if dev_usr is None:
        dev_usr = getpass.getuser()

    return {
        "base_url": base_url,
        "base_path": base_path,
        "data_home": data_home,
        "nodebook_path": nodebook_path,
        "dev_usr": dev_usr,
    }
