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

from ea.sutadapters.UDP.client import *
from ea.sutadapters.UDP.server import *
from ea.sutadapters.UDP.codec import *
from ea.sutadapters.UDP.sniffer import *
from ea.sutadapters.UDP.templates import *

__DESCRIPTION__ = """This adapter enables to send/receive data trought UDP transport protocol.

The User Datagram Protocol (UDP) provides a simple transmission of datagrams to the application level between hosts over an Internet Protocol (IP) network.

More informations in the RFC768."""