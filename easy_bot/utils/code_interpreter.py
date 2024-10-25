import io
import sys
import threading
import queue

def execute_python_script(code: str, timeout: int = 5) -> str:
    """
    Executes a Python script provided as a string and captures its output.

    Args:
        code (str): The Python code to be executed.
        timeout (int): The maximum time to wait for the script to execute, in seconds.

    Returns:
        str: The captured output from the executed code.
    """
    stop_flag = threading.Event()

    def run_code(code, output_queue, stop_flag):
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            exec(code)
            if not stop_flag.is_set():
                output_queue.put(sys.stdout.getvalue())
        except Exception as e:
            output_queue.put(str(e))
        finally:
            sys.stdout = old_stdout

    output_queue = queue.Queue()
    thread = threading.Thread(target=run_code, args=(code, output_queue, stop_flag))
    thread.daemon = True
    thread.start()

    thread.join(timeout)
    output = output_queue.get_nowait() if not output_queue.empty() else ""

    if thread.is_alive():
        stop_flag.set()
        return output + "Execution timed out"
    else:
        return output