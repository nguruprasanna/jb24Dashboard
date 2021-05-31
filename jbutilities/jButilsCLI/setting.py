#Generic
WATCHFOLDER = {

"COMODETS": {   
"W_PATH":"C:\\Users\\guru\\OneDrive\\Documents\\Guru\\MyDev\\Dojango\\COB.COMO.20100201\\COMO",
"W_PATTERN":"tSA*",
"w_RECURSIVELY":True,
"W_IGNORE_PATTERNS":"", 
"W_IGNORE_DIRECTORIES":False, 
"W_CASE_SENISTIVE":True,
"W_FMT" :"T24"
}

#TOCFEE:{
#
#}

}

##Como log format
#JBASE/TAFC/TAFJ
JBENV = "TAFC" 

#Loki Details
# push msg log into grafana-loki
url = 'http://localhost:3100/api/prom/push'
updateOld = "";#for future use - to force loki accept old datatime
