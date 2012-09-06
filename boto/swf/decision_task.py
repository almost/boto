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
# https://github.com/amazonwebservices/aws-sdk-for-ruby/blob/master/lib/aws/simple_workflow/decision_task.rb

from boto.swf.layer1_decisions import Layer1Decisions
from .history_event import HistoryEvent
from .workflow_type import WorkflowType

class DecisionTask(Layer1Decisions):
    """
    Represents a decision task AND the list of decisions in response
    to it.
    """

    def __init__(self, domain, request_options, data):
        self.domain = domain

        self.request_options = request_options

        self.task_token = data['taskToken']

        workflow_id = data['workflowExecution']['workflowId']
        run_id = data['workflowExecution']['runId']
        # self.workflow_execution = WorkflowExecution.new(domain, workflow_id, run_id)

        name = data['workflowType']['name']
        version = data['workflowType']['version']
        self.workflow_type = WorkflowType(domain, name, version)

        self.previous_started_event_id = data['previousStartedEventId']

        self.started_event_id = data['startedEventId']

        self.next_token = data.get('nextPageToken', None)

        self._events = data['events']

        self._next_page_cache = None
        
        self.responded = False
        Layer1Decisions.__init__(self)
        
    def complete(self, execution_context=None):
        """
        Indicate that the decision task has been completed and return
        all the decisions made to SWF.
        
        :type execution_context: string
        :param execution_context: User defined context to add to
            workflow execution.
        """
        if self.responded:
            raise Exception("Already responded!")
        
        self.domain.layer1.respond_decision_task_completed(self.task_token, self._data, execution_context)

        self.responded = True

    def get_event_by_id(self, event_id):
        """
        Returns the event in the event history with the given id (or
        None if no event with that ID exists)

        :type event_id: int
        :param event_id: The id of the event to return
        """
        # Hardly the most efficient way
        for event in self.events(only_new=False):
            if event.event_id == event_id:
                return event
        return None

    def events(self, only_new=True):
        """
        Returns a generator that gives all of the events in the event
        history. By default it only returns new events (events that
        are new since the previous decision task).

        :type only_new: boolean
        :param only_new: Pass in False to get all events, not just new ones
        """
        def filterfn(event):
            if not only_new:
                return True
            elif self.previous_started_event_id is None:
                return True
            elif event.event_id > self.previous_started_event_id:
                return True
            else:
                return False
                
        for e in self._events:
            event = HistoryEvent(e)
            if filterfn(event):
                yield event
        # If we get to the end of the events and the iterator is still
        # being consumed then request another page and get all the
        # events from that (which will also recursivley get all the
        # events from it's next page and so on)
        if self.next_token:
            if self._next_page_cache is None:
                options = dict(self.request_options)
                options["next_page_token"] = self.next_token
                self._next_page_cache  = self.domain.poll_for_decision_task(**options)
            for event in self._next_page_cache.events(False):
                if filterfn(event):
                    yield event
