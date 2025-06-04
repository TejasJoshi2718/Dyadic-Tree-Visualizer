from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox, QScrollArea
)
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
from PyQt5.QtCore import Qt
from fractions import Fraction
import sys


class TreeNode:
    def __init__(self, word, value, depth):
        self.word = word
        self.value = value
        self.depth = depth
        self.left = None
        self.right = None


def build_tree(node, max_depth):
    if node.depth >= max_depth:
        return
    wp, vp = node.word + 'p', (1 + node.value) / 2
    wq, vq = node.word + 'q', (1 - node.value) / 2
    node.left = TreeNode(wp, vp, node.depth + 1)
    node.right = TreeNode(wq, vq, node.depth + 1)
    build_tree(node.left, max_depth)
    build_tree(node.right, max_depth)


def find_bsf_word(target, c=Fraction(1, 2), word="", depth=0, max_depth=10):
    if depth > max_depth:
        return None
    if c == target:
        return word
    p_result = find_bsf_word(target, (1 + c) / 2, word + "p", depth + 1, max_depth)
    if p_result:
        return p_result
    q_result = find_bsf_word(target, (1 - c) / 2, word + "q", depth + 1, max_depth)
    if q_result:
        return q_result
    return None


#def stylize(label, overbar=False, underline=False):
    # Use combining diacritics for overbar (U+0305) and underline (U+0332)
#    result = label
#    if overbar:
#        result += '\u0305'  # overbar
#    if underline:
#        result += '\u0332'  # underline
#    return result
    
def stylize(label, overbar=False, underline=False):
    if overbar and underline:
        return f"<b>{label}</b>"  # bold for both bars
    return label  # normal for only overbar or plain



def generate_rope_sequence(word):
    sequence = ["{" + "<b>1</b>" + "}"]
    rope_id = 2

    for op in word:
        prev = sequence[-1]

        # Step 1a: insert new '|' before closing '}'
        close_idx = prev.rfind("}")
        new_seq = prev[:close_idx] + "|" + prev[close_idx:]

        # Step 1b: insert rope_id before every '|' inside {...}
        open_idx = new_seq.find("{")
        close_idx = new_seq.rfind("}")
        inside = new_seq[open_idx + 1:close_idx]

        # Now carefully insert rope_id before each '|'
        updated_inside = ""
        i = 0
        while i < len(inside):
            if inside[i] == "|":
                updated_inside += str(rope_id) + "|"
                i += 1
            else:
                updated_inside += inside[i]
                i += 1

        # Step 1c: insert rope_id in bold just before closing }
        updated_inside += f"<b>{rope_id}</b>"

        # Rebuild new sequence
        new_seq = new_seq[:open_idx + 1] + updated_inside + new_seq[close_idx:]

        # Step 2d: for 'q' swap LAST '|' and '{'
        if op == 'q':
            brace_index = new_seq.find("{")
            last_pipe_index = new_seq.rfind("|")
            if last_pipe_index != -1 and brace_index != -1:
                new_seq_list = list(new_seq)
                new_seq_list[brace_index], new_seq_list[last_pipe_index] = new_seq_list[last_pipe_index], new_seq_list[brace_index]
                new_seq = ''.join(new_seq_list)

        sequence.append(new_seq)
        rope_id += 1

    return sequence[-1]




class TreeCanvas(QWidget):
    def __init__(self, root, max_depth, highlight_value=None):
        super().__init__()
        self.root = root
        self.max_depth = max_depth
        self.highlight_value = highlight_value
        self.setMinimumSize(1600, 900)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        font = QFont("Courier", 10)
        painter.setFont(font)

        def draw_node(node, x, y, depth):
            if not node:
                return

            dx = 250 // (2 ** depth) + 50
            dy = 120

            if self.highlight_value == node.value:
                pen = QPen(QColor("red"), 2)
                painter.setPen(pen)
                painter.drawEllipse(x - 30, y - 10, 60, 40)

            painter.setPen(QPen(Qt.black))
            text = f"{node.word or 'ROOT'}\n{node.value}"
            painter.drawText(x - 30, y, 60, 40, Qt.AlignCenter, text)

            if node.left:
                painter.drawLine(x, y + 30, x - dx, y + dy)
                draw_node(node.left, x - dx, y + dy, depth + 1)
            if node.right:
                painter.drawLine(x, y + 30, x + dx, y + dy)
                draw_node(node.right, x + dx, y + dy, depth + 1)

        draw_node(self.root, self.width() // 2, 40, 0)
        painter.end()


class TreeVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dyadic Fraction Tree")
        self.resize(1200, 1050)
        self.layout = QVBoxLayout(self)

        self.num_input = QLineEdit()
        self.num_input.setPlaceholderText("Numerator")
        self.den_input = QLineEdit()
        self.den_input.setPlaceholderText("Denominator")
        self.button = QPushButton("Build Tree")
        self.button.clicked.connect(self.build_tree)

        top = QHBoxLayout()
        top.addWidget(self.num_input)
        top.addWidget(self.den_input)
        top.addWidget(self.button)
        self.layout.addLayout(top)

        self.scroll = QScrollArea()
        self.layout.addWidget(self.scroll)

        # Word display
        self.word_label = QLabel("")
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.layout.addWidget(self.word_label)

        # Sequence display
        self.sequence_label = QLabel("")
        self.sequence_label.setAlignment(Qt.AlignCenter)
        self.sequence_label.setFont(QFont("Courier", 16))
        self.sequence_label.setWordWrap(True)
        self.layout.addWidget(self.sequence_label)

    def build_tree(self):
        try:
            num = int(self.num_input.text())
            den = int(self.den_input.text())
            f = Fraction(num, den)
        except:
            QMessageBox.warning(self, "Invalid", "Enter valid integers.")
            return

        if not self.is_dyadic(den):
            QMessageBox.warning(self, "Not Dyadic", "Denominator must be a power of 2.")
            return

        max_depth = den.bit_length() - 1
        word = find_bsf_word(f, max_depth=max_depth)
        if word is None:
            QMessageBox.warning(self, "Not Found", "Could not derive BSF word.")
            return

        sequence = generate_rope_sequence(word)

        self.word_label.setText(f"BSF Word: {word}")
        #self.sequence_label.setText(f"Rope Sequence: {sequence}")
        self.sequence_label.setText(f"Rope Sequence: {sequence}")
        self.sequence_label.setTextFormat(Qt.RichText)

        root = TreeNode("", Fraction(1, 2), 0)
        build_tree(root, max_depth)
        canvas = TreeCanvas(root, max_depth, highlight_value=f)
        self.scroll.setWidget(canvas)
        self.scroll.setWidgetResizable(True)

    def is_dyadic(self, den):
        return den > 0 and (den & (den - 1)) == 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TreeVisualizer()
    w.show()
    sys.exit(app.exec_())

