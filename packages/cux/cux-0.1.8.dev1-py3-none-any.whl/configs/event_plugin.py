EVENT_PLUGINS = {
    "plugins": [
        {
            "name": "next_step",
            "id": 1,
            'topic': 'next_step',
            "type": "event_engine",
            "channel": "next_step_channel",
            "industry": None,
        },
        {
            "name": "default",
            "id": 2,
            'topic': 'basic_tracker',
            "type": "event_engine",
            "channel": "basic_tracker_channel",
            "industry": None,
        },
        {
            "name": "transcript",
            "id": 3,
            'topic': 'transcript',
            "type": "transcript",
            "channel": "transcript_channel",
            "industry": None,
        },
        {
            "name": "qa",
            "id": 4,
            'topic': 'qa',
            "type": "qa",
            "channel": "qa",
            "industry": None,
        },
        {
            "name": "backend_tracker",
            "id":5,
            'topic': 'backend_tracker',
            "type": "backend_tracker",
            "channel": "backend_tracker_channel",
            "industry": None,
        },
        {
            "name": "intelligence",
            "id":6,
            'topic': 'intelligence',
            "type": "event_engine",
            "channel": "intelligence_channel",
            "industry": [3],
        },
        {
            "name": "topic",
            "id":7,
            'topic': 'topic',
            "type": "topic",
            "channel": "topic_channel",
            "industry": None,
        }
    ]
}
