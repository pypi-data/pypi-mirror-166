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

class CreateAlgorithmVersionRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PaiStudio', '2022-01-12', 'CreateAlgorithmVersion')
		self.set_uri_pattern('/api/v1/algorithms/[AlgorithmId]/versions/[AlgorithmVersion]')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_AlgorithmSpec(self): # String
		return self.get_body_params().get('AlgorithmSpec')

	def set_AlgorithmSpec(self, AlgorithmSpec):  # String
		self.add_body_params('AlgorithmSpec', AlgorithmSpec)
	def get_AlgorithmVersion(self): # string
		return self.get_path_params().get('AlgorithmVersion')

	def set_AlgorithmVersion(self, AlgorithmVersion):  # string
		self.add_path_param('AlgorithmVersion', AlgorithmVersion)
	def get_AlgorithmId(self): # string
		return self.get_path_params().get('AlgorithmId')

	def set_AlgorithmId(self, AlgorithmId):  # string
		self.add_path_param('AlgorithmId', AlgorithmId)
