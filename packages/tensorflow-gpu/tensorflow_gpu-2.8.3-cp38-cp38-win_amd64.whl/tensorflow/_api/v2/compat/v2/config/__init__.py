# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.config namespace.
"""

import sys as _sys

from . import experimental
from . import optimizer
from . import threading
from tensorflow.python.eager.context import LogicalDevice
from tensorflow.python.eager.context import LogicalDeviceConfiguration
from tensorflow.python.eager.context import PhysicalDevice
from tensorflow.python.eager.def_function import experimental_functions_run_eagerly
from tensorflow.python.eager.def_function import experimental_run_functions_eagerly
from tensorflow.python.eager.def_function import functions_run_eagerly
from tensorflow.python.eager.def_function import run_functions_eagerly
from tensorflow.python.eager.remote import connect_to_cluster as experimental_connect_to_cluster
from tensorflow.python.eager.remote import connect_to_remote_host as experimental_connect_to_host
from tensorflow.python.framework.config import get_logical_device_configuration
from tensorflow.python.framework.config import get_soft_device_placement
from tensorflow.python.framework.config import get_visible_devices
from tensorflow.python.framework.config import list_logical_devices
from tensorflow.python.framework.config import list_physical_devices
from tensorflow.python.framework.config import set_logical_device_configuration
from tensorflow.python.framework.config import set_soft_device_placement
from tensorflow.python.framework.config import set_visible_devices