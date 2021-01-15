import configparser

def writeToFile(botData):
  config = configparser.ConfigParser()
  config.read('config.ini')
  config['DEFAULT']['guild_id'] = str(botData[0])
  config['DEFAULT']['rolelist'] = str(botData[1])
  with open('config.ini', 'w') as configfile:
    config.write(configfile)

def readFromFile():
  config = configparser.ConfigParser()
  config.read('config.ini')
  return [config['DEFAULT']['guild_id'], config['DEFAULT']['rolelist']]
