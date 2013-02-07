#!/usr/bin/python
import fileinput, sys, os, random

numExecutions = 1

minimumBiomassValues = ['0.1']
meanValues = ['4913']
stdDevValues = ['1','100','200','300','400','500','600','700','800','900','1000','1100','1200','1300','1400','1500','1600', '1700', '1800', '1900', '2000', '2100', '2200', '2300', '2400', '2500', '2600', '2700', '2800', '2900','3000']

xmlTemplate = 'templates/config_template_mn_stddev.xml'
runTemplate = 'templates/bsub_template_stddev.cmd'

indexKey = 'INDEX'
initialDirKey = 'INITIALDIR'
numExecutionKey = 'NUMEXEC'
minimumBiomassKey = 'BIOMASS_MINIMUM'
meanKey = 'MEAN'
stdDevKey = 'STDDEV'
climateKey = 'CLIMATESEED'

def replaceKey( fileName, key, value ):
	for line in fileinput.FileInput(fileName,inplace=1):
		if key in line:
			line = line.replace(key, value)
		sys.stdout.write(line)
	fileinput.close()

os.system('rm -rf stddev/')
os.system('mkdir stddev')

index = 0
print 'creating test workbench'

random.seed()

for numExecution in range(0,numExecutions):
	# each n.execution  has the same seed in all parameter space
	randomValue = str(random.randint(0,10000000))	
	for minimumBiomass in minimumBiomassValues:
		for mean in meanValues :
			for stddev in stdDevValues:
				print 'creating gujarat instance: ' + str(index) + ' for minimum biomass: ' + minimumBiomass + ' mean: ' + mean + ' stddev: ' + stddev + ' and execution: ' + str(numExecution)
				dirName = 'stddev/results_biomin'+minimumBiomass+'_mean'+mean+'_stddev'+stddev+'_ex'+str(numExecution)
				os.system('mkdir '+dirName)
				configName = dirName + '/config.xml'			
				os.system('cp '+xmlTemplate+' '+configName)
				replaceKey(configName, minimumBiomassKey, minimumBiomass)
				replaceKey(configName, meanKey, mean)
				replaceKey(configName, stdDevKey, stddev)
				replaceKey(configName, numExecutionKey, str(numExecution))
				replaceKey(configName, climateKey, randomValue)

				runName = dirName+'/bsub_gujarat.cmd'
				os.system('cp '+runTemplate+' '+runName)
				replaceKey(runName, indexKey, str(index))
				replaceKey(runName, initialDirKey, dirName)
				index += 1

print 'workbench done, submitting tasks'
index = 0
for minimumBiomass in minimumBiomassValues:	
	for mean in meanValues :
		for stddev in stdDevValues:
			for numExecution in range(0,numExecutions):
				print 'submitting gujarat instance: ' + str(index) + ' with min biomass: ' + minimumBiomass + ' mean: ' + mean + ' stddev: ' + stddev + ' and execution: ' + str(numExecution)
				dirName = 'stddev/results_biomin'+minimumBiomass+'_mean'+mean+'_stddev'+stddev+'_ex'+str(numExecution)
				os.system('bsub < '+dirName+'/bsub_gujarat.cmd')
				index += 1

