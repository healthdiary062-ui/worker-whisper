INPUT_VALIDATIONS = {
    "audio": {
        "type": "str",
        "required": False,
        "description": "URL to the audio file (https://...). Optional if audio_base64 is provided."
    },
    "audio_base64": {
        "type": "str",
        "required": False,
        "description": "Base64-encoded audio bytes. Optional if audio (URL) is provided."
    },
    'model': {
        'type': str,
        'required': False,
        'default': 'base'
    },
    'transcription': {
        'type': str,
        'required': False,
        'default': 'plain text'
    },
    'translate': {
        'type': bool,
        'required': False,
        'default': False
    },
    'language': {
        'type': str,
        'required': False,
        'default': None
    },
    'temperature': {
        'type': float,
        'required': False,
        'default': 0
    },
    'best_of': {
        'type': int,
        'required': False,
        'default': 5
    },
    'beam_size': {
        'type': int,
        'required': False,
        'default': 5
    },
    'patience': {
        'type': float,
        'required': False,
        'default': None
    },
    'length_penalty': {
        'type': float,
        'required': False,
        'default': None
    },
    'suppress_tokens': {
        'type': str,
        'required': False,
        'default': '-1'
    },
    'initial_prompt': {
        'type': str,
        'required': False,
        'default': None
    },
    'condition_on_previous_text': {
        'type': bool,
        'required': False,
        'default': True
    },
    'temperature_increment_on_fallback': {
        'type': float,
        'required': False,
        'default': 0.2
    },
    'compression_ratio_threshold': {
        'type': float,
        'required': False,
        'default': 2.4
    },
    'logprob_threshold': {
        'type': float,
        'required': False,
        'default': -1.0
    },
    'no_speech_threshold': {
        'type': float,
        'required': False,
        'default': 0.6
    }
}
