import os
import yaml

class Conf:

 def __init__(self,location=None):
        if not location:
          location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.location=location

 def resource(self):
        stream = open(self.location, "r")
        y=yaml.load(stream)
        stream.close()
        return(y)	 
 def getValue(self,name):
        res=self.resource()
        try:
          out=res[name]
        except :
          out=None
        return(out)  


if __name__ == "__main__":
 cc=Conf()
 print(cc.getValue("settings","logfile"))

