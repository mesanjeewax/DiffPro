# Author: Sanjeewa.R
# Tool Name: IntelliSan DiffPro
# IntelliSan Software Solutions
import sys
import os
import re
import difflib
from collections import Counter, defaultdict
from PyQt5.QtGui import QColor, QIcon, QFont, QPainter, QTextFormat, QTextDocument
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QFileDialog, QLabel, QGraphicsDropShadowEffect, QFontDialog, QMessageBox,
                             QPlainTextEdit, QScrollBar, QSizePolicy, QInputDialog, QProgressDialog, QSplitter)
from PyQt5.QtCore import Qt, QRect, QSize, QThread, pyqtSignal

def create_icon():
    icon_data = base64.b64decode(
        "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"
    )
    pixmap = QPixmap()
    pixmap.loadFromData(icon_data)
    return QIcon(pixmap)


# Simple tokenizer function
def simple_tokenize(text):
    return [word.lower() for word in re.findall(r'\b\w+\b', text) if word.strip()]

# Simple stop words list
STOP_WORDS = set(['the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'of', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might', 'must', 'ought', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their', 'this', 'that', 'these', 'those'])

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)
        self.highlight_current_line()
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.file_path = None

    def load_file(self, file_path):
        self.file_path = file_path
        self.clear()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.setPlainText(file.read())
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            self.setPlainText(f"Error loading file: {str(e)}")

    
    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#2b2b2b"))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#999999"))
                painter.drawText(0, int(top), self.line_number_area.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#3a3a3a")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def paintEvent(self, event):
        super().paintEvent(event)

class FilePane(QWidget):
    def __init__(self, parent=None, pane_id=1):
        super().__init__(parent)
        self.pane_id = pane_id
        self.current_file = None
        self.init_ui()
    
    def init_ui(self):
            layout = QVBoxLayout(self)
                
            top_layout = QVBoxLayout()
            self.file_label = QLabel(f"File {self.pane_id}: No file selected")
            top_layout.addWidget(self.file_label)

            button_layout = QHBoxLayout()
            self.browse_button = QPushButton("Browse")
            self.browse_button.clicked.connect(self.browse_file)
            self.font_button = QPushButton("Change Font")
            self.font_button.clicked.connect(self.change_font)
            self.save_button = QPushButton("Save")
            self.save_button.clicked.connect(self.save_file)
            self.save_button.setEnabled(False)
            self.refresh_button = QPushButton("Refresh")
            self.refresh_button.clicked.connect(self.refresh_file)
            button_layout.addWidget(self.browse_button)
            button_layout.addWidget(self.font_button)
            button_layout.addWidget(self.save_button)
            button_layout.addWidget(self.refresh_button)
            top_layout.addLayout(button_layout)

            layout.addLayout(top_layout)

            # Text editor
            self.text_edit = CodeEditor(self)
            self.text_edit.setAcceptDrops(False)
            self.text_edit.setPlaceholderText(f"Drag and drop file {self.pane_id} here or use Browse button")
            self.text_edit.textChanged.connect(self.enable_save_button)
            layout.addWidget(self.text_edit)

            self.setAcceptDrops(True)
            self.setAcceptDrops(True)
                
    def refresh_file(self):
        if self.current_file:
            self.load_file(self.current_file)
        else:
            QMessageBox.warning(self, "Warning", "No file loaded to refresh.")    

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, f"Select File {self.pane_id}", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        try:
            self.text_edit.load_file(file_path)
            self.file_label.setText(f"File {self.pane_id}: {file_path}")
            self.current_file = file_path
            self.save_button.setEnabled(False)
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            self.text_edit.setPlainText(f"Error loading file: {str(e)}")

    def change_font(self):
        current_font = self.text_edit.font()
        font, ok = QFontDialog.getFont(current_font, self)
        if ok:
            self.text_edit.setFont(font)

    def enable_save_button(self):
        self.save_button.setEnabled(True)

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.text_edit.toPlainText())
                self.save_button.setEnabled(False)
                QMessageBox.information(self, "Save Successful", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Error saving file: {str(e)}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.current_file = file_path
            self.save_file()
            self.file_label.setText(f"File {self.pane_id}: {file_path}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.load_file(files[0])
        event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

def myers_diff(a, b):
    def backtrack(V, D, k, x, y):
        if D == 0:
            return []
        if k == -D or (k != D and V[k - 1] < V[k + 1]):
            k = k + 1
            prev_x, prev_y = V[k] - 1, V[k] - k
        else:
            k = k - 1
            prev_x, prev_y = V[k], V[k] - k
        snake = backtrack(V, D - 1, k, prev_x, prev_y)
        while x < len(a) and y < len(b) and a[x] == b[y]:
            snake.append(('  ', a[x]))
            x, y = x + 1, y + 1
        if x > prev_x:
            snake.append(('- ', a[prev_x]))
        elif y > prev_y:
            snake.append(('+ ', b[prev_y]))
        return snake

    N, M = len(a), len(b)
    V = {1: 0}
    for D in range(N + M + 1):
        for k in range(-D, D + 1, 2):
            if k == -D or (k != D and V[k - 1] < V[k + 1]):
                x = V[k + 1]
            else:
                x = V[k - 1] + 1
            y = x - k
            while x < N and y < M and a[x] == b[y]:
                x, y = x + 1, y + 1
            V[k] = x
            if x >= N and y >= M:
                return backtrack(V, D, k, x, y)
    return []

def optimized_word_count(text):
    word_count = defaultdict(int)
    for word in re.findall(r'\b\w+\b', text.lower()):
        if word not in STOP_WORDS:
            word_count[word] += 1
    return word_count

class SummaryWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text1, text2):
        super().__init__()
        self.text1 = text1
        self.text2 = text2

    def run(self):
        try:
            summary = self.generate_summary()
            self.finished.emit(summary)
        except Exception as e:
            self.error.emit(str(e))

    def generate_summary(self):
        count1 = optimized_word_count(self.text1)
        count2 = optimized_word_count(self.text2)

        unique1 = set(count1.keys()) - set(count2.keys())
        unique2 = set(count2.keys()) - set(count1.keys())

        changed_words = []
        for word in set(count1.keys()) & set(count2.keys()):
            if count1[word] != count2[word]:
                changed_words.append((word, count1[word], count2[word]))

        summary = "Intelligent Summary:\n\n"
        summary += f"Total words in File 1: {sum(count1.values())}\n"
        summary += f"Total words in File 2: {sum(count2.values())}\n\n"
        summary += f"File 1 has {len(unique1)} unique words"
        if unique1:
            summary += f", including: {', '.join(sorted(unique1)[:5])}"
        summary += "\n"
        summary += f"File 2 has {len(unique2)} unique words"
        if unique2:
            summary += f", including: {', '.join(sorted(unique2)[:5])}"
        summary += "\n\n"
        
        if changed_words:
            summary += f"Top {min(5, len(changed_words))} words with frequency changes:\n"
            for word, freq1, freq2 in sorted(changed_words, key=lambda x: abs(x[1]-x[2]), reverse=True)[:5]:
                summary += f"'{word}': {freq1} -> {freq2}\n"
        else:
            summary += "No words with frequency changes found.\n"

        all_words = set(count1.keys()) | set(count2.keys())
        if all_words:
            common_words = set(count1.keys()) & set(count2.keys())
            similarity = len(common_words) / len(all_words)
            summary += f"\nSimilarity between files: {similarity:.2%}\n"
        else:
            summary += "\nBoth files are empty or contain only stop words.\n"

        most_common1 = sorted(count1.items(), key=lambda x: x[1], reverse=True)[:5]
        most_common2 = sorted(count2.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary += "\nMost common words:\n"
        summary += f"File 1: {', '.join([f'{word} ({count})' for word, count in most_common1])}\n"
        summary += f"File 2: {', '.join([f'{word} ({count})' for word, count in most_common2])}\n"

        return summary

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QFileDialog, QLabel, QGraphicsDropShadowEffect, QFontDialog, QMessageBox,
                             QPlainTextEdit, QScrollBar, QSizePolicy, QInputDialog, QProgressDialog, QSplitter)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import difflib
import os
import re
from collections import defaultdict

class SummaryWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text1, text2):
        super().__init__()
        self.text1 = text1
        self.text2 = text2

    def run(self):
        try:
            summary = self.generate_summary()
            self.finished.emit(summary)
        except Exception as e:
            self.error.emit(str(e))

    def generate_summary(self):
        count1 = optimized_word_count(self.text1)
        count2 = optimized_word_count(self.text2)

        unique1 = set(count1.keys()) - set(count2.keys())
        unique2 = set(count2.keys()) - set(count1.keys())

        changed_words = []
        for word in set(count1.keys()) & set(count2.keys()):
            if count1[word] != count2[word]:
                changed_words.append((word, count1[word], count2[word]))

        summary = "Intelligent Summary:\n\n"
        summary += f"Total words in File 1: {sum(count1.values())}\n"
        summary += f"Total words in File 2: {sum(count2.values())}\n\n"
        summary += f"File 1 has {len(unique1)} unique words"
        if unique1:
            summary += f", including: {', '.join(sorted(unique1)[:5])}"
        summary += "\n"
        summary += f"File 2 has {len(unique2)} unique words"
        if unique2:
            summary += f", including: {', '.join(sorted(unique2)[:5])}"
        summary += "\n\n"
        
        if changed_words:
            summary += f"Top {min(5, len(changed_words))} words with frequency changes:\n"
            for word, freq1, freq2 in sorted(changed_words, key=lambda x: abs(x[1]-x[2]), reverse=True)[:5]:
                summary += f"'{word}': {freq1} -> {freq2}\n"
        else:
            summary += "No words with frequency changes found.\n"

        all_words = set(count1.keys()) | set(count2.keys())
        if all_words:
            common_words = set(count1.keys()) & set(count2.keys())
            similarity = len(common_words) / len(all_words)
            summary += f"\nSimilarity between files: {similarity:.2%}\n"
        else:
            summary += "\nBoth files are empty or contain only stop words.\n"

        most_common1 = sorted(count1.items(), key=lambda x: x[1], reverse=True)[:5]
        most_common2 = sorted(count2.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary += "\nMost common words:\n"
        summary += f"File 1: {', '.join([f'{word} ({count})' for word, count in most_common1])}\n"
        summary += f"File 2: {', '.join([f'{word} ({count})' for word, count in most_common2])}\n"

        return summary

class FileComparisonTool(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing FileComparisonTool")
        self.initUI()
        self.file1_path = None
        self.file2_path = None
        self.process_arguments()
        
    def process_arguments(self):
        args = sys.argv[1:]
        if len(args) == 1:
            # If one argument, set as File 1
            self.file1_path = args[0]
            self.file_pane1.load_file(self.file1_path)
        elif len(args) == 2:
            # If two arguments, set as File 1 and File 2, then compare
            self.file1_path = args[0]
            self.file2_path = args[1]
            self.file_pane1.load_file(self.file1_path)
            self.file_pane2.load_file(self.file2_path)
            self.compare_files()    


    def initUI(self):
        print("Setting up UI")
        self.setWindowTitle('DiffPro - Intelligent File Comparison Tool')
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('comparison_icon.png'))  # Ensure you have this icon file

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QLabel {
                font-weight: bold;
                color: #00a8e8;
            }
            QPlainTextEdit {
                background-color: #363636;
                color: #e0e0e0;
                border: 1px solid #4d4d4d;
                border-radius: 5px;
            }
            QSplitter::handle {
                background-color: #4d4d4d;
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #00a8e8;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create a QSplitter for the file panes
        self.splitter = QSplitter(Qt.Horizontal)
        self.file_pane1 = FilePane(pane_id=1)
        self.file_pane2 = FilePane(pane_id=2)
        self.splitter.addWidget(self.file_pane1)
        self.splitter.addWidget(self.file_pane2)
        
        # Set initial sizes
        self.splitter.setSizes([self.width() // 2, self.width() // 2])
        
        main_layout.addWidget(self.splitter)

        button_layout = QHBoxLayout()
        self.compare_button = self.create_button("Compare Files", "#00a8e8")
        self.compare_button.clicked.connect(self.compare_files)
        self.clear_button = self.create_button("Clear", "#ff6b6b")
        self.clear_button.clicked.connect(self.clear_all)
        self.export_button = self.create_button("Export Differences", "#4ecdc4")
        self.export_button.clicked.connect(self.export_results)
        self.summary_button = self.create_button("Intelligent Summary", "#ffa500")
        self.summary_button.clicked.connect(self.generate_summary)
        self.partition_button = self.create_button("Partition File", "#9b59b6")
        self.partition_button.clicked.connect(self.partition_file)
        
        button_layout.addWidget(self.compare_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.summary_button)
        button_layout.addWidget(self.partition_button)
        main_layout.addLayout(button_layout)
        print("UI setup complete")

    def create_button(self, text, color):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(color, 20)};
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        button.setGraphicsEffect(shadow)
        return button

    @staticmethod
    def adjust_color(color, amount):
        color = QColor(color)
        h, s, l, a = color.getHsl()
        return QColor.fromHsl(h, s, min(max(0, l + amount), 255), a).name()

    def compare_files(self):
        text1 = self.file_pane1.text_edit.toPlainText().splitlines()
        text2 = self.file_pane2.text_edit.toPlainText().splitlines()

        diff = list(difflib.ndiff(text1, text2))

        self.file_pane1.text_edit.clear()
        self.file_pane2.text_edit.clear()

        for line in diff:
            if line.startswith('  '):  # unchanged
                self.file_pane1.text_edit.appendPlainText(line[2:])
                self.file_pane2.text_edit.appendPlainText(line[2:])
            elif line.startswith('- '):  # removed
                self.file_pane1.text_edit.appendHtml(f'<span style="background-color: #ff6b6b; color: #2b2b2b;">{line[2:]}</span>')
            elif line.startswith('+ '):  # added
                self.file_pane2.text_edit.appendHtml(f'<span style="background-color: #4ecdc4; color: #2b2b2b;">{line[2:]}</span>')
            elif line.startswith('? '):  # intraline change
                continue  # skip these lines as they're just indicators

        # Ensure both panes have the same number of lines by adding empty lines
        line_count1 = self.file_pane1.text_edit.document().blockCount()
        line_count2 = self.file_pane2.text_edit.document().blockCount()
        max_lines = max(line_count1, line_count2)
        
        self.file_pane1.text_edit.appendPlainText('\n' * (max_lines - line_count1))
        self.file_pane2.text_edit.appendPlainText('\n' * (max_lines - line_count2))

    def clear_all(self):
        self.file_pane1.text_edit.clear()
        self.file_pane2.text_edit.clear()
        self.file_pane1.file_label.setText("File 1: No file selected")
        self.file_pane2.file_label.setText("File 2: No file selected")

    def export_results(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Differences", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                text1 = self.file_pane1.text_edit.toPlainText().splitlines()
                text2 = self.file_pane2.text_edit.toPlainText().splitlines()

                diff = list(difflib.ndiff(text1, text2))

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("File Differences:\n\n")
                    for line in diff:
                        if line.startswith('- '):
                            f.write(f"Removed: {line[2:]}\n")
                        elif line.startswith('+ '):
                            f.write(f"Added:   {line[2:]}\n")

                QMessageBox.information(self, "Export Successful", "Differences exported successfully.")
            except Exception as e:
                error_message = f"An error occurred while exporting: {str(e)}"
                print(error_message)
                QMessageBox.critical(self, "Export Error", error_message)

    def generate_summary(self):
        text1 = self.file_pane1.text_edit.toPlainText()
        text2 = self.file_pane2.text_edit.toPlainText()

        self.summary_worker = SummaryWorker(text1, text2)
        self.summary_worker.finished.connect(self.show_summary)
        self.summary_worker.error.connect(self.show_error)
        self.summary_worker.start()

    def show_summary(self, summary):
        QMessageBox.information(self, "Intelligent Summary", summary)

    def show_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)

    def partition_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Partition", "", "Text Files (*.txt);;All Files (*)")
        if not file_path:
            return

        file_size = os.path.getsize(file_path)
        num_parts, ok = QInputDialog.getInt(self, "Partition File", "Enter number of parts:", 2, 2, 10)
        if not ok:
            return

        chunk_size = file_size // num_parts
        output_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Save Partitions")
        if not output_dir:
            return

        progress_dialog = QProgressDialog("Partitioning file...", "Cancel", 0, num_parts, self)
        progress_dialog.setWindowModality(Qt.WindowModal)

        try:
            with open(file_path, 'rb') as file:
                for i in range(num_parts):
                    chunk = file.read(chunk_size)
                    output_path = os.path.join(output_dir, f"part_{i+1}.txt")
                    with open(output_path, 'wb') as out_file:
                        out_file.write(chunk)
                    progress_dialog.setValue(i + 1)
                    if progress_dialog.wasCanceled():
                        raise Exception("File partitioning canceled by user.")
                    QApplication.processEvents()

            QMessageBox.information(self, "Partition Complete", f"File has been partitioned into {num_parts} parts.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error partitioning file: {str(e)}")

    def create_button(self, text, color):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(color, 20)};
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        button.setGraphicsEffect(shadow)
        return button

    @staticmethod
    def adjust_color(color, amount):
        color = QColor(color)
        h, s, l, a = color.getHsl()
        return QColor.fromHsl(h, s, min(max(0, l + amount), 255), a).name()

    def compare_files(self):
        text1 = self.file_pane1.text_edit.toPlainText().splitlines()
        text2 = self.file_pane2.text_edit.toPlainText().splitlines()

        diff = list(difflib.ndiff(text1, text2))

        self.file_pane1.text_edit.clear()
        self.file_pane2.text_edit.clear()

        for line in diff:
            if line.startswith('  '):  # unchanged
                self.file_pane1.text_edit.appendPlainText(line[2:])
                self.file_pane2.text_edit.appendPlainText(line[2:])
            elif line.startswith('- '):  # removed
                self.file_pane1.text_edit.appendHtml(f'<span style="background-color: #ff6b6b; color: #2b2b2b;">{line[2:]}</span>')
            elif line.startswith('+ '):  # added
                self.file_pane2.text_edit.appendHtml(f'<span style="background-color: #4ecdc4; color: #2b2b2b;">{line[2:]}</span>')
            elif line.startswith('? '):  # intraline change
                continue  # skip these lines as they're just indicators

        # Ensure both panes have the same number of lines by adding empty lines
        line_count1 = self.file_pane1.text_edit.document().blockCount()
        line_count2 = self.file_pane2.text_edit.document().blockCount()
        max_lines = max(line_count1, line_count2)
        
        self.file_pane1.text_edit.appendPlainText('\n' * (max_lines - line_count1))
        self.file_pane2.text_edit.appendPlainText('\n' * (max_lines - line_count2))

    def clear_all(self):
        self.file_pane1.text_edit.clear()
        self.file_pane2.text_edit.clear()
        self.file_pane1.file_label.setText("File 1: No file selected")
        self.file_pane2.file_label.setText("File 2: No file selected")

    def export_results(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Differences", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                text1 = self.file_pane1.text_edit.toPlainText().splitlines()
                text2 = self.file_pane2.text_edit.toPlainText().splitlines()

                diff = myers_diff(text1, text2)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("File Differences:\n\n")
                    for op, line in diff:
                        if op == '- ':
                            f.write(f"Removed: {line}\n")
                        elif op == '+ ':
                            f.write(f"Added:   {line}\n")

                QMessageBox.information(self, "Export Successful", "Differences exported successfully.")
            except Exception as e:
                error_message = f"An error occurred while exporting: {str(e)}"
                print(error_message)
                QMessageBox.critical(self, "Export Error", error_message)

    def generate_summary(self):
        text1 = self.file_pane1.text_edit.toPlainText()
        text2 = self.file_pane2.text_edit.toPlainText()

        self.summary_worker = SummaryWorker(text1, text2)
        self.summary_worker.finished.connect(self.show_summary)
        self.summary_worker.error.connect(self.show_error)
        self.summary_worker.start()

    def show_summary(self, summary):
        QMessageBox.information(self, "Intelligent Summary", summary)

    def show_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)

    def partition_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Partition", "", "Text Files (*.txt);;All Files (*)")
        if not file_path:
            return

        file_size = os.path.getsize(file_path)
        num_parts, ok = QInputDialog.getInt(self, "Partition File", "Enter number of parts:", 2, 2, 10)
        if not ok:
            return

        chunk_size = file_size // num_parts
        output_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Save Partitions")
        if not output_dir:
            return

        progress_dialog = QProgressDialog("Partitioning file...", "Cancel", 0, num_parts, self)
        progress_dialog.setWindowModality(Qt.WindowModal)

        try:
            with open(file_path, 'rb') as file:
                for i in range(num_parts):
                    chunk = file.read(chunk_size)
                    output_path = os.path.join(output_dir, f"part_{i+1}.txt")
                    with open(output_path, 'wb') as out_file:
                        out_file.write(chunk)
                    progress_dialog.setValue(i + 1)
                    if progress_dialog.wasCanceled():
                        raise Exception("File partitioning canceled by user.")
                    QApplication.processEvents()

            QMessageBox.information(self, "Partition Complete", f"File has been partitioned into {num_parts} parts.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error partitioning file: {str(e)}")

if __name__ == '__main__':
    print("Starting application")
    app = QApplication(sys.argv)
    ex = FileComparisonTool()
    print("Showing main window")
    ex.show()
    print("Entering event loop")
    sys.exit(app.exec_())
   