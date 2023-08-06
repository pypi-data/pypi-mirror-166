# nlutils-mini
This is a mini version of nlutils, which only contains the following features:
- Colorful logs based on logging and coloredlogs
- ExperimentLogger, save all parameters to json files with little effort

## Examples

### Simple logger for hyperparameter and performance logging
```python
from nlutils_mini import ExperimentLogger
logger = ExperimentLogger("Test")
lr = 0.001
batch_size = 32

logger.insert_batch_parameters([lr, batch_size])

f1_score = 0.67
accuracy = 0.89

logger.insert_batch_performance([lr, batch_size])
```