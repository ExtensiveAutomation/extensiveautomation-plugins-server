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

import hashlib

import ea.testexecutorlib import TestLibraryLib as TestLibraryLib

__NAME__="""SHA256"""

class SHA256(TestLibraryLib.Library):
	
	def __init__(self, parent, name=None, debug=False, shared=False):
		"""
		This library implements the SHA-2 256 cryptographic hash function.
		
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
	
	def compute (self, data, hexdigit=True):
		"""
		Return the digest of the string data, the result containing  hexadecimal digits (32 octets) or string.
		
		@param data: data 
		@type data: string

		@param hexdigit: return hexadecimal representation (default=True) 
		@type hexdigit: boolean
		
		@return: sha256 digest
		@rtype: string
		"""
		if hexdigit:
			hash =  hashlib.sha256()
			hash.update(data)
			return hash.hexdigest()
		else:
			hash =  hashlib.sha256()
			hash.update(data)
			return hash.digest()