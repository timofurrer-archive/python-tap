# -*- coding: utf-8 -*-

from unittest import TestCase
import sure

import tap


class TapTest(TestCase):
    """
        Test TAP functionalities
    """
    def test_tap_procedure(self):
        """
            Test TAP procedure
        """
        # passed procedure
        passed_proc = tap.TAPProcedure(True)
        passed_proc.passed.should.be.equal("ok")
        str(passed_proc).should.be.equal("ok {id}")

        failed_proc = tap.TAPProcedure(False)
        failed_proc.passed.should.be.equal("not ok")
        str(failed_proc).should.be.equal("not ok {id}")

        full_proc = tap.TAPProcedure(True, "Some Name", "Some Directive", {"key": "some value"})
        full_proc.passed.should.be.equal("ok")
        full_proc.name.should.be.equal("Some Name")
        full_proc.directive.should.be.equal("Some Directive")
        full_proc.data.should.be.equal({"key": "some value"})
        str(full_proc).should.be.equal("""ok {id} - Some Name # Some Directive
  ---
  key: some value
  ...""")

    def test_tap_result_adding_procedure(self):
        """
            Test adding procedure to TAP result
        """
        result = tap.TAPResult()
        result.procedures.should.be.empty
        result.append(True, "Some Name")
        result.procedures.should.have.length_of(1)
        result.procedures[0].passed.should.be.equal("ok")
        result.procedures[0].name.should.be.equal("Some Name")

        result.append(tap.TAPProcedure(False, "Another Proc", tap.TAPProcedure.Directive.TODO))
        result.procedures.should.have.length_of(2)
        result.procedures[1].passed.should.be.equal("not ok")
        result.procedures[1].name.should.be.equal("Another Proc")
        result.procedures[1].directive.should.be.equal(tap.TAPProcedure.Directive.TODO)

    def test_tap_result_adding_procedure_with_iadd_op(self):
        """
            Test adding procedure to TAP result with the += operator
        """
        result = tap.TAPResult()
        result.procedures.should.be.empty
        result += True, "Some Name"
        result.procedures.should.have.length_of(1)
        result.procedures[0].passed.should.be.equal("ok")
        result.procedures[0].name.should.be.equal("Some Name")

        result += tap.TAPProcedure(False, "Another Proc", tap.TAPProcedure.Directive.TODO)
        result.procedures.should.have.length_of(2)
        result.procedures[1].passed.should.be.equal("not ok")
        result.procedures[1].name.should.be.equal("Another Proc")
        result.procedures[1].directive.should.be.equal(tap.TAPProcedure.Directive.TODO)

    def test_tap_result_producer(self):
        """
            Test producing TAP result output
        """
        result = tap.TAPResult()
        result.procedures.should.be.empty
        result += True, "Some Name"
        result += tap.TAPProcedure(False, "Another Proc", "TODO")
        result += True, "Proc with Data", None, {"message": "foo", "severity": "fail"}

        str(result).should.be.equal("""TAP version 13
1..3
ok 1 - Some Name
not ok 2 - Another Proc # TODO
ok 3 - Proc with Data
  ---
  message: foo
  severity: fail
  ...
""")
