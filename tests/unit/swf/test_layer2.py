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

try:
    import unittest2 as unittest
except ImportError:
    import unittest
import httplib

from mock import Mock

from boto.swf.layer1 import Layer1
from boto.swf.layer2 import Layer2
from boto.swf.domain import Domain
from boto.swf.activity_task import ActivityTask
from boto.swf.decision_task import DecisionTask
from boto.swf.history_event import HistoryEvent
from boto.swf.workflow_type import WorkflowType

FIXTURE_DOMAIN = {
  "configuration": {"workflowExecutionRetentionPeriod": "60"},
  "domainInfo": {
    "description": "music",
    "name": "867530901",
    "status": "REGISTERED"
  }
}

FIXTURE_DECISION_TASK = {
  "events":
  [
    {"decisionTaskStartedEventAttributes":
      {"identity": "Decider01",
       "scheduledEventId": 2},
     "eventId": 3,
     "eventTimestamp": 1326593394.566,
     "eventType": "DecisionTaskStarted"},
    {"decisionTaskScheduledEventAttributes":
      {"startToCloseTimeout": "600",
       "taskList":
        {"name": "specialTaskList"}
      },
     "eventId": 2,
     "eventTimestamp": 1326592619.474,
     "eventType": "DecisionTaskScheduled"},
    {"eventId": 1,
     "eventTimestamp": 1326592619.474,
     "eventType": "WorkflowExecutionStarted",
     "workflowExecutionStartedEventAttributes":
      {"childPolicy": "TERMINATE",
       "executionStartToCloseTimeout": "3600",
       "input": "arbitrary-string-that-is-meaningful-to-the-workflow",
       "parentInitiatedEventId": 0,
       "tagList":
        ["music purchase", "digital", "ricoh-the-dog"],
       "taskList":
        {"name": "specialTaskList"},
       "taskStartToCloseTimeout": "600",
       "workflowType":
        {"name": "customerOrderWorkflow",
         "version": "1.0"}
      }
    }
  ],
 "previousStartedEventId": 0,
 "startedEventId": 3,
 "taskToken": "AAAAKgAAAAEAAAAAAAAAATZDvCYwk/hP/X1ZGdJhb+T6OWzcBx2DPhsIi5HF4aGQI4OXrDE7Ny3uM+aiAhGrmeNyVAa4yNIBQuoZuJA5G+BoaB0JuHFBOynHDTnm7ayNH43KhMkfdrDG4elfHSz3m/EtbLnFGueAr7+3NKDG6x4sTKg3cZpOtSguSx05yI1X3AtscS8ATcLB2Y3Aub1YonN/i/k67voca/GFsSiwSz3AAnJj1IPvrujgIj9KUvckwRPC5ET7d33XJcRp+gHYzZsBLVBaRmV3gEYAnp2ICslFn4YSjGy+dFXCNpOa4G1O8pczCbFUGbQ3+5wf0RSaa/xMq2pfdBKnuFp0wp8kw1k+5ZsbtDZeZn8g5GyKCLiLms/xD0OxugGGUe5ZlAoHEkTWGxZj/G32P7cMoCgrcACfFPdx1LNYYEre7YiGiyjGnfW2t5mW7VK9Np28vcXVbdpH4JNEB9OuB1xqL8N8ifPVtc72uxB1i9XEdq/8rkXasSEw4TubB2FwgqnuJstmfEhpOdb5HfhR6OwmnHuk9eszO/fUkGucTUXQP2hhB+Gz",
 "workflowExecution":
  {"runId": "06b8f87a-24b3-40b6-9ceb-9676f28e9493",
   "workflowId": "20110927-T-1"},
 "workflowType":
  {"name": "customerOrderWorkflow",
   "version": "1.0"}
}

FIXTURE_ACTIVITY_TASK = {
 "activityId": "verification-27",
 "activityType":
  {"name": "activityVerify",
   "version": "1.0"},
 "input": "5634-0056-4367-0923,12/12,437",
 "startedEventId": 11,
 "taskToken": "AAAAKgAAAAEAAAAAAAAAAX9p3pcp3857oLXFUuwdxRU5/zmn9f40XaMF7VohAH4jOtjXpZu7GdOzEi0b3cWYHbG5b5dpdcTXHUDPVMHXiUxCgr+Nc/wUW9016W4YxJGs/jmxzPln8qLftU+SW135Q0UuKp5XRGoRTJp3tbHn2pY1vC8gDB/K69J6q668U1pd4Cd9o43//lGgOIjN0/Ihg+DO+83HNcOuVEQMM28kNMXf7yePh31M4dMKJwQaQZG13huJXDwzJOoZQz+XFuqFly+lPnCE4XvsnhfAvTsh50EtNDEtQzPCFJoUeld9g64V/FS/39PHL3M93PBUuroPyHuCwHsNC6fZ7gM/XOKmW4kKnXPoQweEUkFV/J6E6+M1reBO7nJADTrLSnajg6MY/viWsEYmMw/DS5FlquFaDIhFkLhWUWN+V2KqiKS23GYwpzgZ7fgcWHQF2NLEY3zrjam4LW/UW5VLCyM3FpVD3erCTi9IvUgslPzyVGuWNAoTmgJEWvimgwiHxJMxxc9JBDR390iMmImxVl3eeSDUWx8reQltiviadPDjyRmVhYP8",
 "workflowExecution":
  {"runId": "cfa2bd33-31b0-4b75-b131-255bb0d97b3f",
   "workflowId": "20110927-T-1"}
}

class SWFLayer2Base(unittest.TestCase):
    def setUp(self):
        self.mock_layer1 = Mock(spec=Layer1)

class TestSWFLayer2Connection(SWFLayer2Base):
    def setUp(self):
        SWFLayer2Base.setUp(self)
        self.layer2 = Layer2(layer1=self.mock_layer1)
        
    def test_get_domain(self):
        self.mock_layer1.describe_domain.return_value = FIXTURE_DOMAIN
        domain = self.layer2.get_domain("867530901")
        assert domain.name == "867530901"
        assert domain.status == "REGISTERED"
        assert domain.execution_retention_period_in_days == 60

    def test_register_domain(self):
        self.mock_layer1.describe_domain.return_value = FIXTURE_DOMAIN
        domain = self.layer2.register_domain("867530901", 60, "My domain")
        assert domain.name == "867530901"
        self.mock_layer1.register_domain.assert_called_with("867530901", "60", "My domain")

class TestSWFDomain(SWFLayer2Base):
    def setUp(self):
        SWFLayer2Base.setUp(self)
        self.domain = Domain(layer1=self.mock_layer1, data=FIXTURE_DOMAIN)

    def test_poll_for_decision_task(self):
        self.mock_layer1.poll_for_decision_task.return_value = FIXTURE_DECISION_TASK 
        task = self.domain.poll_for_decision_task("mytasklist", "me")
        assert task.task_token == "AAAAKgAAAAEAAAAAAAAAATZDvCYwk/hP/X1ZGdJhb+T6OWzcBx2DPhsIi5HF4aGQI4OXrDE7Ny3uM+aiAhGrmeNyVAa4yNIBQuoZuJA5G+BoaB0JuHFBOynHDTnm7ayNH43KhMkfdrDG4elfHSz3m/EtbLnFGueAr7+3NKDG6x4sTKg3cZpOtSguSx05yI1X3AtscS8ATcLB2Y3Aub1YonN/i/k67voca/GFsSiwSz3AAnJj1IPvrujgIj9KUvckwRPC5ET7d33XJcRp+gHYzZsBLVBaRmV3gEYAnp2ICslFn4YSjGy+dFXCNpOa4G1O8pczCbFUGbQ3+5wf0RSaa/xMq2pfdBKnuFp0wp8kw1k+5ZsbtDZeZn8g5GyKCLiLms/xD0OxugGGUe5ZlAoHEkTWGxZj/G32P7cMoCgrcACfFPdx1LNYYEre7YiGiyjGnfW2t5mW7VK9Np28vcXVbdpH4JNEB9OuB1xqL8N8ifPVtc72uxB1i9XEdq/8rkXasSEw4TubB2FwgqnuJstmfEhpOdb5HfhR6OwmnHuk9eszO/fUkGucTUXQP2hhB+Gz"
        assert len(list(task.events())) == 3

    def test_poll_for_activitity_task(self):
        self.mock_layer1.poll_for_activity_task.return_value = FIXTURE_ACTIVITY_TASK 
        task = self.domain.poll_for_activity_task("mytasklist", "me")
        assert task.activity_id == "verification-27"
        assert task.activity_type.name == "activityVerify"
        assert task.activity_type.version == "1.0"

    def test_start_workflow_execution(self):
        self.mock_layer1.start_workflow_execution.return_value = {"runId": "boom"}
        assert self.domain.start_workflow_execution("newid","workflow", "1.0") == "boom"
        
class TestSWFActivityTask(SWFLayer2Base):
    # TODO
    pass
    
class TestSWFDecisionTask(SWFLayer2Base):
    # TODO
    pass

class TestSWFHistoryEvent(SWFLayer2Base):
    # TODO
    pass
