class LevelStyles():
    ## 1 if bold else 0;color
    info_color = "0;37m"
    success_color = "1;32m"
    warning_color = "1;33m"
    error_color = "1;31m"

class Logger():
    pref = "\033["
    reset = f"{pref}0m"
    def success(self, text):
        print(f'{self.pref}{LevelStyles.success_color}' + text + self.reset)

    def info(self, text):
        print(f'{self.pref}{LevelStyles.info_color}' + text + self.reset)
    
    def warning(self, text):
        print(f'{self.pref}{LevelStyles.warning_color}' + text + self.reset)
    
    def error(self, text):
        print(f'{self.pref}{LevelStyles.error_color}' + text + self.reset)

if __name__ == "__main__":
    logger = Logger()
    logger.success("Success Test")
    logger.info("Info Test")
    logger.warning("Warning Test")
    logger.error('Error Test')
    print("Reset test")
