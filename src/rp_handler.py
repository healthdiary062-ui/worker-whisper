''' infer.py for runpod worker '''

import os
import predict
import base64
import tempfile


import runpod
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.utils import download_files_from_urls, rp_cleanup

from rp_schema import INPUT_VALIDATIONS

MODEL = predict.Predictor()
MODEL.setup()


def run(job):
    job_input = job['input']

    # Cast numeric params to float
    job_input['temperature'] = float(job_input.get('temperature', 0))
    job_input['temperature_increment_on_fallback'] = float(job_input.get('temperature_increment_on_fallback', 0.2))
    job_input['compression_ratio_threshold'] = float(job_input.get('compression_ratio_threshold', 2.4))
    job_input['logprob_threshold'] = float(job_input.get('logprob_threshold', -1.0))
    job_input['no_speech_threshold'] = float(job_input.get('no_speech_threshold', 0.6))

    # Validate input fields
    validated_input = validate(job_input, INPUT_VALIDATIONS)
    if 'errors' in validated_input:
        return {"error": validated_input['errors']}

    # ---------- AUDIO HANDLING: URL or Base64 ----------
    audio_b64 = job_input.get("audio_base64")
    audio_url = job_input.get("audio")

    if audio_b64:
        # Decode base64 into a temp file under input_objects/
        os.makedirs("input_objects", exist_ok=True)
        tmp_fd, tmp_path = tempfile.mkstemp(prefix=f"{job['id']}_", suffix=".audio", dir="input_objects")
        os.close(tmp_fd)

        with open(tmp_path, "wb") as f:
            f.write(base64.b64decode(audio_b64))

        # For the rest of the pipeline, treat this as the audio path
        job_input["audio"] = tmp_path

    elif audio_url:
        # Existing behavior: download from URL
        job_input['audio'] = download_files_from_urls(job['id'], [audio_url])[0]

    else:
        return {"error": "Either 'audio' (URL) or 'audio_base64' must be provided."}

    # ---------- Run Whisper ----------
    whisper_results = MODEL.predict(
        audio=job_input["audio"],
        model_name=job_input.get("model", 'base'),
        transcription=job_input.get('transcription', 'plain_text'),
        translate=job_input.get('translate', False),
        language=job_input.get('language', None),
        temperature=job_input.get('temperature', 0),
        temperature_increment_on_fallback=job_input.get('temperature_increment_on_fallback', 0.2),
        compression_ratio_threshold=job_input.get('compression_ratio_threshold', 2.4),
        logprob_threshold=job_input.get('logprob_threshold', -1.0),
        no_speech_threshold=job_input.get('no_speech_threshold', 0.6),
        condition_on_previous_text=job_input.get('condition_on_previous_text', True),
        initial_prompt=job_input.get('initial_prompt', None),
        word_timestamps=job_input.get('word_timestamps', False)
    )

    # Cleanup temp inputs (including our base64 temp file)
    rp_cleanup.clean(['input_objects'])

    return whisper_results



runpod.serverless.start({"handler": run})
