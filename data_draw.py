import matplotlib.pyplot as plt
import os
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

from wusn.commons import WusnOutput, WusnInput

if __name__ == '__main__':
    history = InMemoryHistory()
    plt.ioff()

    print('Enter a path to an input/output file to view its plot.')
    print('Ctrl+C or Ctrl+D to exit.')

    try:
        while True:
            path = prompt('> ', history=history)
            print(path)
            if not os.path.exists(path):
                print('No such path exists.')
                continue

            try:
                if path.endswith('.test'):
                    obj = WusnInput.from_file(path, True)
                else:
                    obj = WusnOutput.from_text_file(path)
            except Exception:
                print('Failed')
                continue

            anchors = obj.anchors
            x_anchors = [p.x for p in anchors]
            y_anchors = [p.y for p in anchors]
            l = plt.plot(x_anchors, y_anchors, 'go')

            non_anchors = obj.non_anchors
            x_non_anchors = [p.x for p in non_anchors]
            y_non_anchors = [p.y for p in non_anchors]
            k = plt.plot(x_non_anchors, y_non_anchors, 'go')

            plt.setp(l, markersize=5)
            plt.setp(l, markerfacecolor='C1')
            plt.setp(k, markersize=5)
            plt.setp(k, markerfacecolor='C2')
            plt.show()

    except (KeyboardInterrupt, EOFError):
        print()
