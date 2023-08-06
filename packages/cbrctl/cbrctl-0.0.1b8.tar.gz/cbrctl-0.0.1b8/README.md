# Carbonara CLI

Command line tool for configuring and accessing Carbonara metrics in your cluster

## Usage
> Usage: cbrctl [OPTIONS] COMMAND [ARGS]...
>  
>   CLI tool to manage carbonara context of projects
>  
> Options:
>   --help  Show this message and exit.
>  
> Commands:
>   config   Configures target cluster with Carbonara packages.
>   eject    Uninstalls resources configured by Carbonara
>   init     Initialize Carbonara context.
>   refresh  Refreshes the Carbonara Agent.
>   show     Forward one or more local ports to a Grafana pod.
>   status   Current Status.
>   version  Version Info.

## Development
* Requirements: Python>=3.7
* Command to generate wheel: `python setup sdist`
    * Installable can be found in `dist\`
* Command to test in local environment: `python setup develop`
    * Refer: https://packaging.python.org/en/latest/tutorials/packaging-projects/

## Installation
> ❯ pip install cbrctl