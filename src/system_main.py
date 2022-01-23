import logging
from control_tank import ControlTank

logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class MainSystem():
    def __init__(self) -> None:
        self.control_tank = ControlTank()

    def start(self) -> None:
        try:
            self.control_tank.initialize()
            logger.info('system started')
        except Exception as ex:
            logger.error(f'system encontered exception: {ex}')


main_system = MainSystem()
main_system.start()
