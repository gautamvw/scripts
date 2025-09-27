#!/bin/bash

# Variables
TAG_KEY="Environment"
TAG_VALUE="Dev"
REGION="eu-north-1"   # Change to your AWS region

# Get all running instance IDs with the given tag
INSTANCE_IDS=$(aws ec2 describe-instances \
  --region "$REGION" \
  --filters "Name=tag:${TAG_KEY},Values=${TAG_VALUE}" "Name=instance-state-name,Values=running" \
  --query "Reservations[].Instances[].InstanceId" \
  --output text)

if [ -n "$INSTANCE_IDS" ]; then
  echo "Stopping instances: $INSTANCE_IDS"
  aws ec2 stop-instances --region "$REGION" --instance-ids $INSTANCE_IDS
else
  echo "No running instances found with tag ${TAG_KEY}=${TAG_VALUE}"
fi