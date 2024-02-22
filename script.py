import sys
from threading import Lock
from time import sleep
import keyboard
import colorama  

class State:
  def __init__(self) -> None:
    self._terminate = False
    self._begin = False
    self._terminate_lock = Lock()
    self._begin_lock = Lock()
    
  def stop(self) -> None:
    with self._terminate_lock:
      self._terminate = True
    
  def start(self) -> None:
    with self._begin_lock:
      self._begin = True
      
  def should_start(self) -> bool:
    should_begin = False
    with self._begin_lock:
      should_begin = self._begin
    
    return should_begin
  
  
  def should_stop(self) -> bool:
    should_terminate = False
    with self._terminate_lock:
      should_terminate = self._terminate
      
    return should_terminate
  

def play(state: State, events: list[keyboard.KeyboardEvent], speed_factor: float = 1.0, /) -> None:
    """
    slightly modified play function to enable breaking the play of events mid sequence
    """
    keyboard_state = keyboard.stash_state()

    last_time = None
    for event in events:
        if speed_factor > 0 and last_time is not None:
            sleep((event.time - last_time) / speed_factor)
        last_time = event.time

        key = event.scan_code or event.name
        
        if state.should_stop():
          break
        
        keyboard.press(key) if event.event_type == keyboard.KEY_DOWN else keyboard.release(key)

    keyboard.restore_modifiers(keyboard_state)
    

def get_key_events(state: State, key_mapping: tuple[str], hook_begin_handler, /) -> list[keyboard.KeyboardEvent]:
  (start, end) = key_mapping
  
  print(f"{colorama.Fore.GREEN}press {colorama.Fore.RED}{start}{colorama.Fore.GREEN} to start recording\n" 
      f"press {colorama.Fore.RED}{end}{colorama.Fore.GREEN} when you're done\n"
      f"{colorama.Fore.RED}ESC{colorama.Fore.GREEN} to quit{colorama.Style.RESET_ALL}\n"
    )
  
  while not state.should_start():
    if state.should_stop():
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
  
  hook_begin = keyboard.add_hotkey(start, lambda: state.start(), suppress=True)
  keyboard.add_hotkey('escape', lambda: state.stop(), suppress=True)
  
  try:
    keyboard_events = get_key_events(state, (start, end), hook_begin)
    if not keyboard_events:
      return
    
    # main event loop
    while not state.should_stop():
      play(state, keyboard_events)
  except KeyboardInterrupt:
    return
    
    
def main(argv: list[str]) -> None:
  colorama.just_fix_windows_console()
  
  reserved_combo = {'ctrl+c', 'ctrl+z', 'esc'} & {arg.strip().lower() for arg in argv}
  if reserved_combo:
    print(f"{colorama.Fore.RED}the use of the {reserved_combo} combination is reserved for emergency exit{colorama.Style.RESET_ALL}\n")
    return
  
  if len(argv) == 3:
    play_events(*argv[1:])
  else:
    play_events()
      

if __name__ == '__main__':
  argv = sys.argv
  main(argv)