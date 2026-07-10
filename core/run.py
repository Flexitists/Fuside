import os
import subprocess
import sys
import tempfile
import threading


def get_run_command(file_path):
    """Return the command(s) needed to run a file."""
    file_path = os.path.abspath(file_path)
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".py":
        return (["py", file_path], None)

    if ext == ".c":
        exe_path = os.path.splitext(file_path)[0] + ".exe"
        return (["gcc", file_path, "-o", exe_path], [exe_path])

    if ext == ".cpp":
        exe_path = os.path.splitext(file_path)[0] + ".exe"
        return (["g++", file_path, "-o", exe_path], [exe_path])

    if ext == ".pas":
        return (["fpc", file_path], None)

    raise ValueError(f"Unsupported file type: {ext}")


def _write_output(terminal_widget, text):
    if terminal_widget is not None:
        terminal_widget.write(text)


def stop_process(process):
    """Stop a running subprocess if it is still alive."""
    if process is None:
        return False

    if getattr(process, "poll", None) is not None and process.poll() is not None:
        return False

    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], check=False, capture_output=True, text=True)
        else:
            process.terminate()
    except Exception:
        return False

    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        try:
            process.kill()
        except Exception:
            return False

    return True


def _stream_output(process, terminal_widget, done_callback=None):
    try:
        if process.stdout:
            for line in process.stdout:
                _write_output(terminal_widget, line)
    finally:
        if process.stdout:
            process.stdout.close()

    return_code = process.wait()
    _write_output(terminal_widget, f"\n[Process exited with code {return_code}]\n")

    if done_callback:
        done_callback(return_code)


def run_file(file_path=None, terminal_widget=None, content=None, source_name=None, stdin_text=None, done_callback=None):
    """Run a source file and stream output into the terminal widget."""
    if file_path is None:
        if content is None:
            _write_output(terminal_widget, "No content available to run.\n")
            return None

        temp_dir = tempfile.gettempdir()
        source_name = source_name or "untitled.py"
        base_name = os.path.basename(source_name)
        if "." not in base_name:
            base_name = f"{base_name}.py"

        file_path = os.path.join(temp_dir, base_name)
        with open(file_path, "w", encoding="utf-8") as handle:
            handle.write(content)
    elif content is not None:
        with open(file_path, "w", encoding="utf-8") as handle:
            handle.write(content)

    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        _write_output(terminal_widget, f"File not found: {file_path}\n")
        return None

    if terminal_widget is not None:
        terminal_widget.clear()

    try:
        build_command, run_command = get_run_command(file_path)
    except ValueError as exc:
        _write_output(terminal_widget, f"{exc}\n")
        return None

    input_text = stdin_text
    if input_text is None and terminal_widget is not None:
        try:
            input_text = terminal_widget.get_input_text()
        except Exception:
            input_text = None

    if run_command is None:
        process = subprocess.Popen(
            build_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        if input_text is not None:
            process.stdin.write(input_text)
            process.stdin.flush()
            process.stdin.close()
    else:
        build_process = subprocess.Popen(
            build_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        build_output = build_process.communicate()[0] or ""
        if build_process.returncode != 0:
            _write_output(terminal_widget, build_output)
            _write_output(terminal_widget, "\nBuild failed.\n")
            return build_process.returncode

        process = subprocess.Popen(
            run_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        if input_text is not None:
            process.stdin.write(input_text)
            process.stdin.flush()
            process.stdin.close()

    threading.Thread(
        target=_stream_output,
        args=(process, terminal_widget, done_callback),
        daemon=True,
    ).start()
    return process


def run_py(file):
    return run_file(file)


def run_c(file):
    return run_file(file)


def run_cpp(file):
    return run_file(file)


def run_pas(file):
    return run_file(file)

