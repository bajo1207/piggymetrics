#!/usr/bin/env bash
  # CONFIG SERVICE
export CONFIG=piggymetrics-config
docker build -t $CONFIG:$COMMIT ./config
docker tag $CONFIG:$COMMIT $AWS_URL/$CONFIG:$TAG
docker push $AWS_URL/$CONFIG

  # REGISTRY
export REGISTRY=piggymetrics-registry
docker build -t $REGISTRY:$COMMIT ./registry
docker tag $REGISTRY:$COMMIT $AWS_URL/$REGISTRY:$TAG
docker push $AWS_URL/$REGISTRY

  # GATEWAY
export GATEWAY=piggymetrics-gateway
docker build -t $GATEWAY:$COMMIT ./gateway
docker tag $GATEWAY:$COMMIT $AWS_URL/$GATEWAY:$TAG
docker push $AWS_URL/$GATEWAY

  # AUTH SERVICE
export AUTH_SERVICE=piggymetrics-auth-service
docker build -t $AUTH_SERVICE:$COMMIT ./auth-service
docker tag $AUTH_SERVICE:$COMMIT $AWS_URL/$AUTH_SERVICE:$TAG
docker push $AWS_URL/$AUTH_SERVICE

  # ACCOUNT SERVICE
export ACCOUNT_SERVICE=piggymetrics-account-service
docker build -t $ACCOUNT_SERVICE:$COMMIT ./account-service
docker tag $ACCOUNT_SERVICE:$COMMIT $AWS_URL/$ACCOUNT_SERVICE:$TAG
docker push $AWS_URL/$ACCOUNT_SERVICE

  # STATISTICS SERVICE
export STATISTICS_SERVICE=piggymetrics-statistics-service
docker build -t $STATISTICS_SERVICE:$COMMIT ./statistics-service
docker tag $STATISTICS_SERVICE:$COMMIT $AWS_URL/$STATISTICS_SERVICE:$TAG
docker push $AWS_URL/$STATISTICS_SERVICE

  # NOTIFICATION_SERVICE
export NOTIFICATION_SERVICE=piggymetrics-notification-service
docker build -t $NOTIFICATION_SERVICE:$COMMIT ./notification-service
docker tag $NOTIFICATION_SERVICE:$COMMIT $AWS_URL/$NOTIFICATION_SERVICE:$TAG
docker push $AWS_URL/$NOTIFICATION_SERVICE

  # MONITORING
export MONITORING=piggymetrics-monitoring
docker build -t $MONITORING:$COMMIT ./monitoring
docker tag $MONITORING:$COMMIT $AWS_URL/$MONITORING:$TAG
docker push $AWS_URL/$MONITORING

  # TURBINE STREAM SERVICE
export TURBINE=piggymetrics-turbine-stream-service
docker build -t $TURBINE:$COMMIT ./turbine-stream-service
docker tag $TURBINE:$COMMIT $AWS_URL/$TURBINE:$TAG
docker push $AWS_URL/$TURBINE

  # MONGO DB
export MONGO_DB=piggymetrics-mongodb
docker build -t $MONGO_DB:$COMMIT ./mongodb
docker tag $MONGO_DB:$COMMIT $AWS_URL/$MONGO_DB:$TAG
docker push $AWS_URL/$MONGO_DB

  # PIGGYPAL
export PIGGYPAL=piggymetrics-piggypal
docker build -t $PIGGYPAL:$COMMIT ./piggypal
docker tag $PIGGYPAL:$COMMIT $AWS_URL/$PIGGYPAL:$TAG
docker push $AWS_URL/$PIGGYPAL
