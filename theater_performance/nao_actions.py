from sic_framework.devices import Nao
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.devices.common_naoqi.naoqi_motion import (
    NaoPostureRequest,
    NaoqiAnimationRequest
)

from theater_performance.config import NAO_IP


class NaoActions:
    def __init__(self, logger=None):
        self.logger = logger
        self.nao = Nao(ip=NAO_IP)

    def say(self, text):
        if self.logger:
            self.logger.info(f"🗣️ NAO says: {text}")
        self.nao.tts.request(NaoqiTextToSpeechRequest(text))

    def do_gesture(self, animation):
        if self.logger:
            self.logger.info(f"💃 Gesture: {animation}")
        self.nao.motion.request(NaoqiAnimationRequest(animation), block=False)

    def set_stand(self):
        if self.logger:
            self.logger.info("Setting posture → Stand.")
        self.nao.motion.request(NaoPostureRequest("Stand", 0.5))
