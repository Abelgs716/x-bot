"""python add.py "texto del tweet" """
import sys
from common import load_queue, save_queue
q = load_queue(); q.append(" ".join(sys.argv[1:])); save_queue(q)
print(f"En cola: {len(q)}")
