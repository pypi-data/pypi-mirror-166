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

class ListTrainingJobLogsRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'PaiStudio', '2022-01-12', 'ListTrainingJobLogs')
		self.set_uri_pattern('/api/v1/trainingjobs/[TrainingJobId]/logs')
		self.set_method('GET')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_TrainingJobId(self): # string
		return self.get_path_params().get('TrainingJobId')

	def set_TrainingJobId(self, TrainingJobId):  # string
		self.add_path_param('TrainingJobId', TrainingJobId)
	def get_WorkerId(self): # string
		return self.get_query_params().get('WorkerId')

	def set_WorkerId(self, WorkerId):  # string
		self.add_query_param('WorkerId', WorkerId)
	def get_PageSize(self): # integer
		return self.get_query_params().get('PageSize')

	def set_PageSize(self, PageSize):  # integer
		self.add_query_param('PageSize', PageSize)
	def get_EndTime(self): # string
		return self.get_query_params().get('EndTime')

	def set_EndTime(self, EndTime):  # string
		self.add_query_param('EndTime', EndTime)
	def get_StartTime(self): # string
		return self.get_query_params().get('StartTime')

	def set_StartTime(self, StartTime):  # string
		self.add_query_param('StartTime', StartTime)
	def get_PageNumber(self): # integer
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self, PageNumber):  # integer
		self.add_query_param('PageNumber', PageNumber)
