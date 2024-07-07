import matplotlib.pyplot as plt
import matplotlib
from pix2text import Pix2Text
import os

def handwritten2tex(img_fp):
    p2t = Pix2Text.from_config()
    outs = p2t.recognize_formula(img_fp)
    return outs

def tex2img(tex):
    matplotlib.rcParams['mathtext.fontset'] = 'cm'
    matplotlib.rcParams['font.family'] = 'STIXGeneral'

    fig, ax = plt.subplots(figsize=(8, 2))  # サイズを調整
    equation = "$" + tex + "$"
    ax.text(0.5, 0.5, equation, fontsize=20, ha='center', va='center')
    ax.axis('off')
    plt.tight_layout()

    if not os.path.exists("output"):
        os.makedirs("output")
    plt.savefig("output/output.png", dpi=150, bbox_inches='tight')  # DPIとマージンを調整
    plt.close(fig)