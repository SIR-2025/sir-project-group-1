import os
from os.path import dirname, abspath, join

from sic_framework.devices import Nao
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.devices.common_naoqi.naoqi_motion import (
    NaoPostureRequest,
    NaoqiAnimationRequest
)
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import (
    NaoqiMotionRecording,
    PlayRecording
)
from sic_framework.devices.common_naoqi.naoqi_autonomous import NaoRestRequest

from theater_performance.config import NAO_IP


# Path to /theater_performance/motion
MOTION_DIR = join(dirname(abspath(__file__)), "motion")


class NaoActions:
    def __init__(self, logger=None):
        self.logger = logger
        self.nao = Nao(ip=NAO_IP)

    def say(self, text):
        if self.logger:
            self.logger.info(f"NAO says: {text}")
        self.nao.tts.request(NaoqiTextToSpeechRequest(text))

    def do_gesture(self, animation):
        """
        Extended version:
        - If animation starts with 'animations/', treat it as a built-in NAO animation.
        - Otherwise, treat it as a recorded motion file in /theater_performance/motion/.
        """
        try:
            # CASE 1 → Built-in NAO animation (unchanged behaviour)
            if animation.startswith("animations/"):
                if self.logger:
                    self.logger.info(f"Gesture (animation): {animation}")
                self.nao.motion.request(NaoqiAnimationRequest(animation), block=False)
                return

            # CASE 2 → Recorded motion from your /motion folder
            motion_path = join(MOTION_DIR, animation)

            if os.path.exists(motion_path):
                if self.logger:
                    self.logger.info(f"Playing recorded motion: {motion_path}")

                recording = NaoqiMotionRecording.load(motion_path)
                self.nao.motion_record.request(PlayRecording(recording))
                return

            # If neither animation nor motion exists
            if self.logger:
                self.logger.error(f"Gesture not found: {animation}")

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error executing gesture '{animation}': {e}")

    def set_stand(self):
        if self.logger:
            self.logger.info("Setting posture → Stand.")
        self.nao.motion.request(NaoPostureRequest("Stand", 0.5))
        
    def rest(self):
        if self.logger:
            self.logger.info("NAO going to rest mode.")
        self.nao.autonomous.request(NaoRestRequest())

    def sit(self):
        if self.logger:
            self.logger.info("Setting posture → Sit.")
        self.nao.motion.request(NaoPostureRequest("Sit", 0.5))