#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------
# Copyright (c) 2010-2019 Denis Machard
# This file is part of the extensive automation project
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA
# -------------------------------------------------------------------

import base64 
import uuid

import ea.testexecutorlib import TestLibraryLib as TestLibraryLib

__NAME__="""SessionID"""

class SessionID(TestLibraryLib.Library):
	
	def __init__(self, parent, name=None, debug=False, shared=False):
		"""
		This library can be used to generate session ID. 

		@param parent: testcase 
		@type parent: testcase

		@param name: library name used with from origin/to destination (default=None)
		@type name: string/none
		
		@param debug: True to activate debug mode (default=False)
		@type debug: boolean
		
		@param shared: shared adapter (default=False)
		@type shared:	boolean
		"""
		TestLibraryLib.Library.__init__(self, name = __NAME__, parent = parent, debug=debug, realname=name, shared=shared)
	
	def generate(self):
		"""
		Returns a random, 45-character session ID.
		Example: "NzY4YzFmNDdhMTM1NDg3Y2FkZmZkMWJmYjYzNjBjM2Y5O"
		
		@return: 45-character session ID
		@rtype: string
		"""
		uuid_val = (uuid.uuid4().hex + uuid.uuid4().hex).encode('utf-8')
		session_id = base64.b64encode( uuid_val )[:45] 
		return session_id 