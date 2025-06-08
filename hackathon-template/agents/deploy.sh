#!/bin/bash

export GOOGLE_GENAI_USE_VERTEXAI="True"
export GOOGLE_CLOUD_PROJECT="hello-world-418507"
export GOOGLE_CLOUD_LOCATION="us-central1"

export AGENT_PATH="./hotel_agent" # Assuming capital_agent is in the current directory
# Set a name for your Cloud Run service (optional)
export SERVICE_NAME="hotel-agent-service"

# Set an application name (optional)
export APP_NAME="cahotelpital-agent-app"

adk deploy cloud_run \
--project=$GOOGLE_CLOUD_PROJECT \
--region=$GOOGLE_CLOUD_LOCATION \
--service_name=$SERVICE_NAME \
--app_name=$APP_NAME \
--with_ui \
$AGENT_PATH
