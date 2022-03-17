from inventory_modules.click_inventory import click_inventory
from jinja2 import Template

cluster = {
    1: ("10.102.0.193", "10.102.0.194"),
    2: ("10.102.0.194", "10.102.0.195"),
    3: ("10.102.0.195", "10.102.0.193")
    }

inventory = click_inventory(cluster)

template = Template(
"""
{%- for container in click_containers %}
<?xml version="1.0"?>
<clickhouse>
    <logger>
        <level>trace</level>
        <log>/var/log/clickhouse-server/clickhouse-server.log</log>
        <errorlog>/var/log/clickhouse-server/clickhouse-server.err.log</errorlog>
        <size>1000M</size>
        <count>10</count>
    </logger>

    <http_port>{{ 8123 + container[0] }}</http_port>
    <tcp_port>{{ 9000 + container[0] }}</tcp_port>
    <mysql_port>9004</mysql_port>
    <postgresql_port>9005</postgresql_port>
    <interserver_http_port>{{ 9009 + container[0] }}</interserver_http_port>
    <listen_host>::</listen_host>
    <max_connections>4096</max_connections>
    <keep_alive_timeout>3</keep_alive_timeout>

    <grpc>
        <enable_ssl>false</enable_ssl>
        <ssl_cert_file>/path/to/ssl_cert_file</ssl_cert_file>
        <ssl_key_file>/path/to/ssl_key_file</ssl_key_file>
        <ssl_require_client_auth>false</ssl_require_client_auth>
        <ssl_ca_cert_file>/path/to/ssl_ca_cert_file</ssl_ca_cert_file>
        <compression>deflate</compression>
        <compression_level>medium</compression_level>
        <max_send_message_size>-1</max_send_message_size>
        <max_receive_message_size>-1</max_receive_message_size>
        <verbose_logs>false</verbose_logs>
    </grpc>

    <openSSL>
            <certificateFile>/etc/clickhouse-server/server.crt</certificateFile>
            <privateKeyFile>/etc/clickhouse-server/server.key</privateKeyFile>
            <dhParamsFile>/etc/clickhouse-server/dhparam.pem</dhParamsFile>
            <verificationMode>none</verificationMode>
            <loadDefaultCAFile>true</loadDefaultCAFile>
            <cacheSessions>true</cacheSessions>
            <disableProtocols>sslv2,sslv3</disableProtocols>
            <preferServerCiphers>true</preferServerCiphers>
        </server>

            <loadDefaultCAFile>true</loadDefaultCAFile>
            <cacheSessions>true</cacheSessions>
            <disableProtocols>sslv2,sslv3</disableProtocols>
            <preferServerCiphers>true</preferServerCiphers>
            <invalidCertificateHandler>
                <name>RejectCertificateHandler</name>
            </invalidCertificateHandler>
        </client>
    </openSSL>

    <max_concurrent_queries>100</max_concurrent_queries>
    <max_server_memory_usage>0</max_server_memory_usage>
    <max_thread_pool_size>10000</max_thread_pool_size>
    <max_server_memory_usage_to_ram_ratio>0.9</max_server_memory_usage_to_ram_ratio>
    <total_memory_profiler_step>4194304</total_memory_profiler_step>
    <total_memory_tracker_sample_probability>0</total_memory_tracker_sample_probability>
    <uncompressed_cache_size>8589934592</uncompressed_cache_size>
    <mark_cache_size>5368709120</mark_cache_size>
    <mmap_cache_size>1000</mmap_cache_size>
    <compiled_expression_cache_size>134217728</compiled_expression_cache_size>
    <compiled_expression_cache_elements_size>10000</compiled_expression_cache_elements_size>
    <path>/var/lib/clickhouse/</path>
    <tmp_path>/var/lib/clickhouse/tmp/</tmp_path>
    <user_files_path>/var/lib/clickhouse/user_files/</user_files_path>

    <ldap_servers>
    </ldap_servers>

    <user_directories>
        <users_xml>
            <path>users.xml</path>
        </users_xml>
        <local_directory>
            <path>/var/lib/clickhouse/access/</path>
        </local_directory>
    </user_directories>

    <default_profile>default</default_profile>
    <custom_settings_prefixes></custom_settings_prefixes>
    <default_database>default</default_database>
    <timezone>Europe/Moscow</timezone>
    <mlock_executable>true</mlock_executable>
    <remap_executable>false</remap_executable>

    <macros>
        <shard>0{{ container[0] }}</shard>
        <replica>{{ container[1] }}</replica>
    </macros>

    <builtin_dictionaries_reload_interval>3600</builtin_dictionaries_reload_interval>


    <max_session_timeout>3600</max_session_timeout>
    <default_session_timeout>60</default_session_timeout>

    <prometheus>
        <endpoint>/metrics</endpoint>
        <port>{{ 9363 + container[0] }}</port>

        <metrics>true</metrics>
        <events>true</events>
        <asynchronous_metrics>true</asynchronous_metrics>
        <status_info>true</status_info>
    </prometheus>

    <query_log>
        <database>system</database>
        <table>query_log</table>
        <partition_by>toYYYYMM(event_date)</partition_by>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
    </query_log>

    <trace_log>
        <database>system</database>
        <table>trace_log</table>
        <partition_by>toYYYYMM(event_date)</partition_by>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
    </trace_log>

    <query_thread_log>
        <database>system</database>
        <table>query_thread_log</table>
        <partition_by>toYYYYMM(event_date)</partition_by>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
    </query_thread_log>

    <query_views_log>
        <database>system</database>
        <table>query_views_log</table>
        <partition_by>toYYYYMM(event_date)</partition_by>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
    </query_views_log>

    <part_log>
        <database>system</database>
        <table>part_log</table>
        <partition_by>toYYYYMM(event_date)</partition_by>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
    </part_log>

    <metric_log>
        <database>system</database>
        <table>metric_log</table>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
        <collect_interval_milliseconds>1000</collect_interval_milliseconds>
    </metric_log>

    <asynchronous_metric_log>
        <database>system</database>
        <table>asynchronous_metric_log</table>
        <flush_interval_milliseconds>7000</flush_interval_milliseconds>
    </asynchronous_metric_log>

    <opentelemetry_span_log>
        <engine>
            engine MergeTree
            partition by toYYYYMM(finish_date)
            order by (finish_date, finish_time_us, trace_id)
        </engine>
        <database>system</database>
        <table>opentelemetry_span_log</table>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
    </opentelemetry_span_log>

    <crash_log>
        <database>system</database>
        <table>crash_log</table>

        <partition_by />
        <flush_interval_milliseconds>1000</flush_interval_milliseconds>
    </crash_log>

    <session_log>
        <database>system</database>
        <table>session_log</table>

        <partition_by>toYYYYMM(event_date)</partition_by>
        <flush_interval_milliseconds>7500</flush_interval_milliseconds>
    </session_log>

    <top_level_domains_lists>
    </top_level_domains_lists>

    <dictionaries_config>*_dictionary.xml</dictionaries_config>
    <user_defined_executable_functions_config>*_function.xml</user_defined_executable_functions_config>


    <encryption_codecs>
    </encryption_codecs>

    <distributed_ddl>
        <path>/clickhouse/task_queue/ddl</path>
    </distributed_ddl>

    <graphite_rollup_example>
        <pattern>
            <regexp>click_cost</regexp>
            <function>any</function>
            <retention>
                <age>0</age>
                <precision>3600</precision>
            </retention>
            <retention>
                <age>86400</age>
                <precision>60</precision>
            </retention>
        </pattern>
        <default>
            <function>max</function>
            <retention>
                <age>0</age>
                <precision>60</precision>
            </retention>
            <retention>
                <age>3600</age>
                <precision>300</precision>
            </retention>
            <retention>
                <age>86400</age>
                <precision>3600</precision>
            </retention>
        </default>
    </graphite_rollup_example>

    <format_schema_path>/var/lib/clickhouse/format_schemas/</format_schema_path>

    <query_masking_rules>
        <rule>
            <name>hide encrypt/decrypt arguments</name>
            <regexp>((?:aes_)?(?:encrypt|decrypt)(?:_mysql)?)\s*\(\s*(?:'(?:\\'|.)+'|.*?)\s*\)</regexp>
            <replace>\1(???)</replace>
        </rule>
    </query_masking_rules>

    <send_crash_reports>
        <enabled>false</enabled>
        <anonymize>false</anonymize>
        <endpoint>https://6f33034cfe684dd7a3ab9875e57b1c8d@o388870.ingest.sentry.io/5226277</endpoint>
    </send_crash_reports>
</clickhouse>
{% endfor %}
"""
)

for host in inventory["clickhouse"]["_meta"]["hostvars"]:
    print(template.render(
        click_containers=inventory["clickhouse"]["_meta"]["hostvars"][host]["click_containers"])
    )