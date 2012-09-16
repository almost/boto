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

import json
import time
from .activity_type import ActivityType
from . import exceptions
from boto.swf.exceptions import SWFResponseError

class ActivityTask(object):
    """
    A task received by an activity worker requesting tha an activity
    by run. Methods on this object allow the activity to marked as
    completed or failed and to record heartbeats.
    """
    def __init__(self, domain, data):
        self.domain = domain

        self.task_token = data['taskToken']
        self.activity_id = data['activityId']
        self.started_event_id = data['startedEventId']
        self.input = data['input']

        name = data['activityType']['name']
        version = data['activityType']['version']
        self.activity_type = ActivityType(self.domain, name, version)

        workflow_id = data['workflowExecution']['workflowId']
        run_id = data['workflowExecution']['runId']
        # self.workflow_execution = domain.workflow_executions[workflow_id,run_id]

        self.last_heartbeat = -1

        self.responded = False

    def heartbeat(self, details=None, if_since_last=None):
        """
        Used by activity workers to report to the service that the
        ActivityTask is still making progress. The worker can also
        (optionally) specify details of the progress, for example
        percent complete, using the details parameter. This action can
        also be used by the worker as a mechanism to check if
        cancellation is being requested for the activity task. If a
        cancellation is being attempted for the specified task, then
        the boolean cancelRequested flag returned by the service is
        set to true.

        :type details: string
        :param details: If specified, contains details about the
            progress of the task.
        
        :type if_since_last: string
        :param if_since_last: If an insteger is passed in for
            if_since_last a heartbeat will only be recorded if the last
            hearbeat was recorded more than that number of seconds ago.

        :raises: UnknownResourceFault, SWFOperationNotPermittedError
        """
        if if_since_last and time.time() - self.last_heartbeat < if_since_last:
            # Heartbeat already sent more recently than if_since_last
            return
        if details:
            details = json.dumps(details)
        response = self.domain.layer1.record_activity_task_heartbeat(self.task_token, details)
        if response["cancelRequested"]:
            raise exceptions.SWFActivityCancelRequestedError
        self.last_heartbeat = time.time()

    def complete(self, results=None):
        """
        Used by workers to tell the service that the ActivityTask
        completed successfully with a result (if provided).

        :type result: string
        :param result: The result of the activity task. It is a free
            form string that is implementation specific.

        :raises: UnknownResourceFault, SWFOperationNotPermittedError
        """
        if self.responded:
            raise Exception("Already responded to this activity task")
        if results:
            results = json.dumps(results)
        self.domain.layer1.respond_activity_task_completed(self.task_token, results)
        self.responded = True

    def fail(self, reason=None, details=None):
        """
        Used by workers to tell the service that the ActivityTask has
        failed with reason (if specified).

        :type details: string
        :param details: Optional detailed information about the failure.

        :type reason: string
        :param reason: Description of the error that may assist in diagnostics.

        :raises: UnknownResourceFault, SWFOperationNotPermittedError
        """
        if self.responded:
            raise Exception("Already responded to this activity task")
        if details:
            details = json.dumps(details)
        self.domain.layer1.respond_activity_task_failed(self.task_token, details, reason)
        self.responded = True

    def cancel(self, details=None):
        """
        Used by workers to tell the service that the ActivityTask was
        successfully canceled. Additional details can be optionally
        provided using the details argument.

        :type details: string
        :param details: Optional detailed information about the failure.

        :raises: UnknownResourceFault, SWFOperationNotPermittedError
        """
        if self.responded:
            raise Exception("Already responded to this activity task")
        if details:
            details = json.dumps(details)
        self.domain.layer1.respond_activity_task_cancel(self.task_token, details)
        self.responded = True

    
