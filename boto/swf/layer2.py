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

from .layer1 import Layer1
from .domain import Domain

class Layer2(object):
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 is_secure=True, port=None, proxy=None, proxy_port=None,
                 debug=0, session_token=None, region=None, layer1=None):
        # We support passing in the layer1 to aid testing
        if layer1 is not None:
            self.layer1 = layer1
        else:
            self.layer1 = Layer1(
                aws_secret_access_key, aws_secret_access_key, is_secure, port,
                proxy, proxy_port, debug, session_token, region)
            
    def get_domain(self, name):
        """
        Get a Domain object representing a Glacier domain.

        :type name: string
        :param name: The name of the Glacier domain
        """
        data = self.layer1.describe_domain(name)
        return Domain(self.layer1, data)

    def register_domain(self, name,
                        workflow_execution_retention_period_in_days,
                        description=None):
        """
        Registers a new domain.

        :type name: string
        :param name: Name of the domain to register. The name must be unique.

        :type workflow_execution_retention_period_in_days: int

        :param workflow_execution_retention_period_in_days: Specifies
            the duration *in days* for which the record (including the
            history) of workflow executions in this domain should be kept
            by the service. After the retention period, the workflow
            execution will not be available in the results of visibility
            calls. If a duration of NONE is specified, the records for
            workflow executions in this domain are not retained at all.

        :type description: string
        :param description: Textual description of the domain.

        :raises: SWFDomainAlreadyExistsError, SWFLimitExceededError,
            SWFOperationNotPermittedError
        """
        self.layer1.register_domain(name, str(workflow_execution_retention_period_in_days), description)
        return self.get_domain(name)
