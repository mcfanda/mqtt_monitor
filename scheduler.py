from apscheduler.schedulers.background import BackgroundScheduler
from pprint import pprint 

itime={'days':0, 'weeks':0, 'hours':0, 'minutes':0, 'seconds':0}
ctime={'hour':'*', 'minute':'*', 'second':'0'}

def doNothing(arg):
    print(arg)

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
#        self.job=doNothing
#        self.scheduler.add_job(self.introspect,'interval',id="intro", seconds=5,replace_existing=True)

    def setJob(self,fun):
        self.job=fun

    
    def introspect(self):
        for job in self.scheduler.get_jobs():
            print("Scheduler jobs:"+job.id+" scheduled for "+job.next_run_time.strftime("%H:%M:%S"))

        

    def dispatch(self,rule):
        print("Scheduler: implementing %s" % rule['send']);
        if 'interval' in rule:
             print("Scheduler: interval rule activated: %s with id=%s" % (rule['send'],rule['id']));
             ltime=dict_merge(rule['interval'],itime)
             self.scheduler.add_job(self.job,'interval',args=[rule],id=rule['id'], hours=ltime['hours'],minutes=ltime['minutes'],seconds=ltime['seconds'],replace_existing=True)
        else:
            print("nothing")

       

