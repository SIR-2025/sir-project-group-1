import json
import numpy as np
from os.path import abspath
from sic_framework.services.dialogflow_cx.dialogflow_cx import (
    DialogflowCX,
    DialogflowCXConf,
    DetectIntentRequest,
)

from theater_performance.config import (
    NAO_IP,
    DIALOGFLOW_KEYFILE,
    DIALOGFLOW_AGENT_ID,
    DIALOGFLOW_LOCATION
)


class DialogflowHandler:
    """Handles Dialogflow intent detection + gesture mapping."""

    def __init__(self, logger=None):
        self.logger = logger
        self.session_id = np.random.randint(10000)

        # EXACT gesture sequences from teammate’s code
        self.scripted_intents = {
            # INTRO
            "welcome_intent": [
                "animations/Stand/Gestures/Hey_1",
                "animations/Stand/Gestures/Enthusiastic_4"
            ],
            "feel_question": [
                "animations/Stand/Gestures/Explain_3"
            ],
            "feel_game": [
                "animations/Stand/Gestures/Explain_5"
            ],
            "denial_intro": [
                "animations/Stand/Gestures/No_8"
            ],
            "seeing_not_change": [
                "animations/Stand/Gestures/No_3"
            ],

            # DENIAL
            "confident_nao": [
                "almost_swingbat_motion"
            ],
            "practice_show": [
                "almost_swingbat_motion"
            ],
            "denial_response": [
                "animations/Stand/Gestures/No_8",
                "animations/Stand/Gestures/Explain_1",
            ],
            "denial_statement": [
                "animations/Stand/Gestures/No_3"
            ],
            "denial_count_beats": [
                "animations/Stand/Gestures/Explain_1"
            ],
            "lacks_structure": [
                "animations/Stand/Gestures/No_9"
            ],
            "denial_swing": [
                "animations/Stand/Gestures/Explain_1"
            ],

            # DOUBT
            "doubt_baseball_choreo": [
                "animations/Stand/Gestures/Explain_1"
            ],
            "doubt_watch_this": [
                "animations/Stand/Gestures/YouKnowWhat_1"
            ],
            "your_turn": [
                "good_swingbat_motion"
            ],
            "doubt_thats_dancing": [
                "animations/Stand/Gestures/Enthusiastic_4"
            ],
            "doubt_told_you_dance": [
                "animations/Stand/Gestures/Explain_1"
            ],
            "doubt_which_means_dancing": [
                "animations/Stand/Gestures/Yes_1",  
            ],

            # LEARNING
            "learn_dont_dance": [
                "animations/Stand/Gestures/Enthusiastic_4"
            ],
            "learn_try": [
                "animations/Stand/Gestures/Explain_1"
            ],
            "what_you_got": [
                "v1_pre_last_dance_motion"
            ],
            "learn_got_style": [
                "animations/Stand/Gestures/Enthusiastic_4"
            ],
            "learn_grooving_is_dancing": [
                "animations/Stand/Gestures/Yes_1"
            ],

            # ACCEPTANCE
            "accept_can_dance": [
                "final_acceptance_dance_motion"
            ],
            "dance_algorithm": [
                "animations/Stand/Gestures/Explain_1"
            ],
            "accept_exactly": [
                "high_five_motion"
            ],
            "final_ending": [
                "animations/Stand/Gestures/Explain_1",
                "animations/Stand/Gestures/Yes_1",
                "animations/Stand/Gestures/No_3"                
            ]
        }

        # Load Dialogflow key
        keypath = abspath(DIALOGFLOW_KEYFILE)
        with open(keypath) as f:
            keyfile_json = json.load(f)

        conf = DialogflowCXConf(
            keyfile_json=keyfile_json,
            agent_id=DIALOGFLOW_AGENT_ID,
            location=DIALOGFLOW_LOCATION,
            sample_rate_hertz=16000,
            language="en"
        )

        from sic_framework.devices import Nao
        self.nao = Nao(ip=NAO_IP)
        self.cx = DialogflowCX(conf=conf, input_source=self.nao.mic)

        if self.logger:
            self.logger.info("Dialogflow initialized.")

    def detect_intent(self):
        """Detect intent + extract intent_name exactly like teammate."""
        reply = self.cx.request(DetectIntentRequest(self.session_id))

        if reply and reply.intent:
            raw = str(reply.intent)
            intent_name = raw.split("/")[-1]
        else:
            intent_name = None

        if self.logger:
            self.logger.info(f"Detected intent: {intent_name} transcript={reply.transcript}")

        return reply, intent_name

    def is_scripted_intent(self, intent_name):
        return intent_name in self.scripted_intents

    def get_gestures(self, intent_name):
        return self.scripted_intents.get(intent_name, [])
