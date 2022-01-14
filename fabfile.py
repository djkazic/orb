# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 06:45:34
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-14 06:40:39

import re
import os
from invoke import task, Context, Collection
from build_system import third_party
from build_system import versioning
from build_system import ios
from build_system import submodules
from build_system import documentation
from build_system import test
from build_system import release_notes


namespace = Collection(
    third_party, versioning, ios, submodules, documentation, test, release_notes
)