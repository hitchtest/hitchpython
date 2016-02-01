import hitchserve


class PythonService(hitchserve.Service):
    
    def __init__(self, python, module, args, log_line_ready_checker, **kwargs):
        kwargs['command'] = [python, "-u", "-m", module] + args
        kwargs['log_line_ready_checker'] = log_line_ready_checker
        super(PythonService, self).__init__(**kwargs)
        
    def wait_and_get_ipykernel_filename(self, timeout=10):
        kernel_line = self.logs.tail.until(
            lambda line: "--existing" in line[1], timeout=timeout, lines_back=5
        )
        return kernel_line.replace("--existing", "").strip()
