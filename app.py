import sys
import math
import array
import random
import threading
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                               QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, 
                               QPushButton, QListWidget, QLineEdit, QSlider,
                               QFrame, QGridLayout, QGroupBox, QComboBox,
                               QScrollArea)
from PySide6.QtCore import Qt, QBuffer, QByteArray, QIODevice, QTimer, QRectF, QPoint
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QBrush
from PySide6.QtMultimedia import QAudioSink, QAudioFormat

# --- Data Definitions ---
NOTES_ORDER = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_FREQS = {
    "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, 
    "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00, 
    "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88,
    "C (Oct)": 523.25, "D (Oct)": 587.33, "E (Oct)": 659.25
}

SCALES = {
    "Major (Western)": [0, 2, 4, 5, 7, 9, 11],
    "Natural Minor (Western)": [0, 2, 3, 5, 7, 8, 10],
    "Harmonic Minor": [0, 2, 3, 5, 7, 8, 11],
    "Major Pentatonic (World)": [0, 2, 4, 7, 9],
    "Minor Pentatonic (World)": [0, 3, 5, 7, 10],
    "Dorian Mode (Greek/Celtic)": [0, 2, 3, 5, 7, 9, 10],
    "Phrygian Mode (Greek/Spanish)": [0, 1, 3, 5, 7, 8, 10],
    "Lydian Mode (Greek/Jazz)": [0, 2, 4, 6, 7, 9, 11],
    "Mixolydian Mode (Greek/Celtic)": [0, 2, 4, 5, 7, 9, 10],
    "Aeolian (Appalachian Mountain)": [0, 2, 3, 5, 7, 8, 10],
    "Locrian Mode (Jazz/Dissonant)": [0, 1, 3, 5, 6, 8, 10],
    "Whole Tone (Impressionist)": [0, 2, 4, 6, 8, 10],
    "Freygish (Balkan/Klezmer)": [0, 1, 4, 5, 7, 8, 10],
    "Ahavoh Rabboh (Klezmer)": [0, 1, 4, 5, 7, 8, 11],
    "Romani Minor (Gypsy Jazz)": [0, 2, 3, 6, 7, 8, 11],
    "Hijaz Kar (Armenian/Arabic)": [0, 1, 4, 5, 7, 8, 11],
    "Izat Ali (Arabic/Persian)": [0, 1, 4, 5, 7, 8, 10],
    "Shur (Persian Dastgah approx)": [0, 1, 3, 5, 7, 8, 10],
    "Vietnamese Bac (Northern)": [0, 2, 4, 7, 9],
    "Byzantine (Eastern Euro)": [0, 1, 4, 5, 7, 8, 11],
    "Bayati (Arabic approx)": [0, 2, 3, 4, 5, 7, 8, 10],
    "Al-Hijaz (Andalusi)": [0, 1, 4, 5, 7, 8, 10],
    "Todi (Indian Raga)": [0, 1, 3, 6, 7, 8, 11],
    "Hirajoshi (Japanese)": [0, 2, 3, 7, 8],
    "In Sen (Japanese)": [0, 1, 5, 7, 8],
    "Ainu Pentatonic (Japan)": [0, 3, 5, 7, 10],
    "Okinawa (Ryukyu)": [0, 4, 5, 7, 11],
    "Sardinian (Launeddas approx)": [0, 1, 4, 5, 7, 8, 10],
    "Pelog (Indonesian approx)": [0,1, 3, 7, 8],
    "Hungarian Minor": [0, 2, 3, 6, 7, 8, 11],
    "Ambasel (Ethiopian)": [0, 1, 4, 7, 8]
}

CHORDS = {
    "Major": [0, 4, 7],
    "Minor": [0, 3, 7],
    "Diminished": [0, 3, 6],
    "Augmented": [0, 4, 8],
    "Sus4": [0, 5, 7],
    "Dominant 7th": [0, 4, 7, 10],
    "Major 7th": [0, 4, 7, 11],
    "Minor 7th": [0, 3, 7, 10],
    "Minor 6th": [0, 3, 7, 9],
    "Dominant 9th": [0, 4, 7, 10, 14],
    "Major 9th": [0, 4, 7, 11, 14],
    "Minor 9th": [0, 3, 7, 10, 14],
    "Dominant 11th": [0, 4, 7, 10, 14, 17],
    "Dominant 13th": [0, 4, 7, 10, 14, 17, 21],
    "Dom 7th #5 (Altered)": [0, 4, 8, 10],
    "Dom 7th b9 (Altered)": [0, 4, 7, 10, 13]
}

PROGRESSIONS = {
    "Andalusian Cadence (Flamenco)": [("A", "Minor"), ("G", "Major"), ("F", "Major"), ("E", "Major")],
    "12-Bar Blues": [("C", "Dominant 7th"), ("C", "Dominant 7th"), ("C", "Dominant 7th"), ("C", "Dominant 7th"),
                     ("F", "Dominant 7th"), ("F", "Dominant 7th"), ("C", "Dominant 7th"), ("C", "Dominant 7th"),
                     ("G", "Dominant 7th"), ("F", "Dominant 7th"), ("C", "Dominant 7th"), ("G", "Dominant 7th")],
    "Pop / Rock (I-V-vi-IV)": [("C", "Major"), ("G", "Major"), ("A", "Minor"), ("F", "Major")],
    "Hawaiian Vamp (D7-G7-C)": [("D", "Dominant 7th"), ("G", "Dominant 7th"), ("C", "Major")],
    "Gypsy Jazz (ii-V-i)": [("A", "Minor 7b5"), ("D", "Dominant 7th"), ("G", "Minor 6th")],
    "Jazz Turnaround (I-VI7-ii-V7)": [("C", "Major"), ("A", "Dominant 7th"), ("D", "Minor 7th"), ("G", "Dominant 7th")],
    "Secondary Dominant (I - V/vi - vi)": [("C", "Major"), ("E", "Dominant 7th"), ("A", "Minor")]
}

CADENCES = {
    "Perfect Authentic (V - I)": [("G", "Major"), ("C", "Major")],
    "Plagal (IV - I)": [("F", "Major"), ("C", "Major")],
    "Deceptive (V - vi)": [("G", "Major"), ("A", "Minor")],
    "Half (I - V)": [("C", "Major"), ("G", "Major")]
}

DIATONIC_MAJOR = [
    ("I", "Major", [0, 4, 7]), ("ii", "Minor", [0, 3, 7]), ("iii", "Minor", [0, 3, 7]),
    ("IV", "Major", [0, 4, 7]), ("V", "Major", [0, 4, 7]), ("vi", "Minor", [0, 3, 7]),
    ("vii°", "Diminished", [0, 3, 6])
]
DIATONIC_MINOR = [
    ("i", "Minor", [0, 3, 7]), ("ii°", "Diminished", [0, 3, 6]), ("III", "Major", [0, 4, 7]),
    ("iv", "Minor", [0, 3, 7]), ("v", "Minor", [0, 3, 7]), ("VI", "Major", [0, 4, 7]),
    ("VII", "Major", [0, 4, 7])
]

INTERVALS = {
    1: ("Minor 2nd", 1), 2: ("Major 2nd", 2), 3: ("Minor 3rd", 3),
    4: ("Major 3rd", 4), 5: ("Perfect 4th", 5), 6: ("Tritone", 6),
    7: ("Perfect 5th", 7), 8: ("Minor 6th", 8), 9: ("Major 6th", 9),
    10: ("Minor 7th", 10), 11: ("Major 7th", 11), 12: ("Octave", 12)
}

OVERTONES = [
    ("C2 (Fundamental)", 65.41), ("C3 (Octave)", 130.82), ("G3 (Perfect 5th)", 196.23),
    ("C4 (Octave)", 261.64), ("E4 (Major 3rd)", 327.05), ("G4 (Perfect 5th)", 392.46), ("Bb4 (Minor 7th)", 457.87)
]

# --- Drone Generator (QIODevice) ---
class DroneGenerator(QIODevice):
    def __init__(self, root_freq, fifth_freq):
        super().__init__()
        self.root_freq, self.fifth_freq = root_freq, fifth_freq
        self.pos, self.sample_rate = 0, 44100

    def readData(self, maxlen):
        data = array.array('h')
        for _ in range(maxlen // 2):
            t = float(self.pos) / self.sample_rate
            wave = (0.15 * math.sin(2 * math.pi * self.root_freq * t) + 
                    0.10 * math.sin(2 * math.pi * self.fifth_freq * t) +
                    0.05 * math.sin(4 * math.pi * self.root_freq * t))
            data.append(int(wave * 32767))
            self.pos += 1
        return data.tobytes()

    def writeData(self, data): return 0

# --- Audio Engine ---
class AudioEngine:
    def __init__(self):
        self.format = QAudioFormat()
        self.format.setSampleRate(44100)
        self.format.setChannelCount(1)
        self.format.setSampleFormat(QAudioFormat.Int16)
        self.melody_sink = QAudioSink(self.format)
        self.drone_sink = QAudioSink(self.format)
        self.drone_gen = None
        self.volume = 0.8
        self.sidechain_active = False
        self.sidechain_timer = QTimer()
        self.sidechain_timer.timeout.connect(self.sidechain_pulse)

    def set_volume(self, vol):
        self.volume = vol
        if not self.sidechain_active:
            self.melody_sink.setVolume(vol)
            self.drone_sink.setVolume(vol * 0.75)

    def play_frequency(self, freq, duration_ms=600):
        if freq <= 0: return
        sample_rate = self.format.sampleRate()
        num_samples = int(sample_rate * (duration_ms / 1000.0))
        data = array.array('h')
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            wave = (math.sin(2 * math.pi * freq * t) + 
                    0.4 * math.sin(4 * math.pi * freq * t) + 
                    0.2 * math.sin(6 * math.pi * freq * t))
            volume = 0.4
            attack, release = 0.01, 0.2
            if t < attack: volume *= (t / attack)
            elif t > (duration_ms / 1000.0) - release: volume *= max(0, ((duration_ms / 1000.0) - t) / release)
            data.append(int(volume * 32767 * wave))
            
        byte_array = QByteArray(data.tobytes())
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.ReadOnly)
        self.melody_sink.stop()
        self.melody_sink.start(buffer)

    def start_drone(self, root_note):
        self.stop_drone()
        root_freq = NOTE_FREQS[root_note]
        fifth_freq = NOTE_FREQS[NOTES_ORDER[(NOTES_ORDER.index(root_note) + 7) % 12]]
        self.drone_gen = DroneGenerator(root_freq, fifth_freq)
        self.drone_gen.open(QIODevice.ReadOnly)
        self.drone_sink.start(self.drone_gen)

    def stop_drone(self):
        self.drone_sink.stop()
        if self.drone_gen:
            self.drone_gen.close()
            self.drone_gen = None

    def toggle_sidechain(self, active):
        self.sidechain_active = active
        if active:
            self.drone_sink.setVolume(0.1)
            self.sidechain_timer.start(125)
        else:
            self.sidechain_timer.stop()
            self.set_volume(self.volume)

    def sidechain_pulse(self):
        def swell():
            steps = 10
            for i in range(steps):
                vol = 0.1 + (0.9 * (i / steps))
                self.drone_sink.setVolume(vol * self.volume * 0.75)
                time.sleep(0.0125)
        threading.Thread(target=swell, daemon=True).start()

# --- Widgets ---
class CircleOfFifthsWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.is_minor = False
        self.selected_key = "C"
        self.setMinimumSize(400, 450)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width, height = self.width(), self.height()
        cx, cy = width / 2, height / 2 - 20
        radius = min(width, height) / 2 - 60
        
        keys = ["A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F", "C", "G", "D"] if self.is_minor else \
               ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]
               
        painter.setPen(QPen(QColor("#313244"), 2))
        
        for i, key in enumerate(keys):
            angle = (90 - i * 30) * math.pi / 180
            x, y = cx + radius * math.cos(angle), cy - radius * math.sin(angle)
            
            is_selected = (key == self.selected_key)
            if is_selected:
                painter.setBrush(QBrush(QColor("#f38ba8" if self.is_minor else "#89b4fa")))
                text_color = QColor("#11111b")
            elif "b" in key or "#" in key:
                painter.setBrush(QBrush(QColor("#11111b")))
                text_color = QColor("#cdd6f4")
            else:
                painter.setBrush(QBrush(QColor("#313244")))
                text_color = QColor("#cdd6f4")
                
            painter.drawEllipse(QPoint(int(x), int(y)), 30, 30)
            painter.setPen(QPen(text_color))
            display_key = key + "m" if self.is_minor else key
            painter.drawText(QRectF(int(x)-30, int(y)-15, 60, 30), Qt.AlignCenter, display_key)
            painter.setPen(QPen(QColor("#313244"), 2))

    def mousePressEvent(self, event):
        cx, cy = self.width() / 2, self.height() / 2 - 20
        radius = min(self.width(), self.height()) / 2 - 60
        keys = ["A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F", "C", "G", "D"] if self.is_minor else \
               ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]
               
        for i, key in enumerate(keys):
            angle = (90 - i * 30) * math.pi / 180
            x, y = cx + radius * math.cos(angle), cy - radius * math.sin(angle)
            if (event.position().x() - x)**2 + (event.position().y() - y)**2 <= 30**2:
                self.selected_key = key
                self.update()
                self.play_triad(key)
                self.update_info(key)
                break

    def update_info(self, key):
        if self.is_minor:
            rel_maj_idx = (NOTES_ORDER.index(key) + 3) % 12
            rel_key = NOTES_ORDER[rel_maj_idx]
            text = f"<b style='color:#f38ba8'>Key:</b> {key} Minor &nbsp;&nbsp;|&nbsp;&nbsp; <b style='color:#89b4fa'>Relative Major:</b> {rel_key} Major"
        else:
            rel_min_idx = (NOTES_ORDER.index(key) + 9) % 12
            rel_min = NOTES_ORDER[rel_min_idx]
            text = f"<b style='color:#89b4fa'>Key:</b> {key} Major &nbsp;&nbsp;|&nbsp;&nbsp; <b style='color:#f38ba8'>Relative Minor:</b> {rel_min} Minor"
            
        parent_layout = self.parent().layout()
        if parent_layout:
            info_label = parent_layout.itemAt(3).widget()
            info_label.setText(text)

    def play_triad(self, key):
        root_idx = NOTES_ORDER.index(key)
        third_idx = (root_idx + 3) % 12 if self.is_minor else (root_idx + 4) % 12
        fifth_idx = (root_idx + 7) % 12
        def play_chord():
            self.audio.play_frequency(NOTE_FREQS[NOTES_ORDER[root_idx]], 800)
            time.sleep(0.05)
            self.audio.play_frequency(NOTE_FREQS[NOTES_ORDER[third_idx]], 800)
            time.sleep(0.05)
            self.audio.play_frequency(NOTE_FREQS[NOTES_ORDER[fifth_idx]], 1000)
        threading.Thread(target=play_chord, daemon=True).start()


class IntervalTrainerWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.score, self.attempts, self.current_interval = 0, 0, None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        stats_layout = QHBoxLayout()
        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #a6e3a1;")
        stats_layout.addWidget(self.score_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        self.play_btn = QPushButton("Play Interval")
        self.play_btn.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; padding: 15px; font-weight: bold; border-radius: 4px; font-size: 16px; }"
                                    "QPushButton:hover { background-color: #74c7ec; }")
        self.play_btn.clicked.connect(self.new_interval)
        layout.addWidget(self.play_btn)

        self.feedback_label = QLabel("Click 'Play Interval' to begin!")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("font-size: 14px; color: #cdd6f4; padding: 10px;")
        layout.addWidget(self.feedback_label)

        grid = QGridLayout()
        self.interval_buttons = []
        for id, (name, semitones) in INTERVALS.items():
            btn = QPushButton(name)
            btn.setStyleSheet("QPushButton { background-color: #313244; color: #cdd6f4; padding: 10px; border-radius: 4px; }"
                              "QPushButton:hover { background-color: #45475a; }")
            btn.clicked.connect(lambda checked, s=semitones: self.check_answer(s))
            grid.addWidget(btn, (id-1)//3, (id-1)%3)
            self.interval_buttons.append(btn)
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    def new_interval(self):
        self.current_interval = random.randint(1, 12)
        self.play_interval()
        self.feedback_label.setText("What interval did you hear?")
        self.feedback_label.setStyleSheet("font-size: 14px; color: #cdd6f4; padding: 10px;")
        for btn in self.interval_buttons: btn.setEnabled(True)

    def play_interval(self):
        root_freq = NOTE_FREQS["C"]
        target_idx = (NOTES_ORDER.index("C") + self.current_interval) % 12
        target_freq = NOTE_FREQS["C (Oct)"] if self.current_interval == 12 else NOTE_FREQS[NOTES_ORDER[target_idx]]
        def play_thread():
            self.audio.play_frequency(root_freq, 500)
            time.sleep(0.6)
            self.audio.play_frequency(target_freq, 800)
        threading.Thread(target=play_thread, daemon=True).start()

    def check_answer(self, semitones):
        if self.current_interval is None: return
        self.attempts += 1
        correct_name = INTERVALS[self.current_interval][0]
        if semitones == self.current_interval:
            self.score += 1
            self.feedback_label.setText(f"Correct! It was a {correct_name}.")
            self.feedback_label.setStyleSheet("font-size: 14px; color: #a6e3a1; padding: 10px; font-weight: bold;")
        else:
            self.feedback_label.setText(f"Incorrect. It was a {correct_name}.")
            self.feedback_label.setStyleSheet("font-size: 14px; color: #f38ba8; padding: 10px; font-weight: bold;")
        self.score_label.setText(f"Score: {self.score} / {self.attempts}")
        for btn in self.interval_buttons: btn.setEnabled(False)


class ScaleDegreeTrainerWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.score, self.attempts, self.current_degree = 0, 0, None
        self.degrees = ["1 (Do)", "2 (Re)", "3 (Mi)", "4 (Fa)", "5 (Sol)", "6 (La)", "7 (Ti)"]
        self.scale_freqs = [NOTE_FREQS[n] for n in ["C", "D", "E", "F", "G", "A", "B"]]
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        stats_layout = QHBoxLayout()
        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #a6e3a1;")
        stats_layout.addWidget(self.score_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        self.play_btn = QPushButton("Play New Note")
        self.play_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 15px; font-weight: bold; border-radius: 4px; font-size: 16px; }"
                                    "QPushButton:hover { background-color: #b4befe; }")
        self.play_btn.clicked.connect(self.new_note)
        layout.addWidget(self.play_btn)

        self.feedback_label = QLabel("Click 'Play New Note' to hear a cadence and a random note!")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("font-size: 14px; color: #cdd6f4; padding: 10px;")
        layout.addWidget(self.feedback_label)

        grid = QGridLayout()
        self.degree_buttons = []
        for i, name in enumerate(self.degrees):
            btn = QPushButton(name)
            btn.setStyleSheet("QPushButton { background-color: #313244; color: #cdd6f4; padding: 10px; border-radius: 4px; }"
                              "QPushButton:hover { background-color: #45475a; }")
            btn.clicked.connect(lambda checked, idx=i: self.check_answer(idx))
            grid.addWidget(btn, i//4, i%4)
            self.degree_buttons.append(btn)
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    def new_note(self):
        self.current_degree = random.randint(0, 6)
        self.play_sequence()
        self.feedback_label.setText("What scale degree did you hear?")
        self.feedback_label.setStyleSheet("font-size: 14px; color: #cdd6f4; padding: 10px;")
        for btn in self.degree_buttons: btn.setEnabled(True)

    def play_sequence(self):
        c_chord = [NOTE_FREQS["C"], NOTE_FREQS["E"], NOTE_FREQS["G"]]
        f_chord = [NOTE_FREQS["F"], NOTE_FREQS["A"], NOTE_FREQS["C (Oct)"]]
        g_chord = [NOTE_FREQS["G"], NOTE_FREQS["B"], NOTE_FREQS["D (Oct)"]]
        
        def play_thread():
            for chord in [c_chord, f_chord, g_chord, c_chord]:
                for f in chord:
                    self.audio.play_frequency(f, 400)
                time.sleep(0.4)
            time.sleep(0.2)
            self.audio.play_frequency(self.scale_freqs[self.current_degree], 1000)
        threading.Thread(target=play_thread, daemon=True).start()

    def check_answer(self, idx):
        if self.current_degree is None: return
        self.attempts += 1
        correct_name = self.degrees[self.current_degree]
        if idx == self.current_degree:
            self.score += 1
            self.feedback_label.setText(f"Correct! It was {correct_name}.")
            self.feedback_label.setStyleSheet("font-size: 14px; color: #a6e3a1; padding: 10px; font-weight: bold;")
        else:
            self.feedback_label.setText(f"Incorrect. It was {correct_name}.")
            self.feedback_label.setStyleSheet("font-size: 14px; color: #f38ba8; padding: 10px; font-weight: bold;")
        self.score_label.setText(f"Score: {self.score} / {self.attempts}")
        for btn in self.degree_buttons: btn.setEnabled(False)


class ChordQualityTrainerWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.score, self.attempts, self.current_chord = 0, 0, None
        self.chords = {
            "Major": [0, 4, 7],
            "Minor": [0, 3, 7],
            "Diminished": [0, 3, 6],
            "Augmented": [0, 4, 8]
        }
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        stats_layout = QHBoxLayout()
        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #a6e3a1;")
        stats_layout.addWidget(self.score_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        self.play_btn = QPushButton("Play Chord")
        self.play_btn.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; padding: 15px; font-weight: bold; border-radius: 4px; font-size: 16px; }"
                                    "QPushButton:hover { background-color: #95d395; }")
        self.play_btn.clicked.connect(self.new_chord)
        layout.addWidget(self.play_btn)

        self.feedback_label = QLabel("Click 'Play Chord' to begin!")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("font-size: 14px; color: #cdd6f4; padding: 10px;")
        layout.addWidget(self.feedback_label)

        grid = QGridLayout()
        self.chord_buttons = []
        for i, name in enumerate(self.chords.keys()):
            btn = QPushButton(name)
            btn.setStyleSheet("QPushButton { background-color: #313244; color: #cdd6f4; padding: 15px; border-radius: 4px; font-size: 14px; }"
                              "QPushButton:hover { background-color: #45475a; }")
            btn.clicked.connect(lambda checked, n=name: self.check_answer(n))
            grid.addWidget(btn, 0, i)
            self.chord_buttons.append(btn)
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    def new_chord(self):
        self.current_chord = random.choice(list(self.chords.keys()))
        self.play_chord()
        self.feedback_label.setText("What chord quality did you hear?")
        self.feedback_label.setStyleSheet("font-size: 14px; color: #cdd6f4; padding: 10px;")
        for btn in self.chord_buttons: btn.setEnabled(True)

    def play_chord(self):
        intervals = self.chords[self.current_chord]
        root_freq = NOTE_FREQS["C"]
        notes_to_play = []
        for interval in intervals:
            note_idx = (NOTES_ORDER.index("C") + interval) % 12
            notes_to_play.append(NOTE_FREQS[NOTES_ORDER[note_idx]])
            
        def play_thread():
            for f in notes_to_play:
                self.audio.play_frequency(f, 1000)
        threading.Thread(target=play_thread, daemon=True).start()

    def check_answer(self, name):
        if self.current_chord is None: return
        self.attempts += 1
        if name == self.current_chord:
            self.score += 1
            self.feedback_label.setText(f"Correct! It was {self.current_chord}.")
            self.feedback_label.setStyleSheet("font-size: 14px; color: #a6e3a1; padding: 10px; font-weight: bold;")
        else:
            self.feedback_label.setText(f"Incorrect. It was {self.current_chord}.")
            self.feedback_label.setStyleSheet("font-size: 14px; color: #f38ba8; padding: 10px; font-weight: bold;")
        self.score_label.setText(f"Score: {self.score} / {self.attempts}")
        for btn in self.chord_buttons: btn.setEnabled(False)


class MelodicDictationWidget(QWidget):
    """Trains the ear to identify a 3-note melodic sequence."""
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.score, self.attempts = 0, 0
        self.current_sequence = []
        self.user_sequence = []
        self.scale_freqs = [NOTE_FREQS[n] for n in ["C", "D", "E", "F", "G", "A", "B"]]
        self.degrees = ["1 (Do)", "2 (Re)", "3 (Mi)", "4 (Fa)", "5 (Sol)", "6 (La)", "7 (Ti)"]
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        stats_layout = QHBoxLayout()
        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #a6e3a1;")
        stats_layout.addWidget(self.score_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        self.play_btn = QPushButton("Play New Melody (3 Notes)")
        self.play_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 15px; font-weight: bold; border-radius: 4px; font-size: 16px; }"
                                    "QPushButton:hover { background-color: #b4befe; }")
        self.play_btn.clicked.connect(self.new_melody)
        layout.addWidget(self.play_btn)

        self.feedback_label = QLabel("Click 'Play New Melody' to begin!")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("font-size: 14px; color: #cdd6f4; padding: 10px;")
        layout.addWidget(self.feedback_label)

        # Display user's current input
        self.input_display = QLabel("Your Answer: -")
        self.input_display.setAlignment(Qt.AlignCenter)
        self.input_display.setStyleSheet("font-size: 18px; color: #f9e2af; font-weight: bold; padding: 10px;")
        layout.addWidget(self.input_display)

        grid = QGridLayout()
        self.note_buttons = []
        for i, name in enumerate(self.degrees):
            btn = QPushButton(name)
            btn.setStyleSheet("QPushButton { background-color: #313244; color: #cdd6f4; padding: 10px; border-radius: 4px; }"
                              "QPushButton:hover { background-color: #45475a; }")
            btn.clicked.connect(lambda checked, idx=i: self.add_note(idx))
            grid.addWidget(btn, i//4, i%4)
            self.note_buttons.append(btn)
        layout.addLayout(grid)

        ctrl_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear Input")
        clear_btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                "QPushButton:hover { background-color: #eb7d99; }")
        clear_btn.clicked.connect(self.clear_input)
        ctrl_layout.addWidget(clear_btn)

        replay_btn = QPushButton("Replay Melody")
        replay_btn.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                 "QPushButton:hover { background-color: #74c7ec; }")
        replay_btn.clicked.connect(self.play_melody)
        ctrl_layout.addWidget(replay_btn)
        layout.addLayout(ctrl_layout)

        layout.addStretch()
        self.setLayout(layout)

    def new_melody(self):
        self.current_sequence = [random.randint(0, 6) for _ in range(3)]
        self.clear_input()
        self.play_melody()
        self.feedback_label.setText("Enter the 3 notes you heard.")
        self.feedback_label.setStyleSheet("font-size: 14px; color: #cdd6f4; padding: 10px;")
        for btn in self.note_buttons: btn.setEnabled(True)

    def play_melody(self):
        if not self.current_sequence: return
        def play_thread():
            for idx in self.current_sequence:
                self.audio.play_frequency(self.scale_freqs[idx], 400)
                time.sleep(0.4)
        threading.Thread(target=play_thread, daemon=True).start()

    def add_note(self, idx):
        if len(self.user_sequence) < 3:
            self.user_sequence.append(idx)
            self.audio.play_frequency(self.scale_freqs[idx], 300)
            self.update_display()
            if len(self.user_sequence) == 3:
                self.check_answer()

    def clear_input(self):
        self.user_sequence = []
        self.update_display()

    def update_display(self):
        if not self.user_sequence:
            self.input_display.setText("Your Answer: -")
        else:
            notes = [self.degrees[i] for i in self.user_sequence]
            self.input_display.setText(f"Your Answer: {' - '.join(notes)}")

    def check_answer(self):
        if not self.current_sequence or len(self.user_sequence) != 3: return
        self.attempts += 1
        if self.user_sequence == self.current_sequence:
            self.score += 1
            self.feedback_label.setText("Correct!")
            self.feedback_label.setStyleSheet("font-size: 14px; color: #a6e3a1; padding: 10px; font-weight: bold;")
        else:
            correct_notes = [self.degrees[i] for i in self.current_sequence]
            self.feedback_label.setText(f"Incorrect. It was {' - '.join(correct_notes)}.")
            self.feedback_label.setStyleSheet("font-size: 14px; color: #f38ba8; padding: 10px; font-weight: bold;")
        self.score_label.setText(f"Score: {self.score} / {self.attempts}")
        for btn in self.note_buttons: btn.setEnabled(False)


class PhaseShifterWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.notes = ["C", "D", "E", "G", "A", "C (Oct)", "D (Oct)", "E (Oct)"]
        self.steps = 8
        self.grid = [False for _ in range(self.steps)]
        
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.tick1)
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.tick2)
        
        self.step1, self.step2 = 0, 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        info = QLabel("Program a sequence below. Player 2 will play at a slightly faster tempo, drifting in and out of sync with Player 1.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        layout.addWidget(info)

        grid = QGridLayout()
        grid.setSpacing(2)
        self.buttons = []
        for c in range(self.steps):
            btn = QPushButton(str(c+1))
            btn.setFixedSize(40, 40)
            btn.setCheckable(True)
            btn.setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; color: #cdd6f4; }"
                              "QPushButton:checked { background-color: #a6e3a1; color: #11111b; font-weight: bold; }")
            btn.clicked.connect(lambda checked, idx=c: self.toggle_cell(idx))
            grid.addWidget(btn, 0, c)
            self.buttons.append(btn)
        layout.addLayout(grid)

        ctrl_layout = QHBoxLayout()
        self.play_btn = QPushButton("Start Phase Shift")
        self.play_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #b4befe; }")
        self.play_btn.setCheckable(True)
        self.play_btn.clicked.connect(self.toggle_play)
        ctrl_layout.addWidget(self.play_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                "QPushButton:hover { background-color: #eb7d99; }")
        clear_btn.clicked.connect(self.clear_grid)
        ctrl_layout.addWidget(clear_btn)
        layout.addLayout(ctrl_layout)
        
        self.setLayout(layout)

    def toggle_cell(self, idx):
        self.grid[idx] = not self.grid[idx]

    def clear_grid(self):
        for i in range(self.steps):
            self.grid[i] = False
            self.buttons[i].setChecked(False)

    def toggle_play(self):
        if self.play_btn.isChecked():
            self.play_btn.setText("Stop Phase Shift")
            self.step1, self.step2 = 0, 0
            self.timer1.start(500)
            self.timer2.start(491)
        else:
            self.play_btn.setText("Start Phase Shift")
            self.timer1.stop()
            self.timer2.stop()
            for i in range(self.steps):
                if self.grid[i]:
                    self.buttons[i].setStyleSheet("QPushButton { background-color: #a6e3a1; border-radius: 4px; color: #11111b; font-weight: bold; }")
                else:
                    self.buttons[i].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; color: #cdd6f4; }")

    def update_button_color(self, step, color):
        if self.grid[step]:
            self.buttons[step].setStyleSheet(f"QPushButton {{ background-color: {color}; border-radius: 4px; color: #11111b; font-weight: bold; }}")
        else:
            self.buttons[step].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; color: #cdd6f4; }")

    def tick1(self):
        if self.grid[self.step1]:
            self.audio.play_frequency(NOTE_FREQS[self.notes[self.step1]], 300)
        self.update_button_color(self.step1, "#89b4fa")
        prev = (self.step1 - 1) % self.steps
        if prev != self.step2:
            self.update_button_color(prev, "#a6e3a1")
        self.step1 = (self.step1 + 1) % self.steps

    def tick2(self):
        if self.grid[self.step2]:
            def play():
                time.sleep(0.01)
                self.audio.play_frequency(NOTE_FREQS[self.notes[self.step2]], 300)
            threading.Thread(target=play, daemon=True).start()
            
        if self.step2 != self.step1:
            self.update_button_color(self.step2, "#f38ba8")
            prev = (self.step2 - 1) % self.steps
            if prev != self.step1 and prev != self.step2:
                self.update_button_color(prev, "#a6e3a1")
        self.step2 = (self.step2 + 1) % self.steps


class DiatonicChordWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        ctrl_layout = QHBoxLayout()
        ctrl_layout.addWidget(QLabel("Key:"))
        self.key_combo = QComboBox()
        self.key_combo.addItems(NOTES_ORDER)
        ctrl_layout.addWidget(self.key_combo)

        ctrl_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Major", "Minor"])
        ctrl_layout.addWidget(self.mode_combo)
        layout.addLayout(ctrl_layout)

        self.chord_buttons = []
        chord_btn_layout = QHBoxLayout()
        for i in range(7):
            btn = QPushButton(f"Chord {i+1}")
            btn.setMinimumHeight(50)
            btn.setStyleSheet("QPushButton { background-color: #313244; color: #cdd6f4; padding: 5px; border-radius: 4px; font-weight: bold; }"
                              "QPushButton:hover { background-color: #45475a; }")
            btn.clicked.connect(lambda checked, idx=i: self.play_diatonic_chord(idx))
            chord_btn_layout.addWidget(btn)
            self.chord_buttons.append(btn)
        layout.addLayout(chord_btn_layout)

        self.info_label = QLabel("Select a key and mode to generate diatonic chords.")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color: #f9e2af; font-weight: bold; padding: 5px;")
        layout.addWidget(self.info_label)

        self.key_combo.currentTextChanged.connect(self.update_chords)
        self.mode_combo.currentTextChanged.connect(self.update_chords)
        
        self.setLayout(layout)
        self.update_chords()

    def update_chords(self):
        key = self.key_combo.currentText()
        mode = self.mode_combo.currentText()
        pattern = DIATONIC_MAJOR if mode == "Major" else DIATONIC_MINOR
        
        root_idx = NOTES_ORDER.index(key)
        
        for i, (roman, quality, intervals) in enumerate(pattern):
            chord_root_idx = (root_idx + SCALES["Major (Western)" if mode == "Major" else "Natural Minor (Western)"][i]) % 12
            chord_root_note = NOTES_ORDER[chord_root_idx]
            self.chord_buttons[i].setText(f"{roman}\n{chord_root_note} {quality}")
            
        self.info_label.setText(f"Diatonic Triads in {key} {mode}")

    def play_diatonic_chord(self, idx):
        key = self.key_combo.currentText()
        mode = self.mode_combo.currentText()
        pattern = DIATONIC_MAJOR if mode == "Major" else DIATONIC_MINOR
        scale_intervals = SCALES["Major (Western)" if mode == "Major" else "Natural Minor (Western)"]
        
        roman, quality, chord_intervals = pattern[idx]
        root_idx = NOTES_ORDER.index(key)
        chord_root_idx = (root_idx + scale_intervals[idx]) % 12
        
        notes_to_play = []
        for interval in chord_intervals:
            note_idx = (chord_root_idx + interval) % 12
            notes_to_play.append(NOTE_FREQS[NOTES_ORDER[note_idx]])
            
        def play_in_thread():
            for f in notes_to_play:
                self.audio.play_frequency(f, 800)
                time.sleep(0.05)
        threading.Thread(target=play_in_thread, daemon=True).start()


class OvertoneSingerWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.fundamental_freq = 130.81 # C3
        self.overtones = [
            ("3rd (E5)", 5, 659.25),
            ("5th (G5)", 6, 783.99),
            ("Minor 7th (Bb5)", 7, 932.33),
            ("Octave (C6)", 8, 1046.50)
        ]
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        info = QLabel("Throat singers (Tuvan/Tibetan) manipulate their vocal tract to isolate high overtones above a low drone. Click an overtone to 'sing' it.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        layout.addWidget(info)

        self.drone_btn = QPushButton("Start Fundamental Drone (C3)")
        self.drone_btn.setStyleSheet("QPushButton { background-color: #313244; color: #f9e2af; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                     "QPushButton:hover { background-color: #45475a; }")
        self.drone_btn.setCheckable(True)
        self.drone_btn.clicked.connect(self.toggle_drone)
        layout.addWidget(self.drone_btn)

        btn_layout = QHBoxLayout()
        for name, harmonic, freq in self.overtones:
            btn = QPushButton(name)
            btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 15px; font-weight: bold; border-radius: 4px; }"
                              "QPushButton:hover { background-color: #b4befe; }")
            btn.clicked.connect(lambda checked, f=freq: self.audio.play_frequency(f, 1200))
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def toggle_drone(self):
        if self.drone_btn.isChecked():
            self.audio.stop_drone()
            gen = DroneGenerator(self.fundamental_freq, self.fundamental_freq * 1.5)
            gen.open(QIODevice.ReadOnly)
            self.audio.drone_gen = gen
            self.audio.drone_sink.start(gen)
            self.drone_btn.setText("Stop Drone")
            self.drone_btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }")
        else:
            self.audio.stop_drone()
            self.drone_btn.setText("Start Fundamental Drone (C3)")
            self.drone_btn.setStyleSheet("QPushButton { background-color: #313244; color: #f9e2af; padding: 8px; font-weight: bold; border-radius: 4px; }")


class HocketingSequencerWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.notes = ["C", "D", "E", "F", "G", "A", "B", "C (Oct)"]
        self.steps = 8
        self.grid_a = [False for _ in range(self.steps)]
        self.grid_b = [False for _ in range(self.steps)]
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.current_step = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        info = QLabel("Hocketing is splitting a melody between two voices. Program Voice A (Blue) and Voice B (Pink), then play. Used in Medieval Europe and Andean Panpipes.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        layout.addWidget(info)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)
        self.buttons_a = []
        self.buttons_b = []
        
        lbl_a = QLabel("Voice A:")
        grid_layout.addWidget(lbl_a, 0, 0)
        for c in range(self.steps):
            btn = QPushButton()
            btn.setFixedSize(40, 30)
            btn.setCheckable(True)
            btn.setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }"
                              "QPushButton:checked { background-color: #89b4fa; }")
            btn.clicked.connect(lambda checked, idx=c: self.toggle_cell('a', idx))
            grid_layout.addWidget(btn, 0, c + 1)
            self.buttons_a.append(btn)
            
        lbl_b = QLabel("Voice B:")
        grid_layout.addWidget(lbl_b, 1, 0)
        for c in range(self.steps):
            btn = QPushButton()
            btn.setFixedSize(40, 30)
            btn.setCheckable(True)
            btn.setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }"
                              "QPushButton:checked { background-color: #f38ba8; }")
            btn.clicked.connect(lambda checked, idx=c: self.toggle_cell('b', idx))
            grid_layout.addWidget(btn, 1, c + 1)
            self.buttons_b.append(btn)
            
        layout.addLayout(grid_layout)
        
        ctrl_layout = QHBoxLayout()
        self.play_btn = QPushButton("Play Hocket")
        self.play_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #b4befe; }")
        self.play_btn.setCheckable(True)
        self.play_btn.clicked.connect(self.toggle_play)
        ctrl_layout.addWidget(self.play_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                "QPushButton:hover { background-color: #eb7d99; }")
        clear_btn.clicked.connect(self.clear_grid)
        ctrl_layout.addWidget(clear_btn)
        layout.addLayout(ctrl_layout)
        
        self.setLayout(layout)

    def toggle_cell(self, voice, idx):
        if voice == 'a':
            self.grid_a[idx] = not self.grid_a[idx]
        else:
            self.grid_b[idx] = not self.grid_b[idx]

    def clear_grid(self):
        for i in range(self.steps):
            self.grid_a[i] = False
            self.grid_b[i] = False
            self.buttons_a[i].setChecked(False)
            self.buttons_b[i].setChecked(False)

    def toggle_play(self):
        if self.play_btn.isChecked():
            self.play_btn.setText("Stop Hocket")
            self.current_step = 0
            self.timer.start(300)
        else:
            self.play_btn.setText("Play Hocket")
            self.timer.stop()
            self.reset_colors()

    def reset_colors(self):
        for c in range(self.steps):
            if self.grid_a[c]: self.buttons_a[c].setStyleSheet("QPushButton { background-color: #89b4fa; border-radius: 4px; }")
            else: self.buttons_a[c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")
            if self.grid_b[c]: self.buttons_b[c].setStyleSheet("QPushButton { background-color: #f38ba8; border-radius: 4px; }")
            else: self.buttons_b[c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")

    def step(self):
        if self.grid_a[self.current_step]:
            self.audio.play_frequency(NOTE_FREQS[self.notes[self.current_step]], 280)
        if self.grid_b[self.current_step]:
            self.audio.play_frequency(NOTE_FREQS[self.notes[self.current_step]], 280)
            
        for c in range(self.steps):
            is_current = (c == self.current_step)
            if is_current and self.grid_a[c]:
                self.buttons_a[c].setStyleSheet("QPushButton { background-color: #11111b; border: 2px solid #89b4fa; border-radius: 4px; }")
            elif self.grid_a[c]:
                self.buttons_a[c].setStyleSheet("QPushButton { background-color: #89b4fa; border-radius: 4px; }")
            else:
                self.buttons_a[c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")
            if is_current and self.grid_b[c]:
                self.buttons_b[c].setStyleSheet("QPushButton { background-color: #11111b; border: 2px solid #f38ba8; border-radius: 4px; }")
            elif self.grid_b[c]:
                self.buttons_b[c].setStyleSheet("QPushButton { background-color: #f38ba8; border-radius: 4px; }")
            else:
                self.buttons_b[c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")
                
        self.current_step = (self.current_step + 1) % self.steps


class TxalapartaWidget(QWidget):
    """Simulates the Basque Txalaparta: two players interlocking strikes on wooden beams."""
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.steps = 8
        # Player 1 (Red) defaults to even beats, Player 2 (Blue) to odd beats
        self.grid_1 = [True if i % 2 == 0 else False for i in range(self.steps)]
        self.grid_2 = [True if i % 2 != 0 else False for i in range(self.steps)]
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.current_step = 0
        
        self.buttons_1 = []
        self.buttons_2 = []
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        info = QLabel("Txalaparta is a Basque percussion tradition. Two players (Txalapartaris) strike wooden beams. They must interlock perfectly, never hitting at the same time.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        layout.addWidget(info)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)
        
        # Player 1
        lbl_1 = QLabel("Player 1:")
        grid_layout.addWidget(lbl_1, 0, 0)
        for c in range(self.steps):
            btn = QPushButton()
            btn.setFixedSize(30, 30)
            btn.setCheckable(True)
            btn.setChecked(self.grid_1[c])
            btn.setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }"
                              "QPushButton:checked { background-color: #f38ba8; }")
            btn.clicked.connect(lambda checked, idx=c: self.toggle_cell(1, idx))
            grid_layout.addWidget(btn, 0, c + 1)
            self.buttons_1.append(btn)
            
        # Player 2
        lbl_2 = QLabel("Player 2:")
        grid_layout.addWidget(lbl_2, 1, 0)
        for c in range(self.steps):
            btn = QPushButton()
            btn.setFixedSize(30, 30)
            btn.setCheckable(True)
            btn.setChecked(self.grid_2[c])
            btn.setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }"
                              "QPushButton:checked { background-color: #89b4fa; }")
            btn.clicked.connect(lambda checked, idx=c: self.toggle_cell(2, idx))
            grid_layout.addWidget(btn, 1, c + 1)
            self.buttons_2.append(btn)
            
        layout.addLayout(grid_layout)
        
        ctrl_layout = QHBoxLayout()
        self.play_btn = QPushButton("Start Txalaparta")
        self.play_btn.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #95d395; }")
        self.play_btn.setCheckable(True)
        self.play_btn.clicked.connect(self.toggle_play)
        ctrl_layout.addWidget(self.play_btn)
        layout.addLayout(ctrl_layout)
        
        self.setLayout(layout)

    def toggle_cell(self, player, idx):
        if player == 1:
            self.grid_1[idx] = not self.grid_1[idx]
        else:
            self.grid_2[idx] = not self.grid_2[idx]

    def toggle_play(self):
        if self.play_btn.isChecked():
            self.play_btn.setText("Stop Txalaparta")
            self.current_step = 0
            self.timer.start(250) # ~120bpm 8th notes
        else:
            self.play_btn.setText("Start Txalaparta")
            self.timer.stop()

    def step(self):
        # Player 1 plays high woodblock, Player 2 plays low woodblock
        if self.grid_1[self.current_step]:
            self.audio.play_frequency(880, 100) 
        if self.grid_2[self.current_step]:
            self.audio.play_frequency(440, 100)
            
        # Update visuals
        for c in range(self.steps):
            is_current = (c == self.current_step)
            # Player 1
            if is_current and self.grid_1[c]:
                self.buttons_1[c].setStyleSheet("QPushButton { background-color: #11111b; border: 2px solid #f38ba8; border-radius: 4px; }")
            elif self.grid_1[c]:
                self.buttons_1[c].setStyleSheet("QPushButton { background-color: #f38ba8; border-radius: 4px; }")
            else:
                self.buttons_1[c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")
            # Player 2
            if is_current and self.grid_2[c]:
                self.buttons_2[c].setStyleSheet("QPushButton { background-color: #11111b; border: 2px solid #89b4fa; border-radius: 4px; }")
            elif self.grid_2[c]:
                self.buttons_2[c].setStyleSheet("QPushButton { background-color: #89b4fa; border-radius: 4px; }")
            else:
                self.buttons_2[c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")
                
        self.current_step = (self.current_step + 1) % self.steps


class VodouRhythmWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.steps = 12
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.current_step = 0
        
        self.ogan_pattern = [True if i % 3 == 0 else False for i in range(self.steps)]
        self.drum_pattern = [True if i in [0, 3, 4, 6, 9, 10] else False for i in range(self.steps)]
        
        self.ogan_labels = []
        self.drum_labels = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        info = QLabel("Haitian Vodou music uses complex 12/8 polyrhythms to invoke spirits (Loa). The Ogan (iron bell) keeps a steady pulse, while the Tanbou (drum) syncopates around it.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        layout.addWidget(info)

        self.play_btn = QPushButton("Start Rhythm")
        self.play_btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #eb7d99; }")
        self.play_btn.setCheckable(True)
        self.play_btn.clicked.connect(self.toggle_play)
        layout.addWidget(self.play_btn)

        ogan_layout = QHBoxLayout()
        lbl_o = QLabel("Ogan (Bell):")
        lbl_o.setFixedWidth(100)
        ogan_layout.addWidget(lbl_o)
        for i in range(self.steps):
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(24, 24)
            lbl.setStyleSheet("background: #313244; border-radius: 4px;")
            ogan_layout.addWidget(lbl)
            self.ogan_labels.append(lbl)
        layout.addLayout(ogan_layout)

        drum_layout = QHBoxLayout()
        lbl_d = QLabel("Tanbou (Drum):")
        lbl_d.setFixedWidth(100)
        drum_layout.addWidget(lbl_d)
        for i in range(self.steps):
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(24, 24)
            lbl.setStyleSheet("background: #313244; border-radius: 4px;")
            drum_layout.addWidget(lbl)
            self.drum_labels.append(lbl)
        layout.addLayout(drum_layout)

        self.setLayout(layout)

    def toggle_play(self):
        if self.play_btn.isChecked():
            self.play_btn.setText("Stop Rhythm")
            self.current_step = 0
            self.timer.start(200)
        else:
            self.play_btn.setText("Start Rhythm")
            self.timer.stop()
            for lbl in self.ogan_labels + self.drum_labels:
                lbl.setStyleSheet("background: #313244; border-radius: 4px;")

    def step(self):
        prev_step = (self.current_step - 1) % self.steps
        if self.ogan_pattern[prev_step]:
            self.ogan_labels[prev_step].setStyleSheet("background: #45475a; border-radius: 4px;")
        else:
            self.ogan_labels[prev_step].setStyleSheet("background: #313244; border-radius: 4px;")
            
        if self.drum_pattern[prev_step]:
            self.drum_labels[prev_step].setStyleSheet("background: #45475a; border-radius: 4px;")
        else:
            self.drum_labels[prev_step].setStyleSheet("background: #313244; border-radius: 4px;")

        if self.ogan_pattern[self.current_step]:
            self.audio.play_frequency(880, 100)
            self.ogan_labels[self.current_step].setStyleSheet("background: #f9e2af; border-radius: 4px;")
            
        if self.drum_pattern[self.current_step]:
            self.audio.play_frequency(150, 120)
            self.drum_labels[self.current_step].setStyleSheet("background: #89b4fa; border-radius: 4px;")
            
        self.current_step = (self.current_step + 1) % self.steps


class KecakTrainerWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.steps = 8
        self.grid_1 = [True if i % 2 == 0 else False for i in range(self.steps)]
        self.grid_2 = [True if i % 2 != 0 else False for i in range(self.steps)]
        self.grid_3 = [True if i == 2 or i == 6 else False for i in range(self.steps)]
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.current_step = 0
        
        self.buttons_1 = []
        self.buttons_2 = []
        self.buttons_3 = []
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        info = QLabel("Kecak is a Balinese chant where dozens of men interlock their voices to create a dense polyrhythm. The default pattern shows a classic interlocking rhythm.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        layout.addWidget(info)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)
        
        lbl_1 = QLabel("Voice 1 (High):")
        grid_layout.addWidget(lbl_1, 0, 0)
        for c in range(self.steps):
            btn = QPushButton()
            btn.setFixedSize(30, 30)
            btn.setCheckable(True)
            btn.setChecked(self.grid_1[c])
            btn.setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }"
                              "QPushButton:checked { background-color: #f38ba8; }")
            btn.clicked.connect(lambda checked, idx=c: self.toggle_cell(1, idx))
            grid_layout.addWidget(btn, 0, c + 1)
            self.buttons_1.append(btn)
            
        lbl_2 = QLabel("Voice 2 (Mid):")
        grid_layout.addWidget(lbl_2, 1, 0)
        for c in range(self.steps):
            btn = QPushButton()
            btn.setFixedSize(30, 30)
            btn.setCheckable(True)
            btn.setChecked(self.grid_2[c])
            btn.setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }"
                              "QPushButton:checked { background-color: #f9e2af; }")
            btn.clicked.connect(lambda checked, idx=c: self.toggle_cell(2, idx))
            grid_layout.addWidget(btn, 1, c + 1)
            self.buttons_2.append(btn)
            
        lbl_3 = QLabel("Voice 3 (Low):")
        grid_layout.addWidget(lbl_3, 2, 0)
        for c in range(self.steps):
            btn = QPushButton()
            btn.setFixedSize(30, 30)
            btn.setCheckable(True)
            btn.setChecked(self.grid_3[c])
            btn.setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }"
                              "QPushButton:checked { background-color: #89b4fa; }")
            btn.clicked.connect(lambda checked, idx=c: self.toggle_cell(3, idx))
            grid_layout.addWidget(btn, 2, c + 1)
            self.buttons_3.append(btn)
            
        layout.addLayout(grid_layout)
        
        ctrl_layout = QHBoxLayout()
        self.play_btn = QPushButton("Start Kecak")
        self.play_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #b4befe; }")
        self.play_btn.setCheckable(True)
        self.play_btn.clicked.connect(self.toggle_play)
        ctrl_layout.addWidget(self.play_btn)
        layout.addLayout(ctrl_layout)
        
        self.setLayout(layout)

    def toggle_cell(self, voice, idx):
        if voice == 1: self.grid_1[idx] = not self.grid_1[idx]
        elif voice == 2: self.grid_2[idx] = not self.grid_2[idx]
        else: self.grid_3[idx] = not self.grid_3[idx]

    def toggle_play(self):
        if self.play_btn.isChecked():
            self.play_btn.setText("Stop Kecak")
            self.current_step = 0
            self.timer.start(200)
        else:
            self.play_btn.setText("Start Kecak")
            self.timer.stop()

    def step(self):
        if self.grid_1[self.current_step]:
            self.audio.play_frequency(880, 100)
        if self.grid_2[self.current_step]:
            self.audio.play_frequency(440, 100)
        if self.grid_3[self.current_step]:
            self.audio.play_frequency(220, 150)
            
        for c in range(self.steps):
            is_current = (c == self.current_step)
            if is_current and self.grid_1[c]:
                self.buttons_1[c].setStyleSheet("QPushButton { background-color: #11111b; border: 2px solid #f38ba8; border-radius: 4px; }")
            elif self.grid_1[c]:
                self.buttons_1[c].setStyleSheet("QPushButton { background-color: #f38ba8; border-radius: 4px; }")
            else:
                self.buttons_1[c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")
            if is_current and self.grid_2[c]:
                self.buttons_2[c].setStyleSheet("QPushButton { background-color: #11111b; border: 2px solid #f9e2af; border-radius: 4px; }")
            elif self.grid_2[c]:
                self.buttons_2[c].setStyleSheet("QPushButton { background-color: #f9e2af; border-radius: 4px; }")
            else:
                self.buttons_2[c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")
            if is_current and self.grid_3[c]:
                self.buttons_3[c].setStyleSheet("QPushButton { background-color: #11111b; border: 2px solid #89b4fa; border-radius: 4px; }")
            elif self.grid_3[c]:
                self.buttons_3[c].setStyleSheet("QPushButton { background-color: #89b4fa; border-radius: 4px; }")
            else:
                self.buttons_3[c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")
                
        self.current_step = (self.current_step + 1) % self.steps


class MontunoTrainerWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.steps = 16
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.current_step = 0
        
        self.bass_pattern = [
            NOTE_FREQS["C"]/2, None, None, NOTE_FREQS["C"]/2, 
            None, NOTE_FREQS["G"]/2, None, None,
            NOTE_FREQS["C"]/2, None, None, NOTE_FREQS["C"]/2, 
            None, NOTE_FREQS["G"]/2, None, None
        ]
        self.chord_pattern = [
            None, None, [NOTE_FREQS["C"], NOTE_FREQS["E"], NOTE_FREQS["G"]], None,
            [NOTE_FREQS["C"], NOTE_FREQS["E"], NOTE_FREQS["G"]], None, None, [NOTE_FREQS["C"], NOTE_FREQS["E"], NOTE_FREQS["G"]],
            None, None, [NOTE_FREQS["C"], NOTE_FREQS["E"], NOTE_FREQS["G"]], None,
            [NOTE_FREQS["C"], NOTE_FREQS["E"], NOTE_FREQS["G"]], None, None, [NOTE_FREQS["C"], NOTE_FREQS["E"], NOTE_FREQS["G"]]
        ]
        
        self.bass_labels = []
        self.chord_labels = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        info = QLabel("The Montuno is the syncopated, repeating piano vamp that drives Salsa and Cuban music. This is a classic 2-3 pattern in C Major.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        layout.addWidget(info)

        self.play_btn = QPushButton("Start Montuno")
        self.play_btn.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #95d395; }")
        self.play_btn.setCheckable(True)
        self.play_btn.clicked.connect(self.toggle_play)
        layout.addWidget(self.play_btn)

        bass_layout = QHBoxLayout()
        lbl_b = QLabel("Left Hand (Bass):")
        lbl_b.setFixedWidth(120)
        bass_layout.addWidget(lbl_b)
        for i in range(self.steps):
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(20, 20)
            lbl.setStyleSheet("background: #313244; border-radius: 4px;")
            bass_layout.addWidget(lbl)
            self.bass_labels.append(lbl)
        layout.addLayout(bass_layout)

        chord_layout = QHBoxLayout()
        lbl_c = QLabel("Right Hand (Chord):")
        lbl_c.setFixedWidth(120)
        chord_layout.addWidget(lbl_c)
        for i in range(self.steps):
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(20, 20)
            lbl.setStyleSheet("background: #313244; border-radius: 4px;")
            chord_layout.addWidget(lbl)
            self.chord_labels.append(lbl)
        layout.addLayout(chord_layout)

        self.setLayout(layout)

    def toggle_play(self):
        if self.play_btn.isChecked():
            self.play_btn.setText("Stop Montuno")
            self.current_step = 0
            self.timer.start(200)
        else:
            self.play_btn.setText("Start Montuno")
            self.timer.stop()
            for lbl in self.bass_labels + self.chord_labels:
                lbl.setStyleSheet("background: #313244; border-radius: 4px;")

    def step(self):
        prev_step = (self.current_step - 1) % self.steps
        if self.bass_pattern[prev_step]:
            self.bass_labels[prev_step].setStyleSheet("background: #45475a; border-radius: 4px;")
        else:
            self.bass_labels[prev_step].setStyleSheet("background: #313244; border-radius: 4px;")
            
        if self.chord_pattern[prev_step]:
            self.chord_labels[prev_step].setStyleSheet("background: #45475a; border-radius: 4px;")
        else:
            self.chord_labels[prev_step].setStyleSheet("background: #313244; border-radius: 4px;")

        if self.bass_pattern[self.current_step]:
            self.audio.play_frequency(self.bass_pattern[self.current_step], 200)
            self.bass_labels[self.current_step].setStyleSheet("background: #f38ba8; border-radius: 4px;")
            
        if self.chord_pattern[self.current_step]:
            for f in self.chord_pattern[self.current_step]:
                self.audio.play_frequency(f, 200)
            self.chord_labels[self.current_step].setStyleSheet("background: #89b4fa; border-radius: 4px;")
            
        self.current_step = (self.current_step + 1) % self.steps


class InteractiveAudioWidget(QWidget):
    def __init__(self, audio_engine):
        super().__init__()
        self.audio = audio_engine
        self.piano_keys = {}
        self.balkan_timer = QTimer()
        self.balkan_timer.timeout.connect(self.balkan_beat)
        self.balkan_step, self.balkan_pattern = 0, []
        
        # Sequencer Data
        self.seq_notes = ["C (Oct)", "B", "A", "G", "F", "E", "D", "C"]
        self.seq_steps = 8
        self.seq_grid = [[False for _ in range(self.seq_steps)] for _ in range(len(self.seq_notes))]
        self.seq_timer = QTimer()
        self.seq_timer.timeout.connect(self.seq_step)
        self.seq_current_step = 0
        self.seq_bpm = 120

        # Clave Data
        self.clave_timer = QTimer()
        self.clave_timer.timeout.connect(self.clave_step)
        self.clave_step_idx = 0
        self.clave_3_2 = [1,0,0,1,0,0,1,0, 0,0,1,0,1,0,0,0]
        self.clave_2_3 = [0,0,1,0,1,0,0,0, 1,0,0,1,0,0,1,0]
        self.clave_labels = []

        # Konnakol / Tala Data
        self.tala_timer = QTimer()
        self.tala_timer.timeout.connect(self.tala_step)
        self.tala_step_idx = 0
        self.tala_syllables = ["Ta", "Ka", "Dhi", "Mi", "Tha", "Ka", "Dhi", "Mi"]
        self.tala_labels = []

        # Mbira Interlocking Data
        self.mbira_timer = QTimer()
        self.mbira_timer.timeout.connect(self.mbira_step)
        self.mbira_step_idx = 0
        self.mbira_steps = 12
        self.mbira_kushaura_notes = ["C (Oct)", "E (Oct)", "G", "C (Oct)", "E", "G"]
        self.mbira_kutsinhira_notes = ["G", "C (Oct)", "E", "G", "C (Oct)", "E (Oct)"]
        self.mbira_kushaura_labels = []
        self.mbira_kutsinhira_labels = []

        # Tango Habanera Data
        self.tango_timer = QTimer()
        self.tango_timer.timeout.connect(self.tango_step)
        self.tango_step_idx = 0
        self.tango_pattern = [1, 0, 0, 1, 0, 0, 1, 0]
        self.tango_labels = []

        # 12-Tone Matrix Data
        self.tone_row = list(range(12))
        random.shuffle(self.tone_row)
        self.tone_labels = []
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Master Volume
        vol_layout = QHBoxLayout()
        vol_layout.addWidget(QLabel("Master Volume:"))
        self.vol_slider = QSlider(Qt.Horizontal)
        self.vol_slider.setValue(80)
        self.vol_slider.setStyleSheet("QSlider::groove:horizontal { background: #313244; height: 8px; border-radius: 4px; }"
                                      "QSlider::handle:horizontal { background: #cdd6f4; width: 16px; margin: -4px 0; border-radius: 8px; }")
        self.vol_slider.valueChanged.connect(lambda v: self.audio.set_volume(v / 100.0))
        vol_layout.addWidget(self.vol_slider)
        layout.addLayout(vol_layout)

        # --- 1. Scale Explorer & Drone ---
        explorer_group = QGroupBox("Interactive Scale Explorer")
        explorer_layout = QVBoxLayout()
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Root Note:"))
        self.root_combo = QComboBox()
        self.root_combo.addItems(NOTES_ORDER)
        controls_layout.addWidget(self.root_combo)
        controls_layout.addWidget(QLabel("Scale Type:"))
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(SCALES.keys())
        controls_layout.addWidget(self.scale_combo)
        play_btn = QPushButton("Play Scale")
        play_btn.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                               "QPushButton:hover { background-color: #74c7ec; }")
        play_btn.clicked.connect(self.play_selected_scale)
        controls_layout.addWidget(play_btn)
        explorer_layout.addLayout(controls_layout)
        
        drone_layout = QHBoxLayout()
        self.drone_btn = QPushButton("Start Drone (Root + Fifth)")
        self.drone_btn.setStyleSheet("QPushButton { background-color: #313244; color: #f9e2af; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                     "QPushButton:hover { background-color: #45475a; }")
        self.drone_btn.setCheckable(True)
        self.drone_btn.clicked.connect(self.toggle_drone)
        drone_layout.addWidget(self.drone_btn)
        explorer_layout.addLayout(drone_layout)
        
        grid = QGridLayout()
        grid.setSpacing(2)
        white_notes = ["C", "D", "E", "F", "G", "A", "B", "C (Oct)"]
        black_notes = {"C#": 1, "D#": 2, "F#": 4, "G#": 5, "A#": 6}
        col = 0
        for note in white_notes:
            btn = QPushButton(note)
            btn.setFixedHeight(60)
            btn.setObjectName(note)
            btn.setStyleSheet(self.get_key_style(note, False))
            btn.clicked.connect(lambda checked, n=note: self.play_single_note(n))
            grid.addWidget(btn, 0, col, 1, 1)
            self.piano_keys[note] = btn
            col += 1
        for note, pos in black_notes.items():
            btn = QPushButton(note)
            btn.setFixedHeight(40)
            btn.setObjectName(note)
            btn.setStyleSheet(self.get_key_style(note, True))
            btn.clicked.connect(lambda checked, n=note: self.play_single_note(n))
            grid.addWidget(btn, 0, pos - 1, 1, 2, alignment=Qt.AlignTop | Qt.AlignHCenter)
            self.piano_keys[note] = btn
        explorer_layout.addLayout(grid)
        explorer_group.setLayout(explorer_layout)
        layout.addWidget(explorer_group)

        self.root_combo.currentTextChanged.connect(self.highlight_scale)
        self.scale_combo.currentTextChanged.connect(self.highlight_scale)
        self.highlight_scale()

        # --- 2. Txalaparta Trainer (Basque) ---
        txalaparta_group = QGroupBox("Txalaparta Interlocking Trainer (Basque)")
        txalaparta_layout = QVBoxLayout()
        txalaparta_layout.addWidget(TxalapartaWidget(self.audio))
        txalaparta_group.setLayout(txalaparta_layout)
        layout.addWidget(txalaparta_group)

        # --- 3. Haitian Vodou Rhythm Trainer ---
        vodou_group = QGroupBox("Haitian Vodou Rhythm Trainer")
        vodou_layout = QVBoxLayout()
        vodou_layout.addWidget(VodouRhythmWidget(self.audio))
        vodou_group.setLayout(vodou_layout)
        layout.addWidget(vodou_group)

        # --- 4. Kecak Trainer (Balinese) ---
        kecak_group = QGroupBox("Kecak Interlocking Trainer (Balinese)")
        kecak_layout = QVBoxLayout()
        kecak_layout.addWidget(KecakTrainerWidget(self.audio))
        kecak_group.setLayout(kecak_layout)
        layout.addWidget(kecak_group)

        # --- 5. Montuno Trainer (Cuban Salsa) ---
        montuno_group = QGroupBox("Montuno Piano Trainer (Cuban Son / Salsa)")
        montuno_layout = QVBoxLayout()
        montuno_layout.addWidget(MontunoTrainerWidget(self.audio))
        montuno_group.setLayout(montuno_layout)
        layout.addWidget(montuno_group)

        # --- 6. Overtone Singer Simulator ---
        overtone_singer_group = QGroupBox("Overtone Singer Simulator (Tuvan/Tibetan)")
        overtone_singer_layout = QVBoxLayout()
        overtone_singer_layout.addWidget(OvertoneSingerWidget(self.audio))
        overtone_singer_group.setLayout(overtone_singer_layout)
        layout.addWidget(overtone_singer_group)

        # --- 7. Hocketing Sequencer ---
        hocketing_group = QGroupBox("Hocketing Sequencer (Medieval/Andean)")
        hocketing_layout = QVBoxLayout()
        hocketing_layout.addWidget(HocketingSequencerWidget(self.audio))
        hocketing_group.setLayout(hocketing_layout)
        layout.addWidget(hocketing_group)

        # --- 8. Diatonic Chord Function Builder ---
        diatonic_group = QGroupBox("Diatonic Chord Function Builder (Western Harmony)")
        diatonic_layout = QVBoxLayout()
        diatonic_info = QLabel("Select a Key and Mode to generate the 7 diatonic triads. Click a Roman numeral to hear the chord.")
        diatonic_info.setWordWrap(True)
        diatonic_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        diatonic_layout.addWidget(diatonic_info)
        diatonic_layout.addWidget(DiatonicChordWidget(self.audio))
        diatonic_group.setLayout(diatonic_layout)
        layout.addWidget(diatonic_group)

        # --- 9. 12-Tone Matrix Generator (Serialism) ---
        matrix_group = QGroupBox("12-Tone Matrix Generator (Serialism)")
        matrix_layout = QVBoxLayout()
        matrix_info = QLabel("Serialism uses all 12 pitches equally, avoiding any tonal center. 'Generate' creates a random Tone Row (P0). The grid shows Inversions (I0) and Retrogrades (R0).")
        matrix_info.setWordWrap(True)
        matrix_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        matrix_layout.addWidget(matrix_info)

        matrix_ctrl_layout = QHBoxLayout()
        gen_btn = QPushButton("Generate New Row")
        gen_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                              "QPushButton:hover { background-color: #b4befe; }")
        gen_btn.clicked.connect(self.generate_tone_row)
        matrix_ctrl_layout.addWidget(gen_btn)

        play_p0_btn = QPushButton("Play Prime (P0)")
        play_p0_btn.setStyleSheet("QPushButton { background-color: #313244; color: #cdd6f4; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                  "QPushButton:hover { background-color: #45475a; }")
        play_p0_btn.clicked.connect(lambda: self.play_tone_row("P0"))
        matrix_ctrl_layout.addWidget(play_p0_btn)

        play_i0_btn = QPushButton("Play Inversion (I0)")
        play_i0_btn.setStyleSheet("QPushButton { background-color: #313244; color: #cdd6f4; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                  "QPushButton:hover { background-color: #45475a; }")
        play_i0_btn.clicked.connect(lambda: self.play_tone_row("I0"))
        matrix_ctrl_layout.addWidget(play_i0_btn)
        matrix_layout.addLayout(matrix_ctrl_layout)

        matrix_grid_layout = QGridLayout()
        matrix_grid_layout.setSpacing(2)
        for r in range(12):
            row_labels = []
            for c in range(12):
                lbl = QLabel("")
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFixedSize(28, 28)
                lbl.setStyleSheet("background: #313244; color: #cdd6f4; border-radius: 4px;")
                matrix_grid_layout.addWidget(lbl, r, c)
                row_labels.append(lbl)
            self.tone_labels.append(row_labels)
        matrix_layout.addLayout(matrix_grid_layout)
        matrix_group.setLayout(matrix_layout)
        layout.addWidget(matrix_group)
        self.generate_tone_row()

        # --- 10. Mbira Interlocking Simulator (Shona) ---
        mbira_group = QGroupBox("Mbira Interlocking Simulator (Shona - Zimbabwe)")
        mbira_layout = QVBoxLayout()
        mbira_info = QLabel("Shona music features interlocking melodies. 'Kushaura' (lead) plays on the main beats, while 'Kutsinhira' (follower) plays on the off-beats, creating a continuous, cascading ripple.")
        mbira_info.setWordWrap(True)
        mbira_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        mbira_layout.addWidget(mbira_info)

        self.mbira_btn = QPushButton("Start Mbira Pattern")
        self.mbira_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                     "QPushButton:hover { background-color: #b4befe; }")
        self.mbira_btn.setCheckable(True)
        self.mbira_btn.clicked.connect(self.toggle_mbira)
        mbira_layout.addWidget(self.mbira_btn)

        kushaura_layout = QHBoxLayout()
        kushaura_lbl = QLabel("Kushaura:")
        kushaura_lbl.setFixedWidth(80)
        kushaura_layout.addWidget(kushaura_lbl)
        for i in range(self.mbira_steps):
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(24, 24)
            lbl.setStyleSheet("background: #313244; border-radius: 4px;")
            kushaura_layout.addWidget(lbl)
            self.mbira_kushaura_labels.append(lbl)
        mbira_layout.addLayout(kushaura_layout)

        kutsinhira_layout = QHBoxLayout()
        kutsinhira_lbl = QLabel("Kutsinhira:")
        kutsinhira_lbl.setFixedWidth(80)
        kutsinhira_layout.addWidget(kutsinhira_lbl)
        for i in range(self.mbira_steps):
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(24, 24)
            lbl.setStyleSheet("background: #313244; border-radius: 4px;")
            kutsinhira_layout.addWidget(lbl)
            self.mbira_kutsinhira_labels.append(lbl)
        mbira_layout.addLayout(kutsinhira_layout)
        mbira_group.setLayout(mbira_layout)
        layout.addWidget(mbira_group)

        # --- 11. Argentine Tango Rhythm Trainer ---
        tango_group = QGroupBox("Argentine Tango Habanera Trainer")
        tango_layout = QVBoxLayout()
        tango_info = QLabel("The Habanera rhythm is a 3-3-2 syncopated pattern (often felt as 'dum-dum-dum') that is the rhythmic backbone of Tango.")
        tango_info.setWordWrap(True)
        tango_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        tango_layout.addWidget(tango_info)

        self.tango_btn = QPushButton("Start Habanera")
        self.tango_btn.setStyleSheet("QPushButton { background-color: #f9e2af; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                     "QPushButton:hover { background-color: #e6cc87; }")
        self.tango_btn.setCheckable(True)
        self.tango_btn.clicked.connect(self.toggle_tango)
        tango_layout.addWidget(self.tango_btn)

        tango_visual = QHBoxLayout()
        for i in range(8):
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(30, 30)
            lbl.setStyleSheet("background: #313244; border-radius: 4px;")
            tango_visual.addWidget(lbl)
            self.tango_labels.append(lbl)
        tango_layout.addLayout(tango_visual)
        tango_group.setLayout(tango_layout)
        layout.addWidget(tango_group)

        # --- 12. Western Cadence Trainer ---
        cadence_group = QGroupBox("Western Cadence Trainer")
        cadence_layout = QVBoxLayout()
        cadence_info = QLabel("Cadences are chord progressions that end a musical phrase. Click to hear the four main types:")
        cadence_info.setWordWrap(True)
        cadence_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        cadence_layout.addWidget(cadence_info)

        cadence_btns_layout = QHBoxLayout()
        for name in CADENCES.keys():
            btn = QPushButton(name)
            btn.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                              "QPushButton:hover { background-color: #74c7ec; }")
            btn.clicked.connect(lambda checked, n=name: self.play_cadence(n))
            cadence_btns_layout.addWidget(btn)
        cadence_layout.addLayout(cadence_btns_layout)
        cadence_group.setLayout(cadence_layout)
        layout.addWidget(cadence_group)

        # --- 13. Musical Texture Trainer ---
        texture_group = QGroupBox("Musical Texture Trainer")
        texture_layout = QVBoxLayout()
        tex_info = QLabel("Texture defines how melodic lines interact. Click to hear a C major scale played in different textures:")
        tex_info.setWordWrap(True)
        tex_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        texture_layout.addWidget(tex_info)

        tex_btns_layout = QHBoxLayout()
        tex_mono_btn = QPushButton("Monophony (Solo)")
        tex_mono_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                   "QPushButton:hover { background-color: #b4befe; }")
        tex_mono_btn.clicked.connect(lambda: self.play_texture("mono"))
        tex_btns_layout.addWidget(tex_mono_btn)

        tex_hetero_btn = QPushButton("Heterophony (Decorated)")
        tex_hetero_btn.setStyleSheet("QPushButton { background-color: #f9e2af; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                     "QPushButton:hover { background-color: #e6cc87; }")
        tex_hetero_btn.clicked.connect(lambda: self.play_texture("hetero"))
        tex_btns_layout.addWidget(tex_hetero_btn)

        tex_poly_btn = QPushButton("Polyphony (Independent)")
        tex_poly_btn.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                   "QPushButton:hover { background-color: #95d395; }")
        tex_poly_btn.clicked.connect(lambda: self.play_texture("poly"))
        tex_btns_layout.addWidget(tex_poly_btn)
        texture_layout.addLayout(tex_btns_layout)
        texture_group.setLayout(texture_layout)
        layout.addWidget(texture_group)

        # --- 14. Sidechain Pumping Simulator (EDM) ---
        edm_group = QGroupBox("Sidechain Pumping Simulator (EDM)")
        edm_layout = QVBoxLayout()
        edm_info = QLabel("Sidechain compression is the 'pumping' volume effect caused by a kick drum in modern House/EDM music. Start the drone, then toggle the pump!")
        edm_info.setWordWrap(True)
        edm_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        edm_layout.addWidget(edm_info)

        self.sidechain_btn = QPushButton("Start Sidechain Pump (Requires Drone)")
        self.sidechain_btn.setStyleSheet("QPushButton { background-color: #313244; color: #f38ba8; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                         "QPushButton:hover { background-color: #45475a; }")
        self.sidechain_btn.setCheckable(True)
        self.sidechain_btn.clicked.connect(self.toggle_sidechain)
        edm_layout.addWidget(self.sidechain_btn)
        edm_group.setLayout(edm_layout)
        layout.addWidget(edm_group)

        # --- 15. Latin Clave Trainer ---
        clave_group = QGroupBox("Latin Clave Trainer (Afro-Cuban)")
        clave_layout = QVBoxLayout()
        clave_ctrl = QHBoxLayout()
        self.clave_combo = QComboBox()
        self.clave_combo.addItems(["3-2 Son Clave", "2-3 Son Clave"])
        clave_ctrl.addWidget(self.clave_combo)
        
        self.clave_btn = QPushButton("Start Clave")
        self.clave_btn.setStyleSheet("QPushButton { background-color: #f9e2af; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                     "QPushButton:hover { background-color: #e6cc87; }")
        self.clave_btn.setCheckable(True)
        self.clave_btn.clicked.connect(self.toggle_clave)
        clave_ctrl.addWidget(self.clave_btn)
        clave_layout.addLayout(clave_ctrl)

        clave_visual = QHBoxLayout()
        for i in range(16):
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(24, 24)
            lbl.setStyleSheet("background: #313244; border-radius: 4px;")
            clave_visual.addWidget(lbl)
            self.clave_labels.append(lbl)
        clave_layout.addLayout(clave_visual)
        clave_group.setLayout(clave_layout)
        layout.addWidget(clave_group)

        # --- 16. Konnakol / Tala Trainer (Karnatic) ---
        tala_group = QGroupBox("Konnakol / Tala Trainer (South Indian)")
        tala_layout = QVBoxLayout()
        tala_info = QLabel("Adi Tala is an 8-beat rhythmic cycle. Konnakol is the vocalization of these rhythms. Press start to hear the syllables.")
        tala_info.setWordWrap(True)
        tala_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        tala_layout.addWidget(tala_info)
        
        self.tala_btn = QPushButton("Start Adi Tala")
        self.tala_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #b4befe; }")
        self.tala_btn.setCheckable(True)
        self.tala_btn.clicked.connect(self.toggle_tala)
        tala_layout.addWidget(self.tala_btn)

        tala_visual = QHBoxLayout()
        for syl in self.tala_syllables:
            lbl = QLabel(syl)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(50, 40)
            lbl.setStyleSheet("background: #313244; color: #cdd6f4; border-radius: 4px; font-weight: bold;")
            tala_visual.addWidget(lbl)
            self.tala_labels.append(lbl)
        tala_layout.addLayout(tala_visual)
        tala_group.setLayout(tala_layout)
        layout.addWidget(tala_group)

        # --- 17. 8-Step Melody Sequencer ---
        seq_group = QGroupBox("8-Step Melody Sequencer (C Major)")
        seq_layout = QVBoxLayout()
        seq_grid_layout = QGridLayout()
        seq_grid_layout.setSpacing(2)
        
        self.seq_buttons = []
        for r, note in enumerate(self.seq_notes):
            lbl = QLabel(note)
            lbl.setFixedWidth(50)
            seq_grid_layout.addWidget(lbl, r, 0)
            
            row_buttons = []
            for c in range(self.seq_steps):
                btn = QPushButton()
                btn.setFixedSize(40, 30)
                btn.setCheckable(True)
                btn.setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }"
                                  "QPushButton:checked { background-color: #a6e3a1; }")
                btn.clicked.connect(lambda checked, row=r, col=c: self.toggle_seq_cell(row, col))
                seq_grid_layout.addWidget(btn, r, c + 1)
                row_buttons.append(btn)
            self.seq_buttons.append(row_buttons)
            
        seq_layout.addLayout(seq_grid_layout)
        
        seq_ctrl_layout = QHBoxLayout()
        self.seq_play_btn = QPushButton("Play Sequence")
        self.seq_play_btn.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                        "QPushButton:hover { background-color: #74c7ec; }")
        self.seq_play_btn.setCheckable(True)
        self.seq_play_btn.clicked.connect(self.toggle_seq)
        seq_ctrl_layout.addWidget(self.seq_play_btn)
        
        seq_clear_btn = QPushButton("Clear")
        seq_clear_btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #eb7d99; }")
        seq_clear_btn.clicked.connect(self.clear_seq)
        seq_ctrl_layout.addWidget(seq_clear_btn)

        seq_ctrl_layout.addWidget(QLabel("BPM:"))
        self.bpm_slider = QSlider(Qt.Horizontal)
        self.bpm_slider.setMinimum(60)
        self.bpm_slider.setMaximum(240)
        self.bpm_slider.setValue(120)
        self.bpm_slider.valueChanged.connect(self.update_seq_bpm)
        seq_ctrl_layout.addWidget(self.bpm_slider)
        self.bpm_label = QLabel("120")
        self.bpm_label.setFixedWidth(30)
        seq_ctrl_layout.addWidget(self.bpm_label)
        
        seq_layout.addLayout(seq_ctrl_layout)
        seq_group.setLayout(seq_layout)
        layout.addWidget(seq_group)

        # --- 18. Phase Shifter (Minimalism) ---
        phase_group = QGroupBox("Phase Shifter (Minimalism - Steve Reich)")
        phase_layout = QVBoxLayout()
        phase_layout.addWidget(PhaseShifterWidget(self.audio))
        phase_group.setLayout(phase_layout)
        layout.addWidget(phase_group)

        # --- 19. Chord & Progression Builder ---
        chord_group = QGroupBox("Chord & Progression Builder (Altered Chords & Secondary Dominants)")
        chord_layout = QVBoxLayout()
        chord_ctrl_layout = QHBoxLayout()
        chord_ctrl_layout.addWidget(QLabel("Root:"))
        self.chord_root_combo = QComboBox()
        self.chord_root_combo.addItems(NOTES_ORDER)
        chord_ctrl_layout.addWidget(self.chord_root_combo)
        chord_ctrl_layout.addWidget(QLabel("Chord:"))
        self.chord_type_combo = QComboBox()
        self.chord_type_combo.addItems(CHORDS.keys())
        chord_ctrl_layout.addWidget(self.chord_type_combo)
        
        chord_ctrl_layout.addWidget(QLabel("Inversion:"))
        self.inversion_combo = QComboBox()
        self.inversion_combo.addItems(["Root Position", "1st Inversion", "2nd Inversion"])
        chord_ctrl_layout.addWidget(self.inversion_combo)
        
        play_chord_btn = QPushButton("Play Chord")
        play_chord_btn.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                     "QPushButton:hover { background-color: #95d395; }")
        play_chord_btn.clicked.connect(self.play_chord)
        chord_ctrl_layout.addWidget(play_chord_btn)
        chord_layout.addLayout(chord_ctrl_layout)
        
        self.chord_info_label = QLabel("Chord Notes: -")
        self.chord_info_label.setStyleSheet("color: #f9e2af; font-weight: bold; padding: 5px;")
        chord_layout.addWidget(self.chord_info_label)

        prog_layout = QHBoxLayout()
        prog_layout.addWidget(QLabel("Progression:"))
        self.prog_combo = QComboBox()
        self.prog_combo.addItems(PROGRESSIONS.keys())
        prog_layout.addWidget(self.prog_combo)
        play_prog_btn = QPushButton("Play Progression")
        play_prog_btn.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #95d395; }")
        play_prog_btn.clicked.connect(self.play_progression)
        prog_layout.addWidget(play_prog_btn)
        chord_layout.addLayout(prog_layout)

        custom_prog_layout = QVBoxLayout()
        custom_prog_layout.addWidget(QLabel("Build Your Own 4-Chord Loop:"))
        custom_row_layout = QHBoxLayout()
        self.custom_roots = []
        self.custom_types = []
        for i in range(4):
            r_combo = QComboBox()
            r_combo.addItems(NOTES_ORDER)
            custom_row_layout.addWidget(r_combo)
            self.custom_roots.append(r_combo)
            
            t_combo = QComboBox()
            t_combo.addItems(CHORDS.keys())
            custom_row_layout.addWidget(t_combo)
            self.custom_types.append(t_combo)
            
            if i < 3:
                arrow = QLabel("➝")
                arrow.setAlignment(Qt.AlignCenter)
                custom_row_layout.addWidget(arrow)
                
        custom_prog_layout.addLayout(custom_row_layout)
        
        play_custom_btn = QPushButton("Play Custom Loop")
        play_custom_btn.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                      "QPushButton:hover { background-color: #74c7ec; }")
        play_custom_btn.clicked.connect(self.play_custom_progression)
        custom_prog_layout.addWidget(play_custom_btn)
        
        chord_layout.addLayout(custom_prog_layout)
        chord_group.setLayout(chord_layout)
        layout.addWidget(chord_group)

        # --- 20. Tuning System Comparator ---
        tuning_group = QGroupBox("Tuning System Comparator (Just vs Equal)")
        tuning_layout = QVBoxLayout()
        tuning_info = QLabel("Western instruments use 'Equal Temperament' (slightly out of tune so all keys work). 'Just Intonation' uses pure physics. Compare a C Major chord in both:")
        tuning_info.setWordWrap(True)
        tuning_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        tuning_layout.addWidget(tuning_info)

        tuning_btns_layout = QHBoxLayout()
        play_equal_btn = QPushButton("Play Equal Temperament (C, E, G)")
        play_equal_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                     "QPushButton:hover { background-color: #b4befe; }")
        play_equal_btn.clicked.connect(lambda: self.play_tuning("equal"))
        tuning_btns_layout.addWidget(play_equal_btn)

        play_just_btn = QPushButton("Play Just Intonation (C, E, G)")
        play_just_btn.setStyleSheet("QPushButton { background-color: #f9e2af; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                    "QPushButton:hover { background-color: #e6cc87; }")
        play_just_btn.clicked.connect(lambda: self.play_tuning("just"))
        tuning_btns_layout.addWidget(play_just_btn)
        tuning_layout.addLayout(tuning_btns_layout)
        tuning_group.setLayout(tuning_layout)
        layout.addWidget(tuning_group)

        # --- 21. Overtone Series Visualizer ---
        overtone_group = QGroupBox("Overtone Series Visualizer (Acoustic Foundation)")
        overtone_layout = QVBoxLayout()
        overtone_info = QLabel("The Overtone Series is nature's built-in harmony. Every pitch contains these hidden frequencies. Press play to hear why the Major chord is natural to human hearing.")
        overtone_info.setWordWrap(True)
        overtone_info.setStyleSheet("color: #a6adc8; font-size: 12px;")
        overtone_layout.addWidget(overtone_info)

        self.overtone_labels = []
        overtone_lights_layout = QHBoxLayout()
        for name, freq in OVERTONES:
            lbl = QLabel(name.split(" ")[0])
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 16px; border-radius: 4px; font-weight: bold;")
            overtone_lights_layout.addWidget(lbl)
            self.overtone_labels.append(lbl)
        overtone_layout.addLayout(overtone_lights_layout)

        play_ot_btn = QPushButton("Play Overtone Series")
        play_ot_btn.setStyleSheet("QPushButton { background-color: #cba6f7; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                  "QPushButton:hover { background-color: #b4befe; }")
        play_ot_btn.clicked.connect(self.play_overtones)
        overtone_layout.addWidget(play_ot_btn)
        overtone_group.setLayout(overtone_layout)
        layout.addWidget(overtone_group)

        # --- 22. Microtonal Slider ---
        micro_group = QGroupBox("Microtonal Slider (Eastern / Quarter Tones)")
        micro_layout = QVBoxLayout()
        self.micro_slider = QSlider(Qt.Horizontal)
        self.micro_slider.setMinimum(0)
        self.micro_slider.setMaximum(100)
        self.micro_slider.setValue(0)
        self.micro_slider.setStyleSheet("QSlider::groove:horizontal { background: #313244; height: 8px; border-radius: 4px; }"
                                        "QSlider::handle:horizontal { background: #f38ba8; width: 16px; margin: -4px 0; border-radius: 8px; }")
        self.micro_slider.valueChanged.connect(self.update_micro_label)
        micro_layout.addWidget(self.micro_slider)
        self.micro_freq_label = QLabel("Frequency: 261.63 Hz (Note: C)")
        self.micro_freq_label.setStyleSheet("font-weight: bold; color: #f38ba8;")
        micro_layout.addWidget(self.micro_freq_label)
        play_micro_btn = QPushButton("Play Microtone")
        play_micro_btn.setStyleSheet("QPushButton { background-color: #313244; color: #cdd6f4; padding: 8px; border-radius: 4px; }"
                                     "QPushButton:hover { background-color: #45475a; }")
        play_micro_btn.clicked.connect(self.play_microtone)
        micro_layout.addWidget(play_micro_btn)
        micro_group.setLayout(micro_layout)
        layout.addWidget(micro_group)

        # --- 23. Asymmetric Rhythm Trainer (Balkan) ---
        balkan_group = QGroupBox("Asymmetric Rhythm Trainer (Balkan / Aksak)")
        balkan_layout = QVBoxLayout()
        balkan_ctrl_layout = QHBoxLayout()
        balkan_ctrl_layout.addWidget(QLabel("Meter:"))
        self.balkan_combo = QComboBox()
        self.balkan_combo.addItems(["4/4 (2+2+2+2)", "7/8 (2+2+3)", "9/8 (2+2+2+3)"])
        balkan_ctrl_layout.addWidget(self.balkan_combo)
        balkan_layout.addLayout(balkan_ctrl_layout)
        self.balkan_btn = QPushButton("Start Rhythm")
        self.balkan_btn.setStyleSheet("QPushButton { background-color: #f9e2af; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                      "QPushButton:hover { background-color: #e6cc87; }")
        self.balkan_btn.setCheckable(True)
        self.balkan_btn.clicked.connect(self.toggle_balkan)
        balkan_layout.addWidget(self.balkan_btn)
        self.balkan_visual_label = QLabel("Ready...")
        self.balkan_visual_label.setAlignment(Qt.AlignCenter)
        self.balkan_visual_label.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 20px; border-radius: 4px;")
        balkan_layout.addWidget(self.balkan_visual_label)
        balkan_group.setLayout(balkan_layout)
        layout.addWidget(balkan_group)

        # --- 24. Polyrhythm Trainer (African) ---
        rhythm_group = QGroupBox("Polyrhythm Trainer (African 3 against 2)")
        rhythm_layout = QVBoxLayout()
        self.rhythm_timer_2 = QTimer()
        self.rhythm_timer_2.timeout.connect(lambda: self.play_rhythm_click(440, 0))
        self.rhythm_timer_3 = QTimer()
        self.rhythm_timer_3.timeout.connect(lambda: self.play_rhythm_click(330, 1))
        controls_layout = QHBoxLayout()
        self.rhythm_btn = QPushButton("Start Polyrhythm")
        self.rhythm_btn.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }"
                                      "QPushButton:hover { background-color: #95d395; }")
        self.rhythm_btn.setCheckable(True)
        self.rhythm_btn.clicked.connect(self.toggle_rhythm)
        controls_layout.addWidget(self.rhythm_btn)
        rhythm_layout.addLayout(controls_layout)
        lights_layout = QHBoxLayout()
        self.light_2 = QLabel("2: -")
        self.light_2.setAlignment(Qt.AlignCenter)
        self.light_2.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 20px; border-radius: 4px;")
        self.light_3 = QLabel("3: -")
        self.light_3.setAlignment(Qt.AlignCenter)
        self.light_3.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 20px; border-radius: 4px;")
        lights_layout.addWidget(self.light_2)
        lights_layout.addWidget(self.light_3)
        rhythm_layout.addLayout(lights_layout)
        rhythm_group.setLayout(rhythm_layout)
        layout.addWidget(rhythm_group)

        self.setLayout(layout)

    def get_key_style(self, note, is_black):
        if is_black:
            return "QPushButton { background-color: #11111b; color: #cdd6f4; font-weight: bold; border-radius: 4px; font-size: 12px; }"
        return "QPushButton { background-color: #cdd6f4; color: #11111b; font-weight: bold; border-radius: 4px; font-size: 14px; }"

    def highlight_scale(self):
        root = self.root_combo.currentText()
        scale_name = self.scale_combo.currentText()
        intervals = SCALES[scale_name]
        root_idx = NOTES_ORDER.index(root)
        scale_notes = [(NOTES_ORDER[(root_idx + interval) % 12]) for interval in intervals]
        for note, btn in self.piano_keys.items():
            base_note = note.replace(" (Oct)", "")
            is_black = "#" in base_note
            if base_note == root:
                btn.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; font-weight: bold; border-radius: 4px; }")
            elif base_note in scale_notes:
                btn.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; font-weight: bold; border-radius: 4px; }")
            else:
                btn.setStyleSheet(self.get_key_style(base_note, is_black))

    def toggle_drone(self):
        if self.drone_btn.isChecked():
            self.audio.start_drone(self.root_combo.currentText())
            self.drone_btn.setText("Stop Drone")
            self.drone_btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }")
        else:
            self.audio.stop_drone()
            self.drone_btn.setText("Start Drone (Root + Fifth)")
            self.drone_btn.setStyleSheet("QPushButton { background-color: #313244; color: #f9e2af; padding: 8px; font-weight: bold; border-radius: 4px; }")

    def play_single_note(self, note):
        self.audio.play_frequency(NOTE_FREQS[note], 500)

    def play_selected_scale(self):
        root = self.root_combo.currentText()
        intervals = SCALES[self.scale_combo.currentText()]
        root_idx = NOTES_ORDER.index(root)
        notes_to_play = [NOTES_ORDER[(root_idx + interval) % 12] for interval in intervals]
        notes_to_play.append(root + " (Oct)")
        def play_in_thread():
            for note in notes_to_play:
                self.audio.play_frequency(NOTE_FREQS[note], 400)
                time.sleep(0.4)
        threading.Thread(target=play_in_thread, daemon=True).start()

    # --- 12-Tone Logic ---
    def generate_tone_row(self):
        random.shuffle(self.tone_row)
        self.inv_row = [(-n) % 12 for n in self.tone_row]
        
        for r in range(12):
            for c in range(12):
                if r == 0:
                    val = self.tone_row[c]
                else:
                    val = (self.inv_row[c] + r) % 12
                self.tone_labels[r][c].setText(str(val))

    def play_tone_row(self, row_type):
        if row_type == "P0":
            row = self.tone_row
        else:
            row = self.inv_row
            
        def play_in_thread():
            for i, n in enumerate(row):
                self.audio.play_frequency(NOTE_FREQS[NOTES_ORDER[n]], 300)
                self.tone_labels[0 if row_type == "P0" else 1][i].setStyleSheet("background: #89b4fa; color: #11111b; border-radius: 4px; font-weight: bold;")
                time.sleep(0.25)
                self.tone_labels[0 if row_type == "P0" else 1][i].setStyleSheet("background: #313244; color: #cdd6f4; border-radius: 4px;")
        threading.Thread(target=play_in_thread, daemon=True).start()

    # --- Mbira Logic ---
    def toggle_mbira(self):
        if self.mbira_btn.isChecked():
            self.mbira_btn.setText("Stop Mbira Pattern")
            self.mbira_step_idx = 0
            self.mbira_timer.start(150)
        else:
            self.mbira_btn.setText("Start Mbira Pattern")
            self.mbira_timer.stop()
            for lbl in self.mbira_kushaura_labels + self.mbira_kutsinhira_labels:
                lbl.setStyleSheet("background: #313244; border-radius: 4px;")

    def mbira_step(self):
        prev_step = (self.mbira_step_idx - 1) % self.mbira_steps
        self.mbira_kushaura_labels[prev_step].setStyleSheet("background: #313244; border-radius: 4px;")
        self.mbira_kutsinhira_labels[prev_step].setStyleSheet("background: #313244; border-radius: 4px;")

        if self.mbira_step_idx % 2 == 0:
            note_idx = self.mbira_step_idx // 2
            note = self.mbira_kushaura_notes[note_idx]
            self.audio.play_frequency(NOTE_FREQS[note], 200)
            self.mbira_kushaura_labels[self.mbira_step_idx].setStyleSheet("background: #cba6f7; border-radius: 4px;")
        else:
            note_idx = self.mbira_step_idx // 2
            note = self.mbira_kutsinhira_notes[note_idx]
            self.audio.play_frequency(NOTE_FREQS[note], 200)
            self.mbira_kutsinhira_labels[self.mbira_step_idx].setStyleSheet("background: #89b4fa; border-radius: 4px;")
            
        self.mbira_step_idx = (self.mbira_step_idx + 1) % self.mbira_steps

    # --- Tango Logic ---
    def toggle_tango(self):
        if self.tango_btn.isChecked():
            self.tango_btn.setText("Stop Habanera")
            self.tango_step_idx = 0
            self.tango_timer.start(250)
        else:
            self.tango_btn.setText("Start Habanera")
            self.tango_timer.stop()
            for lbl in self.tango_labels:
                lbl.setStyleSheet("background: #313244; border-radius: 4px;")

    def tango_step(self):
        is_hit = self.tango_pattern[self.tango_step_idx] == 1
        
        for i, lbl in enumerate(self.tango_labels):
            if self.tango_pattern[i] == 1:
                lbl.setStyleSheet("background: #45475a; border-radius: 4px;")
            else:
                lbl.setStyleSheet("background: #313244; border-radius: 4px;")
                
        if is_hit:
            self.audio.play_frequency(440, 100)
            self.tango_labels[self.tango_step_idx].setStyleSheet("background: #f9e2af; border-radius: 4px;")
        else:
            self.tango_labels[self.tango_step_idx].setStyleSheet("background: #89b4fa; border-radius: 4px;")
            
        self.tango_step_idx = (self.tango_step_idx + 1) % 8

    # --- Cadence Logic ---
    def play_cadence(self, cadence_name):
        progression = CADENCES[cadence_name]
        def play_in_thread():
            for root, chord_type in progression:
                intervals = CHORDS[chord_type]
                root_idx = NOTES_ORDER.index(root)
                notes_to_play = []
                for interval in intervals:
                    note_idx = (root_idx + interval) % 12
                    notes_to_play.append(NOTE_FREQS[NOTES_ORDER[note_idx]])
                for f in notes_to_play:
                    self.audio.play_frequency(f, 900)
                time.sleep(1.0)
        threading.Thread(target=play_in_thread, daemon=True).start()

    # --- Sequencer Logic ---
    def toggle_seq_cell(self, row, col):
        self.seq_grid[row][col] = not self.seq_grid[row][col]

    def clear_seq(self):
        for r in range(len(self.seq_notes)):
            for c in range(self.seq_steps):
                self.seq_grid[r][c] = False
                self.seq_buttons[r][c].setChecked(False)

    def update_seq_bpm(self, val):
        self.seq_bpm = val
        self.bpm_label.setText(str(val))
        if self.seq_timer.isActive():
            self.seq_timer.start(int(60000 / (self.seq_bpm * 2)))

    def toggle_seq(self):
        if self.seq_play_btn.isChecked():
            self.seq_play_btn.setText("Stop Sequence")
            self.seq_current_step = 0
            self.seq_timer.start(int(60000 / (self.seq_bpm * 2)))
        else:
            self.seq_play_btn.setText("Play Sequence")
            self.seq_timer.stop()
            for r in range(len(self.seq_notes)):
                for c in range(self.seq_steps):
                    if self.seq_grid[r][c]:
                        self.seq_buttons[r][c].setStyleSheet("QPushButton { background-color: #a6e3a1; border-radius: 4px; }")

    def seq_step(self):
        for r in range(len(self.seq_notes)):
            if self.seq_grid[r][self.seq_current_step]:
                note = self.seq_notes[r]
                self.audio.play_frequency(NOTE_FREQS[note], 250)
            
            for c in range(self.seq_steps):
                if c == self.seq_current_step:
                    self.seq_buttons[r][c].setStyleSheet("QPushButton { background-color: #89b4fa; border-radius: 4px; border: 2px solid #11111b; }")
                elif self.seq_grid[r][c]:
                    self.seq_buttons[r][c].setStyleSheet("QPushButton { background-color: #a6e3a1; border-radius: 4px; }")
                else:
                    self.seq_buttons[r][c].setStyleSheet("QPushButton { background-color: #313244; border-radius: 4px; }")
                    
        self.seq_current_step = (self.seq_current_step + 1) % self.seq_steps

    # --- Clave Logic ---
    def toggle_clave(self):
        if self.clave_btn.isChecked():
            self.clave_btn.setText("Stop Clave")
            self.clave_step_idx = 0
            self.clave_timer.start(250)
        else:
            self.clave_btn.setText("Start Clave")
            self.clave_timer.stop()
            for lbl in self.clave_labels:
                lbl.setStyleSheet("background: #313244; border-radius: 4px;")

    def clave_step(self):
        pattern = self.clave_3_2 if "3-2" in self.clave_combo.currentText() else self.clave_2_3
        is_hit = pattern[self.clave_step_idx] == 1
        
        for i, lbl in enumerate(self.clave_labels):
            if pattern[i] == 1:
                lbl.setStyleSheet("background: #45475a; border-radius: 4px;")
            else:
                lbl.setStyleSheet("background: #313244; border-radius: 4px;")
                
        if is_hit:
            self.audio.play_frequency(523.25, 100)
            self.clave_labels[self.clave_step_idx].setStyleSheet("background: #f9e2af; border-radius: 4px;")
        else:
            self.clave_labels[self.clave_step_idx].setStyleSheet("background: #89b4fa; border-radius: 4px;")
            
        self.clave_step_idx = (self.clave_step_idx + 1) % 16

    # --- Tala / Konnakol Logic ---
    def toggle_tala(self):
        if self.tala_btn.isChecked():
            self.tala_btn.setText("Stop Adi Tala")
            self.tala_step_idx = 0
            self.tala_timer.start(250)
        else:
            self.tala_btn.setText("Start Adi Tala")
            self.tala_timer.stop()
            for lbl in self.tala_labels:
                lbl.setStyleSheet("background: #313244; color: #cdd6f4; border-radius: 4px; font-weight: bold;")

    def tala_step(self):
        for i, lbl in enumerate(self.tala_labels):
            if i == 0 or i == 4:
                lbl.setStyleSheet("background: #45475a; color: #cdd6f4; border-radius: 4px; font-weight: bold;")
            else:
                lbl.setStyleSheet("background: #313244; color: #cdd6f4; border-radius: 4px; font-weight: bold;")
                
        self.audio.play_frequency(440, 80)
        if self.tala_step_idx == 0 or self.tala_step_idx == 4:
            self.audio.play_frequency(523.25, 100)
            self.tala_labels[self.tala_step_idx].setStyleSheet("background: #f38ba8; color: #11111b; border-radius: 4px; font-weight: bold;")
        else:
            self.tala_labels[self.tala_step_idx].setStyleSheet("background: #cba6f7; color: #11111b; border-radius: 4px; font-weight: bold;")
            
        self.tala_step_idx = (self.tala_step_idx + 1) % 8

    # --- Texture Logic ---
    def play_texture(self, tex_type):
        scale = ["C", "D", "E", "F", "G", "A", "B", "C (Oct)"]
        def play_in_thread():
            if tex_type == "mono":
                for n in scale:
                    self.audio.play_frequency(NOTE_FREQS[n], 300)
                    time.sleep(0.3)
            elif tex_type == "hetero":
                for n in scale:
                    self.audio.play_frequency(NOTE_FREQS[n], 300)
                    time.sleep(0.05)
                    grace_idx = (NOTES_ORDER.index(n.replace(" (Oct)", "")) + 1) % 12
                    self.audio.play_frequency(NOTE_FREQS[NOTES_ORDER[grace_idx]], 200)
                    time.sleep(0.25)
            elif tex_type == "poly":
                bass_line = ["C", "C", "G", "G", "A", "A", "G", "G"]
                for i, n in enumerate(scale):
                    self.audio.play_frequency(NOTE_FREQS[n], 300)
                    time.sleep(0.05)
                    self.audio.play_frequency(NOTE_FREQS[bass_line[i]] / 2, 300)
                    time.sleep(0.25)
        threading.Thread(target=play_in_thread, daemon=True).start()

    # --- Sidechain Logic ---
    def toggle_sidechain(self):
        if self.sidechain_btn.isChecked():
            if not self.audio.drone_gen:
                self.sidechain_btn.setChecked(False)
                return
            self.sidechain_btn.setText("Stop Sidechain Pump")
            self.sidechain_btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }")
            self.audio.toggle_sidechain(True)
        else:
            self.sidechain_btn.setText("Start Sidechain Pump (Requires Drone)")
            self.sidechain_btn.setStyleSheet("QPushButton { background-color: #313244; color: #f38ba8; padding: 8px; font-weight: bold; border-radius: 4px; }")
            self.audio.toggle_sidechain(False)

    def play_chord(self):
        root = self.chord_root_combo.currentText()
        ctype = self.chord_type_combo.currentText()
        intervals = CHORDS[ctype]
        inv = self.inversion_combo.currentIndex()
        
        root_idx = NOTES_ORDER.index(root)
        notes_to_play = []
        for i, interval in enumerate(intervals):
            note_idx = (root_idx + interval) % 12
            octave_mult = 2 ** (interval // 12)
            freq = NOTE_FREQS[NOTES_ORDER[note_idx]] * octave_mult
            
            if (inv == 1 and i == 0) or (inv == 2 and i <= 1):
                freq *= 2
            notes_to_play.append(freq)
            
        self.chord_info_label.setText(f"Chord: {root} {ctype} ({self.inversion_combo.currentText()})")
        def play_in_thread():
            for f in notes_to_play:
                self.audio.play_frequency(f, 800)
                time.sleep(0.05)
        threading.Thread(target=play_in_thread, daemon=True).start()

    def play_progression(self):
        progression = PROGRESSIONS[self.prog_combo.currentText()]
        def play_in_thread():
            for root, chord_type in progression:
                intervals = CHORDS.get(chord_type, CHORDS["Major"])
                root_idx = NOTES_ORDER.index(root)
                notes_to_play = []
                for interval in intervals:
                    note_idx = (root_idx + interval) % 12
                    octave_mult = 2 ** (interval // 12)
                    notes_to_play.append(NOTE_FREQS[NOTES_ORDER[note_idx]] * octave_mult)
                for f in notes_to_play:
                    self.audio.play_frequency(f, 700)
                time.sleep(0.8)
        threading.Thread(target=play_in_thread, daemon=True).start()

    def play_custom_progression(self):
        progression = []
        for i in range(4):
            root = self.custom_roots[i].currentText()
            ctype = self.custom_types[i].currentText()
            progression.append((root, ctype))
            
        def play_in_thread():
            for root, chord_type in progression:
                intervals = CHORDS[chord_type]
                root_idx = NOTES_ORDER.index(root)
                notes_to_play = []
                for interval in intervals:
                    note_idx = (root_idx + interval) % 12
                    octave_mult = 2 ** (interval // 12)
                    notes_to_play.append(NOTE_FREQS[NOTES_ORDER[note_idx]] * octave_mult)
                for f in notes_to_play:
                    self.audio.play_frequency(f, 800)
                time.sleep(0.8)
        threading.Thread(target=play_in_thread, daemon=True).start()

    def play_tuning(self, tuning_type):
        if tuning_type == "equal":
            freqs = [NOTE_FREQS["C"], NOTE_FREQS["E"], NOTE_FREQS["G"]]
        else:
            freqs = [264.0, 264.0 * (5/4), 264.0 * (3/2)]
            
        def play_in_thread():
            for f in freqs:
                self.audio.play_frequency(f, 1200)
                time.sleep(0.1)
            time.sleep(1.5)
        threading.Thread(target=play_in_thread, daemon=True).start()

    def play_overtones(self):
        def play_in_thread():
            for i, (name, freq) in enumerate(OVERTONES):
                if i > 0:
                    self.overtone_labels[i-1].setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 16px; border-radius: 4px; font-weight: bold;")
                self.overtone_labels[i].setStyleSheet("background: #cba6f7; color: #11111b; padding: 15px; font-size: 16px; border-radius: 4px; font-weight: bold;")
                self.audio.play_frequency(freq, 700)
                time.sleep(0.6)
            time.sleep(0.5)
            self.overtone_labels[-1].setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 16px; border-radius: 4px; font-weight: bold;")
        threading.Thread(target=play_in_thread, daemon=True).start()

    def update_micro_label(self, val):
        base_freq, target_freq = 261.63, 277.18
        self.current_micro_freq = base_freq + (target_freq - base_freq) * (val / 100.0)
        self.micro_freq_label.setText(f"Frequency: {self.current_micro_freq:.2f} Hz (Between C and C#)")

    def play_microtone(self):
        self.audio.play_frequency(self.current_micro_freq, 800)

    def toggle_balkan(self):
        if self.balkan_btn.isChecked():
            self.balkan_btn.setText("Stop Rhythm")
            pattern_text = self.balkan_combo.currentText()
            if "7/8" in pattern_text:
                self.balkan_pattern, delay = [1, 0, 1, 0, 1, 0, 0], 200
            elif "9/8" in pattern_text:
                self.balkan_pattern, delay = [1, 0, 1, 0, 1, 0, 1, 0, 0], 180
            else:
                self.balkan_pattern, delay = [1, 0, 1, 0, 1, 0, 1, 0], 200
            self.balkan_timer.start(delay)
            self.balkan_step = 0
        else:
            self.balkan_btn.setText("Start Rhythm")
            self.balkan_timer.stop()
            self.balkan_visual_label.setText("Ready...")
            self.balkan_visual_label.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 20px; border-radius: 4px;")

    def balkan_beat(self):
        if not self.balkan_pattern: return
        is_accent = self.balkan_pattern[self.balkan_step] == 1
        if is_accent:
            self.audio.play_frequency(523.25, 100)
            self.balkan_visual_label.setText("ACCENT")
            self.balkan_visual_label.setStyleSheet("background: #f9e2af; color: #11111b; padding: 15px; font-size: 20px; border-radius: 4px; font-weight: bold;")
        else:
            self.audio.play_frequency(261.63, 80)
            self.balkan_visual_label.setText("tic")
            self.balkan_visual_label.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 20px; border-radius: 4px;")
        self.balkan_step = (self.balkan_step + 1) % len(self.balkan_pattern)

    def toggle_rhythm(self):
        if self.rhythm_btn.isChecked():
            self.rhythm_btn.setText("Stop Polyrhythm")
            self.rhythm_timer_2.start(1000)
            self.rhythm_timer_3.start(666)
        else:
            self.rhythm_btn.setText("Start Polyrhythm")
            self.rhythm_timer_2.stop()
            self.rhythm_timer_3.stop()
            self.light_2.setText("2: -")
            self.light_3.setText("3: -")
            self.light_2.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 20px; border-radius: 4px;")
            self.light_3.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 20px; border-radius: 4px;")

    def play_rhythm_click(self, freq, light_id):
        self.audio.play_frequency(freq, 100)
        if light_id == 0:
            self.light_2.setText("2: X")
            self.light_2.setStyleSheet("background: #f38ba8; color: #11111b; padding: 15px; font-size: 20px; border-radius: 4px;")
            QTimer.singleShot(100, lambda: self.reset_light(0))
        else:
            self.light_3.setText("3: X")
            self.light_3.setStyleSheet("background: #89b4fa; color: #11111b; padding: 15px; font-size: 20px; border-radius: 4px;")
            QTimer.singleShot(100, lambda: self.reset_light(1))

    def reset_light(self, light_id):
        if light_id == 0:
            self.light_2.setText("2: -")
            self.light_2.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 20px; border-radius: 4px;")
        else:
            self.light_3.setText("3: -")
            self.light_3.setStyleSheet("background: #313244; color: #cdd6f4; padding: 15px; font-size: 20px; border-radius: 4px;")


class GlossaryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.terms = {
            "Ahavoh Rabboh": "Klezmer: A Jewish prayer mode. Similar to the Freygish scale but features a natural 7th, giving it a distinctly emotional, ascending resolution.",
            "Ainu Pentatonic": "Ainu (Japan): A minor pentatonic scale used in traditional Upopo singing of the Ainu people.",
            "Aksak": "Eastern European/Balkan: An asymmetric rhythmic pattern meaning 'limping' in Turkish.",
            "Al-Hijaz": "Andalusi/Arabic: A melodic mode equivalent to the Freygish/Phrygian Dominant scale, characteristic of North African and Arabic music.",
            "Altered Chord": "Jazz/Western: A dominant chord where the 5th or 9th is raised or lowered (e.g., 7#5, 7b9) to increase harmonic tension.",
            "Ambasel": "Ethiopian: A pentatonic scale featuring an augmented second interval, giving it a deeply yearning, minor sound.",
            "Andalusian Cadence": "Flamenco (Spain): A descending chord progression (i-VII-VI-V) foundational to Flamenco.",
            "Aeolian": "Appalachian/Western: The natural minor scale. Heavily used in Appalachian 'Old-Time' string band music.",
            "Arka": "Aymara/Andean: The 'follower' half of a Siku (panpipe) ensemble. It plays the off-beats to interlock with the Ira.",
            "Arrastre": "Argentine Tango: A deliberate dragging of the beat or rhythm, creating a heavy, passionate tension.",
            "Assotor": "Haitian: A large, sacred Vodou drum used to call specific spirits (Loa).",
            "Babendil": "Filipino: A small, single bosses gong played with a pair of bamboo sticks. It acts as the timekeeper in the Kulintang ensemble.",
            "Bandoneon": "Argentine Tango: A square-shaped free-reed instrument (similar to an accordion) that produces the signature melancholy sound of Tango.",
            "Batá": "Afro-Cuban: A double-headed drum shaped like an hourglass, used primarily in Santeria religious music.",
            "Bayati": "Middle Eastern: A common Arabic Maqam scale, featuring a half-flat (quarter tone) second degree.",
            "Berimbau": "Afro-Brazilian: A single-string percussion instrument (musical bow) used to dictate the rhythm and style in Capoeira.",
            "Blue Note": "Blues/Jazz: A note sung or played at a slightly lower pitch for expressive effect.",
            "Buk": "Korean: A traditional wooden barrel drum used to accompany Pansori singing.",
            "Bulgar": "Klezmer: A lively circle dance in 8/8 time, subdivided 3+3+2 (often notated as 2/4).",
            "Byzantine Scale": "Eastern Europe: A double harmonic scale featuring a minor 2nd and major 3rd.",
            "Cak": "Balinese: The sharp, percussive syllable chanted in Kecak, mimicking the interlocking patterns of the Gamelan.",
            "Call and Response": "African/Native American: A structure where a leader's phrase is answered by a group.",
            "Charango": "Andean: A small 10-string lute traditionally made from an armadillo shell.",
            "Circle of Fifths": "Western: A visual representation of the 12 tones, key signatures, and their relationships.",
            "Clave": "Latin/Caribbean: A 5-note rhythmic pattern foundational to Afro-Cuban music.",
            "Colotomic": "Indonesian (Gamelan): The use of specific instruments (like gongs) to mark the structure and time cycles of a piece.",
            "Compás": "Flamenco (Spain): The rhythmic cycle or meter of Flamenco, often a 12-beat cycle.",
            "Counterpoint": "Western (Baroque): The art of writing two or more independent melodic lines that work harmonically together.",
            "Dastgah": "Persian: A musical modal system in traditional Persian art music.",
            "Diaphony": "Bulgarian/Eastern European: A form of polyphony where two voices sing a melody and a drone, often clashing in major or minor 2nds, creating a biting, dissonant harmony.",
            "Diatonic": "Western: Notes or chords that belong to a specific major or minor scale.",
            "Didgeridoo": "Oceania (Aboriginal): A long wooden wind instrument that produces a continuous, dense drone.",
            "Drone": "World/Celtic/Indian: A continuous, sustained note or chord providing harmonic foundation.",
            "Duduk": "Armenian: A double-reed woodwind instrument made of apricot wood, known for its warm, mournful, and highly expressive microtonal sound.",
            "Equal Temperament": "Western: The modern tuning system that divides the octave into 12 exactly equal semitones.",
            "Ethos": "Ancient Greek: The belief that specific musical modes and scales could affect human character and morality (e.g., Dorian instilled courage).",
            "Extended Chords": "Jazz/Western: Chords that add notes beyond the 7th, such as 9ths, 11ths, and 13ths, creating rich, colorful harmonies.",
            "Fakarava": "Tahitian: A rapid, percussive ukulele strumming technique that treats the instrument as much as a drum as a melodic voice.",
            "Freygish": "Balkan/Klezmer: Phrygian Dominant scale; sounds Spanish or Middle Eastern.",
            "Frottoir": "Cajun/Zydeco: A metal washboard worn on the chest and scraped with spoons or bottle openers, central to Zydeco rhythm.",
            "Four-on-the-floor": "EDM: A steady, four-beat drum pattern where the bass drum is hit on every beat of a 4/4 measure.",
            "Gamelan": "World (Indonesia): Ensemble of metallophones and gongs tuned to Slendro or Pelog.",
            "Garifuna": "Central America: An Afro-Indigenous culture known for the Paranda guitar style and the rapid Punta rhythm.",
            "Georgian Polyphony": "Georgian (Caucasus): A ancient tradition of three-part singing featuring parallel fifths and dissonant major second intervals, considered highly consonant in Georgian theory.",
            "Habanera": "Argentine Tango: A syncopated 3-3-2 rhythmic pattern that is the foundation of Tango music.",
            "Haka": "Maori: A traditional posture dance involving rhythmic body slapping, foot stomping, and fierce chanting.",
            "Harmonium": "Indian/Sufi: A small, hand-pumped reed organ that provides a continuous drone and melodic foundation in Qawwali and Indian classical music.",
            "Hemiola": "World/Latin: A rhythmic ratio of 3:2. Playing three notes in the space of two.",
            "Heterophony": "World/Eastern: A texture where multiple performers play the same melody simultaneously, but each adds their own ornaments, variations, or slight delays.",
            "Hijaz Kar": "Armenian/Arabic: A modal scale featuring two augmented second intervals, creating a distinctly Middle Eastern sound.",
            "Hocketing": "Medieval/Andean: A technique where a single melody is split between two or more voices. No voice plays the whole melody; they alternate notes.",
            "Inversion": "Western Harmony: Reordering the notes of a chord so that a note other than the root is the lowest (bass) note. Changes the chord's color and weight.",
            "Ira": "Aymara/Andean: The 'leader' half of a Siku (panpipe) ensemble. It plays the main beats and leads the melody.",
            "Isicathamiya": "South African: A soft, tight a cappella vocal harmony tradition of Zulu migrant workers.",
            "Jangdan": "Korean: The rhythmic cycles in Korean music. They dictate not just the beat, but the emotional tempo of the piece.",
            "Joik": "Saami (Scandinavian): A traditional form of song in Sámi music. Rather than 'about' a subject, a joik is meant to 'evoke' or 'be' the subject.",
            "Just Intonation": "Universal/Acoustic: A tuning system based on pure mathematical ratios (e.g., 3:2 for a fifth). Sounds purer but is less flexible than Equal Temperament.",
            "Kargyraa": "Tuvan (Siberian): A style of throat singing using very low frequencies, created by the rapid vibration of the false vocal cords.",
            "Kashif": "Nubian: A modal system used in Nubian music, often featuring pentatonic structures with unique microtonal inflections.",
            "Katajjaq": "Inuit/Arctic: A form of rhythmic throat singing performed as a game between two women.",
            "Kecak": "Balinese: A form of Balinese vocal music where dozens of men interlock rhythmic syllables (Cak) to create a dense, hypnotic chant.",
            "Ki Ho'alu": "Polynesian (Hawaii): Hawaiian Slack-key guitar; a fingerstyle technique with altered tunings.",
            "Khoomei": "Turkic/Mongolian: Throat singing, a technique allowing singers to produce multiple pitches simultaneously.",
            "Konnakol": "Karnatic (South Indian): The art of vocal percussion. Syllables are spoken to dictate complex rhythmic cycles (Talas).",
            "Kora": "West African: A 21-string bridge-harp used by Griots (storytellers) in West Africa.",
            "Kulintang": "Filipino: An ancient gong and drum ensemble from the southern Philippines. Features a row of small, horizontal knobbed gongs played melodically.",
            "Kushaura": "Shona (Zimbabwe): The lead melodic part in Mbira music. It establishes the core pattern.",
            "Kutsinhira": "Shona (Zimbabwe): The interlocking follower part in Mbira music. It plays in the gaps of the Kushaura to create a continuous stream of notes.",
            "Launeddas": "Sardinian (Italy): A triple clarinet instrument requiring circular breathing, used to play complex polyphonic melodies.",
            "La Pompe": "Romani (Gypsy) Jazz: The rhythmic 'pump' strum pattern on rhythm guitar, characterized by a heavy downbeat and a percussive upstroke.",
            "Loa": "Haitian: A Vodou spirit. Each Loa has a specific rhythm, song, and dance used to invoke them.",
            "Ma": "East Asian (Japan): The concept of 'negative space' or silence between notes.",
            "Maqam": "Eastern (Arabic): Melodic modes using quarter tones.",
            "Mariachi": "Mexican: A musical ensemble that uses stringed instruments (guitarron, vihuela) and trumpets.",
            "Masenqo": "Ethiopian: A single-stringed bowed lute used by Azmari (minstrels) to accompany singing.",
            "Matrix": "Serialism: A 12x12 grid used to map all 48 permutations (Prime, Inversion, Retrograde, Retrograde-Inversion) of a 12-tone row.",
            "Mbira": "Shona (Zimbabwe): A traditional thumb piano with metal tines. Often placed inside a large calabash gourd (deze) for amplification.",
            "Microtone": "World/Eastern: Intervals smaller than a semitone.",
            "Minyo": "Okinawan/Japanese: Traditional folk singing. Okinawan Minyo is characterized by distinct pentatonic scales and heavy use of glissando (pitch sliding).",
            "Montuno": "Cuban/Salsa: A syncopated, repeating piano or guitar vamp that provides the harmonic and rhythmic foundation over which improvisation occurs.",
            "Morin Khuur": "Turkic/Mongolian: The traditional horse-head fiddle.",
            "Mukkuri": "Ainu (Japan): A traditional mouth harp made of bamboo, played by plucking a string while changing the shape of the mouth to alter pitch.",
            "Multiphonics": "World/Tibetan: The technique of producing more than one pitch simultaneously on an instrument or with the voice.",
            "Nuba": "Andalusi (North Africa): A large musical suite in classical Moroccan and Algerian music.",
            "Ogan": "Haitian: An iron bell used in Vodou ensembles to maintain the rhythmic timeline.",
            "Ostinato": "World/Minimalism: A continually repeated musical phrase or rhythm.",
            "Overtone Series": "Universal/Acoustic: The sequence of frequencies that naturally vibrate above a fundamental pitch. The basis of all harmony.",
            "Paranda": "Garifuna: An acoustic guitar style blending African rhythms and Spanish guitar techniques.",
            "Pelog": "Indonesian: One of the two essential tuning scales of Javanese Gamelan music, a 7-tone scale with large and small intervals.",
            "Pentatonic Scale": "World: A musical scale with five notes per octave.",
            "Pansori": "Korean: A traditional form of musical storytelling performed by a vocalist (sorikkun) and a drummer (kosu).",
            "Phase Shifting": "Modern Minimalism: A compositional technique where two identical loops of music are played simultaneously, but one gradually speeds up, causing them to drift in and out of sync.",
            "Poi": "Maori: A tethered weight swung in complex rhythmic patterns, often accompanying women's singing.",
            "Polyphony": "Western/Georgian: A musical texture where two or more independent melodies are played simultaneously.",
            "Polyrhythm": "African: The simultaneous use of two or more conflicting rhythms.",
            "Punta": "Garifuna: A rapid 2/4 rhythmic pattern and dance, often using a hemiola, central to Garifuna music.",
            "Qawwali": "Sufi: A form of devotional Sufi music characterized by extended vocal improvisations, rhythmic clapping, and a building tempo designed to induce trance.",
            "Rada": "Haitian: A major rite in Vodou, characterized by West African (Dahomey) rhythms. It is generally gentler and more rhythmically steady than the Petro rite.",
            "Raga": "Indian: A melodic framework for improvisation.",
            "Rasa": "Indian: The emotional flavor or mood evoked by a specific Raga.",
            "Ryukyu Scale": "Okinawan: A distinct pentatonic scale (Do, Mi, Fa, Sol, Ti) used in Okinawan folk music.",
            "Scale Degree": "Western: The numerical position of a note within a scale (e.g., 1st, 2nd, 3rd, often called Do, Re, Mi).",
            "Secondary Dominant": "Western/Jazz: A dominant 7th chord that resolves to a chord other than the tonic (e.g., E7 resolving to A minor).",
            "Sidechain Compression": "EDM: An audio effect triggered by a kick drum that rapidly lowers the volume of background music, creating a rhythmic 'pumping' effect.",
            "Siku": "Aymara/Andean: Traditional Andean panpipes made of bamboo. They are split into two halves (Ira and Arka) that must interlock to play a melody.",
            "Sistrum": "Ancient Egyptian: A sacred rattle or shaker used in temple rituals to appease the goddess Hathor.",
            "Shruti": "Indian: The smallest interval in Indian classical music; 22 shrutis make an octave.",
            "Singing Bowl": "Tibetan/Himalayan: A bronze or crystal bowl that produces a sustained, rich overtone when struck or rubbed.",
            "Slendro": "Indonesian: A 5-tone roughly equal scale used in Gamelan music.",
            "Steelpan": "Trinidadian: A pitched percussion instrument made from 55-gallon industrial drums, central to Calypso and Soca music.",
            "Sanshin": "Okinawan: A 3-stringed banjo-like lute covered in snakeskin, the precursor to the Japanese shamisen.",
            "Sygyt": "Tuvan (Siberian): A high, whistling style of throat singing, created by manipulating the tongue to isolate high overtones.",
            "Tahrir": "Persian: A vocal technique involving rapid ornamental leaps and vocal vibrations, central to Persian classical singing.",
            "Tala": "Indian: The rhythmic framework or cycle.",
            "Tanbou": "Haitian: A general term for drums in Haitian Vodou, which come in various sizes (e.g., Assotor, Segon) to create polyrhythmic textures.",
            "Tanpura": "Indian: A long-necked plucked string instrument providing a continuous drone.",
            "Taqsīm": "Arabic: An instrumental improvisation. Often metrically free and explores the nuances of a specific Maqam.",
            "Tarab": "Arabic: The concept of musical ecstasy. The state of deep emotional enchantment induced by perfect musical performance.",
            "Tarana": "Sufi/Indian: A vocal style using rhythmic nonsense syllables (e.g., 'tana dere na') to emulate drum patterns and induce a trance state.",
            "Tende": "Tuareg: A traditional drum made from a mortar covered with goatskin, used to accompany desert blues music.",
            "Tenores": "Sardinian (Italy): A style of a cappella polyphonic singing where the bass voice uses sub-harmonic throat singing techniques.",
            "Tetrachord": "Ancient Greek/Western: A group of four notes. Ancient Greek scales were built by conjoining two tetrachords.",
            "Tishoumaren": "Tuareg: Also known as 'desert blues,' a style of music combining traditional Tuareg melodies with electric guitars and Western blues structures.",
            "Tizita": "Ethiopian: A pentatonic scale mode associated with deep nostalgia, longing, and mourning.",
            "Toque": "Afro-Brazilian: A specific rhythmic pattern played on the berimbau in Capoeira.",
            "Tone Row": "Serialism: A specific ordering of the 12 chromatic pitches used as the basis for a 12-tone composition.",
            "Tonkori": "Ainu (Japan): A traditional stringed instrument played by the Ainu people, often used to accompany dances.",
            "Tres": "Cuban: A 3-course (6-string) guitar-like instrument central to Cuban Son music.",
            "Triad": "Western: A set of three notes stacked in thirds (Root, 3rd, 5th).",
            "Tumbao": "Cuban: The basic rhythm played on congas in Salsa and Cuban music.",
            "Txalaparta": "Basque: A wooden percussion instrument consisting of boards struck by two players (Txalapartaris) in strict rhythmic interlock.",
            "Txistu": "Basque: A traditional one-handed flute played alongside the Txalaparta or drum.",
            "Upopo": "Ainu (Japan): Traditional round singing of the Ainu people, often featuring polyphony.",
            "Vocables": "Native American: Non-lexical syllables (like 'hey') used in vocal singing.",
            "Waslah": "Arabic: A musical suite that combines several instrumental and vocal pieces, all in the same Maqam.",
            "Yodel": "Central African/Alpine: A vocal technique involving rapid shifts between the chest register and the head register (falsetto).",
            "Zortziko": "Basque: A traditional dance and meter in 5/8 time, characteristic of Basque folk music."
        }
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search musical terms...")
        self.search_bar.setStyleSheet("QLineEdit { background-color: #313244; color: #cdd6f4; padding: 10px; border: 1px solid #45475a; border-radius: 4px; font-size: 14px; }")
        self.search_bar.textChanged.connect(self.filter_terms)
        layout.addWidget(self.search_bar)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListWidget { background-color: #181825; color: #cdd6f4; border: none; font-size: 14px; }"
                                       "QListWidget::item { padding: 10px; border-bottom: 1px solid #313244; }"
                                       "QListWidget::item:selected { background-color: #313244; color: #89b4fa; }")
        self.list_widget.itemClicked.connect(self.show_definition)
        layout.addWidget(self.list_widget)

        self.definition_label = QLabel("Select a term to see its definition.")
        self.definition_label.setWordWrap(True)
        self.definition_label.setStyleSheet("background-color: #313244; color: #cdd6f4; padding: 20px; border-radius: 4px; font-size: 14px;")
        self.definition_label.setMinimumHeight(100)
        layout.addWidget(self.definition_label)
        self.populate_terms()
        self.setLayout(layout)

    def populate_terms(self, filter_text=""):
        self.list_widget.clear()
        for term, defn in sorted(self.terms.items()):
            if filter_text.lower() in term.lower() or filter_text.lower() in defn.lower():
                self.list_widget.addItem(term)

    def filter_terms(self, text): self.populate_terms(text)
    def show_definition(self, item):
        term = item.text()
        self.definition_label.setText(f"<b style='color:#89b4fa'>{term}:</b><br><br>{self.terms[term]}")


class MusicTheoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Global Music Theory Learner Pro")
        self.resize(1050, 800)
        self.audio_engine = AudioEngine()
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QTabWidget::pane { border: 1px solid #313244; top: -1px; }
            QTabBar::tab { background: #181825; color: #cdd6f4; padding: 10px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 2px; }
            QTabBar::tab:selected { background: #313244; font-weight: bold; color: #89b4fa; }
            QTextEdit { background-color: #181825; color: #cdd6f4; border: none; font-size: 14px; padding: 15px; }
            QLabel { color: #cdd6f4; }
            QFrame#Card { background-color: #181825; border-radius: 8px; }
            QGroupBox { color: #89b4fa; font-weight: bold; border: 1px solid #313244; border-radius: 8px; margin-top: 10px; padding: 15px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
            QComboBox { background-color: #313244; color: #cdd6f4; padding: 5px; border-radius: 4px; }
            QScrollArea { border: none; }
        """)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # --- Create Tabs ---
        self.tabs.addTab(self.create_home_tab(), "Home")
        self.tabs.addTab(self.create_theory_tab("Western", self.get_western_html()), "Western")
        self.tabs.addTab(self.create_theory_tab("Baroque & Counterpoint", self.get_baroque_html()), "Baroque")
        self.tabs.addTab(self.create_theory_tab("Serialism (12-Tone)", self.get_serialism_html()), "Serialism")
        self.tabs.addTab(self.create_theory_tab("Romani (Gypsy) Jazz", self.get_romani_html()), "Romani Jazz")
        self.tabs.addTab(self.create_theory_tab("Electronic (EDM)", self.get_edm_html()), "EDM")
        self.tabs.addTab(self.create_theory_tab("Modern Minimalism", self.get_minimalism_html()), "Minimalism")
        self.tabs.addTab(self.create_theory_tab("Ancient Greek", self.get_greek_html()), "Ancient Greek")
        self.tabs.addTab(self.create_theory_tab("Ancient Egyptian", self.get_egyptian_html()), "Ancient Egyptian")
        self.tabs.addTab(self.create_theory_tab("Nubian (Egypt/Sudan)", self.get_nubian_html()), "Nubian")
        self.tabs.addTab(self.create_theory_tab("Tuareg (Sahara)", self.get_tuareg_html()), "Tuareg")
        self.tabs.addTab(self.create_theory_tab("Indian Classical", self.get_indian_html()), "Indian")
        self.tabs.addTab(self.create_theory_tab("Karnatic (S. Indian)", self.get_karnatic_html()), "Karnatic")
        self.tabs.addTab(self.create_theory_tab("Persian Classical", self.get_persian_html()), "Persian")
        self.tabs.addTab(self.create_theory_tab("Arabic (Tarab)", self.get_arabic_html()), "Arabic")
        self.tabs.addTab(self.create_theory_tab("Sufi (Qawwali)", self.get_sufi_html()), "Sufi")
        self.tabs.addTab(self.create_theory_tab("East Asian", self.get_east_asian_html()), "East Asian")
        self.tabs.addTab(self.create_theory_tab("Ainu (Japan/Russia)", self.get_ainu_html()), "Ainu")
        self.tabs.addTab(self.create_theory_tab("Okinawan (Japan)", self.get_okinawan_html()), "Okinawan")
        self.tabs.addTab(self.create_theory_tab("Korean Gugak (Pansori)", self.get_korean_html()), "Korean")
        self.tabs.addTab(self.create_theory_tab("Vietnamese Traditional", self.get_vietnamese_html()), "Vietnamese")
        self.tabs.addTab(self.create_theory_tab("Indonesian (Gamelan)", self.get_indonesian_html()), "Indonesian")
        self.tabs.addTab(self.create_theory_tab("Balinese (Kecak)", self.get_balinese_html()), "Balinese")
        self.tabs.addTab(self.create_theory_tab("Filipino (Kulintang)", self.get_filipino_html()), "Filipino")
        self.tabs.addTab(self.create_theory_tab("Middle Eastern", self.get_middle_eastern_html()), "Middle Eastern")
        self.tabs.addTab(self.create_theory_tab("Andalusi (N. Africa)", self.get_andalusi_html()), "Andalusi")
        self.tabs.addTab(self.create_theory_tab("Ethiopian (Azmari)", self.get_ethiopian_html()), "Ethiopian")
        self.tabs.addTab(self.create_theory_tab("Tuvan (Siberian)", self.get_tuvan_html()), "Tuvan")
        self.tabs.addTab(self.create_theory_tab("Shona (Zimbabwean)", self.get_shona_html()), "Shona")
        self.tabs.addTab(self.create_theory_tab("Basque (Spain/France)", self.get_basque_html()), "Basque")
        self.tabs.addTab(self.create_theory_tab("Sardinian (Italy)", self.get_sardinian_html()), "Sardinian")
        self.tabs.addTab(self.create_theory_tab("Eastern Euro / Balkan", self.get_balkan_html()), "Balkan")
        self.tabs.addTab(self.create_theory_tab("Bulgarian Choral", self.get_bulgarian_html()), "Bulgarian")
        self.tabs.addTab(self.create_theory_tab("Georgian (Caucasus)", self.get_georgian_html()), "Georgian")
        self.tabs.addTab(self.create_theory_tab("Klezmer", self.get_klezmer_html()), "Klezmer")
        self.tabs.addTab(self.create_theory_tab("Flamenco (Spain)", self.get_flamenco_html()), "Flamenco")
        self.tabs.addTab(self.create_theory_tab("Argentine Tango", self.get_tango_html()), "Tango")
        self.tabs.addTab(self.create_theory_tab("Armenian & Caucasian", self.get_armenian_html()), "Armenian")
        self.tabs.addTab(self.create_theory_tab("Turkic / Mongolian", self.get_turkic_html()), "Turkic/Mongolian")
        self.tabs.addTab(self.create_theory_tab("Tibetan / Himalayan", self.get_tibetan_html()), "Tibetan")
        self.tabs.addTab(self.create_theory_tab("Saami (Scandinavian)", self.get_saami_html()), "Saami")
        self.tabs.addTab(self.create_theory_tab("African", self.get_african_html()), "African")
        self.tabs.addTab(self.create_theory_tab("West African Griot", self.get_griot_html()), "W. African Griot")
        self.tabs.addTab(self.create_theory_tab("Pygmy (Central Africa)", self.get_pygmy_html()), "Pygmy")
        self.tabs.addTab(self.create_theory_tab("South African", self.get_south_african_html()), "South African")
        self.tabs.addTab(self.create_theory_tab("Haitian (Vodou)", self.get_haitian_html()), "Haitian")
        self.tabs.addTab(self.create_theory_tab("Garifuna (C. America)", self.get_garifuna_html()), "Garifuna")
        self.tabs.addTab(self.create_theory_tab("Afro-Brazilian", self.get_afrobrazilian_html()), "Afro-Brazilian")
        self.tabs.addTab(self.create_theory_tab("Afro-Cuban", self.get_afrocuban_html()), "Afro-Cuban")
        self.tabs.addTab(self.create_theory_tab("Cuban Son / Salsa", self.get_salsa_html()), "Cuban Son/Salsa")
        self.tabs.addTab(self.create_theory_tab("Andean / S. America", self.get_andean_html()), "Andean")
        self.tabs.addTab(self.create_theory_tab("Aymara (Andean)", self.get_aymara_html()), "Aymara")
        self.tabs.addTab(self.create_theory_tab("Indigenous Mexican", self.get_mexican_html()), "Mexican")
        self.tabs.addTab(self.create_theory_tab("Cajun & Zydeco", self.get_cajun_html()), "Cajun/Zydeco")
        self.tabs.addTab(self.create_theory_tab("Trinidadian (Calypso)", self.get_trinidadian_html()), "Trinidadian")
        self.tabs.addTab(self.create_theory_tab("Polynesian / Hawaiian", self.get_polynesian_html()), "Polynesian")
        self.tabs.addTab(self.create_theory_tab("Tahitian & Marquesan", self.get_tahitian_html()), "Tahitian")
        self.tabs.addTab(self.create_theory_tab("Maori (Kapa Haka)", self.get_maori_html()), "Maori")
        self.tabs.addTab(self.create_theory_tab("Appalachian (Old-Time)", self.get_appalachian_html()), "Appalachian")
        self.tabs.addTab(self.create_theory_tab("Inuit & Arctic", self.get_inuit_html()), "Inuit/Arctic")
        self.tabs.addTab(self.create_theory_tab("Oceania / Aboriginal", self.get_oceania_html()), "Oceania")
        self.tabs.addTab(self.create_theory_tab("Native American", self.get_native_html()), "Native American")
        self.tabs.addTab(self.create_theory_tab("Celtic & Folk", self.get_celtic_html()), "Celtic & Folk")
        self.tabs.addTab(self.create_theory_tab("Latin & Caribbean", self.get_latin_html()), "Latin & Caribbean")
        self.tabs.addTab(self.create_theory_tab("Blues & Jazz", self.get_blues_html()), "Blues & Jazz")
        self.tabs.addTab(self.create_theory_tab("World / Fusion", self.get_world_html()), "World Fusion")
        self.tabs.addTab(self.create_theory_tab("Instruments", self.get_instruments_html()), "Instruments")
        
        # Visual Theory Tab
        visual_tab = QWidget()
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("<h2>Circle of Fifths Visualizer</h2><p>Click any key to hear its triad and see its relative key.</p>"))
        
        self.circle_widget = CircleOfFifthsWidget(self.audio_engine)
        mode_btn = QPushButton("Switch to Minor Keys")
        mode_btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }")
        mode_btn.clicked.connect(lambda: self.toggle_circle_mode(mode_btn))
        v_layout.addWidget(mode_btn, alignment=Qt.AlignCenter)
        
        v_layout.addWidget(self.circle_widget)
        info_label = QLabel("<b style='color:#89b4fa'>Key:</b> C Major &nbsp;&nbsp;|&nbsp;&nbsp; <b style='color:#f38ba8'>Relative Minor:</b> A Minor")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 16px; padding: 10px;")
        v_layout.addWidget(info_label)
        visual_tab.setLayout(v_layout)
        self.tabs.addTab(visual_tab, "Visual Theory")
        
        # Interactive Audio Tab (with Scroll Area)
        audio_scroll = QScrollArea()
        audio_scroll.setWidgetResizable(True)
        audio_scroll.setWidget(InteractiveAudioWidget(self.audio_engine))
        self.tabs.addTab(audio_scroll, "Interactive Audio")
        
        # Ear Training Tab (with Scroll Area for four trainers)
        ear_scroll = QScrollArea()
        ear_scroll.setWidgetResizable(True)
        ear_tab = QWidget()
        ear_layout = QVBoxLayout(ear_tab)
        ear_layout.addWidget(IntervalTrainerWidget(self.audio_engine))
        ear_layout.addWidget(ScaleDegreeTrainerWidget(self.audio_engine))
        ear_layout.addWidget(ChordQualityTrainerWidget(self.audio_engine))
        ear_layout.addWidget(MelodicDictationWidget(self.audio_engine))
        ear_scroll.setWidget(ear_tab)
        self.tabs.addTab(ear_scroll, "Ear Training")
        
        self.tabs.addTab(GlossaryWidget(), "Glossary")

    def toggle_circle_mode(self, btn):
        self.circle_widget.is_minor = not self.circle_widget.is_minor
        if self.circle_widget.is_minor:
            btn.setText("Switch to Major Keys")
            btn.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }")
            self.circle_widget.selected_key = "A"
        else:
            btn.setText("Switch to Minor Keys")
            btn.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; padding: 8px; font-weight: bold; border-radius: 4px; }")
            self.circle_widget.selected_key = "C"
        self.circle_widget.update()
        self.circle_widget.update_info(self.circle_widget.selected_key)

    def create_home_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        title = QLabel("🌍 Global Music Theory")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #89b4fa;")
        subtitle = QLabel("Learn the sounds of the world, from Western counterpoint to Eastern microtones and modern electronic rhythms.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #a6adc8;")
        instructions = QLabel(
            "<div style='text-align: center; font-size: 14px; color: #cdd6f4;'>"
            "<b>How to use this app:</b><br><br>"
            "1. Navigate the theory tabs to read about different cultural concepts.<br>"
            "2. Visit the <b>Visual Theory</b> tab to interact with the Circle of Fifths (toggle Major/Minor).<br>"
            "3. Use the <b>Interactive Audio</b> tab to play the Basque Txalaparta, Haitian Vodou rhythm, build Altered Jazz Chords, simulate Throat Singing, and generate a 12-Tone Matrix.<br>"
            "4. Train your ears in the <b>Ear Training</b> tab (Intervals, Scale Degrees, Chord Qualities & Melodic Dictation).<br>"
            "5. Use the <b>Glossary</b> to look up unfamiliar terms."
            "</div>"
        )
        instructions.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(instructions)
        layout.addWidget(card)
        tab.setLayout(layout)
        return tab

    def create_theory_tab(self, title, content_html):
        tab = QWidget()
        layout = QVBoxLayout()
        header = QLabel(f"<h1 style='color:#89b4fa;'>{title}</h1>")
        layout.addWidget(header)
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setHtml(content_html)
        layout.addWidget(text_area)
        tab.setLayout(layout)
        return tab

    # --- Content Generation ---
    def get_western_html(self):
        return """
        <h2>Western Music Theory</h2>
        <p>Western music theory is based on the 12-tone equal temperament system. It heavily emphasizes harmony, counterpoint, and notation.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Scales:</b> Major, Minor, Modes (Dorian, Phrygian, Lydian, etc.).</li>
            <li><b>Harmony:</b> Built in thirds (Triads: Root, 3rd, 5th). 7th chords add another third.</li>
            <li><b>Rhythm:</b> Divided into standard time signatures (4/4, 3/4).</li>
            <li><b>Circle of Fifths:</b> A map of key signatures. Check the 'Visual Theory' tab!</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to explore Diatonic Chord Functions, or build Altered Chords (7#5, 7b9)!</i></p>
        """

    def get_baroque_html(self):
        return """
        <h2>Baroque & Counterpoint Theory</h2>
        <p>The Baroque period (1600-1750) in Western music was dominated by the art of Counterpoint, most famously perfected by J.S. Bach.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Counterpoint:</b> The art of writing two or more independent melodic lines that work together harmonically. Instead of a melody with background chords, every voice is its own distinct melody.</li>
            <li><b>Species Counterpoint:</b> A pedagogical method of writing counterpoint with strict rules. It limits rhythms and intervals to teach voice leading.</li>
            <li><b>Parallel Motion Rules:</b> In strict counterpoint, parallel fifths and parallel octaves are forbidden. This is because perfect fifths and octaves sound so consonant that they cause the independent voices to merge into one, destroying the independence of the lines.</li>
            <li><b>Suspensions:</b> A non-chord tone where a note from the previous chord is held over into the next chord, creating tension, before resolving down by step.</li>
        </ul>
        """

    def get_serialism_html(self):
        return """
        <h2>Serialism & 12-Tone Theory</h2>
        <p>In the early 20th century, composers like Arnold Schoenberg felt that traditional Western tonality had been exhausted. They developed Serialism (specifically the 12-tone technique) to treat all 12 pitches of the chromatic scale equally, avoiding any tonal center.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Tone Row (Prime / P0):</b> A specific ordering of the 12 pitches. This row becomes the melodic and harmonic source for the entire composition.</li>
            <li><b>Inversion (I0):</b> The tone row flipped upside down. If the original goes up a major 2nd, the inversion goes down a major 2nd.</li>
            <li><b>Retrograde (R0):</b> The tone row played backward.</li>
            <li><b>Matrix:</b> A 12x12 grid that maps all 48 possible forms of the row (P, I, R, and RI at all 12 transposition levels). The composer reads left-to-right, top-to-bottom, or right-to-left to generate material.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to open the 12-Tone Matrix Generator and hear the Prime and Inversion rows!</i></p>
        """

    def get_romani_html(self):
        return """
        <h2>Romani (Gypsy) Jazz Theory</h2>
        <p>Pioneered by Django Reinhardt in 1930s Paris, Romani Jazz (or Gypsy Jazz) is a fusion of American swing jazz and traditional Romani musette waltzes. It is entirely acoustic and rhythmically driven.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>La Pompe:</b> The definitive rhythm guitar technique. Translating to 'the pump', it is a percussive strumming style where a heavy downbeat is followed by a quick, muted upstroke, creating a continuous pumping rhythm that mimics a drum kit.</li>
            <li><b>Minor 6th Chords:</b> Gypsy jazz heavily favors Minor 6th chords (e.g., Cm6) as tonic chords, rather than standard minor triads or m7 chords. This gives the harmony a distinctly dark, continental sound.</li>
            <li><b>Glissando (Portamento):</b> Lead guitarists use continuous slides (glissando) between notes, a technique borrowed from Romani violin playing, to give the melody a crying, vocal quality.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Romani Minor" scale, and select "Minor 6th" in the Chord Builder!</i></p>
        """

    def get_edm_html(self):
        return """
        <h2>Electronic Dance Music (EDM) Theory</h2>
        <p>EDM is a modern global phenomenon. While it often uses Western scales (like minor pentatonic), its "theory" is rooted in rhythm, timbre, and studio techniques rather than traditional melody and counterpoint.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Four-on-the-Floor:</b> A steady, uninterrupted bass drum hitting on every single beat of a 4/4 measure. This creates a hypnotic, driving pulse.</li>
            <li><b>Sidechain Compression:</b> A production technique where the bass and synth volumes are automatically lowered every time the kick drum hits, creating a rhythmic "pumping" or "breathing" effect.</li>
            <li><b>Build-ups and Drops:</b> The structural theory of EDM relies on tension and release. Snare rolls and rising pitches build tension, culminating in a "drop" where the heaviest bass and beat return.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Drone, then toggle the Sidechain Pump to hear the defining rhythmic effect of modern House music!</i></p>
        """
        
    def get_minimalism_html(self):
        return """
        <h2>Modern Minimalism Theory</h2>
        <p>Emerging in the 1960s as a reaction against the intense complexity of mid-20th-century classical music, Minimalism (Steve Reich, Philip Glass, Terry Riley) returned music to its most basic elements: repetition, slow transformation, and a steady pulse.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Phase Shifting:</b> A technique where two identical musical loops are played simultaneously. One gradually speeds up or slows down, causing the loops to drift in and out of sync, creating hypnotic, evolving patterns.</li>
            <li><b>Ostinato:</b> A continually repeated musical phrase or rhythm. Minimalism is built on ostinatos that rarely change pitch, but change in rhythm or orchestration.</li>
            <li><b>Additive Rhythm:</b> A rhythmic structure where a short pattern is gradually expanded by adding notes.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to experiment with the Phase Shifter widget!</i></p>
        """

    def get_greek_html(self):
        return """
        <h2>Ancient Greek Music Theory</h2>
        <p>Ancient Greek music theory is the foundation of Western musical thought. The Greeks mathematically analyzed acoustics and believed deeply in the <b>Ethos</b> doctrine—the idea that different musical modes could profoundly affect human character and morality.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Tetrachord:</b> The basic building block of Greek scales. A group of four notes spanning a perfect fourth. Two tetrachords joined together formed an octave.</li>
            <li><b>Modes (Tonoi):</b> The Greeks named their scales after regions (Dorian, Phrygian, Lydian). They believed the Dorian mode instilled courage and discipline, while the Phrygian mode could inspire frenzy or ecstasy.</li>
            <li><b>Ethos:</b> The ethical character of music. Greek philosophers like Plato and Aristotle heavily regulated which modes could be played in their ideal societies, fearing that certain scales would corrupt the youth.</li>
            <li><b>Aulos & Lyre:</b> The two main instruments. The Aulos was a double-reed wind instrument associated with Dionysian frenzy, while the Lyre was a stringed instrument associated with Apollo and reason.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the Dorian, Phrygian, and Lydian modes. Imagine the Ethos they might carry!</i></p>
        """

    def get_egyptian_html(self):
        return """
        <h2>Ancient Egyptian Music Theory</h2>
        <p>Ancient Egyptian music was deeply intertwined with religion, ritual, and the afterlife. While no full written scores survive, tomb paintings and artifacts reveal a highly sophisticated musical culture.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Sistrum:</b> A sacred rattle consisting of a metal frame threaded with loose metal discs. Shaken by priestesses of the goddess Hathor, it produced a bright, jangling sound believed to appease the gods and drive away evil.</li>
            <li><b>Benet (Archer's Bow Harp):</b> The most iconic Egyptian instrument. These harps varied from small shoulder harps to massive floor-standing models with up to 22 strings, often heavily decorated with gold and the head of the pharaoh.</li>
            <li><b>Pentatonic and Microtonal Scales:</b> Based on the tuning of surviving flutes and harps, Egyptian music likely used pentatonic scales, but also incorporated microtonal inflections, similar to modern Middle Eastern music.</li>
            <li><b>Call and Response:</b> Tomb lyrics suggest a heavy use of antiphonal (call-and-response) singing between a priest/priestess and the chorus.</li>
        </ul>
        """

    def get_nubian_html(self):
        return """
        <h2>Nubian Music Theory (Egypt/Sudan)</h2>
        <p>Nubian music, originating from the region along the Nile in southern Egypt and northern Sudan, is distinct from Arabic Egyptian music. It is deeply rooted in African pentatonic systems and utilizes a unique modal framework called <b>Kashif</b>.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Kashif:</b> The Nubian modal system. Unlike the Arabic Maqam, Kashif is heavily pentatonic. It relies on specific melodic patterns and microtonal inflections that evoke the landscapes of the Nubian desert.</li>
            <li><b>Tar:</b> A traditional frame drum, essential to Nubian rhythm. It provides a steady, pulsing beat that often accompanies call-and-response singing at weddings and festivals.</li>
            <li><b>Oud:</b> While adopted from Arabic culture, the Nubian Oud is tuned to reflect the Kashif modes, giving it a distinctly Nubian, rather than Arabic, sound.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Ambasel" scale to hear a similar pentatonic structure with augmented 2nds, common in the region.</i></p>
        """

    def get_tuareg_html(self):
        return """
        <h2>Tuareg Music Theory (Sahara)</h2>
        <p>The Tuareg are a nomadic people of the Sahara desert. Their music is traditionally vocal and percussive, but in the 1970s, the introduction of the electric guitar created <b>Tishoumaren</b>, or "desert blues."</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Tishoumaren:</b> A genre blending traditional Tuareg melodies with the blues and rock guitars of artists like Jimi Hendrix. The guitars are often tuned to open chords, creating a continuous, hypnotic drone.</li>
            <li><b>Tendé:</b> A traditional drum made from a mortar covered with a goatskin. It provides a distinct, galloping polyrhythm. Tishoumaren often mimics the Tendé rhythm on the drum kit.</li>
            <li><b>Call and Response:</b> Tuareg music heavily features antiphonal singing, where a lead vocalist is answered by a chorus of men or women.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Minor Pentatonic" scale, which forms the basis of much Tuareg guitar music.</i></p>
        """

    def get_indian_html(self):
        return """
        <h2>Indian Classical Music Theory</h2>
        <p>Indian classical music focuses heavily on melody and rhythm, with harmony being entirely absent in the traditional sense.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Raga:</b> More than a scale, a Raga is a melodic framework for improvisation.</li>
            <li><b>Tala:</b> The rhythmic framework (e.g., Teental is a 16-beat cycle).</li>
            <li><b>Drone (Tanpura):</b> A continuous drone establishes the tonal center.</li>
            <li><b>Shruti:</b> 22 microtones in an octave allowing for pitch inflections.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start a background drone, then play notes on the piano over it!</i></p>
        """

    def get_karnatic_html(self):
        return """
        <h2>Karnatic Music Theory (South Indian)</h2>
        <p>While related to Hindustani (North Indian) music, Karnatic music (South India) is highly mathematically structured and emphasizes composed songs (Kritis) alongside improvisation.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Konnakol:</b> The art of vocal percussion. Konnakol syllables (Ta, Ka, Dhi, Mi, Tha, etc.) are spoken to dictate complex rhythmic patterns with perfect clarity and groove.</li>
            <li><b>Melakarta:</b> The 72 parent ragas (scales) of Karnatic music. They contain exactly 7 notes in both ascending and descending forms, forming the basis of all other ragas.</li>
            <li><b>Adi Tala:</b> The most common rhythmic cycle, consisting of 8 beats. It is often clapped as: Clap, Wave, Clap, Wave (beats 1, 3, 5, 7).</li>
            <li><b>Kalpanaswaram:</b> Improvisation using rhythmic note syllables (Sa, Ri, Ga, Ma). The soloist trades rapid mathematically precise note patterns with the drummer.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Konnakol/Tala Trainer and hear the 8-beat Adi Tala cycle!</i></p>
        """

    def get_persian_html(self):
        return """
        <h2>Persian Classical Music Theory</h2>
        <p>Persian classical music (traditional Iranian music) is based on the <b>Radif</b>, a vast collection of traditional melodies and motifs. It is deeply poetic and heavily utilizes microtones.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Dastgāh:</b> A modal framework. There are 7 main Dastgāhs and several sub-modes (Āvāz). Each Dastgāh has a specific emotional character and rules for ascending and descending.</li>
            <li><b>Tahrir:</b> A highly distinctive vocal technique involving rapid ornamental leaps, vocal vibrations, and undulations. It is often compared to the 'crying' or 'sobbing' of the voice and is central to Persian singing.</li>
            <li><b>Gusheh:</b> Smaller melodic units that make up a Dastgāh. A performance moves through different Gushehs, gradually modulating and returning to the main mode.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Shur" scale approximation or slide the Microtonal Slider!</i></p>
        """

    def get_arabic_html(self):
        return """
        <h2>Arabic Music Theory (Tarab)</h2>
        <p>Arabic classical music is deeply modal and microtonal. However, its core theory extends beyond pitch and rhythm into the concept of <b>Tarab</b>—the psychological state of musical ecstasy.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Tarab:</b> Translates roughly to "musical ecstasy" or "enchantment." It is not a genre, but a theoretical framework. A performance is only considered successful if it induces Tarab in the audience, often causing them to exclaim "Allah!"</li>
            <li><b>Waslah:</b> A musical suite. It is a sequence of different pieces (instrumental preludes, vocal pieces, improvisations) all bound together by the same Maqam (mode).</li>
            <li><b>Taqsīm:</b> A metrically free instrumental improvisation. The performer explores the Maqam, demonstrating technical mastery and building emotional tension before returning to the composed piece.</li>
            <li><b>Iqa':</b> Rhythmic cycles. Unlike Western rhythm, which is divided into measures, Iqa' are specific patterns of strong and weak beats (e.g., Dum-Tak-Tak).</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the 'Bayati' scale or slide the Microtonal Slider to hear the quarter tones essential to Tarab!</i></p>
        """

    def get_sufi_html(self):
        return """
        <h2>Sufi Music Theory (Qawwali)</h2>
        <p>Sufi music is the devotional music of Islamic mysticism. Its primary purpose is to induce <b>Wajd</b>—a state of spiritual ecstasy or trance where the listener feels united with the divine.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Qawwali:</b> A popular form of Sufi music originating in South Asia. It features a lead vocalist (Qawwal) backed by a group of chorus singers, hand-clapping, and a harmonium. The tempo gradually accelerates from a slow, meditative pulse to a frantic, driving rhythm.</li>
            <li><b>Tarana:</b> A vocal style using rhythmic nonsense syllables (e.g., "tana dere na dim tanana"). These syllables are derived from Persian and Arabic drum mnemonics and are used to emulate percussion, bypassing the logical brain to induce trance.</li>
            <li><b>Harmonium:</b> A small, hand-pumped reed organ. It provides a continuous drone and melodic support. It is not native to India but was adopted by Sufi musicians and is now central to the sound.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Konnakol/Tala Trainer to hear a rhythmic vocal cycle similar to Tarana syllables!</i></p>
        """

    def get_east_asian_html(self):
        return """
        <h2>East Asian Music Theory</h2>
        <p>East Asian music historically emphasizes timbre, melody, and nature over Western-style harmony. Pentatonic scales are foundational.</p>
        <h3>Chinese Music</h3>
        <ul><li><b>Wu Yin (Five Tones):</b> The Chinese pentatonic scale, corresponding to philosophical elements.</li></ul>
        <h3>Japanese Music</h3>
        <ul>
            <li><b>Hirajoshi & In Sen:</b> Distinctive 5-tone scales featuring minor 2nd intervals.</li>
            <li><b>Ma (間):</b> The concept of 'negative space' or silence between notes.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the Hirajoshi and In Sen scales!</i></p>
        """

    def get_ainu_html(self):
        return """
        <h2>Ainu Music Theory (Japan/Russia)</h2>
        <p>The Ainu are an indigenous people of Hokkaido (Japan), Sakhalin, and the Kuril Islands (Russia). Their music is deeply animistic, intended to interact with the spirits (Kamuy) present in nature.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Upopo:</b> Traditional Ainu round singing. Often performed by women sitting in a circle, the singers interlock short, repetitive melodic phrases, creating a hypnotic, cyclical texture.</li>
            <li><b>Mukkuri:</b> A traditional mouth harp made of bamboo. The player plucks a string while changing the shape of their mouth cavity to amplify specific overtones, creating a distinct, buzzing melodic sound.</li>
            <li><b>Tonkori:</b> A stringed instrument played by the Ainu. It has a flat body and 5 strings, often played with a droning open string while the melody is plucked on top.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Ainu Pentatonic" scale.</i></p>
        """

    def get_okinawan_html(self):
        return """
        <h2>Okinawan Music Theory (Japan)</h2>
        <p>Okinawa (the Ryukyu Islands) has a musical tradition entirely distinct from mainland Japan. It is heavily vocal, featuring the <b>Sanshin</b> and a unique pentatonic scale.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Ryukyu Scale:</b> A distinct pentatonic scale (Do, Mi, Fa, Sol, Ti). Unlike the Japanese Hirajoshi, this scale has a major third, giving it a bright, open, and distinctly tropical sound.</li>
            <li><b>Sanshin:</b> A 3-stringed banjo-like lute covered in snakeskin. It is the precursor to the Japanese shamisen. The strings are plucked with a plectrum worn on the index finger.</li>
            <li><b>Minyo & Glissando:</b> Okinawan folk singing (Minyo) is characterized by a heavy use of glissando (sliding between pitches) and falsetto. The singer will often slide into notes from below, giving the vocal line a crying, emotional quality.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Okinawa (Ryukyu)" scale!</i></p>
        """

    def get_korean_html(self):
        return """
        <h2>Korean Gugak Theory (Pansori)</h2>
        <p>Korean traditional music (Gugak) spans from court orchestras to folk traditions. <b>Pansori</b> is a highly dramatic form of musical storytelling where a single vocalist is accompanied by a drummer.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Pansori:</b> A long, epic vocal performance (often lasting hours) by a solo singer (Sorikkun). The singer uses a fan to mark dramatic moments, shifting between spoken word (Aniri) and sung narrative (Chang).</li>
            <li><b>Buk:</b> A wooden barrel drum played by the Kosu (drummer). The drummer provides the rhythmic cycle (Jangdan) but also actively participates by shouting vocal encouragements.</li>
            <li><b>Chuimsae:</b> The vocal exclamations made by the drummer and the audience (e.g., "Jihota!", "Suhlsseu!"). This is a crucial element of Korean music, blurring the line between performer and listener.</li>
            <li><b>Jangdan:</b> The rhythmic cycles in Korean music. They dictate not just the beat, but the emotional tempo of the piece (e.g., Jin-yang is slow and sad, Jajinmori is fast and lively).</li>
        </ul>
        """

    def get_vietnamese_html(self):
        return """
        <h2>Vietnamese Traditional Music Theory</h2>
        <p>Vietnamese music is a blend of indigenous Southeast Asian traditions, Chinese influence, and later, French musical elements. It is deeply pentatonic but features unique ornaments and tuning.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Đàn Bầu:</b> A monochord zither (one string). The player touches the string at specific nodes to create pure, bell-like harmonics. It is entirely unique to Vietnam and relies on the acoustic Overtone Series.</li>
            <li><b>Bắc & Nam Modes:</b> Traditional music divides into Northern (Bắc) and Southern (Nam) modes. Bắc is generally happier and uses a major pentatonic, while Nam is melancholic and uses different microtonal inflections.</li>
            <li><b>Vibrato (Luyến láy):</b> Extremely deep, wide vibrato is used on string instruments to bend pitches between the standard notes, filling the "spaces" of the pentatonic scale.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to visualize the Overtone Series (which makes the Đàn Bầu possible), and play the "Vietnamese Bac" scale!</i></p>
        """

    def get_indonesian_html(self):
        return """
        <h2>Indonesian Music Theory (Gamelan)</h2>
        <p>The music of Java and Bali is centered around the Gamelan ensemble (metallophones, xylophones, and gongs). It features unique tuning systems and a deeply layered structure.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Tuning Systems:</b> Gamelan uses two completely distinct scales: <b>Slendro</b> (5 tones, roughly equal) and <b>Pelog</b> (7 tones, unequal intervals).</li>
            <li><b>Heterophony:</b> The central texture of Gamelan. All instruments play the same core melody, but faster instruments add elaborate ornaments while slower instruments play simplified versions.</li>
            <li><b>Colotomic Structure:</b> The music is not measured by measures, but by the strikes of large gongs. The largest gong marks the end of the cyclical phrase.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to hear the 'Pelog' scale, and click the 'Heterophony' button in the Texture Trainer!</i></p>
        """

    def get_balinese_html(self):
        return """
        <h2>Balinese Music Theory (Kecak)</h2>
        <p>While Bali shares the Gamelan tradition with Java, Balinese music is generally faster, louder, and more volatile. The most unique Balinese vocal tradition is <b>Kecak</b>.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Kecak:</b> Also known as the "Monkey Chant." It is a form of Balinese vocal music where dozens of men sit in concentric circles and interlock rhythmic syllables (most commonly "Cak"). There are no instruments; the human voices mimic the interlocking patterns of the Gamelan.</li>
            <li><b>Interlocking (Kotekan):</b> The structural basis of Kecak. Two or more vocal parts split a single fast melody between them. No single singer sings the whole melody; they rapidly alternate notes to create a continuous, hypnotic stream of sound.</li>
            <li><b>Trance:</b> Kecak was originally performed during ritual dances to induce a trance state, allowing spirits to enter the dancers' bodies.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to open the Kecak Interlocking Trainer and hear how three voices interlock to create a dense polyrhythm!</i></p>
        """

    def get_filipino_html(self):
        return """
        <h2>Filipino Music Theory (Kulintang)</h2>
        <p>The Kulintang tradition of the southern Philippines (Mindanao) is one of the oldest gong ensembles in Southeast Asia. Unlike Gamelan, it is highly rhythmic and relies heavily on interlocking patterns.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Kulintang:</b> A row of 8 small, horizontal knobbed gongs. It plays the core melody.</li>
            <li><b>Babendil:</b> A small single gong played with bamboo sticks. It acts as the timekeeper, striking the main beat.</li>
            <li><b>Interlocking Rhythms:</b> The Agung (large wide-rimmed gongs) and Gandingan (four hanging gongs) play intricate, interlocking rhythmic patterns that weave around the Kulintang melody.</li>
            <li><b>Aural Tradition:</b> Kulintang is entirely taught by ear. There is no standardized notation, allowing each player to improvise variations on the memorized patterns.</li>
        </ul>
        """

    def get_middle_eastern_html(self):
        return """
        <h2>Middle Eastern & Central Asian Theory</h2>
        <p>This region features highly developed modal systems that predate Western equal temperament. Microtones (quarter tones) are essential.</p>
        <h3>Arabic (Maqam)</h3>
        <ul>
            <li><b>Maqam:</b> Dictates melodic development, starting notes, and characteristic phrases.</li>
            <li><b>Quarter Tones:</b> The octave is divided into 24 tones.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the 'Bayati' scale or slide the Microtonal Slider!</i></p>
        """

    def get_andalusi_html(self):
        return """
        <h2>Andalusi Music Theory (North Africa)</h2>
        <p>Andalusi music is a classical tradition of Morocco, Algeria, and Tunisia. It originated in the courts of Al-Andalus (medieval Muslim Spain) and blends Arab, Berber, and Spanish elements.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Nuba (Nouba):</b> A large, multi-movement musical suite. Each Nuba is based on a specific modal framework (Tab') and follows a strict rhythmic progression.</li>
            <li><b>Al-Hijaz:</b> A primary melodic mode used in Andalusi music, equivalent to the Phrygian Dominant scale, characterized by an augmented second between the 2nd and 3rd degrees.</li>
            <li><b>Mizan:</b> The rhythmic cycle or meter that dictates the movement of the Nuba.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Al-Hijaz" scale!</i></p>
        """

    def get_ethiopian_html(self):
        return """
        <h2>Ethiopian Music Theory (Azmari)</h2>
        <p>Ethiopian music is entirely unique in Africa, isolated from external influences for millennia. It uses a distinct pentatonic system (the <b>Kignet</b>) that heavily features augmented 2nd intervals, giving it a deeply yearning, emotional quality.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Ambasel:</b> One of the primary Ethiopian scales. It is a pentatonic scale, but its interval structure includes an augmented 2nd (e.g., C, Db, E, G, Ab), creating a distinctly minor, mournful sound.</li>
            <li><b>Tizita:</b> Another primary scale. Often compared to the major pentatonic, but in Ethiopian theory, it is associated with the concept of "nostalgia" or "deep memory" and is played with specific microtonal bends.</li>
            <li><b>Masenqo:</b> A single-stringed bowed lute used by Azmari (minstrels). The player bows the string while pressing it with the side of the finger, allowing for incredible microtonal slides.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Ambasel" scale and hear the unique augmented 2nd interval!</i></p>
        """

    def get_tuvan_html(self):
        return """
        <h2>Tuvan Throat Singing Theory (Siberia)</h2>
        <p>Tuva is a republic in southern Siberia. Tuvan music is famous for its throat singing (Xöömei), where a single singer produces multiple pitches simultaneously by manipulating the vocal tract.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Khoomei:</b> The base style of throat singing. The singer constricts the throat, producing a buzzing fundamental drone while isolating a mid-range harmonic melody.</li>
            <li><b>Sygyt:</b> A high, whistling style. The tongue is placed near the roof of the mouth to isolate extremely high, piercing overtones, creating a sound akin to a bird.</li>
            <li><b>Kargyraa:</b> A deep, growling style. The singer uses the false vocal cords to produce a sub-harmonic an octave below the fundamental, creating an incredibly low, rumbling drone.</li>
            <li><b>Igil:</b> A two-stringed bowed instrument made from a wooden horse head, used to accompany throat singing.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to try the Overtone Singer Simulator. Start the low drone, then click the high overtone buttons to simulate throat singing!</i></p>
        """

    def get_shona_html(self):
        return """
        <h2>Shona Music Theory (Zimbabwe)</h2>
        <p>The Shona people of Zimbabwe have a deep musical tradition centered around the <b>Mbira dzavadzimu</b> (thumb piano). It is used in Bira ceremonies to contact ancestor spirits.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Kushaura & Kutsinhira:</b> The fundamental structure of Shona music is interlocking parts. The <b>Kushaura</b> is the lead part that establishes the pattern. The <b>Kutsinhira</b> is the follower part, which plays in the gaps of the Kushaura, creating a continuous, interwoven stream of notes.</li>
            <li><b>Hosho:</b> A gourd shaker filled with seeds. It provides a steady, swinging 12/8 pulse that anchors the complex interlocking mbira parts.</li>
            <li><b>Cyclical Form:</b> Mbira music is cyclical. A standard piece might be a 48-beat cycle. Players can stay in the cycle for hours, subtly shifting accents and variations.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Mbira Interlocking Simulator and hear the Kushaura and Kutsinhira parts weave together!</i></p>
        """

    def get_basque_html(self):
        return """
        <h2>Basque Music Theory (Spain/France)</h2>
        <p>The Basque Country, straddling the border of Spain and France, possesses a completely unique musical tradition. It is heavily rhythmic and relies on strict interlocking percussion.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Txalaparta:</b> A wooden percussion instrument consisting of thick boards laid over supports (often baskets). Two players (Txalapartaris) strike the boards with thick wooden dowels. The rule is strict: they must never hit the boards at the same time. They interlock their strikes to create a continuous, driving rhythm.</li>
            <li><b>Zortziko:</b> A traditional Basque dance and meter in 5/8 time. It is often subdivided as 2+3 or 3+2, giving it a distinct, limping feel.</li>
            <li><b>Txistu:</b> A three-hole flute played entirely with one hand. This allows the player to play the Txistu while simultaneously playing a drum (Tamboril) with the other hand.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to open the Txalaparta Interlocking Trainer and see how two players must alternate perfectly!</i></p>
        """

    def get_sardinian_html(self):
        return """
        <h2>Sardinian Music Theory (Italy)</h2>
        <p>Sardinia, an island off the coast of Italy, has an isolated and ancient musical culture. It is famous for a cappella vocal polyphony and a unique triple clarinet.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Tenores:</b> A style of polyphonic singing (e.g., Tenores di Bitti). Four male voices sing interlocking parts. The bass voice (Bassu) sings incredibly low, using a sub-harmonic throat singing technique similar to Tuvan Kargyraa, creating a buzzing drone.</li>
            <li><b>Launeddas:</b> A triple clarinet consisting of three pipes. Two pipes play the melody and harmony (often using a drone), while the third is a drone. It requires circular breathing, allowing a player to sustain sound indefinitely.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Sardinian" scale approximation, or use the Overtone Singer Simulator to understand the Bassu sub-harmonic technique.</i></p>
        """

    def get_balkan_html(self):
        return """
        <h2>Eastern European & Balkan Music Theory</h2>
        <p>The music of the Balkans and Eastern Europe is famous for its incredibly complex, "limping" rhythms and rich modal scales.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Aksak (Asymmetric Meter):</b> Beats are grouped in unequal patterns, such as 2+2+3 (7/8 time) or 2+2+2+3 (9/8 time).</li>
            <li><b>Freygish (Phrygian Dominant):</b> A modal scale heavily used in Balkan brass band music.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Asymmetric Rhythm Trainer and feel the 7/8 beat!</i></p>
        """

    def get_bulgarian_html(self):
        return """
        <h2>Bulgarian Choral Theory</h2>
        <p>Bulgarian women's choral music is world-renowned for its piercing, open-throated vocal style and its highly dissonant, complex polyphony.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Diaphony:</b> A traditional form of two-voice polyphony. One voice sings a drone while another sings a highly ornamented melody. The voices deliberately clash on major and minor 2nds, creating a sharp, biting resonance.</li>
            <li><b>Additive Meters:</b> Bulgarian music is famous for asymmetric meters that add groups of 2s and 3s, such as 7/8, 9/8, 11/16, and even 25/16.</li>
            <li><b>"Open Throat" Singing:</b> Singers project from the chest with a completely open throat, creating a bright, powerful, and slightly nasal tone that easily cuts through loud instruments.</li>
        </ul>
        """

    def get_georgian_html(self):
        return """
        <h2>Georgian Music Theory (Caucasus)</h2>
        <p>Georgia has one of the oldest polyphonic traditions in the world, predating Western European polyphony by centuries. It is characterized by stark, dissonant harmonies that are considered perfectly consonant to the Georgian ear.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Three-Voice Polyphony (Mkhrali):</b> Two highly ornamented upper voices sing interlocking melodies over a continuous bass drone. The upper voices often move in parallel fifths.</li>
            <li><b>Consonance of the 2nd:</b> Unlike Western theory, where the major and minor 2nd are considered dissonant intervals that must resolve, Georgian singers frequently emphasize and sustain these 2nds, creating a sharp, buzzing acoustic resonance.</li>
            <li><b>Yodeling (Krimanchuli):</b> A highly virtuosic vocal technique where the singer rapidly alternates between chest voice and falsetto, often used as a rhythmic and textural decoration in the middle voice.</li>
        </ul>
        """

    def get_klezmer_html(self):
        return """
        <h2>Klezmer Music Theory (Ashkenazi Jewish)</h2>
        <p>Klezmer is the traditional instrumental music of the Ashkenazi Jews of Eastern Europe. It is deeply emotive, blending synagogue modes with Eastern European dance rhythms.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Ahavoh Rabboh:</b> The most famous Jewish prayer mode (and scale). It is similar to the Freygish scale but features a natural 7th, giving it a uniquely emotional, ascending resolution.</li>
            <li><b>Bulgar:</b> A lively circle dance in 8/8 time, subdivided 3+3+2. It feels like a jazzy, syncopated waltz.</li>
            <li><b>Krechtz:</b> A vocal-like "sob" or ornamental bend executed on the violin or clarinet, meant to mimic the human cry.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Ahavoh Rabboh" scale!</i></p>
        """

    def get_flamenco_html(self):
        return """
        <h2>Flamenco Music Theory (Spain)</h2>
        <p>Flamenco is a fierce, emotive art form from Andalusia, Spain, combining Romani, Moorish, and Spanish roots. It is built on specific chord progressions and cyclical rhythms.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Andalusian Cadence:</b> A descending chord progression: i - VII - VI - V (e.g., Am - G - F - E). It is the harmonic backbone of Flamenco.</li>
            <li><b>Compás:</b> The rhythmic cycle. Flamenco compás often follows a 12-beat cycle with specific accents.</li>
            <li><b>Phrygian Dominant:</b> A mode built on the 5th degree of the harmonic minor scale, giving Flamenco its distinct "Spanish" sound.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Andalusian Cadence" in the Progression Player!</i></p>
        """

    def get_tango_html(self):
        return """
        <h2>Argentine Tango Music Theory</h2>
        <p>Born in the working-class neighborhoods of Buenos Aires at the turn of the 20th century, Tango is a fusion of African, European, and Indigenous rhythms. It is intensely passionate and structurally rigid.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Habanera Rhythm:</b> A syncopated 3-3-2 pattern (dum... dum... dum-dum). This rhythmic cell is the heartbeat of Tango, derived from Cuban contradanza.</li>
            <li><b>Arrastre:</b> Meaning "drag". Tango musicians deliberately push and pull the tempo, rushing certain beats and dragging others, to create a heavy, emotional tension.</li>
            <li><b>Bandoneon:</b> A square, button-operated free-reed instrument. It is the soul of Tango. Unlike an accordion, it produces different notes on push and pull, allowing for incredibly expressive breathing effects.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Argentine Tango Habanera Trainer and hear the 3-3-2 syncopation!</i></p>
        """

    def get_armenian_html(self):
        return """
        <h2>Armenian & Caucasian Music Theory</h2>
        <p>The music of the Caucasus region (Armenia, Georgia, Azerbaijan) is ancient, featuring complex polyphony and highly ornamented modal melodies.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Duduk:</b> A double-reed instrument made of apricot wood. Its tone is so warm and mournful that it is often mistaken for a human voice. It relies heavily on microtonal vibrato.</li>
            <li><b>Hijaz Kar:</b> A prominent modal scale in Armenian music, featuring two augmented second intervals, creating a deeply exotic and emotional sound.</li>
            <li><b>Georgian Polyphony:</b> Unlike most Eastern music, traditional Georgian singing features complex, dissonant polyphony (three independent voices) that predates Western harmony by centuries.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Hijaz Kar" scale!</i></p>
        """

    def get_turkic_html(self):
        return """
        <h2>Turkic & Mongolian Music Theory</h2>
        <p>The music of Central Asia is deeply tied to the vast steppes and nature. It is famous for its unique vocal techniques and overtone-rich instruments.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Khoomei (Throat Singing):</b> A vocal technique where the singer manipulates the harmonics of their voice to produce two or three distinct pitches simultaneously.</li>
            <li><b>Pentatonic Scales:</b> Melodies are almost entirely pentatonic, allowing them to seamlessly float over the vocal drone.</li>
            <li><b>Morin Khuur:</b> The traditional horse-head fiddle. It produces a continuous drone while the upper string plays the melody.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to try the Overtone Singer Simulator, the acoustic principle that makes throat singing possible!</i></p>
        """

    def get_tibetan_html(self):
        return """
        <h2>Tibetan & Himalayan Music Theory</h2>
        <p>The music of Tibet, Bhutan, and the Himalayas is deeply spiritual, rooted in Buddhist meditation and ritual. It prioritizes timbre, drones, and acoustic phenomena over melodic complexity.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Singing Bowls:</b> Metallic or crystal bowls that, when struck or rubbed, produce a rich fundamental pitch alongside loud, sustained overtones.</li>
            <li><b>Multiphonic Chanting:</b> Also known as 'overtone singing' or 'deep voice chanting'. Monks lower their fundamental pitch drastically while constricting their throat to amplify specific overtones, making a single person sound like a chord.</li>
            <li><b>Non-Metric Rhythm:</b> Chants often lack a strict meter or pulse, unfolding slowly and naturally like a meditation, rather than keeping time.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to try the Overtone Singer Simulator and hear how a fundamental drone can be manipulated!</i></p>
        """

    def get_saami_html(self):
        return """
        <h2>Saami (Scandinavian) Music Theory</h2>
        <p>The Sámi people of Northern Scandinavia (Lapland) have a distinct vocal tradition called Joik (or Luohti). It is one of the oldest musical forms in Europe.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Joik:</b> Unlike a standard song that is 'about' a subject, a Joik is meant to 'evoke' or 'be' the subject (a person, an animal, a place). You don't joik *about* a bear, you joik the bear.</li>
            <li><b>Non-Metric Rhythm:</b> Joiks do not have a strict beat or time signature. They flow freely, driven by the emotion and natural rhythm of the words.</li>
            <li><b>Microtonal Inflection:</b> Joik heavily uses slides, glissandos, and pitches that fall between the cracks of the Western piano keys.</li>
        </ul>
        """

    def get_appalachian_html(self):
        return """
        <h2>Appalachian & Old-Time Music Theory</h2>
        <p>Appalachian music is a fusion of Scottish, Irish, and English folk traditions brought to the mountains of America, heavily influenced by African American banjo playing.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Mountain Modal (Aeolian):</b> Old-Time music frequently uses unaccompanied modal melodies rather than standard major scales. The Aeolian (natural minor) and Dorian modes are staples.</li>
            <li><b>Clawhammer Banjo:</b> A rhythmic playing style where the fingernail strikes down on the strings, creating a highly percussive, syncopated drone.</li>
            <li><b>Drone Strings:</b> Instruments like the banjo and fiddle often feature a top string tuned to an open note (like G or A) that is played continuously, mimicking the bagpipes of their Celtic ancestors.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start a Drone and play the "Aeolian" scale over it!</i></p>
        """

    def get_inuit_html(self):
        return """
        <h2>Inuit & Arctic Music Theory</h2>
        <p>The music of the Inuit, Yupik, and other Arctic peoples is uniquely adapted to the frozen north. It relies heavily on the voice and breath, as wood for instruments is scarce.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Katajjaq (Throat Singing):</b> A musical game traditionally played by two women facing each other. They produce rhythmic, guttural sounds from their throats, alternating breaths so that one singer's exhale is the other's inhale.</li>
            <li><b>Breath as Rhythm:</b> The rhythm in Arctic music is often dictated by the natural limitations of the human lung capacity, creating pulsing, circular patterns.</li>
            <li><b>Pentatonic Melodies:</b> When pitched singing occurs, it often uses small pentatonic intervals, focusing more on the timbre and rhythm than melodic expansion.</li>
        </ul>
        """

    def get_cajun_html(self):
        return """
        <h2>Cajun & Zydeco Music Theory (Louisiana)</h2>
        <p>Cajun and Zydeco are the music of South Louisiana. Cajun music comes from the Acadians (French Canadians expelled by the British), while Zydeco is the music of the Creole (French-speaking Black) population.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Accordion & Fiddle:</b> The melodic foundation of Cajun music. The diatonic button accordion can only play notes of a specific scale, forcing the music into distinct major or minor modes.</li>
            <li><b>Frottoir (Washboard):</b> The defining instrument of Zydeco. A metal washboard worn on the chest and scraped with spoons or bottle openers, providing a highly syncopated, driving rhythm.</li>
            <li><b>Form:</b> Much of this music is built around a standard two-step (4/4) or waltz (3/4) structure, heavily emphasizing the backbeat (beats 2 and 4).</li>
        </ul>
        """

    def get_south_african_html(self):
        return """
        <h2>South African Music Theory (Isicathamiya)</h2>
        <p>South Africa has a rich choral tradition. <b>Isicathamiya</b> is a style developed by Zulu migrant workers living in hostels. It is famous worldwide through the group Ladysmith Black Mambazo.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Soft Step (Isicathamiya):</b> The name translates to "to walk or step like a cat." The choreography is subdued and tight, contrasting with the loud, stomping dances of traditional Zulu war dances (Indlamu).</li>
            <li><b>Four-Part Harmony:</b> Heavy influence from Christian hymns (Mission harmony) fused with Zulu choral traditions. It features a dominant bass voice, a high tenor lead, and alto/baritone backing.</li>
            <li><b>Call and Response:</b> The lead singer proposes a phrase, and the group responds. The lyrics often deal with the hardship of migrant labor, morality, and daily life.</li>
        </ul>
        """

    def get_haitian_html(self):
        return """
        <h2>Haitian Music Theory (Vodou)</h2>
        <p>Haitian Vodou music is a profound fusion of West African (Dahomey and Yoruba) traditions. It is strictly functional: the rhythms are designed to invoke specific spirits, known as <b>Loa</b>.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Rada & Petro:</b> The two main rites of Vodou drumming. Rada is gentler, steadier, and rooted in Dahomey. Petro is faster, more aggressive, and uniquely Haitian.</li>
            <li><b>Ogan:</b> An iron bell that plays a steady, unyielding timeline pattern. It is the foundation of the rhythm, anchoring the drums.</li>
            <li><b>Assotor & Tanbou:</b> A family of sacred drums. The Assotor is the largest. The lead drummer (Hounguenikon) improvises complex, syncopated patterns over the steady Ogan.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Haitian Vodou Rhythm Trainer and see how the Ogan and Drum interlock!</i></p>
        """

    def get_garifuna_html(self):
        return """
        <h2>Garifuna Music Theory (Central America)</h2>
        <p>The Garifuna are an Afro-Indigenous people living in Belize, Guatemala, and Honduras. Their music blends West African polyrhythms with Arawak/Carib elements.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Punta:</b> The most famous Garifuna rhythm and dance. It is a rapid 2/4 pattern heavily syncopated, often using a hemiola (3-against-2 feel). It is danced at wakes to celebrate the passing of life.</li>
            <li><b>Paranda:</b> A slower, acoustic guitar style. It combines African rhythmic patterns with Spanish guitar chords, often used for songs of lament or storytelling.</li>
            <li><b>Call and Response:</b> A heavy reliance on antiphonal singing between a lead vocalist and a chorus of women.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Polyrhythm Trainer (3 against 2) to hear the rhythmic basis of Punta!</i></p>
        """

    def get_pygmy_html(self):
        return """
        <h2>Pygmy Music Theory (Central Africa)</h2>
        <p>The Mbuti and Baka peoples (historically referred to as Pygmies) of the Congo rainforest possess one of the most complex and ancient vocal polyphonic traditions on earth. Their music is deeply communal and tied to the forest.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Yodeling:</b> The defining vocal characteristic. Singers rapidly switch between chest voice and falsetto, allowing a single singer to hold two distinct melodic lines in a round.</li>
            <li><b>Hocketing Polyphony:</b> Complex, interwoven melodies are created not by one singer, but by the entire community. Each singer only contributes one or two notes; the full melody only emerges when all voices combine.</li>
            <li><b>Cyclical Form:</b> The music has no distinct beginning or end. It is a continuous, looping texture that can expand or contract based on the ritual, creating a state of hypnotic trance.</li>
        </ul>
        """

    def get_trinidadian_html(self):
        return """
        <h2>Trinidadian Music Theory (Calypso & Soca)</h2>
        <p>Trinidad and Tobago is the birthplace of the Steelpan and the Calypso tradition. The music is deeply rhythmic, satirical, and tied to the annual Carnival celebration.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Steelpan (Pan):</b> The only acoustic instrument invented in the 20th century. Made from 55-gallon oil drums, the concave surface is tuned to create a full chromatic scale, allowing Western harmony to be played on percussion.</li>
            <li><b>Calypso Rhythm:</b> A syncopated 4/4 rhythm with strong ties to West African drumming and French Creole melodies. It emphasizes the off-beat.</li>
            <li><b>Engine Room:</b> The rhythm section of a steelband. It includes drum kits, congas, iron brakes, and cowbells, creating a dense, polyrhythmic foundation for the melody pans.</li>
            <li><b>Extempo:</b> A highly competitive form of improvised Calypso singing where performers battle each other with rapid, rhyming lyrics.</li>
        </ul>
        """

    def get_afrobrazilian_html(self):
        return """
        <h2>Afro-Brazilian (Capoeira & Candomblé) Theory</h2>
        <p>Brazilian music is a profound fusion of Portuguese harmony, Indigenous melodies, and complex West African polyrhythms brought over during the slave trade. Capoeira and Candomblé are deeply rooted in this African heritage.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Berimbau:</b> A single-string percussion instrument (musical bow). It is the lead instrument in Capoeira, dictating the speed and style of the game through specific rhythmic patterns called Toques.</li>
            <li><b>Toque:</b> A specific rhythmic pattern played on the Berimbau. For example, 'São Bento Grande' is fast and encourages aggressive play, while 'Angola' is slow and strategic.</li>
            <li><b>Ladainha:</b> A solo call-and-response song performed at the beginning of a Capoeira roda (circle). The soloist sings a narrative, and the chorus responds with a single, repetitive phrase.</li>
        </ul>
        """

    def get_afrocuban_html(self):
        return """
        <h2>Afro-Cuban (Santeria & Rumba) Theory</h2>
        <p>Afro-Cuban music is the cornerstone of Latin jazz and Salsa. It is born from the blending of Spanish guitar/harmony with West African Yoruba drumning traditions.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Batá Drums:</b> A family of three double-headed sacred drums used in Santeria religious ceremonies. They can "speak" the Yoruba language using specific tones.</li>
            <li><b>The 6/8 Bell Pattern:</b> Also known as the Afro-Cuban or " cascara" pattern. It is a 3-2 clave structure played in 6/8 time. This single rhythmic pattern is the foundation of almost all Afro-Cuban music and heavily influenced the jazz ride cymbal pattern.</li>
            <li><b>Guaguancó:</b> A sub-genre of Rumba featuring polyrhythmic percussion (claves, congas, and cajones) and a call-and-response vocal structure.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Latin Clave Trainer and hear the 3-2 Son Clave!</i></p>
        """

    def get_salsa_html(self):
        return """
        <h2>Cuban Son & Salsa Theory</h2>
        <p>Salsa is essentially a commercial term for Cuban Son music that was popularized in New York by Puerto Rican and Cuban immigrants. It is a brilliant fusion of Afro-Cuban percussion with Western harmony.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Montuno:</b> A syncopated, repeating 2-bar piano or tres (Cuban guitar) vamp. It provides the harmonic foundation over which the horns and vocalist improvise. It is the defining sound of Salsa.</li>
            <li><b>Tumbao:</b> The syncopated bass and conga pattern. The bass plays 'anticipated' notes (hitting on beat 4 or the 'and' of 4), while the conga strikes an open tone on beat 4, creating a driving forward momentum.</li>
            <li><b>Tres:</b> A 3-course (6-string) Cuban guitar. Its doubled strings and specific tuning give it a piercing, metallic sound, ideal for playing the Montuno.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Montuno Piano Trainer and see how the bass and chord interlock!</i></p>
        """

    def get_griot_html(self):
        return """
        <h2>West African Griot (Mandingo) Theory</h2>
        <p>In West Africa (Mali, Senegal, Guinea, Gambia), the Griot (or Jali) is a historian, storyteller, praise singer, and musician. This oral and musical tradition is the grandfather of the American blues.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Kora:</b> A 21-string harp-lute with a large calabash gourd resonator. It is plucked with the thumb and index finger, allowing the player to perform bass, harmony, and melody simultaneously.</li>
            <li><b>12/8 Hemiola Feel:</b> The foundational rhythm of much West African music is a 12/8 time signature. It can be felt as a 3-against-2 polyrhythm (hemiola), creating a continuous, rolling groove that directly evolved into the shuffle rhythm of blues and jazz.</li>
            <li><b>Call and Response:</b> The Griot sings a line, and the chorus (or another instrument) responds. This is the root of the field holler and the gospel choir response in the Americas.</li>
        </ul>
        """

    def get_oceania_html(self):
        return """
        <h2>Oceania & Aboriginal Australian Music</h2>
        <p>Aboriginal Australian music is among the oldest continuous musical traditions on Earth. It is deeply connected to the land, the Dreamtime, and uses instruments unique to the region.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Didgeridoo (Yidaki):</b> A long wooden wind instrument that produces a continuous, dense drone. Players use <b>circular breathing</b> to maintain the sound indefinitely.</li>
            <li><b>Timbre over Pitch:</b> Rather than playing different notes (melody), Didgeridoo players focus on changing the timbre (tone color) using vocalizations and tongue movements.</li>
            <li><b>Clapsticks (Bilma):</b> Used to keep a strict, unyielding rhythmic pulse against the drone of the didgeridoo.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start a Drone, then play rhythmic notes on the piano to simulate this style!</i></p>
        """

    def get_andean_html(self):
        return """
        <h2>Andean & South American Music Theory</h2>
        <p>Andean music (Peru, Bolivia, Ecuador) is a fusion of pre-Columbian indigenous music and European diatonic harmony.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Pentatonic Foundation:</b> Traditional Inca music relies heavily on pentatonic scales.</li>
            <li><b>Hocketing:</b> A technique used in panpipe ensembles where a melody is shared between two or more players. No single player plays the whole melody; they interlock their notes.</li>
            <li><b>Parallel Harmony:</b> Instruments often play the exact same melody but separated by a perfect fourth or fifth.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to try the Hocketing Sequencer and see how two voices can share a single melody!</i></p>
        """

    def get_aymara_html(self):
        return """
        <h2>Aymara Music Theory (Andean)</h2>
        <p>The Aymara people of the altiplano (Bolivia, Peru, Chile) have a distinct approach to panpipe (Siku) music. It is less about individual expression and more about community interdependence.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Siku:</b> The Aymara panpipe. It is physically impossible for one person to play a full melody on a single Siku; the notes are split across two halves.</li>
            <li><b>Ira & Arka:</b> The two halves of the Siku ensemble. The <b>Ira</b> (leader) plays the first note, and the <b>Arka</b> (follower) plays the second. They must interlock perfectly to create a single melody. This symbolizes the dualistic nature of Aymara cosmology (male/female, day/night).</li>
            <li><b>Continuous Breath:</b> Aymara music often features a continuous, rolling sound. Players overlap their breath and use a technique of gentle tongue-articulation to blur the boundaries between notes.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to try the Hocketing Sequencer and simulate the Ira/Arka interlocking technique!</i></p>
        """

    def get_mexican_html(self):
        return """
        <h2>Indigenous Mexican (Mariachi & Son) Theory</h2>
        <p>Mexican folk music is a vibrant blend of indigenous, Spanish, and African elements. <i>Son</i> (regional folk music) and <i>Mariachi</i> rely on specific stringed instruments and syncopated rhythms.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Hemiola:</b> A rhythmic ratio of 3:2. In Mariachi and Son Jalisciense, musicians often play in 3/4 time but accent the beats in a way that makes it temporarily sound like 6/8. This rhythmic tension is central to Mexican folk music.</li>
            <li><b>Guitarrón:</b> A massive acoustic bass guitar that provides the rhythmic and harmonic foundation in Mariachi music, replacing a drum kit.</li>
            <li><b>Vihuela:</b> A small, high-pitched 5-string guitar that plays sharp, syncopated strumming patterns.</li>
        </ul>
        """

    def get_polynesian_html(self):
        return """
        <h2>Polynesian & Hawaiian Music Theory</h2>
        <p>Polynesian music is a beautiful blend of ancient chants and modern harmony introduced by European missionaries in the 19th century. Hawaii is famous for developing unique stringed instrument traditions.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Ki Ho'alu (Slack-Key Guitar):</b> A fingerstyle guitar tradition where the player loosens ("slacks") the strings to create an open major chord. The thumb plays a alternating bass pattern while the fingers play the melody.</li>
            <li><b>Hawaiian Vamp:</b> A standard 3-chord turnaround (D7 - G7 - C) used to end phrases in traditional Hawaiian songs.</li>
            <li><b>Mele:</b> Chants. Ancient Polynesian music was entirely vocal, using poetry to preserve history and genealogy.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Hawaiian Vamp" in the Progression Player, and play the Mixolydian mode!</i></p>
        """

    def get_tahitian_html(self):
        return """
        <h2>Tahitian & Marquesan Music Theory</h2>
        <p>The music of French Polynesia (Tahiti, Marquesas) is built around rapid, percussive stringed instruments and powerful, rhythmic chanting. It is highly energetic and dance-focused.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Fakarava:</b> A highly rapid, percussive ukulele strumming technique. The ukulele in Tahiti is often tuned higher and strung with all identical strings, turning it into a rhythm instrument as much as a melodic one.</li>
            <li><b>Toe Toe:</b> A traditional Marquesan dance involving rhythmic stomping and slapping of the thighs. The rhythm dictates the melody, not the other way around.</li>
            <li><b>Titaré:</b> A fast, 16th-note picking technique on the ukulele that mimics the flow of water or the rapid flutter of bird wings.</li>
        </ul>
        """

    def get_maori_html(self):
        return """
        <h2>Maori Music Theory (Kapa Haka)</h2>
        <p>The Maori people of New Zealand (Aotearoa) have a powerful musical tradition known as <b>Kapa Haka</b> (performing arts). It is deeply communal, using the body as a primary instrument.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Haka:</b> A posture dance featuring rhythmic body slapping (chest, thighs, arms), foot stomping, and fierce, rhythmic chanting. It is not just a war dance; it is used for welcome, mourning, and celebration.</li>
            <li><b>Poi:</b> A tethered weight (often made of raupo reeds) swung in complex rhythmic patterns. Women swing Poi to accompany singing, creating a hypnotic, polyrhythmic visual and auditory texture.</li>
            <li><b>Unison Singing:</b> Maori choral singing emphasizes perfect unison rather than Western harmony. The power comes from the collective volume and the precise timing of the group.</li>
        </ul>
        """

    def get_celtic_html(self):
        return """
        <h2>Celtic & Folk Music Theory</h2>
        <p>Celtic music (Ireland, Scotland, Brittany) relies heavily on specific modes and rhythmic patterns meant for dancing.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Modes:</b> Dorian and Mixolydian modes are incredibly common, giving Celtic music its 'bright but minor' sound.</li>
            <li><b>Drones:</b> Instruments like the Uilleann pipes sustain a constant root note (drone) while the melody plays on top.</li>
            <li><b>Ornamentation:</b> Players use 'cuts' (quick grace notes) and 'rolls' to articulate notes.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start a Drone and play the Dorian mode over it!</i></p>
        """
        
    def get_latin_html(self):
        return """
        <h2>Latin & Caribbean Music Theory</h2>
        <p>Latin music is a massive fusion of Indigenous, African, and European traditions. Rhythm is the driving force.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Clave:</b> A 5-note rhythmic pattern that acts as the foundational heartbeat of Afro-Cuban music.</li>
            <li><b>Montuno:</b> A repeated syncopated piano or horn vamp.</li>
            <li><b>Samba:</b> A Brazilian genre in 2/4 time featuring heavy polyrhythms.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the Latin Clave Trainer or the Montuno Piano Trainer!</i></p>
        """
        
    def get_blues_html(self):
        return """
        <h2>Blues & Jazz Theory (African American Roots)</h2>
        <p>A completely original American art form that synthesized African polyrhythms, field hollers, and European harmony.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Blue Notes:</b> Slightly flattened 3rds, 5ths, and 7ths.</li>
            <li><b>12-Bar Blues:</b> A standard chord progression based on the I-IV-V chords.</li>
            <li><b>Extended Harmony:</b> Jazz expands traditional triads by adding 7ths, 9ths, 11ths, and 13ths.</li>
            <li><b>Secondary Dominants:</b> Using a dominant 7th chord to resolve to a non-tonic chord (e.g., E7 resolving to A minor).</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to play the "Secondary Dominant" progression, or build Altered Chords (7b9)!</i></p>
        """

    def get_african_html(self):
        return """
        <h2>African Music Theory</h2>
        <p>Sub-Saharan African music focuses on complex polyrhythms and communal participation.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Polyrhythm:</b> Simultaneous conflicting rhythms (e.g., 3 beats against 2 beats).</li>
            <li><b>Call and Response:</b> Leader answered by group.</li>
            <li><b>Pentatonic Scales:</b> 5-note scales.</li>
        </ul>
        <p><i>Use the 'Interactive Audio' tab to start the 3-against-2 Polyrhythm Trainer!</i></p>
        """
        
    def get_native_html(self):
        return """
        <h2>Native American Music Theory</h2>
        <p>Characterized by distinct vocal styles, rhythmic structures, and pentatonic scales.</p>
        <h3>Key Concepts:</h3>
        <ul>
            <li><b>Vocables:</b> Non-lexical syllables (e.g., "hey").</li>
            <li><b>Pentatonic Scales:</b> 5-note scales.</li>
            <li><b>Form:</b> Strophic and cyclic repeating forms.</li>
        </ul>
        """

    def get_world_html(self):
        return """
        <h2>World Music & Fusion Theory</h2>
        <p>Looks at the intersection of global traditions.</p>
        <ul>
            <li><b>Microtonality:</b> Intervals smaller than a semitone.</li>
            <li><b>Gamelan Tuning:</b> Slendro (5-tone) and Pelog (7-tone) scales.</li>
        </ul>
        <p><i>Use the Scale Explorer in 'Interactive Audio' to hear the Indonesian 'Pelog' scale!</i></p>
        """
        
    def get_instruments_html(self):
        return """
        <h2>Instruments of the World</h2>
        <p>Theory is realized through physical instruments. Here are some foundational instruments across cultures.</p>
        <h3>African & Afro-Brazilian & South African & Haitian</h3>
        <ul>
            <li><b>Kora:</b> A 21-string bridge-harp used by Griots in West Africa.</li>
            <li><b>Djembe:</b> A rope-tuned skin-covered goblet drum played with bare hands.</li>
            <li><b>Berimbau:</b> A single-string musical bow used in Afro-Brazilian Capoeira.</li>
            <li><b>Ogan:</b> An iron bell used in Haitian Vodou to maintain the timeline.</li>
            <li><b>Assotor:</b> A massive sacred drum used in Haitian Vodou.</li>
        </ul>
        <h3>Eastern (Indian, Persian & Middle Eastern & Arabic & Sufi)</h3>
        <ul>
            <li><b>Sitar:</b> A plucked stringed instrument known for its resonant, droning sound.</li>
            <li><b>Tanpura:</b> A long-necked plucked lute that provides the continuous drone in Indian music.</li>
            <li><b>Tar:</b> A long-necked Persian lute with a double-bowl body.</li>
            <li><b>Oud:</b> A short-neck lute-type instrument central to Arabic Maqam music.</li>
            <li><b>Qanun:</b> A Middle Eastern zither plucked with metal picks, central to the Arabic Takht ensemble.</li>
            <li><b>Harmonium:</b> A hand-pumped reed organ used in Indian and Sufi Qawwali music.</li>
        </ul>
        <h3>East Asian & Vietnamese & Indonesian & Filipino & Korean & Balinese & Okinawan & Ainu</h3>
        <ul>
            <li><b>Guqin:</b> A ancient Chinese fretless zither, prized for its subtle, meditative sound.</li>
            <li><b>Sanshin:</b> An Okinawan 3-stringed snakeskin lute, precursor to the Shamisen.</li>
            <li><b>Đàn Bầu:</b> A Vietnamese monochord zither that plays only natural harmonics.</li>
            <li><b>Koto:</b> A 13-string Japanese zither played with finger picks.</li>
            <li><b>Saron:</b> A bronze metallophone central to the Indonesian Gamelan ensemble.</li>
            <li><b>Kulintang:</b> A row of 8 small, horizontal knobbed gongs from the Philippines.</li>
            <li><b>Buk:</b> A Korean wooden barrel drum used in Pansori.</li>
            <li><b>Mukkuri:</b> An Ainu bamboo mouth harp.</li>
            <li><b>Tonkori:</b> An Ainu stringed instrument.</li>
        </ul>
        <h3>Egyptian & Nubian & Ethiopian & Tuvan & Shona & Armenian & Tibetan & Turkic & Tuareg & Sardinian & Basque</h3>
        <ul>
            <li><b>Sistrum:</b> An ancient Egyptian sacred rattle used to appease the gods.</li>
            <li><b>Tar:</b> A North African/Nubian frame drum.</li>
            <li><b>Tendé:</b> A Tuareg drum made from a mortar and goatskin.</li>
            <li><b>Masenqo:</b> An Ethiopian single-stringed bowed lute.</li>
            <li><b>Igil:</b> A Tuvan two-stringed bowed instrument, often decorated with a carved horse head.</li>
            <li><b>Mbira:</b> A Shona thumb piano with metal tines, played inside a gourd resonator.</li>
            <li><b>Duduk:</b> An Armenian double-reed instrument with a deeply mournful tone.</li>
            <li><b>Singing Bowl:</b> A Tibetan bronze bowl that produces a rich, sustained overtone when rubbed.</li>
            <li><b>Morin Khuur:</b> The Mongolian horse-head fiddle.</li>
            <li><b>Launeddas:</b> A Sardinian triple clarinet requiring circular breathing.</li>
            <li><b>Txalaparta:</b> A Basque wooden percussion instrument struck by two players in interlocking rhythm.</li>
        </ul>
        <h3>Afro-Cuban & Andean & Mexican & Cajun & Trinidadian</h3>
        <ul>
            <li><b>Batá:</b> An Afro-Cuban double-headed hourglass drum.</li>
            <li><b>Tres:</b> A 6-string Cuban guitar central to Son and Salsa.</li>
            <li><b>Siku:</b> Traditional Aymara/Andean panpipes made of bamboo, split into Ira and Arka halves.</li>
            <li><b>Charango:</b> A small 10-string Andean lute traditionally made from an armadillo shell.</li>
            <li><b>Frottoir:</b> A metal washboard worn on the chest, central to Cajun/Zydeco music.</li>
            <li><b>Steelpan:</b> A pitched percussion instrument made from oil drums, central to Trinidadian Calypso.</li>
            <li><b>Guitarrón:</b> A large, deep-bodied Mexican acoustic bass guitar.</li>
        </ul>
        <h3>Argentine & Appalachian & Ancient Greek</h3>
        <ul>
            <li><b>Bandoneon:</b> A square free-reed instrument that produces the signature sound of Argentine Tango.</li>
            <li><b>5-String Banjo:</b> An instrument with a short drone string, central to Old-Time music.</li>
            <li><b>Fiddle:</b> A violin played with a bow, often tuned to open chords to allow drones.</li>
            <li><b>Aulos:</b> An ancient Greek double-reed instrument associated with Dionysian rites.</li>
        </ul>
        <h3>Polynesian & Maori & Tahitian</h3>
        <ul>
            <li><b>Ukulele:</b> A small 4-string guitar derived from Portuguese instruments, central to Hawaiian and Tahitian music.</li>
            <li><b>Poi:</b> A Maori tethered weight swung rhythmically to accompany singing.</li>
        </ul>
        <h3>Native American</h3>
        <ul>
            <li><b>Courting Flute:</b> A wooden end-blown flute often playing in a pentatonic scale.</li>
        </ul>
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MusicTheoryApp()
    window.show()
    sys.exit(app.exec())