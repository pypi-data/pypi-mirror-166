from signal import SIGKILL, SIGTERM
import asyncio
from ipykernel.ipkernel import IPythonKernel
import ipyparallel as ipp
from ipyparallel.client.magics import ParallelMagics

from .platform_hostfile_update import update_hostfile
from .utils import BColor, colorize_output

IPYPARALLEL_LINE_MAGICS = ("px", "autopx", "pxconfig", "pxresult")
IPYPARALLEL_CELL_MAGICS = ("px",)
BODO_PLATFORM_CUSTOM_LINE_MAGICS = (
    "%pconda",
    "%ppip",
    "%psh",
    "%setup_adls",
    "%update_hostfile",
)

IPYPARALLEL_MAGICS = tuple(
    [f"%{m}" for m in IPYPARALLEL_LINE_MAGICS]
    + [f"%%{m}" for m in IPYPARALLEL_CELL_MAGICS]
)


class IPyParallelKernel(IPythonKernel):
    banner = "IPyParallel Kernel"

    def start(self):
        super().start()
        self.ipyparallel_cluster_started = False
        self.ipyparallel_cluster = None

    def _is_autopx_enabled(self):
        try:
            return self.shell.magics_manager.registry[ParallelMagics.__name__]._autopx
        except:
            return False

    def ipyparallel_magics_already_registered(self) -> bool:
        # Check if any IPyParallel magics are already registered
        return any(
            [
                x in self.shell.magics_manager.magics["line"]
                for x in IPYPARALLEL_LINE_MAGICS
            ]
            + [
                x in self.shell.magics_manager.magics["cell"]
                for x in IPYPARALLEL_CELL_MAGICS
            ]
        )

    def start_ipyparallel_cluster(self):
        if not self.ipyparallel_cluster_started:
            self.log.info("Updating Hostfile...")
            update_hostfile(self.log)

            self.log.info("Starting IPyParallel Cluster...")

            try:
                self.ipyparallel_cluster = ipp.Cluster(
                    engines="bodo"
                )  # Config is taken from ipcluster_config.py
                self.ipyparallel_rc = self.ipyparallel_cluster.start_and_connect_sync()
                self.ipyparallel_view = self.ipyparallel_rc.broadcast_view()
                self.ipyparallel_view.block = True
                self.ipyparallel_view.activate()
            except Exception as e:
                self.log.error(
                    "Something went wrong while trying to start the IPyParallel cluster..."
                )
                self.log.error(f"Error: {e}")
                self.log.info("Shutting Cluster down...")
                # Cluster might have been started, if so then stop it and remove any
                # lingering processes
                if self.ipyparallel_view is not None:
                    # In some cases just stop_cluster_sync left hanging engine processes so view.shutdown was added
                    self.ipyparallel_view.shutdown(hub=True)
                if self.ipyparallel_cluster is not None:
                    self.ipyparallel_cluster.stop_cluster_sync()
                raise e
            else:
                self.ipyparallel_cluster_started = True

    def _log_message(self, message: str):
        stream_content = {"name": "stderr", "text": message}
        self.send_response(self.iopub_socket, "stream", stream_content)

    async def do_execute(
        self,
        code: str,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):
        # If code is run without parallel magics, warn the user
        if not self._is_autopx_enabled() and not code.startswith(
            (*IPYPARALLEL_MAGICS, *BODO_PLATFORM_CUSTOM_LINE_MAGICS)
        ):
            message = colorize_output(
                BColor.WARNING,
                "No IPyParallel Magics detected. For parallel execution, please use an IPyParallel magic such as %%px or %autopx.",
            )
            self._log_message(message)

        # Start the IPyParallel cluster if any IPyParallel
        # magic is used
        if (
            code.startswith(IPYPARALLEL_MAGICS)
            # If magics are already registered, that means user has started an
            # IPyParallel cluster manually, so we shouldn't start one ourselves.
            # This lets users use this kernel as a direct replacement for a regular
            # kernel.
            and not self.ipyparallel_magics_already_registered()
        ):
            try:
                self.start_ipyparallel_cluster()
            except Exception as e:
                # Don't run any code since cluster creation failed
                code = "pass"

        # If the engines are not running, e.g. they were previously started but killed,
        # and code starts with "px" or "autopx", rather than executing the code,
        # we throw an error
        if self.ipyparallel_cluster_started and (
            self._is_autopx_enabled() or code.startswith(IPYPARALLEL_MAGICS)
        ):
            # If engines are not running, e.g. they previously errored out with an exit code, prompt user to restart the kernel and return
            # We use a try-except block here to make sure code doest throw an error for instances when
            # ipyparallel_cluster does not have a property engine_set. The other alternative would be to use a getter
            try:
                if (
                    not self.ipyparallel_cluster.engine_set.running
                    # still allow users to disable autopx
                    and not (code.startswith("%autopx") and self._is_autopx_enabled())
                    # still allow users to run %pxresult
                    and not code.startswith("%pxresult")
                ):
                    message = colorize_output(
                        BColor.FAIL,
                        "IPyParallel Cluster engines previously exited with an error. Please restart the kernel and try again",
                    )
                    self._log_message(message)
                    return
            except:
                pass

        return await super().do_execute(
            code=code,
            silent=silent,
            store_history=store_history,
            user_expressions=user_expressions,
            allow_stdin=allow_stdin,
        )

    async def stop_ipyparallel_cluster(self):
        if self.ipyparallel_cluster_started:
            self.log.info("Stopping IPyParallel Cluster...")

            # If a MPI process is hanging/waiting for other processes
            # the normal IPP shutdown process leaves zombie engines
            # which can create OOM issues.
            # Sending SIGKILL to the engines ensures the processes are
            # stopped and their resources are released.
            await self.ipyparallel_cluster.signal_engines(SIGKILL)
            # Stop the controller separately since the engines should be
            # removed already. 
            await self.ipyparallel_cluster.stop_controller()

            # If a cluster is left in a broken state the cluster file
            # isn't always removed so manually remove it
            self.ipyparallel_cluster.remove_cluster_file()

            try:
                # Just in case the above methods don't work
                self.ipyparallel_cluster.stop_cluster_sync()
            except FileNotFoundError:
                # Cluster.stop_engines will throw FileNotFoundError if logs are already removed.
                # Stop_cluster_sync calls cluster.stop_engines.
                pass

    async def do_shutdown(self, restart):
        await self.stop_ipyparallel_cluster()
        return super().do_shutdown(restart)
