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

class GetNodeMetricsRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PaiStudio', '2022-01-12', 'GetNodeMetrics')
		self.set_uri_pattern('/api/v1/resources/[ResourceGroupID]/nodemetrics/[MetricType]')
		self.set_method('GET')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_MetricType(self): # string
		return self.get_path_params().get('MetricType')

	def set_MetricType(self, MetricType):  # string
		self.add_path_param('MetricType', MetricType)
	def get_ResourceGroupID(self): # string
		return self.get_path_params().get('ResourceGroupID')

	def set_ResourceGroupID(self, ResourceGroupID):  # string
		self.add_path_param('ResourceGroupID', ResourceGroupID)
	def get_GPUType(self): # string
		return self.get_query_params().get('GPUType')

	def set_GPUType(self, GPUType):  # string
		self.add_query_param('GPUType', GPUType)
	def get_TimeStep(self): # string
		return self.get_query_params().get('TimeStep')

	def set_TimeStep(self, TimeStep):  # string
		self.add_query_param('TimeStep', TimeStep)
	def get_EndTime(self): # string
		return self.get_query_params().get('EndTime')

	def set_EndTime(self, EndTime):  # string
		self.add_query_param('EndTime', EndTime)
	def get_StartTime(self): # string
		return self.get_query_params().get('StartTime')

	def set_StartTime(self, StartTime):  # string
		self.add_query_param('StartTime', StartTime)
	def get_Verbose(self): # boolean
		return self.get_query_params().get('Verbose')

	def set_Verbose(self, Verbose):  # boolean
		self.add_query_param('Verbose', Verbose)
