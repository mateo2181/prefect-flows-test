import platform
import prefect
from prefect import Flow, Parameter, task
from prefect.client.secrets import Secret
from prefect.storage import GitHub
from prefect.run_configs import KubernetesRun
import subprocess

PREFECT_PROJECT_NAME = "testing"
FLOW_NAME = "flow_test"
AGENT_LABEL = "etl"

STORAGE = GitHub(
    repo="mateo2181/prefect-flows-test",
    path=f"flows/{FLOW_NAME}.py",
    access_token_secret="GITHUB_ACCESS_TOKEN"
)

RUN_CONFIG = KubernetesRun(labels=[AGENT_LABEL])

@task(log_stdout=True)
def hello_world():
    print(f"Hello from {FLOW_NAME} v2!")
    print(f"Running this task with Prefect: {prefect.__version__} and Python {platform.python_version()}")


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    # user_input = Parameter("user_input", default="Marvin")
    hw = hello_world()

if __name__ == "__main__":
    subprocess.run(
        f"prefect register --project {PREFECT_PROJECT_NAME} -p flows/flow_test.py",
        shell=True,
    )