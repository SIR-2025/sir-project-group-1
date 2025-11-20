# Import basic preliminaries
from sic_framework.core.sic_application import SICApplication
from sic_framework.core import sic_logging

# Import the device(s) we will be using
from sic_framework.devices import Nao
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.devices.common_naoqi.naoqi_motion import NaoqiAnimationRequest, NaoPostureRequest

# Import the service(s) we will be using
from sic_framework.services.dialogflow_cx.dialogflow_cx import (
    DialogflowCX,
    DialogflowCXConf,
    DetectIntentRequest,
    QueryResult,
    RecognitionResult,
)

# Import libraries necessary for the demo
import json
from os.path import abspath, join
import numpy as np


class NaoDialogflowCXDemo(SICApplication):
    """
    NAO Dialogflow CX demo application.
    """

    def __init__(self):
        # Call parent constructor (handles singleton initialization)
        super(NaoDialogflowCXDemo, self).__init__()

        self.nao_ip = "10.0.0.239"
        self.dialogflow_keyfile_path = abspath(join("..", "..", "conf", "google", "google-key.json"))
        self.nao = None
        self.dialogflow_cx = None
        self.session_id = np.random.randint(10000)

        self.set_log_level(sic_logging.INFO)
        
        # Log files will only be written if set_log_file is called. Must be a valid full path to a directory.
        # self.set_log_file("/Users/apple/Desktop/SAIL/SIC_Development/sic_applications/demos/nao/logs")
        
        self.setup()

    def on_recognition(self, message):
        """Callback for recognition results."""
        if message.response:
            if hasattr(message.response, 'recognition_result') and message.response.recognition_result:
                rr = message.response.recognition_result
                if hasattr(rr, 'is_final') and rr.is_final:
                    if hasattr(rr, 'transcript'):
                        self.logger.info(f"Transcript: {rr.transcript}")

    def setup(self):
        """Initialize NAO and Dialogflow CX."""
        self.logger.info("Initializing NAO robot...")
        self.nao = Nao(ip=self.nao_ip)
        nao_mic = self.nao.mic

        self.logger.info("Initializing Dialogflow CX...")

        # Load key
        with open(self.dialogflow_keyfile_path) as f:
            keyfile_json = json.load(f)

        # Agent info
        agent_id = "3e375e92-66e0-42f9-8882-0f3f97988c0e"
        location = "europe-west4"

        dialogflow_conf = DialogflowCXConf(
            keyfile_json=keyfile_json,
            agent_id=agent_id,
            location=location,
            sample_rate_hertz=16000,
            language="en"
        )

        self.dialogflow_cx = DialogflowCX(conf=dialogflow_conf, input_source=nao_mic)
        
        self.logger.info("Initialized Dialogflow CX... registering callback function")
        # Register a callback function to handle recognition results
        self.dialogflow_cx.register_callback(callback=self.on_recognition)
        # Initialize Dialogflow CX with NAO's microphone as input
    def run(self):
        """Main loop."""
        try:
            
            self.nao.tts.request(NaoqiTextToSpeechRequest("Hello, I am Nao, nice to meet you!"))
            self.logger.info(" -- Ready -- ")
            #Demo starts
            while not self.shutdown_event.is_set():
                self.logger.info(" ----- Your turn to talk!")

                reply = self.dialogflow_cx.request(DetectIntentRequest(self.session_id))

                # UPDATED INTENT HANDLING STARTS HERE
                if reply.intent:

                    raw_intent = str(reply.intent)
                    intent_name = raw_intent.split("/")[-1]

                    self.logger.info(f"Raw reply.intent = {raw_intent}")
                    self.logger.info(
                        f"The detected intent: {intent_name} (confidence: {reply.intent_confidence})"
                    )

                    # === INTENT: welcome_intent ===
                    if intent_name == "welcome_intent":
                        self.logger.info("welcome_intent detected - performing wave gesture")
                        self.nao.motion.request(NaoPostureRequest("Stand", 0.5), block=False)
                        self.nao.motion.request(
                            NaoqiAnimationRequest("animations/Stand/Gestures/Hey_1"),
                            block=False
                        )

                    # === INTENT: challenge_dance ===
                    elif intent_name == "challenge_dance":
                        self.logger.info("challenge_dance detected")
                        self.nao.motion.request(
                            NaoqiAnimationRequest("animations/Stand/Gestures/No_1"),
                            block=False
                        )

                    # === INTENT: feel_question ===
                    elif intent_name == "feel_question":
                        self.logger.info("feel_question detected")
                        self.nao.motion.request(
                            NaoqiAnimationRequest("animations/Stand/Gestures/Explain_1"),
                            block=False
                        )

                    # === INTENT: feel_game ===
                    elif intent_name == "feel_game":
                        self.logger.info("feel_game detected")
                        self.nao.motion.request(
                            NaoqiAnimationRequest("animations/Stand/Gestures/Explain_2"),
                            block=False
                        )

                    # === INTENT: denial_intro ===
                    elif intent_name == "denial_intro":
                        self.logger.info("denial_intro detected")
                        self.nao.motion.request(
                            NaoqiAnimationRequest("animations/Stand/Gestures/No_1"),
                            block=False
                        )

                else:
                    self.logger.info("No intent detected")
                # UPDATED INTENT HANDLING ENDS HERE

                # Transcript
                if reply.transcript:
                    self.logger.info(f"User said: {reply.transcript}")

                # Fulfillment message
                if reply.fulfillment_message:
                    text = reply.fulfillment_message
                    self.logger.info(f"NAO reply: {text}")
                    self.nao.tts.request(NaoqiTextToSpeechRequest(text))
                else:
                    self.logger.info("No fulfillment message")

                # Parameters
                if reply.parameters:
                    self.logger.info(f"Parameters: {reply.parameters}")

        except KeyboardInterrupt:
            self.logger.info("Demo interrupted by user")

        except Exception as e:
            self.logger.error(f"Exception: {e}")
            import traceback
            traceback.print_exc()

        finally:
            self.shutdown()


if __name__ == "__main__":
    #Create and run demo
    demo = NaoDialogflowCXDemo()
    demo.run()
