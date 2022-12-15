# Skupper Prometheus Collector

Custom prometheus collector for [Skupper](skupper.io) based on *service-controller* statistics.

## Metrics

| Metric                            | Description                          | Labels                                                                                                                |
| --------------------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| skupper_site_spec_info            | Skupper version and site information | *edge*: 0/1 [^0]<br> *gateway*: 0/1 [^0] <br> *namespace* <br> *site_id* <br> *site_name*  <br> *url*  <br> *version* |
| skupper_site_outgoing_connections | Number of outgoing site connections  | *namespace* <br> *site_name* <br>                                                                                     |
| skupper_service_spec_info         | Service information                  | *address* <br> *protocol*                                                                                             |
| skupper_service_count             | Number of services                   |                                                                                                                       |

[^0]: 0 == False, 1 == True

## Configuration

| Environment Variable               | Description                                    | Default                                     |
| ---------------------------------- | ---------------------------------------------- | ------------------------------------------- |
| **SPC_PORT**                       | Port to listen on.                             | 8000                                        |
| **SPC_LOG_LEVEL**                  | Log level                                      | INFO                                        |
| **SPC_SERVICE_CONTROLLER**         | URL of the service-controller.                 | http://skupper-service-controller:8888/DATA |
| **SPC_SERVICE_CONTROLLER_TIMEOUT** | Timeout in seconds for the service-controller. | 5                                           |

## Deployment

```shell
$ kubectl apply -f https://raw.githubusercontent.com/app-sre/skupper-prometheus-collector/master/openshift/collector.yaml
```
