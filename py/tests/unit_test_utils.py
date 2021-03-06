#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pyspark import SparkConf

from generic_test_utils import *


def asert_h2o_frame(test_suite, h2o_frame, rdd):
    test_suite.assertEquals(h2o_frame.nrow, rdd.count(), "Number of rows should match")
    test_suite.assertEquals(h2o_frame.ncol, 1, "Number of columns should equal 1")
    test_suite.assertEquals(h2o_frame.names, ["values"], "Column should be name values")


def get_default_spark_conf(additional_conf={}):
    conf = SparkConf(). \
        setAppName("pyunit-test"). \
        setMaster("local[*]"). \
        set("spark.driver.memory", "2g"). \
        set("spark.executor.memory", "2g"). \
        set("spark.ext.h2o.client.log.level", "DEBUG"). \
        set("spark.ext.h2o.repl.enabled", "false"). \
        set("spark.task.maxFailures", "1"). \
        set("spark.rpc.numRetries", "1"). \
        set("spark.deploy.maxExecutorRetries", "1"). \
        set("spark.network.timeout", "360s"). \
        set("spark.worker.timeout", "360"). \
        set("spark.ext.h2o.backend.cluster.mode", cluster_mode()). \
        set("spark.ext.h2o.cloud.name", unique_cloud_name("test")). \
        set("spark.ext.h2o.external.start.mode", "auto"). \
        set("spark.ext.h2o.node.log.dir", "build/h2ologs-pyunit/workers"). \
        set("spark.ext.h2o.client.log.dir", "build/h2ologs-pyunit/client")

    if tests_in_external_mode():
        conf.set("spark.ext.h2o.client.ip", local_ip())
        conf.set("spark.ext.h2o.external.cluster.num.h2o.nodes", "1")

    for key in additional_conf:
        conf.set(key, additional_conf[key])

    return conf
