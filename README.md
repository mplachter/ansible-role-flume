[![Ansible Role](https://img.shields.io/ansible/role/19860.svg)](https://galaxy.ansible.com/mplachter/flume/) [![Build Status](https://travis-ci.org/mplachter/apache-flume.svg?branch=master)](https://travis-ci.org/mplachter/apache-flume)

Apache-Flume
=========

Ansible Role for deploying and configuring Apache Flume

* Deploys Apache Flume
* Configures Apache Flume
* Creates `apache-flume` service
  * Runs **agent** only configuration

Requirements
------------

* Running
  * Ansible 2.3+
* Testing
  * Docker/Vagrant
  * Molecule = 1.2.5

Role Variables
--------------

* Java `vars`
  ```
  java_heap_xms: 125
  java_heap_xmx: 250
  ```
* Apache Flume `vars`
  ```
  mirror_url: http://apache.mirrors.ionfish.org/flume
  version: 1.7.0
  ```
* Linux folder/path install `vars`
  ```
  download_path: /tmp
  installation_path: /usr/local
  owner: root
  group: root
  ```
* Apache Flume configuration `vars`
  * Please consult [Flume User Guide](https://flume.apache.org/FlumeUserGuide.html)
  * Currently configuration will allow
    * Agents
      * **Service Will Only Be Created For `agent`**
      * mutiple
      * Will need to manually create more services to run these currently
    * source
      * Only allowing one source for each `agent` currently
    * channel
      * Only allowing one channel for each `agent` currently
    * sinks
      * mutiple
    * sinkgroup
      * Will add all `sinks` in `agent` to `sinkgroup`
  * Due to high Flume configuration possibilies please read the following
    * Please substitute "." for "_" in your flume configuration for **Property Names**
      * **Values Do Not Need The Substitute**
      * Example
        * `kafka_consumer_group_id: testflume`
      * Result
        * `agent.source.kafka.consumer.group.id = testflume`
  * Can pass `apache_flume_config` var to copy configuration over
    * Example
      * `apache_flume_config: file/flume-conf.properties`
    * Result
      * This will copy the **flume-conf.properties** from your file directory onto target machine(s)
* Extra variables
  * HDFS native libaries
    * `hdfs_libs = true`
      * This will pull down `HDFS Native Libs` and place them in `plugin.d/hdfs/native/`
* Example variables
  ```
  mirror_url: http://apache.mirrors.ionfish.org/flume
  version: 1.7.0
  download_path: /tmp
  installation_path: /usr/local
  owner: root
  group: root

  java_heap_xms: 125
  java_heap_xmx: 250
  hdfs_libs: true

  agents:
  - name: agent
    source:
      name: kafkaSource
      type: org.apache.flume.source.kafka.KafkaSource
      kafka_consumer_group_id: flume
      kafka_consumer_auto_offset_reset: latest
      kafka_consumer_max_partition_fetch_bytes: 1048576
      kafka_consumer_heartbeat_interval_ms: 3000
      kafka_consumer_session_timeout_ms: 30000
      kafka_consumer_request_timeout_ms: 40000
      kafka_consumer_fetch_max_wait_ms: 500
      kafka_bootstrap_servers:
        - 127.0.0.1:9092
        - 0.0.0.0:9092
      kafka_topics:
        - topic1
        - topic2
    channel:
      name: kakfaChannel
      type: memory
      capacity: 1000000
      transactionCapacity: 100000
    sinks:
      - name: kafkaHDFSSink1
        type: hdfs
        hdfs_path: "s3n://GFGJFSHFJHFGFHSBJ:fdjhSFUYGSF65678+-saigfew123@hdfs/%{topic}/%y/%m/%d/%H"
        hdfs_filePrefix: FlumeData
        hdfs_inUseSuffix: .tmp
        hdfs_rollInterval: 30
        hdfs_rollSize: 1024
        hdfs_rollCount: 10
        hdfs_idleTimeout: 0
        hdfs_batchSize: 100
        hdfs_fileType: "SequenceFile"
        hdfs_maxOpenFiles: 5000
        hdfs_callTimeout: 10000
        hdfs_threadsPoolSize: 10
        hdfs_rollTimerPoolSize: 1
        hdfs_round: false
        hdfs_roundValue: 1
        hdfs_roundUnit: second
        hdfs_timeZone: Local Time
        hdfs_useLocalTimeStamp: false
        hdfs_closeTries: 0
        hdfs_retryInterval: 180
      - name: kafkaHDFSSink2
        type: hdfs
        hdfs_path: "s3n://GFGJFSHFJHFGFHSBJ:fdjhSFUYGSF65678+-saigfew123@hdfs/%{topic}/%y/%m/%d/%H"
        hdfs_filePrefix: FlumeData
        hdfs_inUseSuffix: .tmp
        hdfs_rollInterval: 30
        hdfs_rollSize: 1024
        hdfs_rollCount: 10
        hdfs_idleTimeout: 0
        hdfs_batchSize: 100
        hdfs_fileType: "SequenceFile"
        hdfs_maxOpenFiles: 5000
        hdfs_callTimeout: 10000
        hdfs_threadsPoolSize: 10
        hdfs_rollTimerPoolSize: 1
        hdfs_round: false
        hdfs_roundValue: 1
        hdfs_roundUnit: second
        hdfs_timeZone: Local Time
        hdfs_useLocalTimeStamp: false
        hdfs_closeTries: 0
        hdfs_retryInterval: 180
    sink_group:
      name: sinkgroup1
      processor_type: load_balance
      processor_backoff: false
      processor_selector: round_robin
  ```

Dependencies
------------

* andrewrothstein.java-oracle-jre

Example Playbook
----------------

    - hosts: all
      roles:
        - role: ansible-role-apache-flume

License
-------

MIT

Author Information
------------------

Matthew Plachter
