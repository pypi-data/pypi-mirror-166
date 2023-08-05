import data_mig.utils.config as cf
from data_mig.utils.notifications import notification

def main():
    cfg = cf.Config(path='../../')
    note = notification(cfg)
    note.send('test')

if __name__ == "__main__":
    main()