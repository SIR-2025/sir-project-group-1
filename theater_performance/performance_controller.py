from theater_performance.dialogflow_handler import DialogflowHandler
from theater_performance.nao_actions import NaoActions
from theater_performance.llm_handler import LLMHandler


class PerformanceController:
    """Matches teammate's scripted behavior + LLM fallback."""

    def __init__(self, logger=None):
        self.logger = logger

        self.nao = NaoActions(logger=logger)
        self.dialogflow = DialogflowHandler()
        self.llm = LLMHandler(logger=logger)

        self.current_state = "INTRODUCTION"
        self.finished = False

    def start_performance(self):
        self.nao.set_stand()
        self.nao.say("Hello, I am Cody, nice to meet you!")
        if self.logger:
            self.logger.info("Performance started.")

    def process_interaction(self):
        reply, intent_name = self.dialogflow.detect_intent()

        if not reply or not reply.transcript:
            if self.logger:
                self.logger.info(" No speech detected.")
            return

        user_input = reply.transcript
        fulfillment = reply.fulfillment_message

        # Scripted intent
        if intent_name and self.dialogflow.is_scripted_intent(intent_name):

            gestures = self.dialogflow.get_gestures(intent_name)

            if self.logger:
                self.logger.info(f"Scripted intent: {intent_name}")
                self.logger.info(f"Gestures: {gestures}")
                self.logger.info(f"Scripted line: {fulfillment}")

            # Play gestures in order
            for g in gestures:
                self.nao.do_gesture(g)

            # Speak scripted Dialogflow line
            if fulfillment:
                self.nao.say(fulfillment)
                
            # After the very last intent, make NAO rest
            if intent_name == "final_ending":
                if self.logger:
                    self.logger.info("Final intent 'final_ending' reached - NAO sits.")
                self.nao.sit()
                self.shutdown()
                self.finished = True
            return

        # LLM fallback
        response = self.llm.generate(
            state=self.current_state,
            user_input=user_input
        )
        self.nao.say(response)

    def shutdown(self):
        
        if self.logger:
            self.nao.rest()
            self.finished = True
            self.logger.info("Performance shutdown complete.")