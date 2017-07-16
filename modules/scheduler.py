from apscheduler.schedulers.background import BackgroundScheduler
import logging


itime={'days':0, 'weeks':0, 'hours':0, 'minutes':0, 'seconds':0}
ctime={'hour':'*', 'minute':'*', 'second':'0'}

def doNothing(arg):
    logging.info(arg)

def dict_merge(data,default):
    res={}
    for key, value in default.items():
        try:
            res[key]=data[key]
        except KeyError:
            res[key] = default[key]
    return(res)

class Scheduler:

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.job=doNothing
#        self.scheduler.add_job(self.introspect,'interval',id="intro", seconds=5,replace_existing=True)

    def setJob(self,fun):
        self.job=fun


    def introspect(self):
        for job in self.scheduler.get_jobs():
            logging.info("Scheduler jobs:"+job.id+" scheduled for "+job.next_run_time.strftime("%H:%M:%S"))



    def dispatch(self,rule):
        if 'interval' in rule:
             logging.info('action "%s" activated with interval:' % rule['name'])
             logging.info("interval: %s" % rule['interval']);
             ltime=dict_merge(rule['interval'],itime)
             self.scheduler.add_job(self.job,'interval',args=[rule],id=rule['id'], hours=ltime['hours'],minutes=ltime['minutes'],seconds=ltime['seconds'],replace_existing=True)
        else:
            logging.info("nothing")



