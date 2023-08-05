import yaml
from data_mig.utils.exceptions import *
import os.path
import os


class Config(object):
    CONNECTED_APP = {}
    DATABASE_CONFIG = {}
    SALESFORCE_CONFIG = {}
    NOTIFICATIONS = {}
    JOB_DEFAULTS = {}
    READ_DEFAULTS = {}
    reads = {}
    jobs = {}

    def __init__(self, path='', config_file=None, reads_file=None, jobs_file=None):
        self._config_filename = os.path.join(path, config_file or os.getenv('CONFIG_FILE', 'config.yml'))
        self._config_reads_filename = os.path.join(path, reads_file or os.getenv('READS_FILE', 'reads.yml'))
        self._config_jobs_filename = os.path.join(path, jobs_file or os.getenv('JOBS_FILE', 'jobs.yml'))
        self.reload()

    def _load_cfg(self):
        try:
            with open(self._config_filename, 'r') as f:
                self._config = yaml.safe_load(f)
        except IOError as e:
            raise ProjectConfigNotFound('{} config file not found'.format(self._config_filename))

        self.DATABASE_CONFIG = self._config.get('DATABASE_CONFIG')
        self.SALESFORCE_CONFIG = self._config.get('SALESFORCE_CONFIG')

        self.SALESFORCE_CONFIG['sf_version'] = self.SALESFORCE_CONFIG.get('sf_version', 54.0)

        self.JOB_DEFAULTS = self._config.get('JOB_DEFAULTS', {})

        # Legacy Job Defaults
        self.JOB_DEFAULTS['validate_only'] = True if self.SALESFORCE_CONFIG.get('validate_only') else \
            self.JOB_DEFAULTS.get('validate_only')
        self.JOB_DEFAULTS['filter_invalid'] = True if self.SALESFORCE_CONFIG.get('filter_invalid') else \
            self.JOB_DEFAULTS.get('filter_invalid')

        self.READ_DEFAULTS = self._config.get('READ_DEFAULTS', {})
        self.CONNECTED_APP = self._config.get('CONNECTED_APP')
        self.NOTIFICATIONS = self._config.get('NOTIFICATIONS')

    def reload(self):
        self._load_cfg()
        self._load_reads()
        self._load_jobs()

    def _load_reads(self):
        try:
            with open(self._config_reads_filename, 'r') as f:
                reads = yaml.safe_load(f)
                if self.READ_DEFAULTS:
                    for read, params in reads.items():
                        for def_key, def_value in self.READ_DEFAULTS.items():
                            if not params.get(def_key):
                                params[def_key] = def_value
        except IOError as e:
            print('Warning {} file not found'.format(self._config_reads_filename))

        self.reads = reads

    def _load_jobs(self):
        self.jobs = []

        try:
            with open(self._config_jobs_filename, 'r') as f:
                jobs = yaml.safe_load(f)
            if jobs.items():
                for series, levels in jobs.items():
                    for jobs in levels:
                        for level, job in jobs.items():
                            job['series'] = series
                            job['level'] = level
                            for def_key, def_value in self.JOB_DEFAULTS.items():
                                if not job.get(def_key):
                                    job[def_key] = def_value
                            self.jobs.append(job)
        except IOError as e:
            print('Warning {} file not found'.format(self._config_jobs_filename))
        except AttributeError as e:
            print('Warning {} file could not be parsed.'.format(self._config_jobs_filename))

    def __repr__(self):
        return "config()"

    def __str__(self):
        return "{}\n{}".format(self.reads, self.jobs)

    def update_config(self):

        with open(self._config_filename, 'w') as f:
            yaml.safe_dump(self._config, f, default_flow_style=False)
            f.close()

    def jobs_by_attr(self, attribute, value):
        return self._by_attr(attribute, value)

    def jobs_by_attr_range(self, attribute, min, max):
        return self._by_attr_range(attribute, min, max)

    def _by_attr(self, attribute, value):
        return [x for x in self.jobs if x.get(attribute) == value]

    def _by_attr_range(self, attribute, min, max):
        return [x for x in self.jobs if min <= x.get(attribute) <= max]
