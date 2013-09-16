###############################################################################
##
##  Copyright 2013 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

__all__ = ('ITestDb', 'IReportGenerator', )

import zope
from zope.interface import Interface, Attribute


class ITestDb(Interface):
   """
   A Test database provides storage and query capabilities
   for test cases, results and related data.
   """

   def importSpec(spec):
      """
      Import a test specification into the test database.

      Returns a pair `(op, id)`, where `op` specifies the operation that
      actually was carried out:

          - None: unchanged
          - 'U': updated
          - 'I': inserted

      The `id` is the new (or existing) database object ID for the spec.
      """


   def getSpecByName(name):
      """
      Find a (currently active, if any) test specification by name.
      """


   def newRun(mode, spec):
      """
      Create a new testsuite run.

      :param mode: The testsuite mode.
      :type mode: str
      :param spec: The test specification.
      :type spec: object (a JSON serializable test spec)
      :returns Deferred -- The test run ID.
      """

   def saveResult(runId, result):
      """
      Saves a test result in the database.

      :param runId: The test run ID.
      :type runId: str
      :param result: The test result. An instance of TestResult.
      :type result: object
      :returns Deferred -- The test result ID.
      """

   def closeRun(runId):
      """
      Closes a testsuite run. After a testsuite run is closed,
      the test result data cannot be changed or new data added.

      :param testRunId: ID of test run as previsouly returned by newRun().
      :type testRunId: str
      """

   def getTestRuns(limit = 10):
      """
      Return a list of latest testruns.
      """

   def getResult(resultId):
      """
      Get a single test result by ID.

      :param resultId: The ID of the test result to retrieve.
      :type resultId: str
      :returns Deferred -- A single instance of TestResult.
      """

   def getResults(runId):
      """
      Get all test results that were ran under the test
      run with the given ID.

      :param runId: The test run ID.
      :type runId: str
      :returns Deferred -- A list of TestResult instances.
      """

   def registerResultFile(resultId, type, sha1, path):
      """
      When a report file generator has produced it's output
      and created (or recreated/modified) a file, it should
      register the file location via this function.

      :param resultId: The ID of the test result this file was generated for.
      :type resultId: str
      :param type: The type of file produced (FIXME: ['html', 'json'] ??)
      :type type: FIXME
      :param sha1: The SHA-1 computed over the generated octet stream.
      :type sha1 str
      :param path: The filesystem path to the generated file.
      :type path: str
      """

ITestDb.TESTMODES = set(['fuzzingwampclient', 'fuzzingclient'])
"""
The list of implemented test modes.
"""


#def computeLink(resultId)


class IReportGenerator(Interface):
   """
   A Report generator is able to produce report files (in a
   format the generator supports) from test results stored
   in a Test database.
   """

   outputDirectory = Attribute("""Default output directory base path. (e.g. 'reports/wamp/servers')""")

   fileExtension = Attribute("""Default file extension for report files (e.g. '.html').""")

   mimeType = Attribute("""Default MIME type for generated reports (e.g. 'text/html').""")


   def writeReportIndexFile(runId, file = None):
      """
      Generate a test report index and write to file like object or
      to an automatically chosen report file (under the default
      output directory

      :param runId: The test run ID for which to generate the index for.
      :type runId: object
      :param file: A file like object or None (automatic)
      :type file: object
      :returns -- None if file was provided, or the pathname
                  of the created report file (automatic).
      """

   def writeReportFile(resultId, file = None):
      """
      Generate a test report and write to file like object or
      to an automatically chosen report file (under the default
      output directory

      :param resultId: The test result ID for which to generate the report for.
      :type resultId: object
      :param file: A file like object or None (automatic)
      :type file: object
      :returns -- None if file was provided, or the pathname
                  of the created report file (automatic).
      """


class ITestRun(Interface):
   """
   """

   def next():
      """
      Returns the next test case for this run or None when
      the test run is finished.

      :returns ICase -- The next test case or None.
      """

   def remaining():
      """
      Number of remaining test cases in this test run.

      :returns int -- Number of remaining test cases.
      """

   def __len__():
      """
      The length of this test run (note that fetching
      test cases does not change the length).
      """




class ITestRunner(Interface):
   """
   """

   def run(spec, observers = []):
      """
      :param observers: An iterable of ITestRunObserver instances.
      :type observers: iterable
      """


class ITestRunObserver(Interface):
   """
   """

   def progress(runId, testRun, test, result, remaining):
      """
      """


class ITestCase(Interface):
   """
   """
   name = Attribute("""Test case name.""")
   description = Attribute("""Test case description.""")
   expectation = Attribute("""Test case expectation.""")

   def run():
      """
      """
