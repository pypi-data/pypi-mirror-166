# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import copy
import time


class FileDataAttribute:
    """The class is for Altas file_data entity attirbute."""

    global_entity_id: str
    name: str
    file_name: str
    path: str
    qualifiedName: str
    full_path: str  # full path requires unique
    file_size: int
    archived: bool
    description: str
    owner: str
    time_created: int
    time_lastmodified: int
    namespace: str
    project_code: str
    project_name: str
    bucketName: str
    createTime: int

    def __init__(
        self,
        _id: str,
        file_name: str,
        path: str,
        size: int,
        owner: str,
        namespace: str,
        project_code: str,
        archive: bool,
    ) -> None:

        self.global_entity_id = _id
        self.name = _id
        self.file_name = file_name
        self.path = path
        self.qualifiedName = _id
        self.full_path = _id
        self.file_size = size
        self.owner = owner
        self.namespace = namespace
        self.project_code = project_code
        self.project_name = project_code
        self.bucketName = project_code

        # default params
        self.archived = archive
        self.description = ''
        cur_time = time.time()
        self.time_created = cur_time
        self.time_lastmodified = cur_time
        self.createTime = cur_time

    def json(self):
        return self.__dict__

class Entity:
    typeName: str
    attributes: FileDataAttribute
    # isIncomplete: bool = False
    # status: str = 'ACTIVE'
    createdBy: str = ''
    # version: int = 0
    # relationshipAttributes: dict
    # customAttributes: dict
    # labels: list

    def __init__(self, typeName: str, attributes: FileDataAttribute, createdBy: str = ''):
        self.typeName = typeName
        self.attributes = copy.deepcopy(attributes)
        self.createdBy = createdBy

    def json(self):
        res = {}
        for key, val in self.__dict__.items():
            if isinstance(val, str) or isinstance(val, int):
                res.update({key: val})
            # if we have sub class type, using the json()
            # function to format the return
            else:
                res.update({key: val.json()})

        return res
