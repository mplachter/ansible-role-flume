import testinfra.utils.ansible_runner
import pytest


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


@pytest.fixture()
def config_file():
    config_f = '/usr/local/flume/conf/flume-conf.properties'
    return config_f


def test_apache_flume_installed(File):
    c_file = File('/usr/local/flume/bin/flume-ng')
    assert c_file.exists
    assert c_file.is_file


def test_apache_flume_flume_env(File):
    c_file = File('/usr/local/flume/conf/flume-env.sh')
    assert c_file.exists
    assert c_file.is_file
    assert c_file.mode == 0644
    assert c_file.group == "root"


def test_apache_flume_config_state(File, config_file):
    c_file = File(config_file)
    assert c_file.exists
    assert c_file.is_file
    assert c_file.mode == 0644
    assert c_file.group == "root"


def test_apache_flume_service(Service):
    ntp_daemon = "apache-flume"
    s = Service(ntp_daemon)
    assert s.is_running
    assert s.is_enabled


def test_apache_flume_java_heap(File):
    c_file = File('/usr/local/flume/conf/flume-env.sh')
    assert c_file.exists
    assert c_file.is_file


def test_apache_flume_check_hdfs_libs(File):
    c_file = File('/usr/local/flume/conf/flume-env.sh')
    assert c_file.contains('-Xms125m -Xmx250m')


def test_apache_flume_systemd(File):
    c_file = File('/etc/systemd/system/apache-flume.service')
    assert c_file.contains('/usr/local/flume/bin/flume-ng agent')


@pytest.mark.parametrize("nodetype,teststring", [
    ("flume-file",
     "agent.sources = httpSource"),
    ("flume-file",
     "agent.channels = httpChannel"),
    ("flume-file",
     "agent.sinks = httpFileSink"),
    ("flume-file",
     "agent.sources.httpSource.type = http"),
    ("flume-file",
     "agent.sources.httpSource.port = 8080"),
    ("flume-file",
     "agent.sources.httpSource.channels = httpChannel"),
    ("flume-file",
     "agent.channels.httpChannel.type = memory"),
    ("flume-file",
     "agent.channels.httpChannel.capacity = 1000000"),
    ("flume-file",
     "agent.channels.httpChannel.transactionCapacity = 100000"),
    ("flume-file",
     "agent.sinks.httpFileSink.sink.directory = /usr/tmp"),
    ("flume-file",
     "agent.sinks.httpFileSink.type = file_roll"),
    ("flume-file",
     "agent.sinks.httpFileSink.sink.rollInterval = 300"),
    ("flume-file",
     "agent.sinks.httpFileSink.channel = httpChannel"),
    ("flume-file",
     "agentkafka.sources = kafkaSource"),
    ("flume-file",
     "agentkafka.channels = kafkaChannel"),
    ("flume-file",
     "agentkafka.sinks = kafkaFileSink1 kafkaFileSink2"),
    ("flume-file",
     "agentkafka.sources.kafkaSource.kafka.topics = topic1, topic2"),
    ("flume-file",
     "agentkafka.sources.kafkaSource.kafka.bootstrap.servers = " +
     "127.0.0.1:9092, 0.0.0.0:9092"),
    ("flume-file",
     "agentkafka.sources.kafkaSource.kafka.consumer.group.id = flume"),
    ("flume-file",
     "agentkafka.sources.kafkaSource.kafka.consumer.auto.offset.reset = " +
     "latest"),
    ("flume-file",
     "agentkafka.sources.kafkaSource.type = " +
     "org.apache.flume.source.kafka.KafkaSource"),
    ("flume-file",
     "agentkafka.sources.kafkaSource.channels = kafkaChannel"),
    ("flume-file",
     "agentkafka.channels.kafkaChannel.type = memory"),
    ("flume-file",
     "agentkafka.channels.kafkaChannel.capacity = 1000000"),
    ("flume-file",
     "agentkafka.channels.kafkaChannel.transactionCapacity = 100000"),
    ("flume-file",
     "agentkafka.sinks.kafkaFileSink1.sink.directory = /usr/tmp"),
    ("flume-file",
     "agentkafka.sinks.kafkaFileSink1.type = file_roll"),
    ("flume-file",
     "agentkafka.sinks.kafkaFileSink1.sink.rollInterval = 300"),
    ("flume-file",
     "agentkafka.sinks.kafkaFileSink1.channel = kafkaChannel"),
    ("flume-file",
     "agentkafka.sinks.kafkaFileSink2.sink.directory = /usr/tmp"),
    ("flume-file",
     "agentkafka.sinks.kafkaFileSink2.type = file_roll"),
    ("flume-file",
     "agentkafka.sinks.kafkaFileSink2.sink.rollInterval = 300"),
    ("flume-file",
     "agentkafka.sinks.kafkaFileSink2.channel = kafkaChannel"),
    ("flume-file",
     "agentkafka.sinkgroups = sinkgroup1"),
    ("flume-file",
     "agentkafka.sinkgroups.sinkgroup1.sinks = " +
     "kafkaFileSink1 kafkaFileSink2"),
    ("flume-file",
     "agentkafka.sinkgroups.processor.backoff = False"),
    ("flume-file",
     "agentkafka.sinkgroups.processor.type = load_balance"),
    ("flume-file",
     "agentkafka.sinkgroups.processor.selector = round_robin"),
    ("flume-hdfs",
     "agent.sources = kafkaSource"),
    ("flume-hdfs",
     "agent.channels = kakfaChannel"),
    ("flume-hdfs",
     "agent.sinks = kafkaHDFSSink1 kafkaHDFSSink2"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.kafka.consumer.fetch.max.wait.ms = 500"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.kafka.topics = topic1, topic2"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.kafka.consumer.heartbeat.interval.ms = 3000"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.kafka.consumer.max.partition.fetch.bytes = " +
     "1048576"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.kafka.bootstrap.servers = " +
     "127.0.0.1:9092, 0.0.0.0:9092"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.kafka.consumer.group.id = flume"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.kafka.consumer.session.timeout.ms = 30000"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.kafka.consumer.auto.offset.reset = latest"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.kafka.consumer.request.timeout.ms = 40000"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.type = " +
     "org.apache.flume.source.kafka.KafkaSource"),
    ("flume-hdfs",
     "agent.sources.kafkaSource.channels = kakfaChannel"),
    ("flume-hdfs",
     "agent.channels.kakfaChannel.type = memory"),
    ("flume-hdfs",
     "agent.channels.kakfaChannel.capacity = 1000000"),
    ("flume-hdfs",
     "agent.channels.kakfaChannel.transactionCapacity = 100000"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.path = s3n://GFGJFSHFJHFGFHSBJ:fdjhSFU" +
     "YGSF65678+-saigfew123@hdfs/%{topic}/%y/%m/%d/%H"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.timeZone = Local Time"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.rollSize = 1024"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.roundValue = 1"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.callTimeout = 10000"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.inUseSuffix = .tmp"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.idleTimeout = 0"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.retryInterval = 180"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.filePrefix = FlumeData"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.rollTimerPoolSize = 1"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.useLocalTimeStamp = False"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.type = hdfs"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.fileType = SequenceFile"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.round = False"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.rollInterval = 30"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.maxOpenFiles = 5000"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.batchSize = 100"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.closeTries = 0"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.roundUnit = second"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.rollCount = 10"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.hdfs.threadsPoolSize = 10"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink1.channel = kakfaChannel"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.path = s3n://GFGJFSHFJHFGFHSBJ:fdjhSF" +
     "UYGSF65678+-saigfew123@hdfs/%{topic}/%y/%m/%d/%H"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.timeZone = Local Time"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.rollSize = 1024"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.roundValue = 1"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.callTimeout = 10000"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.inUseSuffix = .tmp"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.idleTimeout = 0"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.retryInterval = 180"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.filePrefix = FlumeData"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.rollTimerPoolSize = 1"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.useLocalTimeStamp = False"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.type = hdfs"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.fileType = SequenceFile"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.round = False"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.rollInterval = 30"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.maxOpenFiles = 5000"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.batchSize = 100"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.closeTries = 0"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.roundUnit = second"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.rollCount = 10"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.hdfs.threadsPoolSize = 10"),
    ("flume-hdfs",
     "agent.sinks.kafkaHDFSSink2.channel = kakfaChannel"),
    ("flume-hdfs",
     "agent.sinkgroups = sinkgroup1"),
    ("flume-hdfs",
     "agent.sinkgroups.sinkgroup1.sinks = kafkaHDFSSink1 kafkaHDFSSink2"),
    ("flume-hdfs",
     "agent.sinkgroups.processor.backoff = False"),
    ("flume-hdfs",
     "agent.sinkgroups.processor.type = load_balance"),
    ("flume-hdfs",
     "agent.sinkgroups.processor.selector = round_robin")
])
def test_apache_flume_config_sources(File, config_file,
                                     Command, nodetype, teststring):
    c_file = File(config_file)
    if nodetype in Command("hostname").stdout:
        assert c_file.contains(teststring)


def test_apache_flume_listener(Command):
    if 'file_sink' in Command("hostname").stdout:
        listener = Command("netstat -ant")
        assert '8080' in listener.stdout
