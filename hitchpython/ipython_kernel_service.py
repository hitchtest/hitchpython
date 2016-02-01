import hitchserve
import signal
from os import path


class IPythonKernelService(hitchserve.Service):
    """Run an IPython kernel as a service."""
    stop_signal = signal.SIGTERM
    
    def __init__(self, python_package, **kwargs):
        # TODO: Check if python < 3.3 and if so, don't run.
        if path.exists(path.join(python_package.bin_directory, "ipython3")):
            ipython = path.join(python_package.bin_directory, "ipython3")
        elif path.join(python_package.bin_directory, "ipython"):
            ipython = path.join(python_package.bin_directory, "ipython")
        else:
            raise RuntimeError("ipython not found in python package")
        kwargs['command'] = [ipython, "kernel", ]
        kwargs['log_line_ready_checker'] = lambda line: "existing" in line
        super(IPythonKernelService, self).__init__(**kwargs)
        
    def wait_and_get_ipykernel_filename(self, timeout=10):
        kernel_line = self.logs.tail.until(
            lambda line: "--existing" in line[1], timeout=timeout, lines_back=5
        )
        return kernel_line.replace("--existing", "").strip()
