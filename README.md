[![Build Status](https://travis-ci.org/bajo1207/piggymetrics.svg?branch=master)](https://travis-ci.org/bajo1207/piggymetrics)
![GitHub issues](https://img.shields.io/github/issues/bajo1207/piggymetrics)
![GitHub repo size](https://img.shields.io/github/repo-size/bajo1207/piggymetrics)
[![Chat with us on Discord](https://img.shields.io/static/v1?label=&%20us&message=Chat%20with%20us%20on%20Discord&logo=discord&color=gray)](https://discord.gg/8PNmJeS)
![WTFPL License](https://img.shields.io/badge/License-WTFPL-green "This work is licensed under the WTFPL")
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fbajo1207%2Fpiggymetrics.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fbajo1207%2Fpiggymetrics?ref=badge_shield)

![Disclaimer](https://img.shields.io/badge/Disclaimer-This%20is%20a%20student%20project%20in%20progress-red)

# PayPal Integration for Piggy Metrics

Our goal is to get a better understanding of microservice programming and implement a new service into piggymetrics, which allows users to login with their paypal account and track transactions made via paypal in their piggymetrics history.

## Functional services

PiggyMetrics was decomposed into three core microservices. All of them are independently deployable applications, organized around certain business domains. In this project we added a microservice that interacts with these core services to add PayPal Integration to PiggyMetrics.

### Account service
Contains general user input logic and validation: incomes/expenses items, savings and account settings.

### Statistics service
Performs calculations on major statistics parameters and captures time series for each account. Datapoint contains values, normalized to base currency and time period. This data is used to track cash flow dynamics in account lifetime.

### Notification service
Stores users contact information and notification settings (like remind and backup frequency). Scheduled worker collects required information from other services and sends e-mail messages to subscribed customers.


## PiggyPay
This is our new Microservice. It offers the user PayPal Integration. Users can register and login to their account and see their PayPal transaction history. A user can choose to use the PiggyMetrics Authorization Service or to create a PiggyPal account, which couples PiggyMetrics with PayPal.

TODO

Method	| Path	| Description	| User authenticated	| Available from UI
------------- | ------------------------- | ------------- |:-------------:|:----------------:|
GET     | /                   | Get Paypal Login Button         | |
GET     | /piggypal           | Get Paypal Transaction History  | |
GET     | /piggypal-listens   | | |
DELETE  | /piggypal-listens   | Returns current Authorization and erases confidential Information | |

#### Notes
Our Microservice will communicate with the Statistics Service and the Account Service to integrate Paypal support.

## Security

An advanced security configuration is beyond the scope of this proof-of-concept project.

## Infrastructure automation

Deploying microservices, with their interdependence, is much more complex process than deploying monolithic application. It is important to have fully automated infrastructure. We can achieve following benefits with Continuous Delivery approach:

- The ability to release software anytime
- Any build could end up being a release
- Build artifacts once - deploy as needed

Here is a simple Continuous Delivery workflow, implemented in this project:

TODO

In this [configuration](https://github.com/bajo1207/piggymetrics/blob/master/.travis.yml), Travis CI builds tagged images for each successful git push. So, there are always `latest` image for each microservice on TODO and older images, tagged with TODO. It's easy to deploy any of them and quickly rollback, if needed.

## How to run all the things?

Keep in mind, that you are going to start 8 Spring Boot applications, 4 MongoDB instances, 1 Python application and RabbitMq. Make sure you have `4 Gb` RAM available on your machine. You can always run just vital services though: Gateway, Registry, Config, Auth Service, Account Service and PiggyPal.

#### Before you start
- Install Docker and Docker Compose.
- Change environment variable values in `.env` file for more security or leave it as it is.
- Make sure to build the project: `mvn package [-DskipTests]`

#### Production mode
In this mode, all latest images will be pulled from Docker Hub.
Just copy `docker-compose.yml` and hit `docker-compose up`

#### Development mode
If you'd like to build images yourself (with some changes in the code, for example), you have to clone all repository and build artifacts with maven. Then, run `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up`

`docker-compose.dev.yml` inherits `docker-compose.yml` with additional possibility to build images locally and expose all containers ports for convenient development.

If you'd like to start applications in Intellij Idea you need to either use [EnvFile plugin](https://plugins.jetbrains.com/plugin/7861-envfile) or manually export environment variables listed in `.env` file (make sure they were exported: `printenv`)

#### Important endpoints
- http://localhost:80 - Gateway
- http://localhost:8761 - Eureka Dashboard
- http://localhost:9000/hystrix - Hystrix Dashboard (Turbine stream link: `http://turbine-stream-service:8080/turbine/turbine.stream`)
- http://localhost:15672 - RabbitMq management (default login/password: guest/guest)

#### Piggypal User Workflow
  TODO

#### Notes
All Spring Boot applications require already running [Config Server](https://github.com/sqshq/PiggyMetrics#config-service) for startup. But we can start all containers simultaneously because of `depends_on` docker-compose option.

Also, Service Discovery mechanism needs some time after all applications startup. Any service is not available for discovery by clients until the instance, the Eureka server and the client all have the same metadata in their local cache, so it could take 3 heartbeats. Default heartbeat period is 30 seconds.
