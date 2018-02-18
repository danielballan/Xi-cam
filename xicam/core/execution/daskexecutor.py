from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler
from dask.diagnostics import visualize
import dask.threaded
from xicam.core import msg
from appdirs import user_config_dir


class DaskExecutor:
    def __init__(self):
        pass

    def execute(self, wf, client=None):
        import distributed
        # from distributed import Queue

        dsk = wf.convertGraph()

        with Profiler() as prof, ResourceProfiler(dt=0.25) as rprof, CacheProfiler() as cprof:
            # if not client: client = distributed.Client()

            # generate queues
            """
            for node in wf._processes:
                i = node
                for key in i.inputs.keys():
                  j = i.inputs[key]
                  for k in j.subscriptions:
                    # share distributed Queue between sender and receiver
                    q = Queue()
                    j.__internal_data__.queues_in.append({j.name : q})
                    k[1].parent.__internal_data__.queues_out.append({k[0].name : q})
            """

            result = dask.threaded.get(dsk[0], dsk[1])

        msg.logMessage('result:', result, level=msg.DEBUG)
        path = user_config_dir('xicam/profile.html')
        visualize([prof, rprof, cprof], show=False, file_path=path)
        msg.logMessage(f'Profile saved: {path}')
        # client.close()

        #res = {}
        #for f in result:
        #    for fx in f:
        #        for f1 in fx:
        #            res[f1.name] = f1.value

        return result
