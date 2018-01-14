import json
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
 
class ModJSON(StreamCallback):
  def __init__(self):
        pass
        
  def process(self, inputStream, outputStream):
    text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
    jsonObject = json.loads(text)
    count = 0
    def keyVal(self, parentkey, jsonObj, retString):
      for key in jsonObj:
        value = jsonObj[key]
        if isinstance(value, list):
            count=0
            for i in value:
                if isinstance(i, dict) or isinstance(i, list):
                    count=count+1
                    retString = keyVal(self, parentkey +"."+key+"_"+str(count), i, retString)
            if count==0:
                r={key:value}
                retString = retString + parentkey + json.dumps(r)  +"\n"
        elif isinstance(value, dict):
            retString = keyVal(self, parentkey +"."+key, value, retString)        
        else:
            r={key:value}
            retString = retString + parentkey + json.dumps(r)  +"\n"
    
      return retString
    
    retString = keyVal(self, "PA", jsonObject, "")
    
    outputStream.write(bytearray(retString.encode('utf-8')))  

flowFile = session.get()
if (flowFile != None):
  flowFile = session.write(flowFile, ModJSON())
  flowFile = session.putAttribute(flowFile, "filename", flowFile.getAttribute('filename').split('.')[0]+'_translated.json')
session.transfer(flowFile, REL_SUCCESS)
session.commit()