#!/usr/bin/python3

#import shutil
import configparser
import os

print("Building Bundle...")

conf = configparser.ConfigParser()
conf.read("/home/ses/bin/bundle.ini")

bundleLoc = conf["settings"]["dst"] + "/backendBundle"
#bundleTar = conf["settings"]["dst"] + "/backendBundle.tar.gz"
srcCode = conf["settings"]["src"] 

#get next version from db
ver = (os.popen("php /home/ses/bin/bundle/rabbitMQClient.php bundleRequest").read())
print("The next bundle version is version:  " + ver.strip())

#create the uncompressed bundle
os.system("mkdir " + bundleLoc)
os.system("cp -r " + srcCode + " " + bundleLoc)

#compress
bundleTar = conf["settings"]["dst"] + "/BEv" + ver.strip() + ".tar.gz"
os.system("tar -cvzf " + bundleTar + " backendBundle/")

#send to target machine
os.system("scp " + bundleTar + " 192.168.2.11:/home/ses/bundles")

#update bundle version in db
os.system("php /home/ses/bin/bundle/rabbitMQClient.php updateBundleVer")

#clean up
os.system("rm -r -f " + bundleLoc)


print ("Build Complete")

