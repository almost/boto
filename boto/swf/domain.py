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

# Currently incomplete, see layer 1 for the the rest of the
# functionality

from .decision_task import DecisionTask
from .activity_task import ActivityTask
import socket

class Domain(object):
    def __init__(self, layer1, data):
        self.layer1 = layer1
        self.name = data["domainInfo"]["name"]
        self.description = data["domainInfo"]["description"]
        self.status = data["domainInfo"]["status"]
        self.execution_retention_period_in_days = int(data["configuration"]["workflowExecutionRetentionPeriod"])

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
    
    def start_workflow_execution(self, workflow_id,
                                 workflow_name, workflow_version,
                                 task_list=None, child_policy=None,
                                 execution_start_to_close_timeout=None,
                                 input=None, tag_list=None,
                                 task_start_to_close_timeout=None):
        """
        Starts an execution of the workflow type in the specified
        domain using the provided workflowId and input data.

        :type workflow_id: string
        :param workflow_id: The user defined identifier associated with
            the workflow execution. You can use this to associate a
            custom identifier with the workflow execution. You may
            specify the same identifier if a workflow execution is
            logically a restart of a previous execution. You cannot
            have two open workflow executions with the same workflowId
            at the same time.

        :type workflow_name: string
        :param workflow_name: The name of the workflow type.

        :type workflow_version: string
        :param workflow_version: The version of the workflow type.

        :type task_list: string
        :param task_list: The task list to use for the decision tasks
            generated for this workflow execution. This overrides the
            defaultTaskList specified when registering the workflow type.

        :type child_policy: string
        :param child_policy: If set, specifies the policy to use for the
            child workflow executions of this workflow execution if it
            is terminated, by calling the TerminateWorkflowExecution
            action explicitly or due to an expired timeout. This policy
            overrides the default child policy specified when registering
            the workflow type using RegisterWorkflowType. The supported
            child policies are:

             * TERMINATE: the child executions will be terminated.
             * REQUEST_CANCEL: a request to cancel will be attempted
                 for each child execution by recording a
                 WorkflowExecutionCancelRequested event in its history.
                 It is up to the decider to take appropriate actions
                 when it receives an execution history with this event.
             * ABANDON: no action will be taken. The child executions
                 will continue to run.

        :type execution_start_to_close_timeout: int
        :param execution_start_to_close_timeout: The total duration for
            this workflow execution. This overrides the
            defaultExecutionStartToCloseTimeout specified when
            registering the workflow type.

        :type input: int
        :param input: The input for the workflow
            execution. This is a free form string which should be
            meaningful to the workflow you are starting. This input is
            made available to the new workflow execution in the
            WorkflowExecutionStarted history event.

        :type tag_list: list :param tag_list: The list of tags to
            associate with the workflow execution. You can specify a
            maximum of 5 tags. You can list workflow executions with a
            specific tag by calling list_open_workflow_executions or
            list_closed_workflow_executions and specifying a TagFilter.

        :type task_start_to_close_timeout: int
        :param task_start_to_close_timeout: Specifies the maximum duration of
            decision tasks for this workflow execution. This parameter
            overrides the defaultTaskStartToCloseTimout specified when
            registering the workflow type using register_workflow_type.


        :rtype: srting
        :return: The runId for the newly started workflow

        :raises: UnknownResourceFault, TypeDeprecatedFault,
            SWFWorkflowExecutionAlreadyStartedError, SWFLimitExceededError,
            SWFOperationNotPermittedError, DefaultUndefinedFault
        """
        response = self.layer1.start_workflow_execution(
            self.name, workflow_id, workflow_name, workflow_version,
            task_list, child_policy, str(execution_start_to_close_timeout),
            input, tag_list, str(task_start_to_close_timeout))
        return response["runId"]
