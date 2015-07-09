from subprocess import check_output, call
import sys
import math
import time

DELAY = 0.05

parameter = sys.argv[1]

recipes = {
           'kg16':  '(((((2b+b)+b)+b)+(((y+r)+b)+b))+(((2y+y)+(y+b))+2b))',
           'kg32':  '(((((((2b+b)+b)+b)+(2b+b))+(2b+b))+((((r+b)+y)+b)+(2b+b)))+(((((2y+y)+y)+(y+b))+((y+b)+b))+(((y+b)+b)+2b)))',
           'kg64':  '(((((((((2b+b)+b)+b)+2b)+(2b+b))+((2b+b)+b))+((((2b+b)+b)+b)+((y+b)+b)))+((((2b+b)+b)+((y+b)+b))+((((y+r)+b)+b)+(2y+b))))+(((((((2y+y)+y)+y)+2y)+(2y+(y+b)))+((2y+b)+2b))+((((2b+b)+b)+((y+b)+b))+((2y+b)+2b))))',
           'kg128': '(((((((((((2b+b)+b)+b)+2b)+(2b+b))+((2b+b)+b))+((((2b+b)+b)+b)+2b))+((((2b+b)+b)+2b)+(2b+b)))+(((((2b+b)+b)+2b)+(2b+b))+(((y+b)+b)+2b)))+(((((((2b+b)+b)+b)+2b)+(2b+b))+(((y+b)+b)+2b))+((((2y+y)+(y+b))+((y+b)+b))+((y+b)+2b))))+((((((((((2y+y)+y)+y)+y)+2y)+(2y+y))+((2y+y)+(y+r)))+(((2y+y)+(y+b))+((y+b)+b)))+((((2y+y)+(y+b))+((y+b)+b))+((y+b)+2b)))+((((((2b+b)+b)+b)+2b)+((y+b)+2b))+((((2y+y)+y)+(y+b))+((y+b)+2b)))))',
           'mg16':  '(((((2o+o)+o)+(o+b))+(((o+r)+b)+b))+((2b+b)+((o+b)+b)))',
           'mg32':  '(((((((((2o+o)+o)+o)+o)+o)+2o)+(((o+r)+2o)+b))+((2o+b)+2b))+(((((2b+b)+b)+b)+2b)+(((2o+o)+b)+2b)))',
           'mg64':  '((((((((((((2o+o)+o)+o)+o)+o)+2o)+2o)+(2o+o))+(((2o+o)+o)+((o+r)+b)))+(((2o+o)+(o+b))+b))+(((((2o+o)+o)+(o+b))+b)+(((o+b)+b)+2b)))+(((((((2b+b)+b)+b)+b)+2b)+(((o+b)+b)+2b))+(((((2o+o)+o)+(o+b))+b)+(((o+b)+b)+2b))))',
           'mg128': '((((((((((((((2o+o)+o)+o)+o)+o)+2o)+2o)+(2o+o))+((2o+o)+o))+(((2o+o)+o)+o))+(((((2o+o)+o)+o)+2o)+(o+b)))+((((((2o+o)+o)+o)+o)+(2o+b))+((((o+r)+2o)+b)+b)))+(((((((2o+o)+o)+o)+2o)+(o+b))+((2o+b)+2b))+((((2b+b)+b)+2b)+((2o+b)+2b))))+((((((((((2b+b)+b)+b)+b)+b)+(2b+b))+(2b+b))+(((2b+b)+b)+2b))+((((2b+b)+b)+2b)+((2o+b)+2b)))+((((((((2o+o)+o)+o)+o)+o)+(2o+b))+((2o+b)+2b))+((((2b+b)+b)+2b)+((2o+b)+2b)))))',
           'mga16': '2o',
           'mga32': '(((2o+o)+o)+2o)',
           'mga64': '(((((2o+o)+o)+o)+o)+2o)',
           'mga128': '((((((((2o+o)+o)+o)+o)+o)+2o)+2o)+((2o+o)+2o))',
           }

if not parameter:
  print("please provide a parameter for recipe")
  sys.exit()

if parameter in recipes:
  parameter = recipes[parameter]
  

print("comb my gems")

def main():
  tree = parse(parameter)
  fields = [None] * 36
  operations = []
  tree.compute(fields, operations)
  play(operations)


def play(operations):
  
  screen = Screen()
  for op in operations:
    op.execute(screen)
  

class Screen():

  
  def __init__(self):
    coords = str(check_output(['xdotool', 'getmouselocation'])).split(" ")
    self.indexZero = (int(coords[0].split(":")[1]), int(coords[1].split(":")[1]))
    self.gemTypes = (self.indexZero[0] - 60, self.indexZero[1] + 40)
    
  def moveType(self, pos):
    x = self.gemTypes[0] + (pos % 3) * 33
    y = self.gemTypes[1] + math.floor(pos / 3) * 33
    call(['xdotool', 'mousemove', str(x), str(y)])
    time.sleep(DELAY)
    
  def moveField(self, pos):
    x = self.indexZero[0] - (pos % 3) * 28
    y = self.indexZero[1] - math.floor(pos / 3) * 28
    call(['xdotool', 'mousemove', str(x), str(y)])
    time.sleep(DELAY)
    
  def click(self):
    call(['xdotool', 'click', '1'])
    time.sleep(DELAY)
    
  def down(self):
    call(['xdotool', 'mousedown', '1'])
    time.sleep(DELAY)
    
  def up(self):
    call(['xdotool', 'mouseup', '1'])
    time.sleep(DELAY)
    
  def type(self, letter):
    call(['xdotool', 'type', letter])
    time.sleep(DELAY)
    
def parse(code):
  braketCount = 0
  
  for index in range(0, len(code)):
    char = code[index]
    if char == '(':
      braketCount += 1
    elif char == ')':
      braketCount -= 1
    elif char == '+':
      if braketCount == 1:
        return Op(parse(code[1:index]), parse(code[index+1:-1]))
  return Gem(code)

class Op():
  def __init__(self, left, right):
    self.left = left
    self.right = right
    
  def compute(self, fields, operations):
    gem1 = self.left.compute(fields, operations)
    gem2 = self.right.compute(fields, operations)
    operations.append(Combine(gem1, gem2))
    fields[gem1] = None
    return gem2
    
  def __str__(self):
    return "[%s + %s]" % (self.left, self.right)

class Gem():
  def __init__(self, code):
    self.grade = 1
    if len(code) > 1:
      self.grade = int(code[:-1])
    self.code = code[-1]
    
  def compute(self, fields, operations):
    emptyIndex = fields.index(None)
    operations.append(Create(self, emptyIndex))
    fields[emptyIndex] = True
    return emptyIndex
    
    
  def __str__(self):
    return "%s%s" % (self.grade, self.code)


gemTypes = {'o': 0, 'y': 1, 'b': 6, 'r': 3}
  

class Create():
  def __init__(self, gem, target):
    self.gem = gem
    self.target = target
    
  def execute(self, screen):
    screen.moveType(gemTypes[self.gem.code])
    screen.click()
    screen.moveField(self.target)
    screen.click()
    if self.gem.grade > 1:
      for i in range(1, self.gem.grade):
        screen.type('u')
    
    
  def __str__(self):
    return "create(%s)" % (self.gem, )
  
class Combine():
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def execute(self, screen):
    screen.type('g')
    screen.moveField(self.left)
    screen.down()
    screen.moveField(self.right)
    screen.up()

  def __str__(self):
    return "combine(%s, %s)" % (self.left, self.right)
  
main()  
  
