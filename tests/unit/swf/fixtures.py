FIXTURE_DOMAIN = {
  # In the examples on the Glacier API docs it lists this param as
  # workflowExecutionRetentionPeriod but in the rest of the docs, and
  # in the live system itself, it's
  # workflowExecutionRetentionPeriodInDays
  "configuration": {"workflowExecutionRetentionPeriodInDays": "60"},
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
