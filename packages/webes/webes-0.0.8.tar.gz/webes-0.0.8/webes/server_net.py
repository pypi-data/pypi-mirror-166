
# Importing modules


from colorama import Fore, Back, Style
from termcolor import colored
from flask import Flask, render_template
from wincom import *
import os

def server(mode=None):
      global app

      if mode == None:

            try:
                  app = Flask(__name__)
            except ConnectionAbortedError:
                  print('Error internet connection.')
            except ConnectionError:
                  print('Error internet connection')
      elif mode == 'close' or mode == 'stop':

            print(app.run())

            if __name__ == '__main__':
                  app.run()

def getcmd(command):
      return command


def gettemp(template):
      return render_template(template)


def getcss(name):
      if not os.path.exists('static'):
            folder('static')
            folder('static/css')
            file('static/css/'+str(name)+'.css')

      elif not os.path.exists('static/css'):
            folder('static/css')
            file('static/css/'+str(name)+'.css')
      
      elif not os.path.exists('static/css/'+str(name)+'.css'):
            file('static/css/'+str(name)+'.css')

      write(text='/* Created CSS file */', file=f'static/css/{name}.css')




def gethtml(name):
      if not os.path.exists('templates'):
            folder('templates')
            file(f'templates/{name}.html')


      write(text=f'''<!DOCTYPE html>
<html>
<head>
      <meta charset='UTF-8'>
      <link rel='stylesheet' href='../static/css/.css'>
      <title></title>
</head>
<body>

</body>
</html>
      ''', file=f'templates/{name}.html')



      


