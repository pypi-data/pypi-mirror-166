import data_mig.utils.config as cf
from data_mig.jobs.runner import Runner

if __name__ == '__main__':
    runner = Runner(cf.Config(path='../../../'))
    runner.load_by_object('Contact')

