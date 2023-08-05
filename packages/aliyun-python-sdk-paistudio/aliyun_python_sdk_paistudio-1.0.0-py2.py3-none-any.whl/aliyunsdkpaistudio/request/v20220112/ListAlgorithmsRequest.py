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

class ListAlgorithmsRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PaiStudio', '2022-01-12', 'ListAlgorithms')
		self.set_uri_pattern('/api/v1/algorithms')
		self.set_method('GET')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_PageSize(self): # integer
		return self.get_query_params().get('PageSize')

	def set_PageSize(self, PageSize):  # integer
		self.add_query_param('PageSize', PageSize)
	def get_AlgorithmName(self): # string
		return self.get_query_params().get('AlgorithmName')

	def set_AlgorithmName(self, AlgorithmName):  # string
		self.add_query_param('AlgorithmName', AlgorithmName)
	def get_AlgorithmProvider(self): # string
		return self.get_query_params().get('AlgorithmProvider')

	def set_AlgorithmProvider(self, AlgorithmProvider):  # string
		self.add_query_param('AlgorithmProvider', AlgorithmProvider)
	def get_PageNumber(self): # integer
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self, PageNumber):  # integer
		self.add_query_param('PageNumber', PageNumber)
	def get_AlgorithmId(self): # string
		return self.get_query_params().get('AlgorithmId')

	def set_AlgorithmId(self, AlgorithmId):  # string
		self.add_query_param('AlgorithmId', AlgorithmId)
	def get_WorkspaceId(self): # string
		return self.get_query_params().get('WorkspaceId')

	def set_WorkspaceId(self, WorkspaceId):  # string
		self.add_query_param('WorkspaceId', WorkspaceId)
