import logging

class Logger(object):
	def set_logger(class_name):
		logger.logging.getLogger(class_name)
		logger.setLevel(logging.INFO)

		#create the logging file handler
		fh = logging.FileHandler("logs.log")
		
		logging.basicConfig(filename="logs.log", level=logging.INFO)

if __name__ == '__main__':
	main()