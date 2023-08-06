# Azure DevOps pipelines python logger

**Azure pipelines** have a feature called [Logging commands](https://docs.microsoft.com/en-us/azure/devops/pipelines/scripts/logging-commands), which makes it possible to communicate with the Azure pipeline agent.  
These logging commands are often used to set a pipeline variable, but can also be used to write *formatted logs* in the task standard outputs, or write *error/warning messages* on the pipeline results web page.

For example, writing the following logs to the standard output :

```python
print("##[group]Beginning of a group")
print("##[warning]Warning message")
print("##[error]Error message")
print("##[section]Start of a section")
print("##[debug]Debug text")
print("##[command]Command-line being run")
print("##[endgroup]")
```

Will render in the task logs like this :

![](assets/log-formatting.png)

This convenience `python` module is designed to make formatted logging and error/warning messages in Azure pipelines easier to use.  
It uses the python `logging` system by creating a subclass of `logging.LoggerAdapter`.

## Install

```
pip install azlog
```

## Usage

First create an AzLogger
```python
from azlog import AzLogger
# Create the logger
logger = AzLogger(__name__)
logger.setLevel(logging.INFO)
```

The `AzLogger` adapter will create a python Logger with the name provided as argument.  
Internally, `AzLogger` will create a `StreamHandler` using an `AzFormatter` as its formatter   

You can also provide your own logger if you need additionnal handlers :
```python
import logging
from azlog import AzLogger

raw_logger = logging.getLogger(__name__)
raw_logger.addHandler(logging.FileHandler('file.log'))

logger = AzLogger(raw_logger)
logger.setLevel(logging.INFO)
```

You can then use the `AzLogger` to print formatted log messages to your task output
```python
logger.group("Beginning of a group")
logger.warning("Warning message")
logger.error("Error message")
logger.section("Start of a section")
logger.debug("Debug text")
logger.command("Command-line being run")
logger.endgroup("")
```

Will render in the task output like this :

![](assets/log-formatting.png)

Or to raise status messages 
```python
logger.issueerror("Issue an error to the pipeline")
logger.issuewarning("Issue a warning to the pipeline")
```

Will render in the pipeline status page like this :

![](assets/issue_error.png)
![](assets/issue_warning.png)
