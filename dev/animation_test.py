import time

loading_animation = '''
     ________________        Excel File       ________________
    |                |    ---------------->  |                |
    |    Computer    |                       |     FastAPI    |
    |                |                       |                |
    |     _______    |                       |     _______    |
    |    |_______|   |                       |    |_______|   |
    |________________|                       |________________|
'''
def animate_print(text, delay=1):
    while True:
        if '-' in text:
            text  = text.replace('-', '=', 1)
        else: 
            text = text.replace('=', '-', 1)

            
        print(text, end='', flush=True)  # Print the character without newline
        time.sleep(delay)  # Add a delay between characters

# Example usage
animate_print(loading_animation)