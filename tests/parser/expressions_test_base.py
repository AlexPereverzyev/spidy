
import unittest

from spidy.language import *
from spidy.common import *

class ExpressionsTestBase(unittest.TestCase):

    def evaluate(self, exp):
        ectx = Context()
        ectx.set_script([ScriptLine(0, '')])
        ectx.set_test(True)
        ectx.frame_start()
        tree = parse_expression(ectx, 0, exp)
        result = tree.evaluate()
        ectx.frame_end()
        return result