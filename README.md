## AI Acceleration Program - ADK Tech Enablement Workshop

Author: AI Acceleration Core Team, @weiyih

- The APAC FSA team has created this AI Acceleration with the objective of accelerating the adoption of ADK for developers
- The contents have been specially selected to quickly bring delevelopers up to speed to start building custom agent
- Finally, example code is provided on how to deploy the agent to GCP via Agent Engine for Production.


## Prerequisites

- Customer to create non production sandbox GCP account
- Attendees to have the following permission
    - Compute Engine: roles/compute.admin
    - Cloud Storage: roles/storage.admin
    - Vertex AI: roles/aiplatform.admin
    - Cloud Logging: roles/logging.admin
    - roles/discoveryengine.admin
- Developer to setup local laptop with gcloud CLI, refer to [this](https://cloud.google.com/sdk/docs/install)
- Configure credentials for application development, refer to [this](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)


## Setup
- Minimum is python 3.11
- Checkout code
```bash
git clone https://github.com/yapweiyih/google-adk-workshop.git
cd google-adk-workshop
```

## Setup virtual

### python

```bash
# Assume you have python 3.11
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### UV

```bash
# Install python
uv python install 3.11

# Pin a specific python version for current project
uv python pin 3.11
uv sync

# identify your virtual environment
uv python find
```

### Conda
```bash
conda create -n adk_release python=3.11 ipykernel -y
conda activate adk_release
pip install -r requirements.txt
```


### Vscode
- Install 'jupyter' vscode extension
- Reload vscode
- Open the notebook and make sure the top right kernel is pointing to the newly created virtual env.


## Reference

Please use the following resources to learn more about ADK:
- [ADK Documetation](https://google.github.io/adk-docs/)
- [ADK Code Repository](https://github.com/google/adk-python)

## Credits

We would like to thanks the following team for the content of this workshop:

- ADK Team
- Agent Start Kits Team
- Developer Relation Team
