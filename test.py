from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

# 1. Keep the completer so 'Tab' still suggests these, but they aren't mandatory
status_completer = WordCompleter(['active', 'down'], ignore_case=True)

def test_user_input():
    # 2. Create a history object to remember past inputs
    session_history = InMemoryHistory()
    
    print("Welcome! Type anything. Press 'Up' arrow for history. Type 'exit' to quit.")
    
    # 3. Use a loop so you can enter multiple lines and test the history
    while True:
        user_input = prompt(
            "active / down > ", 
            completer=status_completer,
            history=session_history # This enables the Up/Down arrow history
        )
        
        # Provide a way to cleanly exit the loop
        if user_input.strip().lower() == 'exit':
            print("Goodbye!")
            break
            
        print(f"You entered: {user_input}")

if __name__ == "__main__":
    test_user_input()