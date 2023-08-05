from typing import Optional, Dict

from lab_partner_utils.commands import lab_build_image_impl


project_name = ''
project_version = ''
project_path = ''


def lab_build_image(registry_name: str, nocache: bool = False, build_args: Optional[Dict[str, str]] = None):
    lab_build_image_impl(registry_name, project_name, project_version, project_path, nocache)
