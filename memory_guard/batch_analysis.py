conversations = [
    {
        'user_message': "...",
        'ai_response': "...",
        'context_history': []
    },
    # ... more conversations
]

batch_result = sensor.batch_analyze(conversations)
print(f"High Risk Conversations: {batch_result['high_risk_conversations']}")
