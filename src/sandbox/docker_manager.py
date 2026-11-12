"""Docker sandbox manager for isolated execution."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
import docker
from docker.errors import ContainerError, ImageNotFound, APIError


@dataclass
class ExecutionResult:
    exit_code: int
    stdout: str
    stderr: str
    timeout: bool
    oom_killed: bool


class DockerSandbox:
    def __init__(
        self,
        image_tag: str = "uet-ml-sandbox:latest",
        mem_limit: str = "512m",
        timeout_seconds: int = 30,
    ):
        self.image_tag = image_tag
        self.mem_limit = mem_limit
        self.timeout_seconds = timeout_seconds
        self._client: Optional[docker.DockerClient] = None

    @property
    def client(self) -> docker.DockerClient:
        if self._client is None:
            self._client = docker.from_env()
        return self._client

    def run_grading(
        self,
        workspace_dir: Path,
        runner_script: str = "runner.py",
    ) -> ExecutionResult:
        """
        Run the grading container with strict isolation:
        - Network disabled (network_mode='none')
        - Memory and swap bounded
        - Execution timeout enforced
        """
        volumes: Dict[str, Dict[str, str]] = {
            str(workspace_dir.resolve()): {
                "bind": "/sandbox",
                "mode": "ro",  # Read-only mount inside sandbox for security
            }
        }

        container = None
        try:
            container = self.client.containers.create(
                image=self.image_tag,
                command=["python", runner_script],
                network_mode="none",
                mem_limit=self.mem_limit,
                memswap_limit=self.mem_limit,
                nano_cpus=1_000_000_000,  # 1 CPU
                volumes=volumes,
                working_dir="/sandbox",
                detach=True,
            )

            container.start()

            # Wait with timeout
            result = container.wait(timeout=self.timeout_seconds)
            exit_code = result.get("StatusCode", 1)

            # Inspect to see if killed by OOM
            container_info = container.attrs or self.client.api.inspect_container(container.id)
            oom_killed = container_info.get("State", {}).get("OOMKilled", False)

            stdout = container.logs(stdout=True, stderr=False).decode("utf-8", errors="replace")
            stderr = container.logs(stdout=False, stderr=True).decode("utf-8", errors="replace")

            return ExecutionResult(
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                timeout=False,
                oom_killed=oom_killed,
            )

        except Exception as e:
            # Check for read timeout / execution timeout
            is_timeout = "Read timed out" in str(e) or "timeout" in str(e).lower()
            return ExecutionResult(
                exit_code=-1,
                stdout="",
                stderr=f"Execution error: {str(e)}",
                timeout=is_timeout,
                oom_killed=False,
            )
        finally:
            if container:
                try:
                    container.remove(force=True)
                except Exception:
                    pass
