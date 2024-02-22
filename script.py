import sys
from threading import Lock
from time import sleep
import keyboard
import colorama  

class State:
  def __init__(self) -> None:
    self.terminate = False
    self.begin = False
    self.terminate_lock = Lock()
    self.begin_lock = Lock()
    
  def stop(self) -> None:
    with self.terminate_lock:
      self.terminate = True
    
  def start(self) -> None:
    with self.begin_lock:
      self.begin = True


def cleanup(*args) -> None:
  (state,) = args
  state.stop()
  
  
def begin(*args) -> None:
  (state,) = args
  state.start()
  

def get_key_events(state: State, key_mapping: tuple[str], hook_begin_handler, /) -> list[keyboard.KeyboardEvent]:
  (start, end) = key_mapping
  
  print(f"{colorama.Fore.GREEN}press {colorama.Fore.RED}{start}{colorama.Fore.GREEN} to start recording\n" 
      f"press {colorama.Fore.RED}{end}{colorama.Fore.GREEN} when you're done\n"
      f"{colorama.Fore.RED}ESC{colorama.Fore.GREEN} to quit{colorama.Style.RESET_ALL}\n"
    )
  
  while not state.begin:
    if state.terminate:
      return []
    
  keyboard.remove_hotkey(hook_begin_handler)
  
  print(f"{colorama.Fore.GREEN}start recording{colorama.Style.RESET_ALL}")
  keyboard_events = keyboard.record(until=end, suppress=True)
  
  print("starting sequence in:  ", end='')
  for i in range(5, 0, -1):
    print(f"\033[D{colorama.Fore.RED}{i}{colorama.Style.RESET_ALL}", end='', flush=True)
    sleep(1)
  
  print(f"\033[G{colorama.Fore.GREEN}running keyboard events sequence...{colorama.Style.RESET_ALL}")
  return keyboard_events


def play_events(start: str='page up', end: str='page down') -> None:
  colorama.just_fix_windows_console()
  
  state: State = State()
  
  hook_begin = keyboard.add_hotkey(start, begin, args=(state,), suppress=True)
  keyboard.add_hotkey('escape', cleanup, args=(state,), suppress=True)
  
  try:
    keyboard_events = get_key_events(state, (start, end), hook_begin)
    
    if not keyboard_events:
      return
    
    # main event loop
    while not state.terminate:
      keyboard.play(keyboard_events)
  except KeyboardInterrupt:
    pass
    
    
def main(argv: list[str]) -> None:
  colorama.just_fix_windows_console()
  
  if 'ctrl+c' in argv:
    print(f"{colorama.Fore.RED}the use of the ctrl+c combination is reserved for emergency exit{colorama.Style.RESET_ALL}\n")
    return
  
  if len(argv) == 3:
    play_events(*argv[1:])
  else:
    play_events()
      

if __name__ == '__main__':
  argv = sys.argv
  main(argv)