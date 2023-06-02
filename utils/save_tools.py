SAVE_DIR = "./images"

def save_html(fig, filename):
    fig.write_html(f'{SAVE_DIR}/{filename}.html')