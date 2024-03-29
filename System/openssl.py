#!/usr/bin/env python
# -*- coding=utf-8 -*-

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

import sys
import subprocess

from ea.testexecutorlib import TestValidatorsLib as TestValidators
from ea.testexecutorlib import TestTemplatesLib as TestTemplates
from ea.testexecutorlib import TestOperatorsLib as TestOperators
from ea.testexecutorlib import TestAdapterLib as TestAdapter

__NAME__="""OpenSSL"""

AGENT_EVENT_INITIALIZED = "AGENT_INITIALIZED"
AGENT_TYPE_EXPECTED='myagent'

OPENSSL_BIN = "openssl"

class OpenSSL(TestAdapter.Adapter):
		
	def __init__(self, parent, name=None, debug=False, shared=False, agentSupport=False, 
											agent=None, logEventSent=True, logEventReceived=True):
		"""
		OpenSSL wrapper

		@param parent: parent testcase
		@type parent: testcase

		@param name: adapter name used with from origin/to destination (default=None)
		@type name: string/none

		@param debug: active debug mode (default=False)
		@type debug:	boolean

		@param shared: shared adapter (default=False)
		@type shared:	boolean
		
		@param agentSupport: agent support (default=False)
		@type agentSupport: boolean
		
		@param agent: agent to use (default=None)
		@type agent: string/none
		"""
		TestAdapter.Adapter.__init__(self, name = __NAME__, parent = parent, 
																							debug=debug, realname=name,
																							agentSupport=agentSupport, agent=agent, shared=shared,
																							caller=TestAdapter.caller(),
																							agentType=AGENT_TYPE_EXPECTED)
		self.parent = parent
		
		self.logEventSent = logEventSent
		self.logEventReceived = logEventReceived
		self.cfg = {}
		if agent is not None:
			self.cfg['agent'] = agent
			self.cfg['agent-name'] = agent['name']
		self.cfg['agent-support'] = agentSupport
		
		self.TIMER_ALIVE_AGT = TestAdapter.Timer(parent=self, duration=20, name="keepalive-agent", callback=self.aliveAgent,
																																logEvent=False, enabled=True)
		self.__checkConfig()
		
		# initialize the agent with no data
		if agent is not None:
			if self.cfg['agent-support']:
				self.prepareAgent(data={'shared': shared})
				if self.agentIsReady(timeout=30) is None: raise Exception("Agent %s is not ready" % self.cfg['agent-name'] )
				self.TIMER_ALIVE_AGT.start()
			
	def __checkConfig(self):	
		"""
		Private function
		"""
		self.debug("config: %s" % self.cfg)	
		if self.cfg['agent-support'] :
			self.warning('Agent used Name=%s Type=%s' % (self.cfg['agent']['name'], self.cfg['agent']['type']) ) 

	def onReset(self):
		"""
		Called automatically on reset adapter
		"""
		if self.cfg['agent-support'] :
			# stop timer
			self.TIMER_ALIVE_AGT.stop()
			# cleanup remote agent
			self.resetAgent()

	def receivedNotifyFromAgent(self, data):
		"""
		Function to reimplement
		"""
		if data['cmd'] == AGENT_EVENT_INITIALIZED:
			tpl = TestTemplates.TemplateMessage()
			layer = TestTemplates.TemplateLayer('AGENT')
			layer.addKey("ready", True)
			tpl.addLayer(layer= layer)
			self.logRecvEvent( shortEvt = "Agent Is Ready" , tplEvt = tpl )	

	def receivedErrorFromAgent(self, data):
		"""
		Function to reimplement
		"""
		self.error( 'Error on agent: %s' % data )

	def receivedDataFromAgent(self, data):
		"""
		Function to reimplement
		"""
		self.debug( 'Data received from agent: %s' % data )

	def sendNotifyToAgent(self, data):
		"""
		Send notify to agent
		"""
		self.parent.sendNotifyToAgent(adapterId=self.getAdapterId(), agentName=self.cfg['agent-name'], agentData=data)
	
	def prepareAgent(self, data):
		"""
		prepare agent
		"""
		self.parent.sendReadyToAgent(adapterId=self.getAdapterId(), agentName=self.cfg['agent-name'], agentData=data)
	
	def initAgent(self, data):
		"""
		Init agent
		"""
		self.parent.sendInitToAgent(adapterId=self.getAdapterId(), agentName=self.cfg['agent-name'], agentData=data)

	def resetAgent(self):
		"""
		Reset agent
		"""
		self.parent.sendResetToAgent(adapterId=self.getAdapterId(), agentName=self.cfg['agent-name'], agentData='')

	def aliveAgent(self):
		"""
		Keep alive agent
		"""
		self.parent.sendAliveToAgent(adapterId=self.getAdapterId(), agentName=self.cfg['agent-name'], agentData='')
		self.TIMER_ALIVE_AGT.restart()

	def agentIsReady(self, timeout=1.0):
		"""
		Waits to receive "agent ready" event until the end of the timeout
		
		@param timeout: time max to wait to receive event in second (default=1s)
		@type timeout: float	
		
		@return: an event matching with the template or None otherwise
		@rtype: templatemessage		
		"""
		tpl = TestTemplates.TemplateMessage()
		layer = TestTemplates.TemplateLayer('AGENT')
		layer.addKey("ready", True)
		tpl.addLayer(layer= layer)
		evt = self.received( expected = tpl, timeout = timeout )
		return evt
		
		
	def execute(self, cmd):
		"""
		Execute the openssl command

		@param cmd: openssl argument
		@type cmd: string
		"""
		run = "%s %s" % (OPENSSL_BIN, cmd)
		self.debug(run)
		ps = subprocess.Popen(run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		out, err  = ps.communicate() 
		if out is None:
			self.error("unable to run openssl command: %s" % err)
		
		out = out.decode('latin-1').encode("utf-8") 
		
		tpl_rsp = TestTemplates.TemplateMessage()
		layer_openssl = TestTemplates.TemplateLayer('OPENSSL')
		layer_openssl.addKey(name='output', data=out)
		tpl_rsp.addLayer( layer_openssl )
		
		if self.logEventReceived:
			self.logRecvEvent( shortEvt = "openssl event", tplEvt = tpl_rsp ) # log event 		

		
	def hasReceivedEvent(self, expected, timeout=1.0):
		"""
		Wait to receive "openssl event" until the end of the timeout.
		
		@param expected:  output expected
		@type expected: string

		@param timeout: time to wait in seconds (default=1s)
		@type timeout: float
	
		@return: openssl event or none otherwise
		@rtype:	templatemessage/templatelayer/none	
		"""
		TestAdapter.check_timeout(caller=TestAdapter.caller(), timeout=timeout)

		tpl_expected = TestTemplates.TemplateMessage()
		layer_openssl = TestTemplates.TemplateLayer('OPENSSL')
		layer_openssl.addKey(name='output', data=expected)
		tpl_expected.addLayer( layer_openssl )
		
		evt = self.received( expected = tpl_expected, timeout = timeout )
		if evt is None:
			return None
		return evt