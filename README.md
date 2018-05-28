## Logger For Python

### Installation:
    pip install log4py

#### usage:
	from log4py import create_logger


	log = create_logger(__name__)

	log.info("hello world")


	@create_logger()
	class A:
		def __init__(self):
			self.logger.info("hello A")

	A()
