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

from .decision_task import DecisionTask
from .activity_task import ActivityTask
import socket

class Domain(object):
    def __init__(self, layer1, name):
        self.layer1 = layer1
        self.name = name

    def poll_for_decision_task(self, task_list, identity=None, next_page_token=None, reverse_order=None):
        """
        Used by deciders to get a DecisionTask from the specified
        decision taskList. A decision task may be returned for any
        open workflow execution that is using the specified task
        list. The task includes a paginated view of the history of the
        workflow execution. The decider should use the workflow type
        and the history to determine how to properly handle the task.

        This initiates a long poll, where the service holds the HTTP
        connection open and responds as soon as a task becomes
        available. The maximum time the service holds on to the
        request before responding is 60 seconds. If no task is
        available within 60 seconds, the poll will return an empty
        result which will be returned as a None.

        :type task_list: string
        :param task_list: Specifies the task list to poll for decision tasks.

        :type identity: string
        :param identity: Identity of the decider making the request,
            which is recorded in the DecisionTaskStarted event in the
            workflow history. This enables diagnostic tracing when
            problems arise. The form of this identity is user defined.

        :type maximum_page_size: integer :param maximum_page_size: The
            maximum number of history events returned in each page. The
            default is 100, but the caller can override this value to a
            page size smaller than the default. You cannot specify a page
            size greater than 100.

        :type next_page_token: string
        :param next_page_token: If on a previous call to this method a
            NextPageToken was returned, the results are being paginated.
            To get the next page of results, repeat the call with the
            returned token and all other arguments unchanged.

        :type reverse_order: boolean
        :param reverse_order: When set to true, returns the events in
            reverse order. By default the results are returned in
            ascending order of the eventTimestamp of the events.

        :raises: UnknownResourceFault, SWFOperationNotPermittedError
        """
        options = dict(task_list=task_list, identity=identity, next_page_token=next_page_token, reverse_order=reverse_order)
        data = self.layer1.poll_for_decision_task(
            domain=self.name, task_list=task_list,
            identity=identity, next_page_token=next_page_token,
            reverse_order=reverse_order)
        if "events" in data:
            return DecisionTask(self, options, data)
        else:
            return None

    def poll_for_activity_task(self, task_list, identity=None):
        """
        Used by workers to get an ActivityTask from the specified
        activity taskList. This initiates a long poll, where the
        service holds the HTTP connection open and responds as soon as
        a task becomes available. The maximum time the service holds
        on to the request before responding is 60 seconds. If no task
        is available within 60 seconds, the poll will return an empty
        result which will be returned as a None. If a task is returned,
        the worker should use its type to identify and process it
        correctly.

        :type task_list: string
        :param task_list: Specifies the task list to poll for activity tasks.

        :type identity: string
        :param identity: Identity of the worker making the request, which
            is recorded in the ActivityTaskStarted event in the workflow
            history. This enables diagnostic tracing when problems arise.
            The form of this identity is user defined.

        :raises: UnknownResourceFault, SWFOperationNotPermittedError
        """
        data = self.layer1.poll_for_activity_task(domain=self.name, task_list=task_list, identity=identity)
        if "activityId" in data:
            return ActivityTask(self, data)
        else:
            return None
