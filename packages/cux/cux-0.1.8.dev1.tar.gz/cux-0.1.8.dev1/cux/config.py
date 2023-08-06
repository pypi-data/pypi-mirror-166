SQL_CONFIG = {
    'ip': '47.92.192.123',
    'username': 'dbconn',
    'ssh_password': '(#mG%so$nW7e!oAO5',
    'ssh_pkey': '/home/gaoang/.ssh/id_rsa',
    'sql_ip': 'base2',
    'app_username': 'developer',
    'app_password': 'p8RpIJnFUhnx2oa0',
    'dev_ip': '39.101.129.56',
    'dev_pass': '3JzzykEclearH3Z',
    'dev_oss_prefix': 'https://sale-dev.oss-cn-zhangjiakou.aliyuncs.com',
    'test_ip': '39.103.221.243',
    'test_pass': 'WeFkaFjRb5XEUfxf',
    'test_oss_prefix': 'https://sale-test.oss-cn-zhangjiakou.aliyuncs.com',
}

AI_PROCESS_DEMO = [
    'id', 'organization_id', 'conversation_id', 'is_storaged',
    'is_audio_pre_processed', 'is_transcript', 'is_text_pre_processed',
    'is_event_engine_complete', 'is_es_insert_complete', 'is_prebi_complete',
    'is_qa_complete', 'is_keyword_complete', 'is_abstract_complete',
    'is_complete', 'single_file_path', 'splicing_file_path', 'is_delete',
    'update_at', 'create_at', 'is_deal_risk_complete',
    'is_conversation_topic_complete'
]

INTELLIGENCE_DEMO = [
    'id', 'conversation_url', 'organization_id', 'conversation_id',
    'event_name', 'create_at', 'update_at', 'title', 'content', 'company',
    'begin_time', 'status', 'is_delete', 'is_old_data', 'predict_is_real'
]
