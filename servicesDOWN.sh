#!/usr/bin/env bash

aws2 ecs update-service --service config --desired-count 0 --cluster PiggyCluster

aws2 ecs update-service --service account-service --desired-count 0 --cluster PiggyCluster

aws2 ecs update-service --service registry --desired-count 0 --cluster PiggyCluster

aws2 ecs update-service --service gateway --desired-count 0 --cluster PiggyCluster

aws2 ecs update-service --service account-mongodb --desired-count 0 --cluster PiggyCluster

aws2 ecs update-service --service auth-service --desired-count 0 --cluster PiggyCluster

aws2 ecs update-service --service auth-mongodb --desired-count 0 --cluster PiggyCluster

aws2 ecs update-service --service piggypal --desired-count 0 --cluster PiggyCluster