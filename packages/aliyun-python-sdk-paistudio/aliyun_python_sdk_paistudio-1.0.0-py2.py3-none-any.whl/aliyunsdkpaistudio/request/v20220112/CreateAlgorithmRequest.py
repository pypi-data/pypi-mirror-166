# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RoaRequest
from aliyunsdkpaistudio.endpoint import endpoint_data

class CreateAlgorithmRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PaiStudio', '2022-01-12', 'CreateAlgorithm')
		self.set_uri_pattern('/api/v1/algorithms')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_AlgorithmName(self): # string
		return self.get_body_params().get('AlgorithmName')

	def set_AlgorithmName(self, AlgorithmName):  # string
		self.add_body_params('AlgorithmName', AlgorithmName)
	def get_AlgorithmDescription(self): # string
		return self.get_body_params().get('AlgorithmDescription')

	def set_AlgorithmDescription(self, AlgorithmDescription):  # string
		self.add_body_params('AlgorithmDescription', AlgorithmDescription)
	def get_WorkspaceId(self): # string
		return self.get_body_params().get('WorkspaceId')

	def set_WorkspaceId(self, WorkspaceId):  # string
		self.add_body_params('WorkspaceId', WorkspaceId)
