# -*- coding: utf-8 -*-
# Copyright (c) 2012 Thomas Parslow http://almostobsolete.net/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

# Based on
#https://github.com/amazonwebservices/aws-sdk-for-ruby/blob/master/lib/aws/simple_workflow/history_event.rb

from boto.swf.layer1_decisions import Layer1Decisions
import json
import datetime

class HistoryEvent(object):
    """
    An event in a workflow execution history.
    """
    def __init__(self, details):
        self.details = details
        self.event_type = self.details['eventType']
        self.event_id = self.details['eventId']
        self.created_at = datetime.datetime.fromtimestamp(self.details['eventTimestamp'])

        attributes_key = "%s%sEventAttributes" % (self.event_type[0].lower(), self.event_type[1:])
        self.attributes = HistoryEventAttributes(details[attributes_key])

def underscores_to_camelcase(name):
    parts = name.split("_")
    return "%s%s" % (parts[0], "".join([x[0].upper() + x[1:] for x in parts[1:]]))
        
class HistoryEventAttributes(object):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        try:
            value = self.data[underscores_to_camelcase(key)]
        except KeyError:
            raise AttributeError(key)
        value = self._cast(key, value)
        setattr(self, key, value)
        return value

    def _cast(self, key, value):
        if isinstance(value, dict):
            value = HistoryEventAttributes(value)
        # TODO: cast other types of values
        return value
