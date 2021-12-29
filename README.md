# singapore-taxi-api

singapore-taxi-api

documentation: <https://documenter.getpostman.com/view/3827865/TWDdjDup>

api url: <https://56a8l7a79c.execute-api.ap-southeast-1.amazonaws.com/prod>

## Requirement

- install python (3.8)
- install chalice

## Testing and run

```zsh
// test api in local
$ chalice local

// deploy serverless api to aws
$ chalice deploy --stage <stage>

// deploy development
$ chalice deploy --stage dev

// deploy production
$ chalice deploy --stage prod

// create deploy zip, inside .chalice/deployments folder
$ chalice package --single-file OUT

// remove serverless services in aws (api gateway, lambda, iam-role)
$ chalice delete

// check more chalice command
$ chalice --help
```
