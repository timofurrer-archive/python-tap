# -*- coding: utf-8 -*-

"""
    Module providing a TAPWriter and a TAPProcedure representation class.
"""

__version__ = "0.0.1"
__author__ = "Timo Furrer"
__email__ = "tuxtimo@gmail.com"

import yaml


class TAPError(Exception):
    """
        Base class for all TAP errors
    """
    pass


class BailOutError(TAPError):
    """
        This exception is raised if the expected test plan
        overflows.
    """
    def __init__(self, plan):
        TAPError.__init__(self, "Bail Out! Expected test plan of {} tests overflowed".format(plan))


class TAPProcedure(object):  # pylint: disable=too-few-public-methods
    """
        Represents one TAP procedure
    """
    class Directive(object):  # pylint: disable=too-few-public-methods
        """
            All allowed directives
        """
        TODO = "TODO"
        SKIP = "SKIP"


    def __init__(self, passed, name=None, directive=None, data=None):
        self._passed = passed
        self.name = name
        self.directive = directive
        self.data = data

    @property
    def passed(self):
        """
            Returns if the procedure passed or not
        """
        return "ok" if self._passed else "not ok"

    def __str__(self):
        """
            Returns the Procedure as line
        """
        output = "{} {{id}}".format(self.passed)

        if self.name:
            output += " - {}".format(self.name)

        if self.directive:
            output += " # {}".format(self.directive)

        if self.data:
            output += "\n  ---\n"
            yaml_data = yaml.dump(self.data, default_flow_style=False)
            for line in yaml_data.splitlines():
                output += "  {}\n".format(line)
            output += "  ..."
        return output


class BailOutProcedure(TAPProcedure):  # pylint: disable=too-few-public-methods
    """
        Dummy procedure when test plan bailed out.
    """
    def __init__(self, message):
        TAPProcedure.__init__(self, False)
        self.message = message

    def __str__(self):
        """
            Returns the Procedure as line
        """
        return "Bail Out! {}".format(self.message)



class TAPResult(object):
    """
        Write a TAP result file
    """
    def __init__(self, plan=None, description=None):
        self.procedures = []
        self.expected_plan = plan
        self.description = description

    @property
    def plan(self):
        """
            Returns the test plan of the current result
        """
        return len(self.procedures)

    @plan.setter
    def plan(self, plan):
        """
            Sets the expected test plan (amount of procedures)
        """
        self.expected_plan = plan

    def append(self, passed, name=None, directive=None, data=None):
        """
            Adds a procedure to write
        """
        if self.plan == self.expected_plan:
            raise BailOutError(self.expected_plan)

        if isinstance(passed, TAPProcedure):
            self.procedures.append(passed)
        else:
            self.procedures.append(TAPProcedure(passed, name, directive, data))
        return True

    def __iadd__(self, procedure):
        """
            Adds a procedure to write
        """
        if isinstance(procedure, tuple):
            procedure = TAPProcedure(*procedure)
        self.append(procedure)
        return self

    def ok(self, name=None, directive=None, data=None):  # pylint: disable=invalid-name
        """
            Add passed TAP procedure
        """
        self.append(TAPProcedure(True, name, directive, data))
        return True

    def not_ok(self, name=None, directive=None, data=None):
        """
            Add failed TAP procedure
        """
        self.append(TAPProcedure(False, name, directive, data))
        return True

    def bail_out(self, message):
        """
            Bail out test plan with given message
        """
        self.procedures.append(BailOutProcedure(message))
        return True

    def __str__(self):
        """
            Returns a string representation of the TAP file
        """
        output = "TAP version 13\n"
        if not self.procedures:  # no procedures found to write to result file
            output += "# no procedures found\n"
            return output

        output += "1..{}\n".format(len(self.procedures))
        if self.description:
            for line in self.description.splitlines():
                output += "# {}\n".format(line)

        for i, procedure in enumerate(self.procedures, 1):
            output += str(procedure).format(id=i) + "\n"
        return output

    def write(self, targetfile):
        """
            Write TAP procedures to result file
        """
        with open(targetfile, "w") as targetf:
            targetf.write(str(self))
