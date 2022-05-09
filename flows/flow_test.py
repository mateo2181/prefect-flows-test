import platform
import pandas as pd
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

RUN_CONFIG = KubernetesRun(
    image_pull_policy="Always",
    labels=[AGENT_LABEL],
    image="europe-west6-docker.pkg.dev/zoomcamp-340819/prefect-agents/prefect-agents-etl:latest"
)

@task
def extract_and_load(dataset: str) -> None:
    logger = prefect.context.get("logger")
    file = f"gs://football_transfers/transfers/{dataset}"
    df = pd.read_csv(file)
    logger.info("Dataset %s with %d rows loaded to DB", dataset, len(df))

@task(log_stdout=True)
def hello_world():
    print(f"Hello from {FLOW_NAME} v2!")
    print(f"Running this task with Prefect: {prefect.__version__} and Python {platform.python_version()}")


with Flow(FLOW_NAME, storage=STORAGE, run_config=RUN_CONFIG,) as flow:
    # user_input = Parameter("user_input", default="Marvin")
    hw = hello_world()
    extract_and_load("1999_dutch_eredivisie.csv")

if __name__ == "__main__":
    subprocess.run(
        f"prefect register --project {PREFECT_PROJECT_NAME} -p flows/flow_test.py",
        shell=True,
    )