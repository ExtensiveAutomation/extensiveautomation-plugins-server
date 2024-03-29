#!/usr/bin/env python
# -*- coding=utf-8 -*-

# ------------------------------------------------------------------
# Copyright (c) 2018-2019 Denys Barleben
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

from ea.testexecutorlib import TestTemplatesLib as TestTemplatesLib

def ansibleAgent(layerName='ANSIBLE', get=None, event=None, cmd=None):
    """
    Construct a template
    :param layerName:
    :param get:
    :param event:
    :param cmd:
    :return:
    """

    tpl = TestTemplatesLib.TemplateLayer(layerName)

    if get is not None:
        tpl.addKey(name='get', data=get)

    if event is not None:
        tpl.addKey(name='event', data=event)

    if cmd is not None:
        tpl.addKey(name='cmd', data=cmd)

    return tpl
