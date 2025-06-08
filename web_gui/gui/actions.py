import signal
import socketserver
import time
import psutil
import structlog

log = structlog.get_logger()

class Controller:
    @staticmethod
    def get_free_port():
        with socketserver.TCPServer(("localhost", 0), None) as s:
            return s.server_address[1]

    @staticmethod
    def get_processes_by_port(port: int):
        processes = []
        for proc in psutil.process_iter():
            try:
                for conn in proc.net_connections(kind="inet"):
                    if conn.laddr.port == port:
                        processes.append(proc)
                        break
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                continue
            except psutil.AccessDenied:
                pass
        return processes

    @staticmethod
    def terminate(port: int, timeout: int = 0):
        procs = Controller.get_processes_by_port(port)
        for proc in procs:
            try:
                log.warning(
                    f"[TERMINATE] Sending SIGTERM to PID {proc.pid} using port {port}"
                )
                proc.send_signal(signal.SIGTERM)
            except Exception as e:
                log.warning(f"[ERROR] Could not terminate PID {proc.pid}: {e}")

    @staticmethod
    def shutdown(port: int, timeout: int):
        procs = Controller.get_processes_by_port(port)
        time.sleep(timeout)
        for proc in procs:
            try:
                log.info(f"[SHUTDOWN] Sending SIGINT to PID {proc.pid} using port {port}")
                proc.send_signal(signal.SIGINT)

                try:
                    proc.wait(timeout=timeout)
                    log.info(f"[INFO] PID {proc.pid} exited cleanly.")
                except psutil.TimeoutExpired:
                    log.warning(
                        f"[WARN] PID {proc.pid} did not exit after {timeout}s. Trying SIGTERM..."
                    )
                    proc.terminate()
                    try:
                        proc.wait(timeout=timeout)
                        log.info(f"[INFO] PID {proc.pid} terminated after SIGTERM.")
                    except psutil.TimeoutExpired:
                        log.warning(f"[ERROR] PID {proc.pid} still alive. Forcing kill...")
                        proc.kill()

            except Exception as e:
                log.warning(f"[ERROR] Could not shutdown PID {proc.pid}: {e}")

    @staticmethod
    def kill(port: int):
        procs = Controller.get_processes_by_port(port)
        for proc in procs:
            try:
                log.info(f"[KILL] Force killing PID {proc.pid} using port {port}")
                proc.kill()
            except Exception as e:
                log.warning(f"[ERROR] Could not kill PID {proc.pid}: {e}")

    @staticmethod
    def kill_port(port: int):
        # Legacy method (still supported for backward compatibility)
        Controller.terminate(port)
