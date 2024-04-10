from io import StringIO
from django.test import TestCase
from django.core import management
from tests.models import SimpleTable1, SimpleTable2


class LoadcsvTestCase(TestCase):
    def _test_table(self, obj, correct):
        for i, row in enumerate(obj):
            self.assertEqual(row.id, correct[i][0])
            self.assertEqual(row.a, correct[i][1])
            self.assertEqual(row.b, correct[i][2])
            self.assertEqual(row.c, correct[i][3])

    def test_loadcsv_model(self):
        out = StringIO()
        management.call_command('loadcsv', 'test1.csv', 'test1', stdout=out)
        self.assertEqual(int(out.getvalue()), 2)
        correct = [[1, 'hello', 'world', 'today'], [2, 'and', 'next', 'line']]
        self._test_table(SimpleTable1.objects.all(), correct)

    def test_loadcsv_set_columns(self):
        out = StringIO()
        management.call_command('loadcsv', 'test2.csv', 'test2', stdout=out)
        self.assertEqual(int(out.getvalue()), 2)
        correct = [[1, 'hello', '', 'today'], [2, 'and', '', 'line']]
        self._test_table(SimpleTable2.objects.all(), correct)
