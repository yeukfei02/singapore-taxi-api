# singapore-taxi-api

singapore-taxi-api

documentation:

api url:

## Requirement:

- install python (3.8)
- install chalice

## Testing and run:

```
// test api in local
$ chalice local

// deploy serverless api to aws
$ chalice deploy --stage <stage>

// development
$ chalice deploy --stage dev

// production
$ chalice deploy --stage prod

// remove serverless services in aws (api gateway, lambda, s3, cloudformation)
$ chalice delete

// use help to see what command can use
$ chalice --help

Usage: chalice [OPTIONS] COMMAND [ARGS]...

Options:
  --version             Show the version and exit.
  --project-dir TEXT    The project directory path (absolute or
                        relative).Defaults to CWD

  --debug / --no-debug  Print debug logs to stderr.
  --help                Show this message and exit.

Commands:
  delete
  deploy
  dev                Development and debugging commands for chalice.
  gen-policy
  generate-models    Generate a model from Chalice routes.
  generate-pipeline  Generate a cloudformation template for a starter CD...
  generate-sdk
  invoke             Invoke the deployed lambda function NAME.
  local
  logs
  new-project
  package
  url
```
