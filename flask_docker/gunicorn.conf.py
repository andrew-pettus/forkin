import os
#We are IO Bound, so prefer async over threads
worker_class = "gevent"

try:
    env_level = os.getenv( "LOG_LEVEL", None )
    if env_level is None:
        loglevel = "ERROR"
    else:
        loglevel = env_level
except:
    loglevel = "ERROR"

#If k8s or swarm are auto scaling horizontally it doesn't make sense to size workers based on CPU
#sync workers would be single-proc'd and thread-tuned based on the application
#gevent workers are single proc'd and set to two workers
env = os.getenv("EXEC_ENV", None)
if env == "DISTRIBUTED":
    workers = 2
else:
    import multiprocessing
    workers = multiprocessing.cpu_count() * 2 + 1