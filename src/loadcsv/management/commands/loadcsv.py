import os
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.utils import ProgrammingError
from loadcsv.models import ModelWithCSV


_cmd = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s"
_cmd_opts = "FIELDS TERMINATED BY '%s' LINES TERMINATED BY '%s' IGNORE 1 LINES"
_load_data_infile_cmd_fmt = "%s %s %s;"


class Command(BaseCommand):
    help = "loads a csv into a database table"

    def add_arguments(self, parser):
        parser.add_argument("csv", nargs="?", type=str, help="csv file")
        parser.add_argument("dbtable", nargs="?", type=str,
                            help="database table")

    def _find_csv_filepath(self, fname):
        for f in os.listdir():
            if os.path.isdir(f):
                if "fixtures" in os.listdir(f):
                    fpath = os.path.join(f, "fixtures", fname)
                    if os.path.isfile(fpath):
                        return fpath
        raise CommandError("Couldn't file csv file: %s" % fname)

    def _find_model(self, dbtable):
        for model in apps.get_models():
            if model._meta.db_table == dbtable:
                return model
        raise CommandError("Couldn't file database table")

    def _find_csv_params(self, model):
        is_model_csv = issubclass(model, ModelWithCSV)
        if is_model_csv:
            return {
                'field_delimeter': model.CSV.field_delimeter,
                'line_end': model.CSV.line_end,
                'cmd_extra': model.CSV.cmd_extra
            }
        else:
            return {
                'field_delimeter': ',',
                'line_end': '\\n',
                'cmd_extra': ''
            }

    def _make_cmd(self, fpath, dbtable, params):
        cmd = _cmd % (fpath, dbtable)
        options = _cmd_opts % (params['field_delimeter'], params['line_end'])
        return _load_data_infile_cmd_fmt % (cmd, options, params['cmd_extra'])

    def handle(self, *args, **options):
        fpath = self._find_csv_filepath(options['csv'])
        dbtable = options['dbtable']
        model = self._find_model(dbtable)
        params = self._find_csv_params(model)
        cmd = self._make_cmd(fpath, dbtable, params)
        cursor = connection.cursor()
        try:
            nr_records_inserted = cursor.execute(cmd)
        except ProgrammingError as e:
            raise CommandError(e)
        if nr_records_inserted == 0:
            raise CommandError("No records inserted into database table")
        return str(nr_records_inserted)
