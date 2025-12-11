from sic_framework.core.sic_application import SICApplication
from sic_framework.core import sic_logging

from theater_performance.performance_controller import PerformanceController


class TheaterPerformanceApp(SICApplication):
    """Entry point for theater performance."""

    def __init__(self):
        super().__init__()
        self.set_log_level(sic_logging.INFO)
        self.controller = PerformanceController(logger=self.logger)

    def run(self):
        self.controller.start_performance()

        try:
            while not self.shutdown_event.is_set():
                self.controller.process_interaction()

        except KeyboardInterrupt:
            self.logger.info("Shutdown requested by user.")

        finally:
            self.controller.shutdown()
            self.shutdown()


if __name__ == "__main__":
    TheaterPerformanceApp().run()
