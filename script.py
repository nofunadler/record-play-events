import sys
from time import sleep
import keyboard
import colorama

class State:
  def __init__(self) -> None:
    self.begin = False
    self.terminate = False
    
  def stop(self) -> None:
    self.terminate = True
    
  def start(self) -> None:
    self.begin = True
    

def setup(*args) -> None:
  (state,) = args
  state.start()
  

def cleanup(*args) -> None:
  (state,) = args
  state.stop()

def main(start: str='page up', end: str='page down') -> None:
  colorama.just_fix_windows_console()
  
  state: State = State()
  
  keyboard.add_hotkey('escape', cleanup, args=(state,))
  
  keyboard.add_hotkey(start, setup, args=(state,))
  
  print(f"{colorama.Fore.GREEN}press {colorama.Fore.RED}{start}{colorama.Fore.GREEN} to start recording\n" 
        f"press {colorama.Fore.RED}{end}{colorama.Fore.GREEN} when you're done\n"
        f"ESC to terminate the program{colorama.Style.RESET_ALL}\n"
      )
  
  while not state.begin:
    if state.terminate:
      return
  
  print(f"{colorama.Fore.GREEN}start recording{colorama.Style.RESET_ALL}")
  keyboard_events = keyboard.record(until=end)
  
  print("starting sequence in:  ", end='')
  for i in range(5, 0, -1):
    print(f"\033[D{colorama.Fore.RED}{i}{colorama.Style.RESET_ALL}", end='', flush=True)
    sleep(1)
  
  print(f"\033[G{colorama.Fore.GREEN}running keyboard events sequence...{colorama.Style.RESET_ALL}")
  while not state.terminate:
    keyboard.play(keyboard_events)
    
    
if __name__ == '__main__':
  argv = sys.argv
  
  if len(argv) == 3:
    main(*argv[1:])
  else:
    main()