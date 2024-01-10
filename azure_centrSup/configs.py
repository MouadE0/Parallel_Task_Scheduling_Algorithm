

##################
# Batch account  #
##################

batch = {
    "name": "",
    "key": "",
    "url": ""
}


###################################################
# Blob container which will store results of runs #
###################################################

blob_container = {
    "url": "REPLACE_WITH_CONTAINER_REFERENCE",
    "sas_token": "TOKEN"

######################
# Configuration Pool #
######################

#rule of scability of pool
rule_scaling = (
                '// Get pending tasks for the past 5 minutes.\n'
                '$samples = $ActiveTasks.GetSamplePercent(TimeInterval_Minute * 5);\n'
                '// If we have fewer than 70 percent data points, we use the last sample point, otherwise we use the maximum of last sample point and the history average.\n'
                '$tasks = $samples < 70 ? max(0, $ActiveTasks.GetSample(1)) : '
                'max( $ActiveTasks.GetSample(1), avg($ActiveTasks.GetSample(TimeInterval_Minute * 5)));\n'
                '// If number of pending tasks is not 0, set targetVM to pending tasks, otherwise half of current dedicated.\n'
                '$targetVMs = $tasks > 0 ? $tasks : max(0, $TargetDedicatedNodes / 2);\n'
                '// The pool size is capped. This value should be adjusted according to your use case.\n'
                'cappedPoolSize = 5;\n'
                '$TargetLowPriorityNodes = max(0, min($targetVMs, cappedPoolSize));\n'
                '// Set node deallocation mode - keep nodes active only until tasks finish\n'
                '$NodeDeallocationOption = taskcompletion;'
               )


#####################
# Configuration Job #
#####################

#Repository (Github,Gitlab, etc.) contenant les inputs
repository = 'REPO_ADDRESS'


#Commandes de la tâche de préparation(clonage d'un repo Azure Devops et installation des packages python nécessaires pour le process mpi)
cmd_prep_task = (
                  "bash -c 'git init; git clone {0} ; cd st7-pfast ; chmod +x install.sh ; ./install.sh'".format(repository)
                 )



######################
# Configuration Task #
######################

nb_processes = 2 ## jusqu a 5

#copier le script d'execution dans le dossier partagé du noeud
coordination_command = "bash -c 'ls; cp $AZ_BATCH_JOB_PREP_DIR/wd/st7-pfast/*.py  $AZ_BATCH_NODE_SHARED_DIR'"

start_command = (
       "bash -c 'mpirun -np {0} -host $AZ_BATCH_HOST_LIST -wdir $AZ_BATCH_NODE_SHARED_DIR python3 $AZ_BATCH_NODE_SHARED_DIR/classic.py; mpirun -np {0} -host $AZ_BATCH_HOST_LIST -wdir $AZ_BATCH_NODE_SHARED_DIR python3 $AZ_BATCH_NODE_SHARED_DIR/parallel.py'".format(nb_processes)
      )