import jupyter_client
from os import path, getuid

        
class IPythonResponse(object):
    """Represent a response from a python command sent to IPython."""
    def __init__(self, returnval=None, text=None, error=None):
        self.returnval = returnval
        self.text = text
        self.error = error


class IPythonStepLibrary(object):
    """Common steps to run commands against embedded IPython."""
    def startup_connection(self, ipykernel_filename):
        self.kernel_manager = jupyter_client.KernelManager(
            connection_file=jupyter_client.find_connection_file(
                ipykernel_filename,
                path=[
                    ".",
                    path.join("/", "run", "user", str(getuid()), "jupyter"),
                    path.join(
                        path.expanduser("~"),
                        ".ipython", "profile_default", "security"
                    )
                ],
            )
        )
        self.kernel_manager.load_connection_file()
        self.client = self.kernel_manager.blocking_client()
        self.client.start_channels()
        reply = self.client.get_shell_msg()
        
    def run(self, command, silent=False, swallow_exception=False):
        import sys
        if not silent:
            sys.stdout.write(">>> {}".format(command).encode('utf8'))
        self.client.execute(command)
        reply = self.client.get_shell_msg()
        response = IPythonResponse()
        if reply['content']['status'] == 'ok':
            for iopub in self.client.iopub_channel.get_msgs():
                content = iopub['content']
                if "text" in content:
                    if not silent:
                        sys.stdout.write(str(content['text']).encode('utf8'))
                    response.text = content['text']
                if "data" in content:
                    if "text/plain" in content['data']:
                        response.returnval = content['data']['text/plain']
                        if not silent:
                            sys.stdout.write(str("{}\n".format(content['data']['text/plain'])).encode('utf8'))
        elif reply['content']['status'] == 'error':
            response.error = "\n".join(reply['content']['traceback'])
            if not swallow_exception:
                raise RuntimeError("\n".join(reply['content']['traceback']))
            else:
                sys.stderr.write("\n".join(reply['content']['traceback']).encode('utf8'))
        return response
    
    def assert_true(self, command):
        assert self.run(command).returnval == "True"
        
    def assert_result(self, command, result=None):
        assert self.run(command).returnval == result
        
    def assert_output(self, command=None, output=None):
        assert output in self.run(command).error
        
    def assert_exception(self, command=None, exception=None):
        assert exception in self.run(command, swallow_exception=True).error

    def shutdown_connection(self):
        self.client.shutdown()
        reply = client.get_shell_msg()
        if reply['content']['status'] == 'error':
            raise RuntimeError("Ipython kernel shutdown error")
