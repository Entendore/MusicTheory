"""
Music Theory Learning App - Main Application Window
Enhanced with ear training, scale relationships, search/filter, play buttons, and more.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QListWidget, QListWidgetItem,
    QScrollArea, QFrame, QSplitter, QSizePolicy, QStackedWidget,
    QToolBar, QStatusBar, QTabWidget, QGroupBox, QTextEdit, QGridLayout,
    QLineEdit, QSpinBox, QCheckBox, QSlider, QProgressBar
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QColor, QPalette, QLinearGradient, QPen, QShortcut, QKeySequence

from music_engine import (
    NOTE_NAMES, WESTERN_SCALES, CHORD_TYPES, CHORD_PROGRESSIONS,
    INTERVAL_NAMES, INTERVAL_SHORT, INTERVAL_CONSONANCE, TIME_SIGNATURES,
    CIRCLE_OF_FIFTHS_ORDER, MAJOR_KEY_SIGNATURES, MINOR_KEY_SIGNATURES,
    SCALE_RELATIONSHIPS,
    get_scale_notes, get_chord_notes, get_chord_formula,
    note_to_midi, midi_to_freq,
    get_relative_minor, get_relative_major,
    get_dominant_key, get_subdominant_key,
    get_scale_notes_from_intervals,
    INDIAN_RAGAS, ARABIC_MAQAMS, CHINESE_SCALES, JAPANESE_SCALES,
    KOREAN_SCALES, INDONESIAN_SCALES, BALKAN_MUSIC,
    AFRICAN_MUSIC, LATIN_AMERICAN_MUSIC, CELTIC_MUSIC, TURKISH_MAKAMS,
    PERSIAN_DASTGAHS, CARNATIC_RAGAS,
    NATIVE_AMERICAN_MUSIC,
    MUSICAL_SYMBOLS, DYNAMIC_MARKINGS, RHYTHM_PATTERNS,
    WORLD_RHYTHM_TRADITIONS, ORNAMENTATION_SYMBOLS, TEMPO_MARKINGS,
    RHYTHM_CONCEPTS, NOTE_VALUE_HIERARCHY, REST_SYMBOLS_GUIDE,
    ACCIDENTAL_RULES,
)
from piano_widget import PianoWidget, CircleOfFifthsWidget, audio_engine
from quiz_module import QuizWidget

GLOBAL_STYLE = """
QMainWindow { background: #f8f9fa; }
QToolBar { background: white; border-bottom: 2px solid #ecf0f1; padding: 5px; spacing: 5px; }
QStatusBar { background: #2c3e50; color: white; font-size: 12px; padding: 3px; }
QScrollArea { border: none; background: transparent; }
QGroupBox {
    font-weight: bold; font-size: 14px;
    border: 2px solid #e8ecf0; border-radius: 12px;
    margin-top: 15px; padding: 20px; padding-top: 35px; background: white;
}
QGroupBox::title { subcontrol-origin: margin; left: 20px; padding: 0 10px; color: #2c3e50; }
QComboBox {
    padding: 8px 12px; border: 2px solid #dce1e3; border-radius: 8px;
    background: white; font-size: 13px; min-width: 120px;
}
QComboBox:focus { border-color: #3498db; }
QComboBox::drop-down { border: none; width: 30px; }
QListWidget {
    border: 2px solid #e8ecf0; border-radius: 10px;
    padding: 5px; background: white; font-size: 13px; outline: none;
}
QListWidget::item { padding: 10px 15px; border-radius: 8px; margin: 2px 0; }
QListWidget::item:hover { background: #eaf2f8; }
QListWidget::item:selected { background: #3498db; color: white; }
QTabWidget::pane { border: 2px solid #e8ecf0; border-radius: 10px; background: white; padding: 5px; }
QTabBar::tab {
    padding: 10px 20px; margin-right: 2px;
    border-top-left-radius: 8px; border-top-right-radius: 8px;
    font-weight: bold; font-size: 12px; color: #7f8c8d;
    background: #f5f6fa; border: 2px solid #e8ecf0; border-bottom: none;
}
QTabBar::tab:selected { background: white; color: #3498db; border-bottom: 2px solid white; }
QLineEdit {
    padding: 8px 12px; border: 2px solid #dce1e3; border-radius: 8px;
    background: white; font-size: 13px;
}
QLineEdit:focus { border-color: #3498db; }
QSpinBox {
    padding: 6px 10px; border: 2px solid #dce1e3; border-radius: 8px;
    background: white; font-size: 12px; min-width: 70px;
}
"""

DARK_STYLE = """
QMainWindow { background: #1a1a2e; }
QToolBar { background: #16213e; border-bottom: 2px solid #0f3460; padding: 5px; spacing: 5px; }
QStatusBar { background: #16213e; color: #e0e0e0; font-size: 12px; padding: 3px; }
QScrollArea { border: none; background: transparent; }
QGroupBox {
    font-weight: bold; font-size: 14px;
    border: 2px solid #0f3460; border-radius: 12px;
    margin-top: 15px; padding: 20px; padding-top: 35px; background: #16213e; color: #e0e0e0;
}
QGroupBox::title { subcontrol-origin: margin; left: 20px; padding: 0 10px; color: #e94560; }
QComboBox {
    padding: 8px 12px; border: 2px solid #0f3460; border-radius: 8px;
    background: #16213e; color: #e0e0e0; font-size: 13px; min-width: 120px;
}
QComboBox:focus { border-color: #e94560; }
QComboBox::drop-down { border: none; width: 30px; }
QComboBox QAbstractItemView { background: #16213e; color: #e0e0e0; selection-background-color: #e94560; }
QListWidget {
    border: 2px solid #0f3460; border-radius: 10px;
    padding: 5px; background: #16213e; color: #e0e0e0; font-size: 13px; outline: none;
}
QListWidget::item { padding: 10px 15px; border-radius: 8px; margin: 2px 0; color: #e0e0e0; }
QListWidget::item:hover { background: #0f3460; }
QListWidget::item:selected { background: #e94560; color: white; }
QTabWidget::pane { border: 2px solid #0f3460; border-radius: 10px; background: #1a1a2e; padding: 5px; }
QTabBar::tab {
    padding: 10px 20px; margin-right: 2px;
    border-top-left-radius: 8px; border-top-right-radius: 8px;
    font-weight: bold; font-size: 12px; color: #a0a0a0;
    background: #16213e; border: 2px solid #0f3460; border-bottom: none;
}
QTabBar::tab:selected { background: #1a1a2e; color: #e94560; border-bottom: 2px solid #1a1a2e; }
QLineEdit {
    padding: 8px 12px; border: 2px solid #0f3460; border-radius: 8px;
    background: #16213e; color: #e0e0e0; font-size: 13px;
}
QLineEdit:focus { border-color: #e94560; }
QSpinBox {
    padding: 6px 10px; border: 2px solid #0f3460; border-radius: 8px;
    background: #16213e; color: #e0e0e0; font-size: 12px; min-width: 70px;
}
QLabel { color: #e0e0e0; }
QTextEdit { background: #16213e; color: #e0e0e0; border: 2px solid #0f3460; border-radius: 8px; }
QScrollBar:vertical { background: #16213e; width: 12px; border-radius: 6px; }
QScrollBar::handle:vertical { background: #0f3460; border-radius: 6px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QSplitter::handle { background: #0f3460; }
QSlider::groove:horizontal { background: #0f3460; height: 8px; border-radius: 4px; }
QSlider::handle:horizontal { background: #e94560; width: 18px; margin: -5px 0; border-radius: 9px; }
QSlider::sub-page:horizontal { background: #e94560; border-radius: 4px; }
QProgressBar { background: #0f3460; border-radius: 6px; text-align: center; color: #e0e0e0; }
QProgressBar::chunk { background: #e94560; border-radius: 6px; }
InfoCard { background: #16213e; border-left: 4px solid #0f3460; border-radius: 8px; }
QFrame { background: #1a1a2e; }
"""


class SectionTitle(QLabel):
    def __init__(self, text, subtitle=""):
        super().__init__(text)
        self.setFont(QFont('Segoe UI', 20, QFont.Bold))
        self.setStyleSheet("color: #2c3e50; margin: 5px 0;")


class InfoCard(QFrame):
    def __init__(self, title: str, content: str, color: str = "#3498db", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            InfoCard {{
                background: white; border-left: 4px solid {color};
                border-radius: 8px; padding: 15px 20px; margin: 5px 0;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)
        title_label = QLabel(title)
        title_label.setFont(QFont('Segoe UI', 13, QFont.Bold))
        title_label.setStyleSheet(f"color: {color};")
        layout.addWidget(title_label)
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setFont(QFont('Segoe UI', 11))
        content_label.setStyleSheet("color: #555; line-height: 1.5;")
        layout.addWidget(content_label)


class PlayButton(QPushButton):
    """A styled play button for audio playback."""
    def __init__(self, text="Play", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(34)
        self.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2ecc71, stop:1 #27ae60);
                color: white; border: none; border-radius: 17px;
                padding: 6px 18px; font-size: 12px;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #27ae60, stop:1 #1e8449); }
            QPushButton:disabled { background: #bdc3c7; color: #95a5a6; }
        """)
        if not audio_engine.is_available:
            self.setEnabled(False)
            self.setText("Play (no audio)")
            self.setStyleSheet("""
                QPushButton {
                    background: #bdc3c7; color: #95a5a6;
                    border: none; border-radius: 17px; padding: 6px 18px; font-size: 12px;
                }
            """)


class NoteBadge(QLabel):
    """A styled note badge for displaying scale/chord notes."""
    def __init__(self, text="", color="#3498db", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(50, 35)
        self.setStyleSheet(f"background: {color}; color: white; border-radius: 6px; padding: 5px; font-weight: bold; font-size: 13px;")

    def set_active(self, color="#3498db", text=""):
        if text:
            self.setText(text)
        self.setStyleSheet(f"background: {color}; color: white; border-radius: 6px; padding: 5px; font-weight: bold; font-size: 13px;")

    def set_inactive(self):
        self.setText("")
        self.setStyleSheet("background: transparent; border: none; min-width: 40px;")


class SearchFilterList(QWidget):
    """A combined search box + filtered list widget."""
    selectionChanged = Signal(str)

    def __init__(self, items: list, parent=None):
        super().__init__(parent)
        self.all_items = items
        self._setup_ui(items)

    def _setup_ui(self, items):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.textChanged.connect(self._filter)
        layout.addWidget(self.search_box)

        self.list_widget = QListWidget()
        self.list_widget.addItems(items)
        if items:
            self.list_widget.setCurrentRow(0)
        self.list_widget.currentTextChanged.connect(self.selectionChanged.emit)
        layout.addWidget(self.list_widget)

    def _filter(self, text):
        self.list_widget.clear()
        filtered = [item for item in self.all_items if text.lower() in item.lower()]
        self.list_widget.addItems(filtered)
        if filtered:
            self.list_widget.setCurrentRow(0)

    def current_text(self):
        return self.list_widget.currentItem().text() if self.list_widget.currentItem() else ""

    def set_items(self, items):
        self.all_items = items
        self.search_box.clear()
        self.list_widget.clear()
        self.list_widget.addItems(items)
        if items:
            self.list_widget.setCurrentRow(0)


# ============================================================
# WESTERN MODULE
# ============================================================
class WesternModule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(10)

        title = SectionTitle("Western Music Theory", "Explore scales, chords, intervals, ear training, and more")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setFont(QFont('Segoe UI', 11))
        tabs.addTab(self._create_scales_tab(), "Scales")
        tabs.addTab(self._create_chords_tab(), "Chords")
        tabs.addTab(self._create_intervals_tab(), "Intervals")
        tabs.addTab(self._create_progressions_tab(), "Progressions")
        tabs.addTab(self._create_cof_tab(), "Circle of Fifths")
        tabs.addTab(self._create_time_tab(), "Time Signatures")
        tabs.addTab(self._create_ear_training_tab(), "Ear Training")
        tabs.addTab(self._create_scale_rel_tab(), "Scale Relations")
        tabs.addTab(self._create_scale_compare_tab(), "Compare Scales")
        tabs.addTab(self._create_polyrhythm_tab(), "Polyrhythm Lab")
        tabs.addTab(self._create_rhythm_explorer_tab(), "Rhythm Explorer")
        tabs.addTab(self._create_voicings_tab(), "Chord Voicings")
        tabs.addTab(self._create_transpose_tab(), "Transpose")
        tabs.addTab(self._create_metronome_tab(), "Metronome")
        layout.addWidget(tabs)

    def _make_play_row(self, *buttons):
        row = QHBoxLayout()
        row.setSpacing(8)
        for btn in buttons:
            row.addWidget(btn)
        row.addStretch()
        return row

    def _create_scales_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        root_group = QGroupBox("Root Note")
        rg_layout = QHBoxLayout(root_group)
        self.scale_root_combo = QComboBox()
        self.scale_root_combo.addItems(NOTE_NAMES)
        self.scale_root_combo.currentTextChanged.connect(self._update_scale_display)
        rg_layout.addWidget(QLabel("Root:"))
        rg_layout.addWidget(self.scale_root_combo)
        left_layout.addWidget(root_group)

        scale_group = QGroupBox("Scale Type")
        sg_layout = QVBoxLayout(scale_group)
        self.scale_search_list = SearchFilterList(list(WESTERN_SCALES.keys()))
        self.scale_search_list.setMaximumHeight(350)
        self.scale_search_list.selectionChanged.connect(self._update_scale_display)
        sg_layout.addWidget(self.scale_search_list)
        left_layout.addWidget(scale_group)

        left_layout.addStretch()
        left_panel.setMaximumWidth(320)
        layout.addWidget(left_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.scale_info_card = QFrame()
        self.scale_info_card.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 20px; }")
        si_layout = QVBoxLayout(self.scale_info_card)

        self.scale_name_label = QLabel()
        self.scale_name_label.setFont(QFont('Segoe UI', 18, QFont.Bold))
        self.scale_name_label.setStyleSheet("color: #2c3e50;")
        si_layout.addWidget(self.scale_name_label)

        self.scale_mood_label = QLabel()
        self.scale_mood_label.setFont(QFont('Segoe UI', 12))
        self.scale_mood_label.setStyleSheet("color: #e67e22; font-style: italic; margin-bottom: 10px;")
        si_layout.addWidget(self.scale_mood_label)

        # Play scale button
        self.play_scale_btn = PlayButton("Play Scale Ascending")
        self.play_scale_btn.clicked.connect(self._play_scale)
        si_layout.addLayout(self._make_play_row(self.play_scale_btn))

        self.scale_desc_label = QLabel()
        self.scale_desc_label.setWordWrap(True)
        self.scale_desc_label.setFont(QFont('Segoe UI', 11))
        self.scale_desc_label.setStyleSheet("color: #555; line-height: 1.6; margin-bottom: 10px;")
        si_layout.addWidget(self.scale_desc_label)

        # Techniques tip
        self.scale_tech_label = QLabel()
        self.scale_tech_label.setWordWrap(True)
        self.scale_tech_label.setFont(QFont('Segoe UI', 11))
        self.scale_tech_label.setStyleSheet("color: #16a085; background: #eafaf1; padding: 10px; border-radius: 8px; margin-bottom: 10px;")
        si_layout.addWidget(self.scale_tech_label)

        notes_frame = QFrame()
        notes_layout = QHBoxLayout(notes_frame)
        notes_layout.setSpacing(5)
        self.note_labels = []
        for _ in range(12):
            badge = QLabel("")
            badge.setAlignment(Qt.AlignCenter)
            badge.setFixedSize(50, 35)
            badge.setStyleSheet("background: #ecf0f1; color: #7f8c8d; border-radius: 6px; padding: 5px; font-weight: bold; font-size: 13px;")
            self.note_labels.append(badge)
            notes_layout.addWidget(badge)
        si_layout.addWidget(notes_frame)

        self.scale_intervals_label = QLabel()
        self.scale_intervals_label.setFont(QFont('Segoe UI', 11))
        self.scale_intervals_label.setStyleSheet("color: #7f8c8d; margin-top: 5px;")
        si_layout.addWidget(self.scale_intervals_label)

        self.scale_songs_label = QLabel()
        self.scale_songs_label.setWordWrap(True)
        self.scale_songs_label.setFont(QFont('Segoe UI', 11))
        self.scale_songs_label.setStyleSheet("color: #8e44ad; margin-top: 10px;")
        si_layout.addWidget(self.scale_songs_label)

        # Favorite button for scales
        self.scale_fav_btn = QPushButton("\u2606")
        self.scale_fav_btn.setFont(QFont('Segoe UI', 18))
        self.scale_fav_btn.setFixedSize(36, 36)
        self.scale_fav_btn.setCursor(Qt.PointingHandCursor)
        self.scale_fav_btn.setStyleSheet("""
            QPushButton { border: none; background: transparent; color: #bdc3c7; }
            QPushButton:hover { color: #f39c12; }
        """)
        self.scale_fav_btn.clicked.connect(self._toggle_scale_favorite)
        si_layout.addWidget(self.scale_fav_btn)

        right_layout.addWidget(self.scale_info_card)
        self.scale_piano = PianoWidget(3, 2)
        right_layout.addWidget(self.scale_piano)
        right_layout.addStretch()
        layout.addWidget(right_panel, 1)

        self._update_scale_display()
        return widget

    def _update_scale_display(self, text=None):
        root = self.scale_root_combo.currentText()
        scale_name = self.scale_search_list.current_text()
        if not scale_name or scale_name not in WESTERN_SCALES:
            return
        info = WESTERN_SCALES[scale_name]
        notes = get_scale_notes(root, scale_name)

        self.scale_name_label.setText(f"{root} {scale_name}")
        self.scale_mood_label.setText(f"Mood: {info['mood']}")
        self.scale_desc_label.setText(info['description'])
        self.scale_tech_label.setText(info.get('techniques', ''))

        for i, badge in enumerate(self.note_labels):
            if i < len(notes):
                badge.setText(notes[i])
                bg = "#e74c3c" if i == 0 else "#3498db"
                badge.setStyleSheet(f"background: {bg}; color: white; border-radius: 6px; padding: 5px; font-weight: bold; font-size: 13px; min-width: 40px;")
            else:
                badge.setText("")
                badge.setStyleSheet("background: transparent; border: none; min-width: 40px;")

        intervals = info['intervals']
        interval_names = [INTERVAL_SHORT.get(i, str(i)) for i in intervals]
        self.scale_intervals_label.setText(f"Intervals: {' - '.join(interval_names)}")

        if 'famous_songs' in info:
            self.scale_songs_label.setText("Famous songs: " + " | ".join(info['famous_songs']))
        else:
            self.scale_songs_label.setText("")

        self.scale_piano.highlight_notes_root_and_scale(root, notes, 4)

    def _play_scale(self):
        root = self.scale_root_combo.currentText()
        scale_name = self.scale_search_list.current_text()
        if scale_name and scale_name in WESTERN_SCALES:
            notes = get_scale_notes(root, scale_name)
            seq = [(n, 4) for n in notes] + [(notes[-1], 4), (notes[-2], 4), (notes[-3], 4),
                                                  (notes[-4], 4), (notes[-5], 4), (notes[-6], 4) if len(notes) > 6 else (notes[0], 4),
                                                  (root, 4)]
            audio_engine.play_sequence(seq, interval_ms=300)

    def _toggle_scale_favorite(self):
        scale_name = self.scale_search_list.current_text()
        if not scale_name:
            return
        main_win = self.window()
        if hasattr(main_win, '_is_favorite') and main_win._is_favorite('Western', scale_name):
            main_win._remove_favorite('Western', scale_name)
            self.scale_fav_btn.setText("\u2606")
            self.scale_fav_btn.setStyleSheet("QPushButton { border: none; background: transparent; color: #bdc3c7; } QPushButton:hover { color: #f39c12; }")
        elif hasattr(main_win, '_add_favorite'):
            main_win._add_favorite('Western', scale_name)
            self.scale_fav_btn.setText("\u2605")
            self.scale_fav_btn.setStyleSheet("QPushButton { border: none; background: transparent; color: #f39c12; }")

    def _create_chords_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        root_group = QGroupBox("Root Note")
        rg_layout = QHBoxLayout(root_group)
        self.chord_root_combo = QComboBox()
        self.chord_root_combo.addItems(NOTE_NAMES)
        self.chord_root_combo.currentTextChanged.connect(self._update_chord_display)
        rg_layout.addWidget(QLabel("Root:"))
        rg_layout.addWidget(self.chord_root_combo)
        left_layout.addWidget(root_group)

        chord_group = QGroupBox("Chord Type")
        cg_layout = QVBoxLayout(chord_group)
        self.chord_search_list = SearchFilterList(list(CHORD_TYPES.keys()))
        self.chord_search_list.setMaximumHeight(400)
        self.chord_search_list.selectionChanged.connect(self._update_chord_display)
        cg_layout.addWidget(self.chord_search_list)
        left_layout.addWidget(chord_group)

        left_layout.addStretch()
        left_panel.setMaximumWidth(320)
        layout.addWidget(left_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.chord_info_frame = QFrame()
        self.chord_info_frame.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 20px; }")
        ci_layout = QVBoxLayout(self.chord_info_frame)

        self.chord_name_label = QLabel()
        self.chord_name_label.setFont(QFont('Segoe UI', 18, QFont.Bold))
        self.chord_name_label.setStyleSheet("color: #2c3e50;")
        ci_layout.addWidget(self.chord_name_label)

        self.chord_quality_label = QLabel()
        self.chord_quality_label.setFont(QFont('Segoe UI', 12))
        self.chord_quality_label.setStyleSheet("color: #27ae60; font-style: italic; margin-bottom: 5px;")
        ci_layout.addWidget(self.chord_quality_label)

        self.chord_formula_label = QLabel()
        self.chord_formula_label.setFont(QFont('Segoe UI', 11))
        self.chord_formula_label.setStyleSheet("color: #8e44ad; margin-bottom: 10px;")
        ci_layout.addWidget(self.chord_formula_label)

        self.play_chord_btn = PlayButton("Play Chord")
        self.play_chord_btn.clicked.connect(self._play_chord)
        ci_layout.addLayout(self._make_play_row(self.play_chord_btn))

        self.chord_notes_label = QLabel()
        self.chord_notes_label.setFont(QFont('Segoe UI', 14, QFont.Bold))
        self.chord_notes_label.setStyleSheet("color: #2980b9; margin-bottom: 10px;")
        ci_layout.addWidget(self.chord_notes_label)

        self.chord_badges_layout = QHBoxLayout()
        self.chord_note_badges = []
        for _ in range(7):
            badge = QLabel("")
            badge.setAlignment(Qt.AlignCenter)
            badge.setFixedSize(50, 35)
            badge.setStyleSheet("background: #ecf0f1; color: #7f8c8d; border-radius: 6px; padding: 5px; font-weight: bold; font-size: 13px;")
            self.chord_note_badges.append(badge)
            self.chord_badges_layout.addWidget(badge)
        ci_layout.addLayout(self.chord_badges_layout)

        self.chord_intervals_label = QLabel()
        self.chord_intervals_label.setFont(QFont('Segoe UI', 11))
        self.chord_intervals_label.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        ci_layout.addWidget(self.chord_intervals_label)

        right_layout.addWidget(self.chord_info_frame)
        self.chord_piano = PianoWidget(3, 2)
        right_layout.addWidget(self.chord_piano)
        right_layout.addStretch()
        layout.addWidget(right_panel, 1)

        self._update_chord_display()
        return widget

    def _update_chord_display(self, text=None):
        root = self.chord_root_combo.currentText()
        chord_name = self.chord_search_list.current_text()
        if not chord_name or chord_name not in CHORD_TYPES:
            return
        info = CHORD_TYPES[chord_name]
        notes = get_chord_notes(root, chord_name)
        symbol = f"{root}{info['symbol']}" if info['symbol'] else root

        self.chord_name_label.setText(f"{symbol} ({chord_name})")
        self.chord_quality_label.setText(f"Quality: {info['quality']}")
        self.chord_formula_label.setText(f"Formula: {info.get('formula', '')}")
        self.chord_notes_label.setText(f"Notes: {' - '.join(notes)}")

        for i, badge in enumerate(self.chord_note_badges):
            if i < len(notes):
                badge.setText(notes[i])
                bg = "#e74c3c" if i == 0 else "#27ae60"
                badge.setStyleSheet(f"background: {bg}; color: white; border-radius: 6px; padding: 5px; font-weight: bold; font-size: 13px;")
            else:
                badge.setText("")
                badge.setStyleSheet("background: transparent; border: none;")

        intervals = info['intervals']
        interval_names = [f"{INTERVAL_SHORT.get(iv, str(iv))}" for iv in intervals]
        self.chord_intervals_label.setText(f"Structure: {' - '.join(interval_names)}")
        self.chord_piano.highlight_notes(notes, 'chord', 4)

    def _play_chord(self):
        root = self.chord_root_combo.currentText()
        chord_name = self.chord_search_list.current_text()
        if chord_name and chord_name in CHORD_TYPES:
            notes = get_chord_notes(root, chord_name)
            audio_engine.play_chord([(n, 4) for n in notes])

    def _create_intervals_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(15)

        title = QLabel("Musical Intervals")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        desc = QLabel("An interval is the distance between two pitches. Understanding intervals is fundamental to understanding melody, harmony, and ear training. The consonance/dissonance classification below describes how 'stable' or 'tense' each interval sounds.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        grid = QGridLayout()
        grid.setSpacing(8)

        for i, (semitones, name) in enumerate(INTERVAL_NAMES.items()):
            card = QFrame()
            is_consonant = 'Perfect' in INTERVAL_CONSONANCE[semitones][0] or 'imperfect' in INTERVAL_CONSONANCE[semitones][0]
            border_color = "#27ae60" if is_consonant else "#e74c3c"
            card.setStyleSheet(f"""
                QFrame {{
                    background: white; border: 1px solid #e8ecf0;
                    border-radius: 10px; padding: 10px; border-top: 3px solid {border_color};
                }}
                QFrame:hover {{ border-color: #3498db; background: #f0f8ff; }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 8, 10, 8)

            short = INTERVAL_SHORT[semitones]
            short_label = QLabel(short)
            short_label.setFont(QFont('Segoe UI', 14, QFont.Bold))
            short_label.setAlignment(Qt.AlignCenter)
            short_label.setStyleSheet(f"color: {border_color};")
            card_layout.addWidget(short_label)

            name_label = QLabel(name)
            name_label.setFont(QFont('Segoe UI', 10))
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("color: #555;")
            card_layout.addWidget(name_label)

            semi_label = QLabel(f"{semitones} semitones")
            semi_label.setFont(QFont('Segoe UI', 9))
            semi_label.setAlignment(Qt.AlignCenter)
            semi_label.setStyleSheet("color: #aab; margin-top: 3px;")
            card_layout.addWidget(semi_label)

            con_type = INTERVAL_CONSONANCE[semitones][0]
            con_color = "#27ae60" if 'Perfect' in con_type or 'imperfect' in con_type else "#e74c3c" if 'Dissonance' in con_type else "#e67e22"
            con_label = QLabel(con_type)
            con_label.setFont(QFont('Segoe UI', 8, QFont.Bold))
            con_label.setAlignment(Qt.AlignCenter)
            con_label.setStyleSheet(f"color: {con_color}; margin-top: 2px;")
            card_layout.addWidget(con_label)

            play_iv_btn = PlayButton("Play")
            play_iv_btn.setFixedHeight(26)
            play_iv_btn.setFont(QFont('Segoe UI', 9, QFont.Bold))
            def _play_this_interval(semitones=semitones, btn=play_iv_btn):
                root_idx = 0  # C
                target_idx = (root_idx + semitones) % 12
                audio_engine.play_interval(NOTE_NAMES[root_idx], 4, NOTE_NAMES[target_idx], 4, mode='melodic')
            play_iv_btn.clicked.connect(_play_this_interval)
            card_layout.addWidget(play_iv_btn)

            row = i // 4
            col = i % 4
            grid.addWidget(card, row, col)

        layout.addLayout(grid)
        layout.addStretch()
        scroll.setWidget(content)
        layout2 = QVBoxLayout(widget)
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.addWidget(scroll)
        return widget

    def _create_progressions_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        desc = QLabel("Chord progressions are sequences of chords that create harmonic movement. These are the most common progressions found in Western music. Understanding these patterns is essential for songwriting, improvisation, and musical analysis.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        # Key selector + play progression
        prog_ctrl = QHBoxLayout()
        prog_ctrl.addWidget(QLabel("Key:"))
        self.prog_key_combo = QComboBox()
        self.prog_key_combo.addItems(NOTE_NAMES)
        self.prog_key_combo.setCurrentText('C')
        self.prog_key_combo.setFixedWidth(80)
        prog_ctrl.addWidget(self.prog_key_combo)
        self.prog_play_all_btn = PlayButton("Play All Progressions")
        self.prog_play_all_btn.clicked.connect(self._play_all_progressions)
        prog_ctrl.addWidget(self.prog_play_all_btn)
        prog_ctrl.addWidget(QLabel("  Tempo:"))
        self.prog_tempo_spin = QSpinBox()
        self.prog_tempo_spin.setRange(40, 200)
        self.prog_tempo_spin.setValue(100)
        self.prog_tempo_spin.setSuffix(" BPM")
        self.prog_tempo_spin.setFixedWidth(100)
        prog_ctrl.addWidget(self.prog_tempo_spin)
        prog_ctrl.addStretch()
        layout.addLayout(prog_ctrl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(10)

        colors = ["#e74c3c", "#3498db", "#2ecc71", "#e67e22", "#9b59b6", "#1abc9c", "#f39c12", "#e84393", "#2980b9", "#d35400"]

        for i, (name, info) in enumerate(CHORD_PROGRESSIONS.items()):
            color = colors[i % len(colors)]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-left: 4px solid {color}; border-radius: 10px; padding: 15px 20px; margin: 5px 0; }}")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(15, 12, 15, 12)

            name_label = QLabel(name)
            name_label.setFont(QFont('Segoe UI', 14, QFont.Bold))
            name_label.setStyleSheet(f"color: {color};")
            cl.addWidget(name_label)

            example_label = QLabel(f"Example in C: {info['example_key']}")
            example_label.setFont(QFont('Segoe UI', 13, QFont.Bold))
            example_label.setStyleSheet("color: #2c3e50; margin-top: 5px;")
            cl.addWidget(example_label)

            desc_label = QLabel(info['description'])
            desc_label.setWordWrap(True)
            desc_label.setFont(QFont('Segoe UI', 11))
            desc_label.setStyleSheet("color: #555; line-height: 1.6; margin-top: 8px;")
            cl.addWidget(desc_label)

            if 'tips' in info:
                tips_label = QLabel(f"Tip: {info['tips']}")
                tips_label.setWordWrap(True)
                tips_label.setFont(QFont('Segoe UI', 10))
                tips_label.setStyleSheet("color: #16a085; background: #eafaf1; padding: 8px; border-radius: 6px; margin-top: 5px;")
                cl.addWidget(tips_label)

            play_prog_btn = PlayButton(f"Play in {self.prog_key_combo.currentText()}")
            play_prog_btn.setProperty('prog_name', name)
            play_prog_btn.clicked.connect(self._play_single_progression)
            cl.addWidget(play_prog_btn)

            genre_label = QLabel(f"Genres: {', '.join(info['genres'])}")
            genre_label.setWordWrap(True)
            genre_label.setFont(QFont('Segoe UI', 10))
            genre_label.setStyleSheet("color: #8e44ad; margin-top: 5px;")
            cl.addWidget(genre_label)

            content_layout.addWidget(card)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        return widget

    def _play_single_progression(self):
        btn = self.sender()
        if not btn:
            return
        prog_name = btn.property('prog_name')
        if prog_name not in CHORD_PROGRESSIONS:
            return
        key = self.prog_key_combo.currentText()
        example = CHORD_PROGRESSIONS[prog_name]['example_key']
        chords = [c.strip() for c in example.split(' - ')]

        root_idx = NOTE_NAMES.index(key) if key in NOTE_NAMES else 0
        note_sequence = []

        for chord_sym in chords:
            base = chord_sym.rstrip('m7dimaug51369 ')
            if base in NOTE_NAMES:
                c_idx = NOTE_NAMES.index(base)
                offset = root_idx
                new_root = NOTE_NAMES[(c_idx + offset) % 12]
                sym_rest = chord_sym[len(base):]
                if 'dim' in sym_rest:
                    ctype = 'Diminished'
                elif 'aug' in sym_rest:
                    ctype = 'Augmented'
                elif sym_rest.startswith('m') or sym_rest.startswith('min'):
                    if '7' in sym_rest:
                        ctype = 'Minor 7th'
                    else:
                        ctype = 'Minor'
                elif '7' in sym_rest:
                    if 'maj' in sym_rest or 'M' in sym_rest:
                        ctype = 'Major 7th'
                    elif 'dim' in sym_rest:
                        ctype = 'Half-Dim 7th'
                    else:
                        ctype = 'Dominant 7th'
                elif 'sus' in sym_rest:
                    ctype = 'Sus4'
                else:
                    ctype = 'Major'
                chord_notes = get_chord_notes(new_root, ctype)
                if chord_notes:
                    for n in chord_notes:
                        note_sequence.append((n, 4))
                    note_sequence.append(None)  # separator between chords

        if note_sequence and audio_engine.is_available:
            beat_ms = int(60000 / self.prog_tempo_spin.value())
            # Play each chord using audio_engine
            chord_groups = []
            current_chord = []
            for item in note_sequence:
                if item is None:
                    if current_chord:
                        chord_groups.append(current_chord)
                        current_chord = []
                else:
                    current_chord.append(item)
            if current_chord:
                chord_groups.append(current_chord)

            for chord_notes in chord_groups:
                audio_engine.play_chord(chord_notes, duration=4 * beat_ms / 1000.0)
                import time
                time.sleep(4 * beat_ms / 1000.0 * 0.9)

    def _play_all_progressions(self):
        """Play all progressions in sequence."""
        if not audio_engine.is_available:
            return
        import time
        beat_ms = int(60000 / self.prog_tempo_spin.value())
        chord_dur = 2 * beat_ms / 1000.0

        for prog_name, prog_info in list(CHORD_PROGRESSIONS.items())[:5]:
            example = prog_info['example_key']
            chords = [c.strip() for c in example.split(' - ')]
            for chord_sym in chords:
                base = chord_sym.rstrip('m7dimaug51369 ')
                if base in NOTE_NAMES:
                    sym_rest = chord_sym[len(base):]
                    if 'dim' in sym_rest:
                        ctype = 'Diminished'
                    elif sym_rest.startswith('m') or sym_rest.startswith('min'):
                        ctype = 'Minor'
                    elif '7' in sym_rest:
                        ctype = 'Dominant 7th'
                    else:
                        ctype = 'Major'
                    chord_notes = get_chord_notes(base, ctype)
                    if chord_notes:
                        audio_engine.play_chord([(n, 4) for n in chord_notes], duration=chord_dur)
                        time.sleep(chord_dur * 0.9)
            time.sleep(0.3)

    def _create_cof_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)

        self.cof_widget = CircleOfFifthsWidget()
        layout.addWidget(self.cof_widget, 1)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 0, 0, 0)

        title = QLabel("Circle of Fifths")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        right_layout.addWidget(title)

        desc = QLabel("The Circle of Fifths shows the relationships between the 12 chromatic pitches. Moving clockwise adds a sharp; counter-clockwise adds a flat. Green dots show closely related keys.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin: 10px 0;")
        right_layout.addWidget(desc)

        self.cof_combo = QComboBox()
        self.cof_combo.addItems(CIRCLE_OF_FIFTHS_ORDER)
        self.cof_combo.currentTextChanged.connect(self._update_cof)
        right_layout.addWidget(self.cof_combo)

        self.cof_info = QLabel()
        self.cof_info.setWordWrap(True)
        self.cof_info.setFont(QFont('Segoe UI', 11))
        self.cof_info.setStyleSheet("color: #555; margin-top: 10px; line-height: 1.6;")
        right_layout.addWidget(self.cof_info)

        right_layout.addStretch()
        right_panel.setMaximumWidth(300)
        layout.addWidget(right_panel)

        self._update_cof('C')
        return widget

    def _update_cof(self, key):
        sigs = MAJOR_KEY_SIGNATURES.get(key, 0)
        rel_min = get_relative_minor(key)
        dom = get_dominant_key(key)
        sub = get_subdominant_key(key)

        sharp_flat = ""
        if sigs > 0:
            if key in ['F#', 'C#', 'G#', 'D#', 'A#', 'E#', 'B']:
                sharp_flat = f"{sigs} sharp{'s' if sigs > 1 else ''}"
            else:
                sharp_flat = f"{sigs} flat{'s' if sigs > 1 else ''}"

        notes = get_scale_notes(key, 'Major (Ionian)')
        self.cof_info.setText(
            f"Key: {key} Major\n\n"
            f"Key Signature: {sharp_flat if sharp_flat else 'No sharps or flats'}\n\n"
            f"Relative Minor: {rel_min}\n"
            f"Dominant (V): {dom}\n"
            f"Subdominant (IV): {sub}\n\n"
            f"Scale Notes:\n{', '.join(notes)}\n\n"
            f"Closely related keys (green): {key}, {dom}, {sub}, {rel_min}, and their parallels."
        )

        highlighted = set(get_scale_notes(key, 'Major (Ionian)'))
        related = {key, dom, sub, rel_min}
        self.cof_widget.set_highlighted(highlighted, key, related)

    def _create_time_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        title = QLabel("Time Signatures")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        desc = QLabel("Time signatures indicate the number of beats per measure and the note value that receives one beat. They define the rhythmic feel of music. Odd meters (5/4, 7/8, 9/8, 11/8) are common in Balkan, Indian, and progressive rock.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        layout.addWidget(desc)

        grid = QGridLayout()
        grid.setSpacing(10)
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#e67e22", "#9b59b6", "#1abc9c", "#f39c12", "#e84393", "#2980b9"]

        for i, (ts, info) in enumerate(TIME_SIGNATURES.items()):
            color = colors[i % len(colors)]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-top: 4px solid {color}; border-radius: 10px; padding: 15px; }}")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(12, 10, 12, 10)

            ts_label = QLabel(ts)
            ts_label.setFont(QFont('Segoe UI', 20, QFont.Bold))
            ts_label.setAlignment(Qt.AlignCenter)
            ts_label.setStyleSheet(f"color: {color};")
            cl.addWidget(ts_label)

            name_label = QLabel(info['name'])
            name_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
            name_label.setAlignment(Qt.AlignCenter)
            cl.addWidget(name_label)

            feel_label = QLabel(f"Feel: {info['feel']}")
            feel_label.setWordWrap(True)
            feel_label.setFont(QFont('Segoe UI', 10))
            feel_label.setAlignment(Qt.AlignCenter)
            feel_label.setStyleSheet("color: #555; margin-top: 5px;")
            cl.addWidget(feel_label)

            ex_label = QLabel(f"Examples: {info['examples']}")
            ex_label.setWordWrap(True)
            ex_label.setFont(QFont('Segoe UI', 9))
            ex_label.setAlignment(Qt.AlignCenter)
            ex_label.setStyleSheet("color: #8e44ad; margin-top: 3px;")
            cl.addWidget(ex_label)

            row = i // 3
            col = i % 3
            grid.addWidget(card, row, col)

        layout.addLayout(grid)
        layout.addStretch()
        scroll.setWidget(content)
        layout2 = QVBoxLayout(widget)
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.addWidget(scroll)
        return widget

    def _create_ear_training_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        title = QLabel("Ear Training Studio")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        ear_tabs = QTabWidget()
        ear_tabs.setFont(QFont('Segoe UI', 11))
        ear_tabs.addTab(self._create_ear_intervals_tab(), "Intervals")
        ear_tabs.addTab(self._create_ear_scales_tab(), "Scales")
        ear_tabs.addTab(self._create_ear_chords_tab(), "Chords")
        layout.addWidget(ear_tabs)
        return widget

    # ---- Ear Training: Intervals ----
    def _create_ear_intervals_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        desc = QLabel("Listen to two notes and identify the interval. Click the correct interval name to test yourself, or use 'Show Answer' if stuck. Start with easy intervals (P5, P4, M3) and work up to harder ones (m2, TT).")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Root:"))
        self.ear_root_combo = QComboBox()
        self.ear_root_combo.addItems(NOTE_NAMES)
        self.ear_root_combo.setCurrentText('C')
        ctrl.addWidget(self.ear_root_combo)
        ctrl.addWidget(QLabel("Mode:"))
        self.ear_mode_combo = QComboBox()
        self.ear_mode_combo.addItems(['Melodic (ascending)', 'Harmonic (together)'])
        ctrl.addWidget(self.ear_mode_combo)
        ctrl.addStretch()
        layout.addLayout(ctrl)

        play_row = QHBoxLayout()
        self.ear_play_btn = PlayButton("Play Interval")
        self.ear_play_btn.clicked.connect(self._play_ear_interval)
        play_row.addWidget(self.ear_play_btn)
        self.ear_reveal_btn = QPushButton("Show Answer")
        self.ear_reveal_btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.ear_reveal_btn.setFixedHeight(34)
        self.ear_reveal_btn.setStyleSheet("QPushButton { background: #e67e22; color: white; border: none; border-radius: 17px; padding: 6px 18px; } QPushButton:hover { background: #d35400; }")
        self.ear_reveal_btn.clicked.connect(self._reveal_ear_answer)
        play_row.addWidget(self.ear_reveal_btn)
        self.ear_new_btn = QPushButton("New Interval")
        self.ear_new_btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.ear_new_btn.setFixedHeight(34)
        self.ear_new_btn.setStyleSheet("QPushButton { background: #3498db; color: white; border: none; border-radius: 17px; padding: 6px 18px; } QPushButton:hover { background: #2980b9; }")
        self.ear_new_btn.clicked.connect(self._new_ear_interval)
        play_row.addWidget(self.ear_new_btn)
        play_row.addStretch()
        layout.addLayout(play_row)

        self.ear_result_frame = QFrame()
        self.ear_result_frame.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 20px; }")
        er_layout = QVBoxLayout(self.ear_result_frame)
        self.ear_interval_label = QLabel("Click 'Play Interval' to start!")
        self.ear_interval_label.setFont(QFont('Segoe UI', 16, QFont.Bold))
        self.ear_interval_label.setAlignment(Qt.AlignCenter)
        self.ear_interval_label.setStyleSheet("color: #2c3e50;")
        er_layout.addWidget(self.ear_interval_label)
        self.ear_detail_label = QLabel("")
        self.ear_detail_label.setWordWrap(True)
        self.ear_detail_label.setFont(QFont('Segoe UI', 12))
        self.ear_detail_label.setAlignment(Qt.AlignCenter)
        self.ear_detail_label.setStyleSheet("color: #555; margin-top: 10px;")
        er_layout.addWidget(self.ear_detail_label)
        layout.addWidget(self.ear_result_frame)

        # Clickable answer buttons grid
        answer_group = QGroupBox("Click Your Answer")
        ag_layout = QGridLayout(answer_group)
        ag_layout.setSpacing(6)
        self._ear_answer_btns = []
        for i, (semi, name) in enumerate(INTERVAL_NAMES.items()):
            if semi == 0:
                continue
            short = INTERVAL_SHORT[semi]
            btn = QPushButton(f"{short}\n{name}")
            btn.setFont(QFont('Segoe UI', 9, QFont.Bold))
            btn.setFixedHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty('interval_semitones', semi)
            con = INTERVAL_CONSONANCE[semi][0]
            is_consonant = 'Perfect' in con or 'imperfect' in con
            border_color = "#27ae60" if is_consonant else "#e74c3c"
            btn.setStyleSheet(f"""
                QPushButton {{ padding: 4px; border: 2px solid #dce1e3; border-radius: 8px;
                              background: white; color: #2c3e50; }}
                QPushButton:hover {{ border-color: {border_color}; background: #f8f9fa; }}
            """)
            btn.clicked.connect(self._check_ear_answer)
            ag_layout.addWidget(btn, (i-1) // 4, (i-1) % 4)
            self._ear_answer_btns.append(btn)
        layout.addWidget(answer_group)

        # Score tracking
        self.ear_iv_score_layout = QHBoxLayout()
        self.ear_iv_score_label = QLabel("Score: 0 / 0")
        self.ear_iv_score_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.ear_iv_score_label.setStyleSheet("color: #27ae60;")
        self.ear_iv_score_layout.addWidget(self.ear_iv_score_label)
        self.ear_iv_streak_label = QLabel("Streak: 0")
        self.ear_iv_streak_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.ear_iv_streak_label.setStyleSheet("color: #e67e22;")
        self.ear_iv_score_layout.addWidget(self.ear_iv_streak_label)
        self.ear_iv_score_layout.addStretch()
        layout.addLayout(self.ear_iv_score_layout)

        ref_group = QGroupBox("Quick Reference - Song Associations")
        ref_layout = QVBoxLayout(ref_group)
        for interval, song in [("m2 (1 st)", "Jaws theme"), ("M2 (2 st)", "Happy Birthday"), ("m3 (3 st)", "Greensleeves"), ("M3 (4 st)", "When the Saints Go Marching In"), ("P4 (5 st)", "Here Comes the Bride"), ("TT (6 st)", "The Simpsons"), ("P5 (7 st)", "Star Wars theme"), ("m6 (8 st)", "The Entertainer"), ("M6 (9 st)", "My Bonnie"), ("m7 (10 st)", "Somewhere (WSS)"), ("M7 (11 st)", "Take On Me"), ("P8 (12 st)", "Somewhere Over the Rainbow")]:
            row = QLabel(f"<b>{interval}</b> - {song}")
            row.setFont(QFont('Segoe UI', 10))
            row.setStyleSheet("color: #555; padding: 2px 0;")
            ref_layout.addWidget(row)
        scroll_ref = QScrollArea()
        scroll_ref.setWidgetResizable(True)
        scroll_ref.setWidget(ref_group)
        scroll_ref.setMaximumHeight(200)
        layout.addWidget(scroll_ref)
        layout.addStretch()
        self._current_ear_interval = None
        self._ear_iv_score = 0
        self._ear_iv_total = 0
        self._ear_iv_streak = 0
        self._ear_iv_answered = False
        self._new_ear_interval()
        return widget

    def _check_ear_answer(self):
        """Check if the clicked interval button matches the current ear training interval."""
        if self._current_ear_interval is None or self._ear_iv_answered:
            return
        btn = self.sender()
        if not btn:
            return
        guessed = btn.property('interval_semitones')
        correct = self._current_ear_interval
        self._ear_iv_answered = True
        self._ear_iv_total += 1

        if guessed == correct:
            self._ear_iv_score += 1
            self._ear_iv_streak += 1
            self.ear_interval_label.setText(f"Correct! {INTERVAL_SHORT[correct]} - {INTERVAL_NAMES[correct]}")
            self.ear_interval_label.setStyleSheet("color: #27ae60; font-size: 18px; font-weight: bold;")
            btn.setStyleSheet("QPushButton { background: #27ae60; color: white; border: 2px solid #27ae60; border-radius: 8px; padding: 4px; }")
        else:
            self._ear_iv_streak = 0
            self.ear_interval_label.setText(f"Wrong! It was {INTERVAL_SHORT[correct]} - {INTERVAL_NAMES[correct]} (you guessed {INTERVAL_SHORT[guessed]})")
            self.ear_interval_label.setStyleSheet("color: #e74c3c; font-size: 16px; font-weight: bold;")
            btn.setStyleSheet("QPushButton { background: #e74c3c; color: white; border: 2px solid #e74c3c; border-radius: 8px; padding: 4px; }")
            # Highlight correct answer
            for b in self._ear_answer_btns:
                if b.property('interval_semitones') == correct:
                    b.setStyleSheet("QPushButton { background: #27ae60; color: white; border: 2px solid #27ae60; border-radius: 8px; padding: 4px; }")

        self.ear_iv_score_label.setText(f"Score: {self._ear_iv_score} / {self._ear_iv_total}")
        self.ear_iv_streak_label.setText(f"Streak: {self._ear_iv_streak}")
        self.ear_detail_label.setText(f"Classification: {INTERVAL_CONSONANCE[correct][0]}\n{INTERVAL_CONSONANCE[correct][1]}")

    def _new_ear_interval(self):
        import random
        interval_num = random.randint(1, 12)
        self._current_ear_interval = interval_num
        self._ear_iv_answered = False
        self.ear_interval_label.setText("Listen and guess the interval!")
        self.ear_interval_label.setStyleSheet("color: #2c3e50;")
        self.ear_detail_label.setText("")
        # Reset all answer buttons
        if hasattr(self, '_ear_answer_btns'):
            for b in self._ear_answer_btns:
                semi = b.property('interval_semitones')
                con = INTERVAL_CONSONANCE.get(semi, ('Dissonance', ''))[0]
                is_consonant = 'Perfect' in con or 'imperfect' in con
                border_color = "#27ae60" if is_consonant else "#e74c3c"
                b.setStyleSheet(f"""
                    QPushButton {{ padding: 4px; border: 2px solid #dce1e3; border-radius: 8px;
                                  background: white; color: #2c3e50; }}
                    QPushButton:hover {{ border-color: {border_color}; background: #f8f9fa; }}
                """)

    def _play_ear_interval(self):
        if self._current_ear_interval is None:
            return
        self._ear_iv_answered = False
        root = self.ear_root_combo.currentText()
        root_idx = NOTE_NAMES.index(root)
        target_idx = (root_idx + self._current_ear_interval) % 12
        target = NOTE_NAMES[target_idx]

        mode = 'harmonic' if 'Harmonic' in self.ear_mode_combo.currentText() else 'melodic'
        audio_engine.play_interval(root, 4, target, 4, mode=mode)

        self.ear_interval_label.setText("What interval did you hear?")
        self.ear_interval_label.setStyleSheet("color: #3498db;")
        self.ear_detail_label.setText("")

    def _reveal_ear_answer(self):
        if self._current_ear_interval is None:
            return
        num = self._current_ear_interval
        name = INTERVAL_NAMES[num]
        short = INTERVAL_SHORT[num]
        con_type, con_desc = INTERVAL_CONSONANCE.get(num, ('', ''))

        self.ear_interval_label.setText(f"{short} - {name} ({num} semitones)")
        self.ear_interval_label.setStyleSheet("color: #27ae60; font-size: 18px; font-weight: bold;")
        self.ear_detail_label.setText(f"Classification: {con_type}\n{con_desc}")

    # ---- Ear Training: Scales ----
    def _create_ear_scales_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        desc = QLabel("Listen to a scale being played, then try to identify it. Covers Western scales. The scale is played ascending and then descending.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Difficulty:"))
        self.ear_scale_diff = QComboBox()
        self.ear_scale_diff.addItems(['Easy (6 scales)', 'Medium (12 scales)', 'Hard (all scales)'])
        ctrl.addWidget(self.ear_scale_diff)
        ctrl.addStretch()
        layout.addLayout(ctrl)

        play_row = QHBoxLayout()
        self.ear_scale_play_btn = PlayButton("Play Scale")
        self.ear_scale_play_btn.clicked.connect(self._play_ear_scale)
        play_row.addWidget(self.ear_scale_play_btn)
        self.ear_scale_reveal_btn = QPushButton("Show Answer")
        self.ear_scale_reveal_btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.ear_scale_reveal_btn.setFixedHeight(34)
        self.ear_scale_reveal_btn.setStyleSheet("QPushButton { background: #e67e22; color: white; border: none; border-radius: 17px; padding: 6px 18px; } QPushButton:hover { background: #d35400; }")
        self.ear_scale_reveal_btn.clicked.connect(self._reveal_ear_scale)
        play_row.addWidget(self.ear_scale_reveal_btn)
        self.ear_scale_new_btn = QPushButton("New Scale")
        self.ear_scale_new_btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.ear_scale_new_btn.setFixedHeight(34)
        self.ear_scale_new_btn.setStyleSheet("QPushButton { background: #3498db; color: white; border: none; border-radius: 17px; padding: 6px 18px; } QPushButton:hover { background: #2980b9; }")
        self.ear_scale_new_btn.clicked.connect(self._new_ear_scale)
        play_row.addWidget(self.ear_scale_new_btn)
        play_row.addStretch()
        layout.addLayout(play_row)

        self.ear_scale_result = QFrame()
        self.ear_scale_result.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 20px; }")
        esr_layout = QVBoxLayout(self.ear_scale_result)
        self.ear_scale_label = QLabel("Click 'Play Scale' to start!")
        self.ear_scale_label.setFont(QFont('Segoe UI', 16, QFont.Bold))
        self.ear_scale_label.setAlignment(Qt.AlignCenter)
        self.ear_scale_label.setStyleSheet("color: #2c3e50;")
        esr_layout.addWidget(self.ear_scale_label)
        self.ear_scale_detail = QLabel("")
        self.ear_scale_detail.setWordWrap(True)
        self.ear_scale_detail.setFont(QFont('Segoe UI', 11))
        self.ear_scale_detail.setAlignment(Qt.AlignCenter)
        self.ear_scale_detail.setStyleSheet("color: #555; margin-top: 10px;")
        esr_layout.addWidget(self.ear_scale_detail)
        layout.addWidget(self.ear_scale_result)

        self.ear_scale_piano = PianoWidget(4, 1)
        self.ear_scale_piano.setMinimumHeight(140)
        layout.addWidget(self.ear_scale_piano)

        # Score
        self.ear_scale_score_layout = QHBoxLayout()
        self.ear_scale_score_label = QLabel("Score: 0 / 0")
        self.ear_scale_score_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.ear_scale_score_label.setStyleSheet("color: #27ae60;")
        self.ear_scale_score_layout.addWidget(self.ear_scale_score_label)
        self.ear_scale_streak_label = QLabel("Streak: 0")
        self.ear_scale_streak_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.ear_scale_streak_label.setStyleSheet("color: #e67e22;")
        self.ear_scale_score_layout.addWidget(self.ear_scale_streak_label)
        self.ear_scale_score_layout.addStretch()
        layout.addLayout(self.ear_scale_score_layout)

        layout.addStretch()
        self._current_ear_scale = None
        self._ear_scale_score = 0
        self._ear_scale_total = 0
        self._ear_scale_streak = 0
        self._new_ear_scale()
        return widget

    def _get_ear_scale_pool(self):
        import random
        easy = ['Major (Ionian)', 'Natural Minor (Aeolian)', 'Pentatonic Major', 'Pentatonic Minor', 'Blues Scale', 'Dorian']
        medium = easy + ['Mixolydian', 'Phrygian', 'Lydian', 'Harmonic Minor', 'Melodic Minor', 'Whole Tone']
        hard = list(WESTERN_SCALES.keys())
        diff = self.ear_scale_diff.currentText()
        if 'Easy' in diff:
            return easy
        elif 'Medium' in diff:
            return medium
        return hard

    def _new_ear_scale(self):
        import random
        pool = self._get_ear_scale_pool()
        self._current_ear_scale = random.choice(pool)
        self.ear_scale_label.setText("Listen and guess the scale!")
        self.ear_scale_label.setStyleSheet("color: #2c3e50;")
        self.ear_scale_detail.setText("")
        self.ear_scale_piano.clear_highlights()

    def _play_ear_scale(self):
        import random
        if not self._current_ear_scale:
            return
        root = random.choice(NOTE_NAMES)
        notes = get_scale_notes(root, self._current_ear_scale)
        if not notes:
            return
        self.ear_scale_piano.clear_highlights()
        self.ear_scale_piano.highlight_notes_root_and_scale(root, notes, 4)
        seq = [(n, 4) for n in notes] + list(reversed([(n, 4) for n in notes]))
        audio_engine.play_sequence(seq, interval_ms=350)
        self.ear_scale_label.setText(f"What scale is this? (Root: {root})")
        self.ear_scale_label.setStyleSheet("color: #3498db;")
        self.ear_scale_detail.setText("")

    def _reveal_ear_scale(self):
        if not self._current_ear_scale:
            return
        name = self._current_ear_scale
        info = WESTERN_SCALES.get(name, {})
        mood = info.get('mood', '')
        self.ear_scale_label.setText(name)
        self.ear_scale_label.setStyleSheet("color: #27ae60; font-size: 18px; font-weight: bold;")
        self.ear_scale_detail.setText(f"Mood: {mood}\nNotes: {', '.join(get_scale_notes('C', name))}")

    # ---- Ear Training: Chords ----
    def _create_ear_chords_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        desc = QLabel("Listen to a chord and identify its type. Chords are played harmonically (all notes at once). Focus on the quality: is it major, minor, diminished, or something more complex?")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Difficulty:"))
        self.ear_chord_diff = QComboBox()
        self.ear_chord_diff.addItems(['Easy (triads)', 'Medium (7th chords)', 'Hard (all chords)'])
        ctrl.addWidget(self.ear_chord_diff)
        ctrl.addStretch()
        layout.addLayout(ctrl)

        play_row = QHBoxLayout()
        self.ear_chord_play_btn = PlayButton("Play Chord")
        self.ear_chord_play_btn.clicked.connect(self._play_ear_chord)
        play_row.addWidget(self.ear_chord_play_btn)
        self.ear_chord_reveal_btn = QPushButton("Show Answer")
        self.ear_chord_reveal_btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.ear_chord_reveal_btn.setFixedHeight(34)
        self.ear_chord_reveal_btn.setStyleSheet("QPushButton { background: #e67e22; color: white; border: none; border-radius: 17px; padding: 6px 18px; } QPushButton:hover { background: #d35400; }")
        self.ear_chord_reveal_btn.clicked.connect(self._reveal_ear_chord)
        play_row.addWidget(self.ear_chord_reveal_btn)
        self.ear_chord_new_btn = QPushButton("New Chord")
        self.ear_chord_new_btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.ear_chord_new_btn.setFixedHeight(34)
        self.ear_chord_new_btn.setStyleSheet("QPushButton { background: #3498db; color: white; border: none; border-radius: 17px; padding: 6px 18px; } QPushButton:hover { background: #2980b9; }")
        self.ear_chord_new_btn.clicked.connect(self._new_ear_chord)
        play_row.addWidget(self.ear_chord_new_btn)
        play_row.addStretch()
        layout.addLayout(play_row)

        self.ear_chord_result = QFrame()
        self.ear_chord_result.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 20px; }")
        ecr_layout = QVBoxLayout(self.ear_chord_result)
        self.ear_chord_label = QLabel("Click 'Play Chord' to start!")
        self.ear_chord_label.setFont(QFont('Segoe UI', 16, QFont.Bold))
        self.ear_chord_label.setAlignment(Qt.AlignCenter)
        self.ear_chord_label.setStyleSheet("color: #2c3e50;")
        ecr_layout.addWidget(self.ear_chord_label)
        self.ear_chord_detail = QLabel("")
        self.ear_chord_detail.setWordWrap(True)
        self.ear_chord_detail.setFont(QFont('Segoe UI', 11))
        self.ear_chord_detail.setAlignment(Qt.AlignCenter)
        self.ear_chord_detail.setStyleSheet("color: #555; margin-top: 10px;")
        ecr_layout.addWidget(self.ear_chord_detail)
        layout.addWidget(self.ear_chord_result)

        self.ear_chord_piano = PianoWidget(4, 1)
        self.ear_chord_piano.setMinimumHeight(140)
        layout.addWidget(self.ear_chord_piano)

        self.ear_chord_score_layout = QHBoxLayout()
        self.ear_chord_score_label = QLabel("Score: 0 / 0")
        self.ear_chord_score_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.ear_chord_score_label.setStyleSheet("color: #27ae60;")
        self.ear_chord_score_layout.addWidget(self.ear_chord_score_label)
        self.ear_chord_streak_label = QLabel("Streak: 0")
        self.ear_chord_streak_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.ear_chord_streak_label.setStyleSheet("color: #e67e22;")
        self.ear_chord_score_layout.addWidget(self.ear_chord_streak_label)
        self.ear_chord_score_layout.addStretch()
        layout.addLayout(self.ear_chord_score_layout)

        layout.addStretch()
        self._current_ear_chord = None
        self._ear_chord_root = None
        self._new_ear_chord()
        return widget

    def _get_ear_chord_pool(self):
        easy = ['Major', 'Minor', 'Diminished', 'Augmented', 'Sus4', 'Power Chord (5)']
        medium = easy + ['Major 7th', 'Minor 7th', 'Dominant 7th', 'Half-Dim 7th', 'Diminished 7th']
        hard = list(CHORD_TYPES.keys())
        diff = self.ear_chord_diff.currentText()
        if 'Easy' in diff:
            return easy
        elif 'Medium' in diff:
            return medium
        return hard

    def _new_ear_chord(self):
        import random
        pool = self._get_ear_chord_pool()
        self._current_ear_chord = random.choice(pool)
        self._ear_chord_root = random.choice(NOTE_NAMES)
        self.ear_chord_label.setText("Listen and guess the chord type!")
        self.ear_chord_label.setStyleSheet("color: #2c3e50;")
        self.ear_chord_detail.setText("")
        self.ear_chord_piano.clear_highlights()

    def _play_ear_chord(self):
        if not self._current_ear_chord:
            return
        root = self._ear_chord_root
        notes = get_chord_notes(root, self._current_ear_chord)
        if not notes:
            return
        self.ear_chord_piano.clear_highlights()
        self.ear_chord_piano.highlight_notes_root_and_scale(root, notes, 4)
        audio_engine.play_chord([(n, 4) for n in notes], duration=1.5)
        self.ear_chord_label.setText(f"What chord type is this? (Root: {root})")
        self.ear_chord_label.setStyleSheet("color: #3498db;")
        self.ear_chord_detail.setText("")

    def _reveal_ear_chord(self):
        if not self._current_ear_chord:
            return
        name = self._current_ear_chord
        root = self._ear_chord_root
        info = CHORD_TYPES.get(name, {})
        symbol = info.get('symbol', '')
        quality = info.get('quality', '')
        formula = info.get('formula', '')
        display = f"{root}{symbol}" if symbol else root
        self.ear_chord_label.setText(f"{display} - {name}")
        self.ear_chord_label.setStyleSheet("color: #27ae60; font-size: 18px; font-weight: bold;")
        self.ear_chord_detail.setText(f"Quality: {quality}\nFormula: {formula}\nNotes: {', '.join(get_chord_notes(root, name))}")

    def _create_scale_rel_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        ctrl = QGroupBox("Select Key")
        ctrl_layout = QHBoxLayout(ctrl)
        self.rel_combo = QComboBox()
        self.rel_combo.addItems(NOTE_NAMES)
        self.rel_combo.currentTextChanged.connect(self._update_scale_rel)
        ctrl_layout.addWidget(QLabel("Key:"))
        ctrl_layout.addWidget(self.rel_combo)
        left_layout.addWidget(ctrl)

        rel_group = QGroupBox("Relationship Type")
        rel_l = QVBoxLayout(rel_group)
        self.rel_list = QListWidget()
        self.rel_list.addItems(SCALE_RELATIONSHIPS.keys())
        self.rel_list.setCurrentRow(0)
        self.rel_list.setMaximumHeight(250)
        self.rel_list.currentTextChanged.connect(self._update_scale_rel)
        rel_l.addWidget(self.rel_list)
        left_layout.addWidget(rel_group)

        left_layout.addStretch()
        left_panel.setMaximumWidth(320)
        layout.addWidget(left_panel)

        right = QScrollArea()
        right.setWidgetResizable(True)
        self.rel_content = QWidget()
        self.rel_layout = QVBoxLayout(self.rel_content)
        self.rel_layout.setSpacing(10)
        right.setWidget(self.rel_content)
        layout.addWidget(right, 1)

        self._update_scale_rel()
        return widget

    def _update_scale_rel(self, text=None):
        while self.rel_layout.count():
            item = self.rel_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        key = self.rel_combo.currentText()
        rel_type = self.rel_list.currentItem().text() if self.rel_list.currentItem() else ""
        if not rel_type or rel_type not in SCALE_RELATIONSHIPS:
            return

        info = SCALE_RELATIONSHIPS[rel_type]
        from music_engine import get_scale_notes

        # Calculate related key
        if rel_type == 'Relative Minor':
            related = get_relative_minor(key)
            related_scale = 'Natural Minor (Aeolian)'
            color = "#9b59b6"
        elif rel_type == 'Relative Major':
            related = get_relative_major(key)
            related_scale = 'Major (Ionian)'
            color = "#3498db"
        elif rel_type == 'Dominant':
            related = get_dominant_key(key)
            related_scale = 'Major (Ionian)'
            color = "#e67e22"
        elif rel_type == 'Subdominant':
            related = get_subdominant_key(key)
            related_scale = 'Major (Ionian)'
            color = "#2ecc71"
        elif rel_type == 'Parallel Minor':
            related = key
            related_scale = 'Natural Minor (Aeolian)'
            color = "#e74c3c"
        else:
            related = key
            related_scale = 'Major (Ionian)'
            color = "#3498db"

        # Title
        t = QLabel(f"{key} -> {related} ({rel_type})")
        t.setFont(QFont('Segoe UI', 18, QFont.Bold))
        t.setStyleSheet(f"color: {color};")
        self.rel_layout.addWidget(t)

        # Description
        d = QLabel(info['description'])
        d.setWordWrap(True)
        d.setFont(QFont('Segoe UI', 11))
        d.setStyleSheet("color: #555; line-height: 1.6; margin: 10px 0; padding: 15px; background: #f8f9fa; border-radius: 10px;")
        self.rel_layout.addWidget(d)

        # Original scale
        orig_notes = get_scale_notes(key, 'Major (Ionian)')
        orig_frame = QFrame()
        orig_frame.setStyleSheet("background: white; border: 2px solid #e8ecf0; border-radius: 10px; padding: 15px; margin: 5px 0;")
        ol = QVBoxLayout(orig_frame)
        ol.addWidget(QLabel(f"<b>{key} Major</b>: {', '.join(orig_notes)}"))
        self.rel_layout.addWidget(orig_frame)

        # Related scale
        rel_notes = get_scale_notes(related, related_scale)
        rel_frame = QFrame()
        rel_frame.setStyleSheet(f"background: white; border: 2px solid {color}; border-radius: 10px; padding: 15px; margin: 5px 0;")
        rl = QVBoxLayout(rel_frame)
        rl.addWidget(QLabel(f"<b>{related} {related_scale}</b>: {', '.join(rel_notes)}"))
        self.rel_layout.addWidget(rel_frame)

        # Shared notes
        shared = set(orig_notes) & set(rel_notes)
        only_orig = set(orig_notes) - set(rel_notes)
        only_rel = set(rel_notes) - set(orig_notes)

        if shared:
            s = QLabel(f"Shared notes: {', '.join(sorted(shared))}")
            s.setWordWrap(True)
            s.setFont(QFont('Segoe UI', 11))
            s.setStyleSheet("color: #27ae60; margin-top: 5px;")
            self.rel_layout.addWidget(s)
        if only_orig:
            s = QLabel(f"Only in {key}: {', '.join(sorted(only_orig))}")
            s.setFont(QFont('Segoe UI', 11))
            s.setStyleSheet("color: #3498db;")
            self.rel_layout.addWidget(s)
        if only_rel:
            s = QLabel(f"Only in {related}: {', '.join(sorted(only_rel))}")
            s.setFont(QFont('Segoe UI', 11))
            s.setStyleSheet(f"color: {color};")
            self.rel_layout.addWidget(s)

        self.rel_layout.addStretch()

    def _create_rhythm_explorer_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(15)

        title = QLabel("Rhythm Explorer")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        desc = QLabel("Deep dive into the language of rhythm: note values, rest symbols, world rhythm traditions, subdivision concepts, and the building blocks of groove across cultures.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        # --- Section 1: Note Value Hierarchy ---
        nv_group = QGroupBox("Note Value Hierarchy")
        nv_layout = QVBoxLayout(nv_group)
        nv_layout.setSpacing(8)

        # Header row
        hdr = QHBoxLayout()
        for h_text, w in [("Note Value", 200), ("Beats (4/4)", 80), ("Dotted", 80), ("Rest", 100)]:
            h = QLabel(h_text)
            h.setFont(QFont('Segoe UI', 10, QFont.Bold))
            h.setStyleSheet("color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 4px;")
            h.setFixedWidth(w)
            hdr.addWidget(h)
        hdr.addStretch()
        nv_layout.addLayout(hdr)

        colors = ["#e74c3c", "#e67e22", "#f39c12", "#27ae60", "#3498db", "#9b59b6"]
        for i, nv in enumerate(NOTE_VALUE_HIERARCHY):
            row = QHBoxLayout()
            color = colors[i % len(colors)]
            name_l = QLabel(nv['name'])
            name_l.setFont(QFont('Segoe UI', 11, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            name_l.setFixedWidth(200)
            row.addWidget(name_l)

            beats_l = QLabel(str(nv['beats']))
            beats_l.setFont(QFont('Segoe UI', 11))
            beats_l.setAlignment(Qt.AlignCenter)
            beats_l.setStyleSheet("color: #2c3e50; background: #f8f9fa; border-radius: 6px; padding: 4px;")
            beats_l.setFixedWidth(80)
            row.addWidget(beats_l)

            dot_val = nv['beats'] + nv['dot_adds']
            dot_l = QLabel(str(dot_val))
            dot_l.setFont(QFont('Segoe UI', 11))
            dot_l.setAlignment(Qt.AlignCenter)
            dot_l.setStyleSheet("color: #8e44ad; background: #f5eef8; border-radius: 6px; padding: 4px;")
            dot_l.setFixedWidth(80)
            row.addWidget(dot_l)

            rest_l = QLabel(nv['rest_symbol'])
            rest_l.setFont(QFont('Segoe UI', 14, QFont.Bold))
            rest_l.setAlignment(Qt.AlignCenter)
            rest_l.setStyleSheet("color: #7f8c8d;")
            rest_l.setFixedWidth(100)
            row.addWidget(rest_l)

            row.addStretch()
            nv_layout.addLayout(row)

            tip_l = QLabel(nv['description'])
            tip_l.setWordWrap(True)
            tip_l.setFont(QFont('Segoe UI', 9))
            tip_l.setStyleSheet("color: #95a5a6; padding-left: 210px; margin-bottom: 4px;")
            nv_layout.addWidget(tip_l)

        layout.addWidget(nv_group)

        # --- Section 2: Rest Symbols Guide ---
        rs_group = QGroupBox("Rest Symbols Guide")
        rs_layout = QVBoxLayout(rs_group)
        rs_layout.setSpacing(6)

        for i, rs in enumerate(REST_SYMBOLS_GUIDE):
            color = colors[i % len(colors)]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-left: 4px solid {color}; border-radius: 8px; padding: 8px 12px; margin: 2px 0; }}")
            cl = QHBoxLayout(card)
            name_l = QLabel(rs['name'])
            name_l.setFont(QFont('Segoe UI', 11, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            name_l.setFixedWidth(150)
            cl.addWidget(name_l)
            looks_l = QLabel(f"Looks like: {rs['looks_like']}")
            looks_l.setFont(QFont('Segoe UI', 10))
            looks_l.setStyleSheet("color: #555;")
            cl.addWidget(looks_l)
            beats_l = QLabel(f"Duration: {rs['beats']} beats")
            beats_l.setFont(QFont('Segoe UI', 10))
            beats_l.setStyleSheet("color: #2c3e50;")
            cl.addWidget(beats_l)
            mem_l = QLabel(f"Memory: {rs['memory']}")
            mem_l.setFont(QFont('Segoe UI', 9))
            mem_l.setStyleSheet("color: #7f8c8d; font-style: italic;")
            cl.addWidget(mem_l)
            cl.addStretch()
            rs_layout.addWidget(card)

        layout.addWidget(rs_group)

        # --- Section 3: Rhythm Concepts ---
        rc_group = QGroupBox("Rhythm Concepts & Terminology")
        rc_layout = QVBoxLayout(rc_group)
        rc_layout.setSpacing(8)

        for i, (name, info) in enumerate(RHYTHM_CONCEPTS.items()):
            color = colors[i % len(colors)]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-top: 3px solid {color}; border-radius: 8px; padding: 10px 12px; margin: 4px 0; }}")
            cl = QVBoxLayout(card)
            name_l = QLabel(name)
            name_l.setFont(QFont('Segoe UI', 12, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            cl.addWidget(name_l)
            desc_l = QLabel(info['description'])
            desc_l.setWordWrap(True)
            desc_l.setFont(QFont('Segoe UI', 10))
            desc_l.setStyleSheet("color: #555; line-height: 1.5;")
            cl.addWidget(desc_l)
            ex_l = QLabel(f"Examples: {info['examples']}")
            ex_l.setWordWrap(True)
            ex_l.setFont(QFont('Segoe UI', 9))
            ex_l.setStyleSheet("color: #8e44ad; margin-top: 3px;")
            cl.addWidget(ex_l)
            imp_l = QLabel(info['importance'])
            imp_l.setWordWrap(True)
            imp_l.setFont(QFont('Segoe UI', 9))
            imp_l.setStyleSheet("color: #27ae60; background: #eafaf1; padding: 6px; border-radius: 6px; margin-top: 3px;")
            cl.addWidget(imp_l)
            rc_layout.addWidget(card)

        layout.addWidget(rc_group)

        # --- Section 4: World Rhythm Traditions ---
        wr_group = QGroupBox("World Rhythm Traditions")
        wr_layout = QVBoxLayout(wr_group)
        wr_layout.setSpacing(8)

        self.wr_combo = QComboBox()
        self.wr_combo.addItems(list(WORLD_RHYTHM_TRADITIONS.keys()))
        self.wr_combo.currentTextChanged.connect(self._update_wr_display)
        wr_layout.addWidget(self.wr_combo)

        self.wr_info_frame = QFrame()
        self.wr_info_frame.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 15px; }")
        self.wr_info_layout = QVBoxLayout(self.wr_info_frame)
        wr_layout.addWidget(self.wr_info_frame)

        # World rhythm playback button
        self.wr_play_btn = PlayButton("Play Rhythm Pattern")
        self.wr_play_btn.clicked.connect(self._play_world_rhythm)
        wr_layout.addWidget(self.wr_play_btn)

        layout.addWidget(wr_group)

        layout.addStretch()
        scroll.setWidget(content)
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        # Initialize display
        self._update_wr_display()
        return widget

    def _update_wr_display(self, text=None):
        name = self.wr_combo.currentText()
        if name not in WORLD_RHYTHM_TRADITIONS:
            return
        info = WORLD_RHYTHM_TRADITIONS[name]

        while self.wr_info_layout.count():
            item = self.wr_info_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        name_l = QLabel(name)
        name_l.setFont(QFont('Segoe UI', 16, QFont.Bold))
        name_l.setStyleSheet("color: #2c3e50;")
        self.wr_info_layout.addWidget(name_l)

        meta_row = QHBoxLayout()
        for label_text, value, color in [
            ("Pattern", info.get('pattern_name', ''), "#e74c3c"),
            ("Origin", info.get('origin', ''), "#3498db"),
            ("Region", info.get('region', ''), "#2ecc71"),
            ("BPM", info.get('bpm_range', ''), "#e67e22"),
        ]:
            badge = QLabel(f"{label_text}: {value}")
            badge.setFont(QFont('Segoe UI', 9, QFont.Bold))
            badge.setStyleSheet(f"color: white; background: {color}; border-radius: 8px; padding: 3px 10px;")
            meta_row.addWidget(badge)
        meta_row.addStretch()
        self.wr_info_layout.addLayout(meta_row)

        instruments_l = QLabel(f"Instruments: {info.get('instruments', '')}")
        instruments_l.setWordWrap(True)
        instruments_l.setFont(QFont('Segoe UI', 10))
        instruments_l.setStyleSheet("color: #8e44ad; margin-top: 5px;")
        self.wr_info_layout.addWidget(instruments_l)

        desc_l = QLabel(info.get('description', ''))
        desc_l.setWordWrap(True)
        desc_l.setFont(QFont('Segoe UI', 10))
        desc_l.setStyleSheet("color: #555; line-height: 1.6; margin-top: 8px;")
        self.wr_info_layout.addWidget(desc_l)

        feel_l = QLabel(f"Feeling: {info.get('feeling', '')}")
        feel_l.setWordWrap(True)
        feel_l.setFont(QFont('Segoe UI', 10))
        feel_l.setStyleSheet("color: #e67e22; background: #fef5e7; padding: 8px; border-radius: 6px; margin-top: 5px;")
        self.wr_info_layout.addWidget(feel_l)

        culture_l = QLabel(f"Cultural Context: {info.get('cultural_context', '')}")
        culture_l.setWordWrap(True)
        culture_l.setFont(QFont('Segoe UI', 10))
        culture_l.setStyleSheet("color: #2c3e50; background: #eaf2f8; padding: 8px; border-radius: 6px; margin-top: 5px;")
        self.wr_info_layout.addWidget(culture_l)

        # Visual pattern display
        pattern = info.get('pattern', [])
        if pattern:
            pat_label = QLabel("Rhythm Pattern (hit = colored, rest = gray):")
            pat_label.setFont(QFont('Segoe UI', 10, QFont.Bold))
            pat_label.setStyleSheet("color: #2c3e50; margin-top: 8px;")
            self.wr_info_layout.addWidget(pat_label)
            pat_row = QHBoxLayout()
            pat_row.setSpacing(2)
            for beat in pattern:
                dot = QLabel("")
                dot.setFixedSize(18, 18)
                if beat:
                    dot.setStyleSheet("background: #e74c3c; border-radius: 9px;")
                else:
                    dot.setStyleSheet("background: #ecf0f1; border-radius: 9px;")
                pat_row.addWidget(dot)
            pat_row.addStretch()
            self.wr_info_layout.addLayout(pat_row)

    def _play_world_rhythm(self):
        name = self.wr_combo.currentText()
        if name not in WORLD_RHYTHM_TRADITIONS:
            return
        pattern = WORLD_RHYTHM_TRADITIONS[name].get('pattern', [])
        if not pattern:
            return
        # Create a simple polyrhythm-style playback from the pattern
        bpm = 120
        for beat_val in pattern:
            if beat_val:
                audio_engine.play_note('C', 4)
            import time
            beat_duration = 60.0 / bpm / 2  # eighth-note subdivision
            time.sleep(beat_duration * 0.8)

    def _create_polyrhythm_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        title = QLabel("Polyrhythm Lab")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        desc = QLabel("Explore polyrhythms from around the world. Multiple rhythmic cycles play simultaneously, creating interlocking patterns fundamental to African, Indian, and Latin American music. Watch how beats from different layers align and separate.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        from music_engine import POLYRHYTHM_PATTERNS

        # Pattern selector + controls
        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Pattern:"))
        self.poly_combo = QComboBox()
        self.poly_combo.addItems(list(POLYRHYTHM_PATTERNS.keys()))
        self.poly_combo.currentTextChanged.connect(self._update_poly_display)
        ctrl.addWidget(self.poly_combo)
        ctrl.addSpacing(20)
        ctrl.addWidget(QLabel("BPM:"))
        self.poly_bpm = QSpinBox()
        self.poly_bpm.setRange(40, 240)
        self.poly_bpm.setValue(120)
        self.poly_bpm.setSuffix(" BPM")
        ctrl.addWidget(self.poly_bpm)
        ctrl.addStretch()
        layout.addLayout(ctrl)

        # Play button
        play_row = QHBoxLayout()
        self.poly_play_btn = PlayButton("Play Polyrhythm (4 beats)")
        self.poly_play_btn.clicked.connect(self._play_polyrhythm)
        play_row.addWidget(self.poly_play_btn)
        play_row.addStretch()
        layout.addLayout(play_row)

        # Info area
        self.poly_info_frame = QFrame()
        self.poly_info_frame.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 20px; }")
        self.poly_info_layout = QVBoxLayout(self.poly_info_frame)
        layout.addWidget(self.poly_info_frame)

        # Visualization area
        self.poly_viz_frame = QFrame()
        self.poly_viz_frame.setFixedHeight(120)
        self.poly_viz_frame.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 10px; }")
        self.poly_viz_layout = QVBoxLayout(self.poly_viz_frame)
        layout.addWidget(self.poly_viz_frame)

        layout.addStretch()
        self._update_poly_display()
        return widget

    def _update_poly_display(self, text=None):
        from music_engine import POLYRHYTHM_PATTERNS
        name = self.poly_combo.currentText()
        if name not in POLYRHYTHM_PATTERNS:
            return
        info = POLYRHYTHM_PATTERNS[name]

        # Clear info
        while self.poly_info_layout.count():
            item = self.poly_info_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        name_l = QLabel(name)
        name_l.setFont(QFont('Segoe UI', 18, QFont.Bold))
        name_l.setStyleSheet("color: #2c3e50;")
        self.poly_info_layout.addWidget(name_l)

        meta_row = QHBoxLayout()
        for label_text, value, color in [
            ("Origin", info['origin'], "#3498db"),
            ("Difficulty", info['difficulty'], "#e67e22"),
            ("Layers", str(len(info['layers'])), "#9b59b6"),
        ]:
            badge = QLabel(f"{label_text}: {value}")
            badge.setFont(QFont('Segoe UI', 10, QFont.Bold))
            badge.setStyleSheet(f"color: white; background: {color}; border-radius: 8px; padding: 3px 10px;")
            meta_row.addWidget(badge)
        meta_row.addStretch()
        self.poly_info_layout.addLayout(meta_row)

        desc_l = QLabel(info['description'])
        desc_l.setWordWrap(True)
        desc_l.setFont(QFont('Segoe UI', 11))
        desc_l.setStyleSheet("color: #555; line-height: 1.6; margin-top: 10px;")
        self.poly_info_layout.addWidget(desc_l)

        # Layer descriptions
        for layer in info['layers']:
            layer_l = QLabel(f"  {layer['name']}: {layer['beats']} beats/cycle (pitch: {layer['pitch']})")
            layer_l.setFont(QFont('Segoe UI', 10))
            layer_l.setStyleSheet("color: #2c3e50; padding: 2px 0; border-left: 3px solid #3498db; margin-left: 10px;")
            self.poly_info_layout.addWidget(layer_l)

        # Visualization - show beat positions
        while self.poly_viz_layout.count():
            item = self.poly_viz_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        from math import gcd
        from functools import reduce
        all_beats = [l['beats'] for l in info['layers']]
        lcm = reduce(lambda a, b: a * b // gcd(a, b), all_beats)
        colors_list = ["#e74c3c", "#3498db", "#2ecc71", "#e67e22", "#9b59b6"]

        for li, layer in enumerate(info['layers']):
            layer_row = QHBoxLayout()
            label = QLabel(f"{layer['name'][:12]}:")
            label.setFont(QFont('Segoe UI', 9, QFont.Bold))
            label.setFixedWidth(110)
            label.setStyleSheet(f"color: {colors_list[li % len(colors_list)]};")
            layer_row.addWidget(label)

            viz_widget = QWidget()
            viz_layout = QHBoxLayout(viz_widget)
            viz_layout.setContentsMargins(0, 0, 0, 0)
            viz_layout.setSpacing(1)

            for pos in range(lcm):
                is_hit = pos % layer['beats'] == 0
                dot = QLabel("")
                dot.setFixedSize(14, 14)
                if is_hit:
                    dot.setStyleSheet(f"background: {colors_list[li % len(colors_list)]}; border-radius: 7px;")
                else:
                    dot.setStyleSheet("background: #ecf0f1; border-radius: 7px;")
                viz_layout.addWidget(dot)

            layer_row.addWidget(viz_widget, 1)
            self.poly_viz_layout.addLayout(layer_row)

        # Resolution marker
        res_l = QLabel(f"Resolution: every {lcm} pulses (all layers align)")
        res_l.setFont(QFont('Segoe UI', 9))
        res_l.setStyleSheet("color: #7f8c8d; margin-top: 3px;")
        self.poly_viz_layout.addWidget(res_l)

    def _play_polyrhythm(self):
        from music_engine import POLYRHYTHM_PATTERNS
        name = self.poly_combo.currentText()
        if name not in POLYRHYTHM_PATTERNS:
            return
        pattern = POLYRHYTHM_PATTERNS[name]['layers']
        bpm = self.poly_bpm.value()
        audio_engine.play_polyrhythm(pattern, bpm=bpm, duration_beats=4.0)

    def _create_scale_compare_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        title = QLabel("Scale Comparison Tool")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        desc = QLabel("Compare any two scales side by side. See shared notes, unique notes, and hear them played. This is invaluable for understanding modal interchange, scale substitution, and how different scales create different moods over the same root.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        # Controls
        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Root:"))
        self.sc_root_combo = QComboBox()
        self.sc_root_combo.addItems(NOTE_NAMES)
        self.sc_root_combo.currentTextChanged.connect(self._update_scale_compare)
        ctrl.addWidget(self.sc_root_combo)
        ctrl.addSpacing(20)

        ctrl.addWidget(QLabel("Scale A:"))
        self.sc_scale_a = QComboBox()
        self.sc_scale_a.addItems(list(WESTERN_SCALES.keys()))
        self.sc_scale_a.setCurrentText('Major (Ionian)')
        self.sc_scale_a.currentTextChanged.connect(self._update_scale_compare)
        ctrl.addWidget(self.sc_scale_a)
        ctrl.addSpacing(20)

        ctrl.addWidget(QLabel("Scale B:"))
        self.sc_scale_b = QComboBox()
        self.sc_scale_b.addItems(list(WESTERN_SCALES.keys()))
        self.sc_scale_b.setCurrentText('Natural Minor (Aeolian)')
        self.sc_scale_b.currentTextChanged.connect(self._update_scale_compare)
        ctrl.addWidget(self.sc_scale_b)
        ctrl.addStretch()
        layout.addLayout(ctrl)

        # Play buttons
        play_row = QHBoxLayout()
        self.sc_play_a = PlayButton("Play Scale A")
        self.sc_play_a.clicked.connect(self._play_scale_a_compare)
        play_row.addWidget(self.sc_play_a)
        self.sc_play_b = PlayButton("Play Scale B")
        self.sc_play_b.clicked.connect(self._play_scale_b_compare)
        play_row.addWidget(self.sc_play_b)
        self.sc_play_shared = PlayButton("Play Shared Notes")
        self.sc_play_shared.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #e67e22,stop:1 #d35400);
                        color: white; border: none; border-radius: 17px; padding: 6px 18px; font-size: 12px; }
            QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #d35400,stop:1 #e74c3c); }
            QPushButton:disabled { background: #bdc3c7; color: #95a5a6; }
        """)
        if not audio_engine.is_available:
            self.sc_play_shared.setEnabled(False)
            self.sc_play_shared.setText("Play Shared (no audio)")
        self.sc_play_shared.clicked.connect(self._play_shared_notes)
        play_row.addWidget(self.sc_play_shared)
        play_row.addStretch()
        layout.addLayout(play_row)

        # Result area
        self.sc_result = QFrame()
        self.sc_result.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 20px; }")
        self.sc_result_layout = QVBoxLayout(self.sc_result)
        layout.addWidget(self.sc_result)

        # Dual pianos
        piano_row = QHBoxLayout()
        self.sc_piano_a = PianoWidget(4, 1)
        self.sc_piano_a.setMinimumHeight(160)
        piano_row.addWidget(self.sc_piano_a)
        self.sc_piano_b = PianoWidget(4, 1)
        self.sc_piano_b.setMinimumHeight(160)
        piano_row.addWidget(self.sc_piano_b)
        layout.addLayout(piano_row)

        self._update_scale_compare()
        return widget

    def _update_scale_compare(self, text=None):
        # Clear old content
        while self.sc_result_layout.count():
            item = self.sc_result_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        root = self.sc_root_combo.currentText()
        name_a = self.sc_scale_a.currentText()
        name_b = self.sc_scale_b.currentText()

        notes_a = get_scale_notes(root, name_a) if name_a in WESTERN_SCALES else []
        notes_b = get_scale_notes(root, name_b) if name_b in WESTERN_SCALES else []

        if not notes_a or not notes_b:
            return

        set_a = set(notes_a)
        set_b = set(notes_b)
        shared = sorted(set_a & set_b)
        only_a = sorted(set_a - set_b)
        only_b = sorted(set_b - set_a)

        # Scale A header
        header_a = QLabel(f"<b style='color:#3498db;font-size:16px;'>{root} {name_a}</b>")
        header_a.setFont(QFont('Segoe UI', 14, QFont.Bold))
        self.sc_result_layout.addWidget(header_a)

        # Scale A badges
        badges_a_row = QHBoxLayout()
        for n in notes_a:
            is_shared = n in shared
            bg = "#27ae60" if n == root else ("#e67e22" if is_shared else "#3498db")
            badge = QLabel(n)
            badge.setAlignment(Qt.AlignCenter)
            badge.setFixedSize(42, 30)
            badge.setStyleSheet(f"background:{bg};color:white;border-radius:6px;font-weight:bold;font-size:12px;")
            badges_a_row.addWidget(badge)
        self.sc_result_layout.addLayout(badges_a_row)

        # Scale B header
        header_b = QLabel(f"<b style='color:#9b59b6;font-size:16px;'>{root} {name_b}</b>")
        header_b.setFont(QFont('Segoe UI', 14, QFont.Bold))
        self.sc_result_layout.addWidget(header_b)

        badges_b_row = QHBoxLayout()
        for n in notes_b:
            is_shared = n in shared
            bg = "#27ae60" if n == root else ("#e67e22" if is_shared else "#9b59b6")
            badge = QLabel(n)
            badge.setAlignment(Qt.AlignCenter)
            badge.setFixedSize(42, 30)
            badge.setStyleSheet(f"background:{bg};color:white;border-radius:6px;font-weight:bold;font-size:12px;")
            badges_b_row.addWidget(badge)
        self.sc_result_layout.addLayout(badges_b_row)

        # Summary
        summary = QLabel(
            f"<b>Shared notes ({len(shared)}):</b> {', '.join(shared) if shared else 'None'}<br>"
            f"<span style='color:#3498db'><b>Only in {name_a} ({len(only_a)}):</b> {', '.join(only_a) if only_a else 'None'}</span><br>"
            f"<span style='color:#9b59b6'><b>Only in {name_b} ({len(only_b)}):</b> {', '.join(only_b) if only_b else 'None'}</span><br>"
            f"<span style='color:#e67e22'><b>Difference:</b> {len(only_a) + len(only_b)} notes differ</span>"
        )
        summary.setWordWrap(True)
        summary.setFont(QFont('Segoe UI', 11))
        summary.setStyleSheet("color: #555; line-height: 1.6; margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 8px;")
        self.sc_result_layout.addWidget(summary)

        # Update pianos
        self.sc_piano_a.highlight_notes_root_and_scale(root, notes_a, 4)
        self.sc_piano_b.highlight_notes_root_and_scale(root, notes_b, 4)

        # Store shared for playback
        self._sc_shared = [n for n in notes_a if n in set_b]

    def _play_scale_a_compare(self):
        root = self.sc_root_combo.currentText()
        name = self.sc_scale_a.currentText()
        if name in WESTERN_SCALES:
            notes = get_scale_notes(root, name)
            seq = [(n, 4) for n in notes] + [(root, 4)]
            audio_engine.play_sequence(seq, interval_ms=300)

    def _play_scale_b_compare(self):
        root = self.sc_root_combo.currentText()
        name = self.sc_scale_b.currentText()
        if name in WESTERN_SCALES:
            notes = get_scale_notes(root, name)
            seq = [(n, 4) for n in notes] + [(root, 4)]
            audio_engine.play_sequence(seq, interval_ms=300)

    def _play_shared_notes(self):
        if hasattr(self, '_sc_shared') and self._sc_shared:
            seq = [(n, 4) for n in self._sc_shared] + [(self._sc_shared[0], 4)]
            audio_engine.play_sequence(seq, interval_ms=350)

    def _create_voicings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        title = QLabel("Chord Voicing Library")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        desc = QLabel("Explore different voicings for each chord type. A voicing determines which octave and inversion a chord's notes are played in, dramatically changing its sound and emotional character. Click any voicing to hear it and see it on the piano.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Root:"))
        self.voicings_root = QComboBox()
        self.voicings_root.addItems(NOTE_NAMES)
        self.voicings_root.currentTextChanged.connect(self._update_voicings)
        ctrl.addWidget(self.voicings_root)
        ctrl.addSpacing(20)
        ctrl.addWidget(QLabel("Chord Type:"))
        self.voicings_type = QComboBox()
        self.voicings_type.addItems(list(CHORD_TYPES.keys()))
        self.voicings_type.currentTextChanged.connect(self._update_voicings)
        ctrl.addWidget(self.voicings_type)
        ctrl.addStretch()
        layout.addLayout(ctrl)

        self.voicings_result = QFrame()
        self.voicings_result.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 20px; }")
        self.voicings_layout = QVBoxLayout(self.voicings_result)
        layout.addWidget(self.voicings_result)

        self.voicings_piano = PianoWidget(3, 2)
        layout.addWidget(self.voicings_piano)
        layout.addStretch()

        self._update_voicings()
        return widget

    def _update_voicings(self, text=None):
        while self.voicings_layout.count():
            item = self.voicings_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        root = self.voicings_root.currentText()
        ctype = self.voicings_type.currentText()
        if ctype not in CHORD_TYPES:
            return

        notes = get_chord_notes(root, ctype)
        if not notes:
            return

        from music_engine import note_to_midi

        name_l = QLabel(f"{root} {ctype} - Voicings")
        name_l.setFont(QFont('Segoe UI', 18, QFont.Bold))
        name_l.setStyleSheet("color: #2c3e50;")
        self.voicings_layout.addWidget(name_l)

        formula_l = QLabel(f"Formula: {CHORD_TYPES[ctype].get('formula', '')} | Notes: {', '.join(notes)}")
        formula_l.setFont(QFont('Segoe UI', 11))
        formula_l.setStyleSheet("color: #555; margin-bottom: 10px;")
        self.voicings_layout.addWidget(formula_l)

        # Generate voicings: root position, 1st inversion, 2nd inversion, close, open, spread
        voicings = []

        # Root position
        root_pos = [(n, 4) for n in notes]
        voicings.append(("Root Position", root_pos, "#3498db"))

        # Inversions
        if len(notes) >= 3:
            inv1 = list(root_pos[1:]) + [(notes[0], 5)]
            voicings.append(("1st Inversion", inv1, "#2ecc71"))
        if len(notes) >= 4:
            inv2 = list(root_pos[2:]) + [(notes[0], 5), (notes[1], 5)]
            voicings.append(("2nd Inversion", inv2, "#e67e22"))
        if len(notes) >= 5:
            inv3 = list(root_pos[3:]) + [(notes[0], 5), (notes[1], 5), (notes[2], 5)]
            voicings.append(("3rd Inversion", inv3, "#9b59b6"))

        # Close voicing (higher octave)
        close = [(n, 5) for n in notes]
        voicings.append(("Close Voicing (5th octave)", close, "#e84393"))

        # Open voicing (spread across octaves)
        if len(notes) >= 3:
            open_v = [(notes[0], 3), (notes[1], 4), (notes[2], 4)]
            if len(notes) >= 4:
                open_v.append((notes[3], 5))
            if len(notes) >= 5:
                open_v.append((notes[4], 5))
            voicings.append(("Open Voicing (spread)", open_v, "#1abc9c"))

        # Drop 2 voicing (for 4+ note chords)
        if len(notes) >= 4:
            drop2 = [(notes[0], 4), (notes[2], 4), (notes[3], 5)]
            voicings.append(("Drop 2", drop2, "#c0392b"))

        colors_cycle = ["#3498db", "#2ecc71", "#e67e22", "#9b59b6", "#e84393", "#1abc9c", "#c0392b", "#f39c12"]
        for i, (vname, vnotes, vcolor) in enumerate(voicings):
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: #f8f9fa; border-left: 4px solid {vcolor}; border-radius: 8px; padding: 10px 15px; margin: 4px 0; }}")
            card.setCursor(Qt.PointingHandCursor)
            cl = QHBoxLayout(card)
            cl.setContentsMargins(12, 8, 12, 8)

            vname_l = QLabel(vname)
            vname_l.setFont(QFont('Segoe UI', 11, QFont.Bold))
            vname_l.setStyleSheet(f"color: {vcolor};")
            vname_l.setFixedWidth(200)
            cl.addWidget(vname_l)

            for n, oct in vnotes:
                badge = QLabel(f"{n}{oct}")
                badge.setAlignment(Qt.AlignCenter)
                badge.setStyleSheet(f"background: {vcolor}; color: white; border-radius: 5px; padding: 3px 8px; font-weight: bold; font-size: 11px; margin: 1px;")
                badge.setFixedHeight(26)
                cl.addWidget(badge)

            play_v_btn = PlayButton("Play")
            play_v_btn.setFixedHeight(26)
            play_v_btn.setFont(QFont('Segoe UI', 9, QFont.Bold))
            def _play_voicing(notes_list=vnotes):
                audio_engine.play_chord(notes_list, duration=1.2)
            play_v_btn.clicked.connect(_play_voicing)
            cl.addWidget(play_v_btn)

            def _show_voicing(notes_list=vnotes):
                note_names = [n for n, o in notes_list]
                self.voicings_piano.clear_highlights()
                self.voicings_piano.highlight_notes(note_names, 'chord', 4)
            card.mousePressEvent = lambda event, nl=vnotes: (_show_voicing(nl), _play_voicing.__wrapped__() if hasattr(_play_voicing, '__wrapped__') else None)

            # Use click on the card frame to show on piano
            def _on_card_click(event, notes_list=vnotes):
                note_names = [n for n, o in notes_list]
                self.voicings_piano.clear_highlights()
                self.voicings_piano.highlight_notes(note_names, 'chord', 4)
            card.mousePressEvent = _on_card_click

            self.voicings_layout.addWidget(card)

        self.voicings_layout.addStretch()

    def _create_transpose_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        title = QLabel("Transposition Tool")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        desc = QLabel("Transpose any sequence of notes or chords to a different key. Essential for musicians who need to adapt sheet music for different instruments or vocal ranges. Select the original key, the target key, and enter your notes.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("From Key:"))
        self.transpose_from = QComboBox()
        self.transpose_from.addItems(NOTE_NAMES)
        self.transpose_from.setCurrentText('C')
        ctrl.addWidget(self.transpose_from)
        ctrl.addSpacing(20)
        ctrl.addWidget(QLabel("To Key:"))
        self.transpose_to = QComboBox()
        self.transpose_to.addItems(NOTE_NAMES)
        self.transpose_to.setCurrentText('G')
        self.transpose_to.currentTextChanged.connect(self._do_transpose)
        self.transpose_from.currentTextChanged.connect(self._do_transpose)
        ctrl.addWidget(self.transpose_to)
        ctrl.addStretch()
        layout.addLayout(ctrl)

        self.transpose_input = QLineEdit()
        self.transpose_input.setPlaceholderText("Enter notes separated by spaces or commas (e.g., C E G B) or chords (e.g., Cmaj Am F G)...")
        self.transpose_input.setFont(QFont('Segoe UI', 12))
        self.transpose_input.setFixedHeight(40)
        self.transpose_input.textChanged.connect(self._do_transpose)
        layout.addWidget(self.transpose_input)

        # Quick presets
        preset_row = QHBoxLayout()
        preset_label = QLabel("Quick presets:")
        preset_label.setFont(QFont('Segoe UI', 10, QFont.Bold))
        preset_label.setStyleSheet("color: #7f8c8d;")
        preset_row.addWidget(preset_label)
        presets = ["C E G C", "C D E F G A B C", "C E G B", "D F A C", "C Eb G Bb"]
        for p in presets:
            btn = QPushButton(p)
            btn.setFont(QFont('Segoe UI', 9))
            btn.setFixedHeight(28)
            btn.setStyleSheet("""
                QPushButton { padding: 4px 12px; border: 1px solid #dce1e3; border-radius: 10px;
                              background: white; color: #2c3e50; }
                QPushButton:hover { background: #3498db; color: white; border-color: #3498db; }
            """)
            btn.clicked.connect(lambda checked, text=p: self.transpose_input.setText(text))
            preset_row.addWidget(btn)
        preset_row.addStretch()
        layout.addLayout(preset_row)

        self.transpose_result = QFrame()
        self.transpose_result.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 20px; }")
        self.transpose_result_layout = QVBoxLayout(self.transpose_result)
        layout.addWidget(self.transpose_result)

        # Transpose piano
        self.transpose_piano = PianoWidget(3, 2)
        layout.addWidget(self.transpose_piano)

        layout.addStretch()
        return widget

    def _do_transpose(self, text=None):
        while self.transpose_result_layout.count():
            item = self.transpose_result_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        from_idx = NOTE_NAMES.index(self.transpose_from.currentText())
        to_idx = NOTE_NAMES.index(self.transpose_to.currentText())
        semitone_shift = (to_idx - from_idx) % 12

        input_text = self.transpose_input.text().strip()
        if not input_text:
            placeholder = QLabel("Enter notes above to see the transposition")
            placeholder.setFont(QFont('Segoe UI', 13))
            placeholder.setStyleSheet("color: #95a5a6; padding: 20px;")
            placeholder.setAlignment(Qt.AlignCenter)
            self.transpose_result_layout.addWidget(placeholder)
            self.transpose_piano.clear_highlights()
            return

        # Parse notes
        tokens = input_text.replace(',', ' ').split()
        original_notes = []
        for token in tokens:
            clean = token.strip()
            if clean in NOTE_NAMES:
                original_notes.append(clean)

        if not original_notes:
            nope = QLabel("No valid note names found. Use: C C# D D# E F F# G G# A A# B")
            nope.setFont(QFont('Segoe UI', 11))
            nope.setStyleSheet("color: #e74c3c; padding: 10px;")
            nope.setAlignment(Qt.AlignCenter)
            self.transpose_result_layout.addWidget(nope)
            self.transpose_piano.clear_highlights()
            return

        # Transpose
        transposed = []
        for note in original_notes:
            idx = NOTE_NAMES.index(note)
            new_idx = (idx + semitone_shift) % 12
            transposed.append(NOTE_NAMES[new_idx])

        # Display
        shift_dir = "up" if semitone_shift != 0 else ""
        interval_name = INTERVAL_SHORT.get(semitone_shift, str(semitone_shift))

        header = QLabel(f"Transposition: {self.transpose_from.currentText()} -> {self.transpose_to.currentText()} ({interval_name}, {semitone_shift} semitones)")
        header.setFont(QFont('Segoe UI', 14, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        self.transpose_result_layout.addWidget(header)

        # Original row
        orig_row = QHBoxLayout()
        orig_label = QLabel("Original:")
        orig_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        orig_label.setStyleSheet("color: #3498db;")
        orig_label.setFixedWidth(80)
        orig_row.addWidget(orig_label)
        for note in original_notes:
            badge = QLabel(note)
            badge.setAlignment(Qt.AlignCenter)
            badge.setStyleSheet("background: #3498db; color: white; border-radius: 6px; padding: 5px 10px; font-weight: bold; font-size: 13px; margin: 2px;")
            badge.setFixedHeight(32)
            orig_row.addWidget(badge)
        orig_row.addStretch()
        self.transpose_result_layout.addLayout(orig_row)

        # Arrow
        arrow = QLabel("      \u2193")
        arrow.setFont(QFont('Segoe UI', 18, QFont.Bold))
        arrow.setStyleSheet("color: #27ae60;")
        arrow.setAlignment(Qt.AlignCenter)
        self.transpose_result_layout.addWidget(arrow)

        # Transposed row
        trans_row = QHBoxLayout()
        trans_label = QLabel("Transposed:")
        trans_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        trans_label.setStyleSheet("color: #27ae60;")
        trans_label.setFixedWidth(80)
        trans_row.addWidget(trans_label)
        for note in transposed:
            badge = QLabel(note)
            badge.setAlignment(Qt.AlignCenter)
            badge.setStyleSheet("background: #27ae60; color: white; border-radius: 6px; padding: 5px 10px; font-weight: bold; font-size: 13px; margin: 2px;")
            badge.setFixedHeight(32)
            trans_row.addWidget(badge)
        trans_row.addStretch()
        self.transpose_result_layout.addLayout(trans_row)

        # Play buttons
        btn_row = QHBoxLayout()
        play_orig = PlayButton("Play Original")
        play_orig.clicked.connect(lambda: audio_engine.play_sequence([(n, 4) for n in original_notes], interval_ms=300))
        btn_row.addWidget(play_orig)
        play_trans = PlayButton("Play Transposed")
        play_trans.clicked.connect(lambda: audio_engine.play_sequence([(n, 4) for n in transposed], interval_ms=300))
        btn_row.addWidget(play_trans)
        btn_row.addStretch()
        self.transpose_result_layout.addLayout(btn_row)

        # Update piano
        self.transpose_piano.clear_highlights()
        self.transpose_piano.highlight_notes(transposed, 'scale', 4)

    def _create_metronome_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        title = QLabel("Metronome")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        desc = QLabel("A metronome is the most fundamental practice tool for any musician. Set the tempo, choose a time signature, and develop your sense of rhythm. The visual beat indicator and click sounds help you internalize steady timing.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        # Controls
        ctrl = QHBoxLayout()

        ctrl.addWidget(QLabel("BPM:"))
        self.metro_bpm_spin = QSpinBox()
        self.metro_bpm_spin.setRange(20, 300)
        self.metro_bpm_spin.setValue(120)
        self.metro_bpm_spin.setSuffix(" BPM")
        self.metro_bpm_spin.setFixedWidth(120)
        self.metro_bpm_spin.valueChanged.connect(self._update_metronome_bpm)
        ctrl.addWidget(self.metro_bpm_spin)

        ctrl.addSpacing(20)
        ctrl.addWidget(QLabel("Beats:"))
        self.metro_beats = QComboBox()
        self.metro_beats.addItems(['2', '3', '4', '5', '6', '7', '8', '9'])
        self.metro_beats.setCurrentText('4')
        ctrl.addWidget(self.metro_beats)

        ctrl.addSpacing(20)
        self.metro_start_btn = PlayButton("Start")
        self.metro_start_btn.clicked.connect(self._toggle_metronome)
        ctrl.addWidget(self.metro_start_btn)

        ctrl.addStretch()
        layout.addLayout(ctrl)

        # BPM Slider
        self.metro_slider = QSlider(Qt.Horizontal)
        self.metro_slider.setRange(20, 300)
        self.metro_slider.setValue(120)
        self.metro_slider.valueChanged.connect(self._on_metro_slider)
        layout.addWidget(self.metro_slider)

        # Tap tempo
        tap_row = QHBoxLayout()
        self.metro_tap_btn = QPushButton("Tap Tempo")
        self.metro_tap_btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.metro_tap_btn.setFixedHeight(40)
        self.metro_tap_btn.setStyleSheet("""
            QPushButton { padding: 8px 24px; border: 2px solid #e67e22; border-radius: 20px;
                          background: white; color: #e67e22; }
            QPushButton:hover { background: #e67e22; color: white; }
        """)
        self.metro_tap_btn.clicked.connect(self._tap_tempo)
        tap_row.addWidget(self.metro_tap_btn)

        # Tempo presets
        tempo_presets = [("Largo", 50), ("Adagio", 70), ("Andante", 90), ("Moderato", 115), ("Allegro", 140), ("Vivace", 170), ("Presto", 200)]
        for name, bpm in tempo_presets:
            btn = QPushButton(f"{name}\n{bpm}")
            btn.setFont(QFont('Segoe UI', 8, QFont.Bold))
            btn.setFixedHeight(40)
            btn.setFixedWidth(70)
            btn.setStyleSheet("""
                QPushButton { padding: 4px; border: 1px solid #dce1e3; border-radius: 8px;
                              background: white; color: #2c3e50; }
                QPushButton:hover { background: #3498db; color: white; border-color: #3498db; }
            """)
            btn.clicked.connect(lambda checked, b=bpm: (self.metro_bpm_spin.setValue(b), self.metro_slider.setValue(b)))
            tap_row.addWidget(btn)

        tap_row.addStretch()
        layout.addLayout(tap_row)

        # Visual beat indicator
        self.metro_viz_frame = QFrame()
        self.metro_viz_frame.setFixedHeight(80)
        self.metro_viz_frame.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 10px; }")
        self.metro_viz_layout = QHBoxLayout(self.metro_viz_frame)
        self.metro_viz_layout.setSpacing(5)
        layout.addWidget(self.metro_viz_frame)
        self._init_metronome_viz()

        # Status
        self.metro_status = QLabel("Stopped")
        self.metro_status.setFont(QFont('Segoe UI', 13, QFont.Bold))
        self.metro_status.setAlignment(Qt.AlignCenter)
        self.metro_status.setStyleSheet("color: #95a5a6;")
        layout.addWidget(self.metro_status)

        layout.addStretch()

        # Metronome state
        self._metro_running = False
        self._metro_timer = QTimer()
        self._metro_timer.timeout.connect(self._metro_tick)
        self._metro_current_beat = 0
        self._metro_tap_times = []

        return widget

    def _init_metronome_viz(self):
        while self.metro_viz_layout.count():
            item = self.metro_viz_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        num_beats = int(self.metro_beats.currentText())
        self._metro_dots = []
        for i in range(num_beats):
            dot = QLabel("")
            dot.setAlignment(Qt.AlignCenter)
            is_downbeat = (i == 0)
            size = 50 if is_downbeat else 36
            dot.setFixedSize(size, size)
            color = "#e74c3c" if is_downbeat else "#3498db"
            dot.setStyleSheet(f"background: #ecf0f1; border-radius: {size//2}px; border: 3px solid {color};")
            self.metro_viz_layout.addWidget(dot)
            self._metro_dots.append((dot, color))
        self.metro_viz_layout.addStretch()

    def _update_metronome_bpm(self, val=None):
        self.metro_slider.blockSignals(True)
        self.metro_slider.setValue(self.metro_bpm_spin.value())
        self.metro_slider.blockSignals(False)
        if self._metro_running:
            self._metro_timer.setInterval(int(60000 / self.metro_bpm_spin.value()))

    def _on_metro_slider(self, val):
        self.metro_bpm_spin.blockSignals(True)
        self.metro_bpm_spin.setValue(val)
        self.metro_bpm_spin.blockSignals(False)
        if self._metro_running:
            self._metro_timer.setInterval(int(60000 / val))

    def _tap_tempo(self):
        import time
        now = time.time()
        self._metro_tap_times.append(now)
        # Keep only last 5 taps
        self._metro_tap_times = self._metro_tap_times[-5:]
        if len(self._metro_tap_times) >= 2:
            intervals = [self._metro_tap_times[i+1] - self._metro_tap_times[i] for i in range(len(self._metro_tap_times)-1)]
            avg_interval = sum(intervals) / len(intervals)
            if avg_interval > 0:
                bpm = int(60000 / (avg_interval * 1000))
                bpm = max(20, min(300, bpm))
                self.metro_bpm_spin.setValue(bpm)
                self.metro_slider.setValue(bpm)

    def _toggle_metronome(self):
        if self._metro_running:
            self._metro_running = False
            self._metro_timer.stop()
            self.metro_start_btn.setText("Start")
            self.metro_status.setText("Stopped")
            self.metro_status.setStyleSheet("color: #95a5a6;")
            # Reset dots
            for dot, color in self._metro_dots:
                size = dot.width()
                dot.setStyleSheet(f"background: #ecf0f1; border-radius: {size//2}px; border: 3px solid {color};")
        else:
            self._metro_running = True
            self._metro_current_beat = 0
            self._metro_timer.setInterval(int(60000 / self.metro_bpm_spin.value()))
            self._metro_timer.start()
            self.metro_start_btn.setText("Stop")
            bpm = self.metro_bpm_spin.value()
            tempo_name = ""
            if bpm <= 55: tempo_name = "Largo"
            elif bpm <= 75: tempo_name = "Adagio"
            elif bpm <= 100: tempo_name = "Andante"
            elif bpm <= 130: tempo_name = "Moderato"
            elif bpm <= 160: tempo_name = "Allegro"
            elif bpm <= 185: tempo_name = "Vivace"
            else: tempo_name = "Presto"
            self.metro_status.setText(f"Playing - {bpm} BPM ({tempo_name})")
            self.metro_status.setStyleSheet("color: #27ae60;")

    def _metro_tick(self):
        num_beats = int(self.metro_beats.currentText())
        beat = self._metro_current_beat % num_beats

        # Update visuals
        for i, (dot, color) in enumerate(self._metro_dots):
            size = dot.width()
            if i == beat:
                dot.setStyleSheet(f"background: {color}; border-radius: {size//2}px; border: 3px solid {color};")
            else:
                dot.setStyleSheet(f"background: #ecf0f1; border-radius: {size//2}px; border: 3px solid {color};")

        # Play click sound
        if audio_engine.is_available and not audio_engine._muted:
            freq = 1000.0 if beat == 0 else 700.0
            try:
                import numpy as np
                from piano_widget import sd
                sr = 44100
                dur = 0.05
                t = np.linspace(0, dur, int(sr * dur), False)
                wave = np.sin(2 * np.pi * freq * t)
                # Quick decay envelope
                env = np.exp(-t * 60)
                wave = (wave * env * 0.3).astype(np.float32)
                sd.play(wave, sr)
            except Exception:
                pass

        self._metro_current_beat += 1

        # Reinit viz if beat count changed
        if len(self._metro_dots) != num_beats:
            self._init_metronome_viz()


# ============================================================
# EASTERN MODULE
# ============================================================
class EasternModule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(10)

        title = SectionTitle("Eastern Music Theory", "Explore Indian ragas, Arabic maqams, and Asian scales")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setFont(QFont('Segoe UI', 11))
        tabs.addTab(self._create_indian_tab(), "Indian Ragas")
        tabs.addTab(self._create_arabic_tab(), "Arabic Maqams")
        tabs.addTab(self._create_persian_tab(), "Persian Dastgahs")
        tabs.addTab(self._create_carnatic_tab(), "Carnatic Ragas")
        tabs.addTab(self._create_chinese_tab(), "Chinese Scales")
        tabs.addTab(self._create_japanese_tab(), "Japanese Scales")
        tabs.addTab(self._create_korean_tab(), "Korean Scales")
        tabs.addTab(self._create_indonesian_tab(), "Indonesian")
        tabs.addTab(self._create_turkish_tab(), "Turkish Makams")

        # Shared piano for Eastern scales
        self.eastern_piano = PianoWidget(start_octave=3, num_octaves=2)
        self.eastern_piano.show_labels(True)
        piano_container = QFrame()
        piano_container.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 10px; padding: 5px; }")
        pc_layout = QVBoxLayout(piano_container)
        pc_layout.setContentsMargins(10, 5, 10, 5)
        
        piano_header = QHBoxLayout()
        piano_label = QLabel("Piano (approximate - microtonal scales may differ)")
        piano_label.setFont(QFont('Segoe UI', 10))
        piano_label.setStyleSheet("color: #7f8c8d;")
        piano_header.addWidget(piano_label)
        
        self.eastern_play_btn = PlayButton("Play Scale Ascending")
        self.eastern_play_btn.clicked.connect(self._play_eastern_scale)
        piano_header.addWidget(self.eastern_play_btn)
        
        self.eastern_clear_btn = QPushButton("Clear")
        self.eastern_clear_btn.setFont(QFont('Segoe UI', 10))
        self.eastern_clear_btn.setStyleSheet("""
            QPushButton { padding: 6px 14px; border: 1px solid #dce1e3; border-radius: 12px;
                          background: white; color: #7f8c8d; }
            QPushButton:hover { background: #f5f6fa; }
        """)
        self.eastern_clear_btn.clicked.connect(lambda: self.eastern_piano.clear_highlights())
        piano_header.addWidget(self.eastern_clear_btn)
        piano_header.addStretch()
        pc_layout.addLayout(piano_header)
        pc_layout.addWidget(self.eastern_piano)
        
        layout.addWidget(tabs)
        layout.addWidget(piano_container)

    def _play_eastern_scale(self):
        """Play the currently highlighted eastern scale notes."""
        notes = self.eastern_piano.get_current_scale_with_octaves(4)
        if notes:
            audio_engine.play_sequence(notes, interval_ms=400)

    def _create_raga_info(self, raga_name, info, is_indian=True):
        """Create raga/maqam info content with enhanced fields."""
        widgets = []

        name_label = QLabel(raga_name)
        name_label.setFont(QFont('Segoe UI', 22, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        widgets.append(name_label)

        # Notes
        notes_frame = QFrame()
        notes_frame.setStyleSheet("background: #f8f9fa; border-radius: 10px; padding: 10px;")
        nl = QHBoxLayout(notes_frame)
        for note in info['notes']:
            is_special = 'k' in note or 'K' in note
            badge = QLabel(note)
            badge.setAlignment(Qt.AlignCenter)
            bg = "#e67e22" if is_special else "#3498db"
            badge.setStyleSheet(f"background: {bg}; color: white; border-radius: 6px; padding: 5px 10px; font-weight: bold; font-size: 13px; margin: 2px;")
            badge.setFixedSize(45, 30)
            nl.addWidget(badge)
        widgets.append(notes_frame)

        # Standard info cards
        if is_indian:
            cards = [
                ("Thaat", info.get('thaat', ''), "#3498db"),
                ("Time", info.get('time', ''), "#e67e22"),
                ("Season", info.get('season', ''), "#2ecc71"),
                ("Mood / Rasa", info['mood'], "#9b59b6"),
                ("Western Equivalent", info.get('equivalent_western', ''), "#1abc9c"),
            ]
            if 'vadi_samvadi' in info:
                vadi, samvadi = info['vadi_samvadi']
                cards.append(("Vadi (King Note)", vadi, "#e74c3c"))
                cards.append(("Samvadi (Queen Note)", samvadi, "#e74c3c"))
            if 'pakad' in info:
                cards.append(("Pakad (Characteristic Phrase)", info['pakad'], "#8e44ad"))
        else:
            cards = [
                ("Mood", info['mood'], "#e67e22"),
                ("Region", info.get('region', ''), "#3498db"),
                ("Western Equivalent", info.get('equivalent_western', ''), "#1abc9c"),
            ]
            if 'family' in info:
                cards.append(("Maqam Family", info['family'], "#9b59b6"))

        for title, content, color in cards:
            widgets.append(InfoCard(title, content, color))

        # Description
        desc = QLabel(info['description'])
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #555; line-height: 1.7; margin-top: 10px; padding: 15px; background: white; border-radius: 10px; border: 1px solid #e8ecf0;")
        widgets.append(desc)

        # Classical note
        if 'chnote' in info:
            cn = QLabel(f"Note: {info['chnote']}")
            cn.setWordWrap(True)
            cn.setFont(QFont('Segoe UI', 10))
            cn.setStyleSheet("color: #e67e22; background: #fef5e7; padding: 10px; border-radius: 8px; margin-top: 8px;")
            widgets.append(cn)

        # Famous pieces
        field = 'famous_recordings' if 'famous_recordings' in info else 'famous_pieces'
        if field in info:
            rec_label = QLabel("Famous Recordings:")
            rec_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
            rec_label.setStyleSheet("color: #8e44ad; margin-top: 10px;")
            widgets.append(rec_label)
            for rec in info[field]:
                r = QLabel(f"  - {rec}")
                r.setFont(QFont('Segoe UI', 11))
                r.setStyleSheet("color: #555; padding: 3px 10px;")
                widgets.append(r)

        # Piano + play button for ragas with Western-interval data
        if is_indian and 'asc_intervals' in info:
            intervals = info['asc_intervals']
            western_notes = [NOTE_NAMES[i % 12] for i in intervals]
            piano = PianoWidget(3, 2)
            piano.highlight_notes(western_notes, 'scale')
            widgets.append(piano)
            play_btn = PlayButton("Play Western Approximation")
            play_btn.clicked.connect(
                lambda checked, notes=western_notes: audio_engine.play_sequence(
                    [(n, 4) for n in notes] + [(notes[0], 4)], interval_ms=400))
            play_row = QHBoxLayout()
            play_row.addWidget(play_btn)
            play_row.addStretch()
            note_row = QWidget()
            note_row.setLayout(play_row)
            widgets.append(note_row)

        return widgets

    def _create_indian_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)

        self.raga_search_list = SearchFilterList(list(INDIAN_RAGAS.keys()))
        self.raga_search_list.setMaximumWidth(300)
        self.raga_search_list.selectionChanged.connect(self._update_raga_display)
        layout.addWidget(self.raga_search_list)

        right = QScrollArea()
        right.setWidgetResizable(True)
        self.raga_content = QWidget()
        self.raga_layout = QVBoxLayout(self.raga_content)
        self.raga_layout.setSpacing(10)
        right.setWidget(self.raga_content)
        layout.addWidget(right, 1)

        self._update_raga_display("Raga Yaman")
        return widget

    def _update_raga_display(self, raga_name):
        if raga_name not in INDIAN_RAGAS:
            return
        while self.raga_layout.count():
            item = self.raga_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for w in self._create_raga_info(raga_name, INDIAN_RAGAS[raga_name], True):
            self.raga_layout.addWidget(w)
        
        # Add "Show on Shared Piano" button for ragas with interval data
        raga_info = INDIAN_RAGAS[raga_name]
        if 'asc_intervals' in raga_info:
            western_notes = [NOTE_NAMES[i % 12] for i in raga_info['asc_intervals']]
            show_on_shared = QPushButton("Show on Shared Piano")
            show_on_shared.setFont(QFont('Segoe UI', 10, QFont.Bold))
            show_on_shared.setStyleSheet("""
                QPushButton { padding: 6px 16px; border: 1px solid #9b59b6; border-radius: 12px;
                              background: #9b59b6; color: white; }
                QPushButton:hover { background: #8e44ad; }
            """)
            show_on_shared.clicked.connect(lambda checked, notes=western_notes: self.eastern_piano.highlight_notes(notes, 'scale'))
            self.raga_layout.addWidget(show_on_shared)
        
        self.raga_layout.addStretch()

    def _create_arabic_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)

        self.maqam_search_list = SearchFilterList(list(ARABIC_MAQAMS.keys()))
        self.maqam_search_list.setMaximumWidth(300)
        self.maqam_search_list.selectionChanged.connect(self._update_maqam_display)
        layout.addWidget(self.maqam_search_list)

        right = QScrollArea()
        right.setWidgetResizable(True)
        self.maqam_content = QWidget()
        self.maqam_layout = QVBoxLayout(self.maqam_content)
        self.maqam_layout.setSpacing(10)
        right.setWidget(self.maqam_content)
        layout.addWidget(right, 1)

        self._update_maqam_display("Maqam Rast")
        return widget

    def _update_maqam_display(self, maqam_name):
        if maqam_name not in ARABIC_MAQAMS:
            return
        while self.maqam_layout.count():
            item = self.maqam_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for w in self._create_raga_info(maqam_name, ARABIC_MAQAMS[maqam_name], False):
            self.maqam_layout.addWidget(w)
        
        # Add "Show on Shared Piano" button for maqams with notes data
        maqam_info = ARABIC_MAQAMS[maqam_name]
        maqam_notes = maqam_info.get('notes', [])
        playable = [n for n in maqam_notes if n in NOTE_NAMES]
        if playable:
            show_on_shared = QPushButton("Show on Shared Piano")
            show_on_shared.setFont(QFont('Segoe UI', 10, QFont.Bold))
            show_on_shared.setStyleSheet("""
                QPushButton { padding: 6px 16px; border: 1px solid #e67e22; border-radius: 12px;
                              background: #e67e22; color: white; }
                QPushButton:hover { background: #d35400; }
            """)
            show_on_shared.clicked.connect(lambda checked, notes=playable: self.eastern_piano.highlight_notes(notes, 'scale'))
            self.maqam_layout.addWidget(show_on_shared)
        
        self.maqam_layout.addStretch()

    def _create_scale_tab_content(self, scales_dict, extra_fields=None):
        """Generic scale tab creator for Chinese, Japanese, Korean, Indonesian."""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        colors = ["#e74c3c", "#3498db", "#2ecc71", "#e67e22", "#9b59b6", "#1abc9c", "#f39c12", "#e84393"]

        for i, (name, info) in enumerate(scales_dict.items()):
            color = colors[i % len(colors)]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 15px; margin: 5px 0; }}")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(15, 12, 15, 12)

            name_l = QLabel(name)
            name_l.setFont(QFont('Segoe UI', 14, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            cl.addWidget(name_l)

            if 'intervals' in info and 'notes' in info:
                notes_l = QLabel(f"Notes: {' - '.join(info['notes'])}")
                notes_l.setFont(QFont('Segoe UI', 12))
                notes_l.setStyleSheet("color: #2c3e50;")
                cl.addWidget(notes_l)

                # Highlight on piano button
                scale_notes = info['notes']
                def _highlight_on_piano(notes=scale_notes):
                    playable = [n for n in notes if n in NOTE_NAMES]
                    if playable:
                        self.eastern_piano.highlight_notes(playable, 'scale')
                piano_btn = QPushButton("Show on Piano")
                piano_btn.setFont(QFont('Segoe UI', 9, QFont.Bold))
                piano_btn.setStyleSheet("""
                    QPushButton { padding: 4px 12px; border: 1px solid #3498db; border-radius: 10px;
                                  background: #3498db; color: white; }
                    QPushButton:hover { background: #2980b9; }
                """)
                piano_btn.clicked.connect(_highlight_on_piano)
                piano_row = QHBoxLayout()
                piano_row.addStretch()
                piano_row.addWidget(piano_btn)
                piano_row.addStretch()
                cl.addLayout(piano_row)

            mood_l = QLabel(f"Mood: {info['mood']}")
            mood_l.setFont(QFont('Segoe UI', 11))
            mood_l.setStyleSheet("color: #e67e22;")
            cl.addWidget(mood_l)

            # Extra fields
            if extra_fields:
                for field_key, label_text in extra_fields:
                    if field_key in info:
                        fl = QLabel(f"{label_text}: {info[field_key]}")
                        fl.setFont(QFont('Segoe UI', 10))
                        fl.setStyleSheet("color: #555;")
                        cl.addWidget(fl)

            desc_l = QLabel(info['description'])
            desc_l.setWordWrap(True)
            desc_l.setFont(QFont('Segoe UI', 10))
            desc_l.setStyleSheet("color: #555; line-height: 1.6; margin-top: 5px;")
            cl.addWidget(desc_l)

            if 'techniques' in info:
                tech_l = QLabel("Techniques: " + ", ".join(info['techniques']))
                tech_l.setWordWrap(True)
                tech_l.setFont(QFont('Segoe UI', 10, QFont.Bold))
                tech_l.setStyleSheet("color: #2980b9; margin-top: 5px;")
                cl.addWidget(tech_l)

            if 'instruments' in info:
                inst_l = QLabel("Instruments: " + ", ".join(info['instruments']))
                inst_l.setWordWrap(True)
                inst_l.setFont(QFont('Segoe UI', 10))
                inst_l.setStyleSheet("color: #8e44ad; margin-top: 3px;")
                cl.addWidget(inst_l)

            layout.addWidget(card)

        layout.addStretch()
        scroll.setWidget(content)
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        return widget

    def _create_chinese_tab(self):
        return self._create_scale_tab_content(CHINESE_SCALES, [('element', 'Element'), ('season', 'Season'), ('usage', 'Usage')])

    def _create_japanese_tab(self):
        return self._create_scale_tab_content(JAPANESE_SCALES, [('usage', 'Usage')])

    def _create_korean_tab(self):
        desc = QLabel("Korean traditional music (gugak) uses three main modes (jo) that express the uniquely Korean concept of 'han' (deep bittersweet emotion), 'jeong' (warm affection), and joy.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        widget = self._create_scale_tab_content(KOREAN_SCALES, [('instruments', 'Key Instruments')])
        # Prepend description
        scroll_content = widget.findChild(QScrollArea).widget()
        if scroll_content:
            scroll_content.layout().insertWidget(0, desc)
        return widget

    def _create_persian_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        desc = QLabel("Persian dastgahs are the modal system of Iranian classical music. Unlike the Arabic maqam system, there are 7 primary dastgahs plus numerous subsidiary \"avaz\" modes. Each dastgah has its own characteristic melodic fragments (gusheh), cadential patterns (forud), and emotional territory. The Persian tradition emphasizes vocal music (avaz) and poetry.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        left_layout.addWidget(desc)

        dastgah_list = SearchFilterList(list(PERSIAN_DASTGAHS.keys()))
        dastgah_list.setMaximumHeight(400)
        dastgah_list.selectionChanged.connect(lambda name: self._show_persian_info(name, right_scroll))
        left_layout.addWidget(dastgah_list)
        left_layout.addStretch()
        left_panel.setMaximumWidth(340)
        layout.addWidget(left_panel)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_content = QWidget()
        right_content.setLayout(QVBoxLayout(right_content))
        right_scroll.setWidget(right_content)
        layout.addWidget(right_scroll, 1)

        dastgah_list.list_widget.setCurrentRow(0)
        self._show_persian_info(list(PERSIAN_DASTGAHS.keys())[0], right_scroll)
        return widget

    def _show_persian_info(self, name, scroll):
        if name not in PERSIAN_DASTGAHS:
            return
        info = PERSIAN_DASTGAHS[name]
        content = scroll.widget()
        while content.layout().count():
            item = content.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        widgets = []

        name_label = QLabel(name)
        name_label.setFont(QFont('Segoe UI', 22, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        widgets.append(name_label)

        if 'notes' in info:
            notes_frame = QFrame()
            notes_frame.setStyleSheet("background: #f8f9fa; border-radius: 10px; padding: 10px;")
            nl = QHBoxLayout(notes_frame)
            for note in info['notes']:
                badge = QLabel(note)
                badge.setAlignment(Qt.AlignCenter)
                bg = "#e67e22" if 'k' in note or '~' in note or 'E' in note else "#3498db"
                badge.setStyleSheet(f"background: {bg}; color: white; border-radius: 6px; padding: 5px 10px; font-weight: bold; font-size: 13px; margin: 2px;")
                badge.setFixedSize(45, 30)
                nl.addWidget(badge)
            widgets.append(notes_frame)

        cards = [
            ("Mood", info['mood'], "#e67e22"),
            ("Region", info.get('region', ''), "#3498db"),
            ("Western Equivalent", info.get('equivalent_western', ''), "#1abc9c"),
        ]
        for title, content_text, color in cards:
            widgets.append(InfoCard(title, content_text, color))

        desc = QLabel(info['description'])
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #555; line-height: 1.7; margin-top: 10px; padding: 15px; background: white; border-radius: 10px; border: 1px solid #e8ecf0;")
        widgets.append(desc)

        if 'famous_pieces' in info:
            rec = QLabel("Famous Pieces: " + ", ".join(info['famous_pieces']))
            rec.setWordWrap(True)
            rec.setFont(QFont('Segoe UI', 10))
            rec.setStyleSheet("color: #8e44ad; margin-top: 8px;")
            widgets.append(rec)

        if 'instruments' in info:
            inst = QLabel("Key Instruments: " + ", ".join(info['instruments']))
            inst.setWordWrap(True)
            inst.setFont(QFont('Segoe UI', 10))
            inst.setStyleSheet("color: #16a085; margin-top: 5px; background: #eafaf1; padding: 8px; border-radius: 6px;")
            widgets.append(inst)

        # Piano with playable western notes
        playable = [n for n in info.get('notes', []) if n in NOTE_NAMES]
        if playable:
            piano = PianoWidget(3, 2)
            piano.highlight_notes(playable, 'scale')
            widgets.append(piano)

            play_btn = PlayButton("Play Western Approximation")
            play_btn.clicked.connect(lambda checked, notes=playable: audio_engine.play_sequence([(n, 4) for n in notes] + [(notes[0], 4)], interval_ms=400))
            widgets.append(play_btn)

        for w in widgets:
            content.layout().addWidget(w)
        content.layout().addStretch()

    def _create_carnatic_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        desc = QLabel("Carnatic music is the classical music tradition of South India, distinct from the Hindustani (North Indian) tradition. Its foundation is the 72 Melakarta ragas (parent scales) and their derived janya ragas. Carnatic music emphasizes composed works (kritis, varnams) and structured improvisation (alapana, kalpanaswaram, neraval, thanam) within a tala (rhythmic cycle).")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        left_layout.addWidget(desc)

        raga_list = SearchFilterList(list(CARNATIC_RAGAS.keys()))
        raga_list.setMaximumHeight(400)
        raga_list.selectionChanged.connect(lambda name: self._show_carnatic_info(name, right_scroll))
        left_layout.addWidget(raga_list)
        left_layout.addStretch()
        left_panel.setMaximumWidth(340)
        layout.addWidget(left_panel)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_content = QWidget()
        right_content.setLayout(QVBoxLayout(right_content))
        right_scroll.setWidget(right_content)
        layout.addWidget(right_scroll, 1)

        raga_list.list_widget.setCurrentRow(0)
        self._show_carnatic_info(list(CARNATIC_RAGAS.keys())[0], right_scroll)
        return widget

    def _show_carnatic_info(self, name, scroll):
        if name not in CARNATIC_RAGAS:
            return
        info = CARNATIC_RAGAS[name]
        content = scroll.widget()
        while content.layout().count():
            item = content.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        widgets = []

        name_label = QLabel(name)
        name_label.setFont(QFont('Segoe UI', 22, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        widgets.append(name_label)

        # Carnatic swara notation
        if 'notes' in info:
            notes_frame = QFrame()
            notes_frame.setStyleSheet("background: #fdf2e9; border-radius: 10px; padding: 10px;")
            nl = QHBoxLayout(notes_frame)
            for note in info['notes']:
                badge = QLabel(note)
                badge.setAlignment(Qt.AlignCenter)
                bg = "#e67e22"
                badge.setStyleSheet(f"background: {bg}; color: white; border-radius: 6px; padding: 5px 8px; font-weight: bold; font-size: 12px; margin: 2px;")
                badge.setFixedSize(45, 30)
                nl.addWidget(badge)
            widgets.append(notes_frame)

        # Western equivalent notes
        if 'western_notes' in info:
            wn_frame = QFrame()
            wn_frame.setStyleSheet("background: #eaf2f8; border-radius: 10px; padding: 10px;")
            wl = QHBoxLayout(wn_frame)
            for note in info['western_notes']:
                badge = QLabel(note)
                badge.setAlignment(Qt.AlignCenter)
                badge.setStyleSheet(f"background: #3498db; color: white; border-radius: 6px; padding: 5px 8px; font-weight: bold; font-size: 12px; margin: 2px;")
                badge.setFixedSize(42, 30)
                wl.addWidget(badge)
            widgets.append(wn_frame)

        cards = [
            ("Melakarta", info.get('melakarta', ''), "#9b59b6"),
            ("Mood / Rasa", info['mood'], "#e67e22"),
            ("Performance Time", info.get('time', ''), "#2ecc71"),
            ("Western Equivalent", info.get('equivalent_western', ''), "#1abc9c"),
        ]
        for title, content_text, color in cards:
            if content_text:
                widgets.append(InfoCard(title, content_text, color))

        desc = QLabel(info['description'])
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #555; line-height: 1.7; margin-top: 10px; padding: 15px; background: white; border-radius: 10px; border: 1px solid #e8ecf0;")
        widgets.append(desc)

        if 'famous_pieces' in info:
            rec = QLabel("Famous Compositions: " + ", ".join(info['famous_pieces']))
            rec.setWordWrap(True)
            rec.setFont(QFont('Segoe UI', 10))
            rec.setStyleSheet("color: #8e44ad; margin-top: 8px;")
            widgets.append(rec)

        if 'instruments' in info:
            inst = QLabel("Key Instruments: " + ", ".join(info['instruments']))
            inst.setWordWrap(True)
            inst.setFont(QFont('Segoe UI', 10))
            inst.setStyleSheet("color: #16a085; margin-top: 5px; background: #eafaf1; padding: 8px; border-radius: 6px;")
            widgets.append(inst)

        # Piano with playable western notes
        playable = [n for n in info.get('western_notes', []) if n in NOTE_NAMES]
        if playable:
            piano = PianoWidget(3, 2)
            piano.highlight_notes(playable, 'scale')
            widgets.append(piano)

            play_btn = PlayButton("Play Scale")
            play_btn.clicked.connect(lambda checked, notes=playable: audio_engine.play_sequence([(n, 4) for n in notes] + [(notes[0], 4)], interval_ms=400))
            widgets.append(play_btn)

        for w in widgets:
            content.layout().addWidget(w)
        content.layout().addStretch()

    def _create_indonesian_tab(self):
        desc = QLabel("Indonesian gamelan music uses tuning systems (laras) that divide the octave differently from Western equal temperament. Slendro and Pelog are the two primary tuning systems, creating the characteristic ethereal sound of Indonesian music.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        widget = self._create_scale_tab_content(INDONESIAN_SCALES, [('instruments', 'Key Instruments'), ('techniques', 'Key Techniques')])
        scroll_content = widget.findChild(QScrollArea).widget()
        if scroll_content:
            scroll_content.layout().insertWidget(0, desc)
        return widget

    def _create_turkish_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        desc = QLabel("Turkish classical music uses a sophisticated makam system with unique comma divisions (Arel-Ezgi-Uzdilek system). Turkish makams differ subtly from Arabic maqams in their microtonal treatment and melodic development (semai, pesrev, sarki forms).")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        colors = ["#e74c3c", "#3498db", "#2ecc71", "#e67e22"]
        for i, (name, info) in enumerate(TURKISH_MAKAMS.items()):
            color = colors[i % len(colors)]
            card = InfoCard(name, "", color)
            cl = card.layout()
            mood_l = QLabel(f"Mood: {info['mood']}")
            mood_l.setFont(QFont('Segoe UI', 11))
            mood_l.setStyleSheet("color: #555;")
            cl.addWidget(mood_l)
            desc_l = QLabel(info['description'])
            desc_l.setWordWrap(True)
            desc_l.setFont(QFont('Segoe UI', 10))
            desc_l.setStyleSheet("color: #555; margin-top: 5px;")
            cl.addWidget(desc_l)
            inst_l = QLabel(f"Instruments: {', '.join(info['instruments'])}")
            inst_l.setFont(QFont('Segoe UI', 10))
            inst_l.setStyleSheet("color: #3498db; margin-top: 3px;")
            cl.addWidget(inst_l)

            # Check for playable notes
            makam_notes = info.get('notes', [])
            playable = [n for n in makam_notes if n in NOTE_NAMES] if makam_notes else []
            if playable:
                def _show_turkish_on_piano(notes=playable):
                    self.eastern_piano.highlight_notes(notes, 'scale')
                show_piano_btn = QPushButton("Show on Piano")
                show_piano_btn.setFont(QFont('Segoe UI', 9, QFont.Bold))
                show_piano_btn.setStyleSheet("""
                    QPushButton { padding: 4px 12px; border: 1px solid #3498db; border-radius: 10px;
                                  background: #3498db; color: white; }
                    QPushButton:hover { background: #2980b9; }
                """)
                show_piano_btn.clicked.connect(_show_turkish_on_piano)
                piano_row = QHBoxLayout()
                piano_row.addStretch()
                piano_row.addWidget(show_piano_btn)
                piano_row.addStretch()
                cl.addLayout(piano_row)
            elif 'notes' not in info:
                # No notes data - show a note about microtones
                micro_l = QLabel("(Microtonal - uses Turkish comma divisions beyond Western 12-TET)")
                micro_l.setFont(QFont('Segoe UI', 9))
                micro_l.setStyleSheet("color: #95a5a6; font-style: italic; margin-top: 5px;")
                cl.addWidget(micro_l)

            layout.addWidget(card)

        layout.addStretch()
        scroll.setWidget(content)
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        return widget


# ============================================================
# WORLD MODULE
# ============================================================
class WorldModule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(10)

        title = SectionTitle("World Music Theory", "Explore traditions from Africa, Latin America, the Balkans, and more")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setFont(QFont('Segoe UI', 11))
        tabs.addTab(self._create_tradition_tab(AFRICAN_MUSIC, "African music traditions are characterized by complex polyrhythms, call-and-response patterns, and communal music-making. Rhythm is often considered more central than melody or harmony."), "African")
        tabs.addTab(self._create_latin_tab(), "Latin American")
        tabs.addTab(self._create_tradition_tab(CELTIC_MUSIC, "Celtic music is primarily modal, using Dorian, Mixolydian, Aeolian, and Ionian modes. Ornamentation and melodic variation are key expressive elements in Irish, Scottish, and Breton traditions."), "Celtic")
        tabs.addTab(self._create_tradition_tab(BALKAN_MUSIC, "Balkan music is famous for its asymmetric odd meters (7/8, 9/8, 11/8) and modal scales shared with Turkish and Arabic music through centuries of Ottoman influence. These rhythms create infectious, driving grooves."), "Balkan")
        tabs.addTab(self._create_native_american_tab(), "Native American")
        tabs.addTab(self._create_comparison_tab(), "Cross-Cultural Comparison")
        tabs.addTab(self._create_instruments_tab(), "Instruments")

        # Shared piano for World scales
        self.world_piano = PianoWidget(start_octave=3, num_octaves=2)
        self.world_piano.show_labels(True)
        piano_container = QFrame()
        piano_container.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 10px; padding: 5px; }")
        pc_layout = QVBoxLayout(piano_container)
        pc_layout.setContentsMargins(10, 5, 10, 5)
        
        piano_header = QHBoxLayout()
        piano_label = QLabel("Piano (approximate - some scales use microtones)")
        piano_label.setFont(QFont('Segoe UI', 10))
        piano_label.setStyleSheet("color: #7f8c8d;")
        piano_header.addWidget(piano_label)
        
        self.world_play_btn = PlayButton("Play Scale Ascending")
        self.world_play_btn.clicked.connect(self._play_world_scale)
        piano_header.addWidget(self.world_play_btn)
        
        self.world_clear_btn = QPushButton("Clear")
        self.world_clear_btn.setFont(QFont('Segoe UI', 10))
        self.world_clear_btn.setStyleSheet("""
            QPushButton { padding: 6px 14px; border: 1px solid #dce1e3; border-radius: 12px;
                          background: white; color: #7f8c8d; }
            QPushButton:hover { background: #f5f6fa; }
        """)
        self.world_clear_btn.clicked.connect(lambda: self.world_piano.clear_highlights())
        piano_header.addWidget(self.world_clear_btn)
        piano_header.addStretch()
        pc_layout.addLayout(piano_header)
        pc_layout.addWidget(self.world_piano)
        
        layout.addWidget(tabs)
        layout.addWidget(piano_container)

    def _play_world_scale(self):
        """Play the currently highlighted world scale notes."""
        notes = self.world_piano.get_current_scale_with_octaves(4)
        if notes:
            audio_engine.play_sequence(notes, interval_ms=400)

    def _create_tradition_tab(self, data, intro_text):
        widget = QWidget()
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        desc = QLabel(intro_text)
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        colors = ["#e74c3c", "#3498db", "#2ecc71", "#e67e22", "#9b59b6"]
        for i, (name, info) in enumerate(data.items()):
            color = colors[i % len(colors)]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-left: 4px solid {color}; border-radius: 10px; padding: 15px; margin: 5px 0; }}")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(15, 12, 15, 12)

            name_l = QLabel(name)
            name_l.setFont(QFont('Segoe UI', 14, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            cl.addWidget(name_l)

            if 'mood' in info:
                mood_l = QLabel(f"Character: {info['mood']}")
                mood_l.setFont(QFont('Segoe UI', 11))
                mood_l.setStyleSheet("color: #555;")
                cl.addWidget(mood_l)

            desc_l = QLabel(info['description'])
            desc_l.setWordWrap(True)
            desc_l.setFont(QFont('Segoe UI', 11))
            desc_l.setStyleSheet("color: #555; line-height: 1.6; margin-top: 8px;")
            cl.addWidget(desc_l)

            if 'beats_pattern' in info:
                bp_l = QLabel(f"Beat pattern: {info['beats_pattern']}")
                bp_l.setFont(QFont('Segoe UI', 10))
                bp_l.setStyleSheet("color: #c0392b; margin-top: 5px;")
                cl.addWidget(bp_l)

            if 'techniques' in info:
                tech_l = QLabel("Key Techniques: " + ", ".join(info['techniques']))
                tech_l.setWordWrap(True)
                tech_l.setFont(QFont('Segoe UI', 10, QFont.Bold))
                tech_l.setStyleSheet("color: #2980b9; margin-top: 8px;")
                cl.addWidget(tech_l)

            if 'instruments' in info:
                inst_l = QLabel("Instruments: " + ", ".join(info['instruments']))
                inst_l.setWordWrap(True)
                inst_l.setFont(QFont('Segoe UI', 10))
                inst_l.setStyleSheet("color: #8e44ad; margin-top: 5px;")
                cl.addWidget(inst_l)

            # Highlight on world piano button
            if 'notes' in info:
                scale_notes = info['notes']
                def _highlight_on_world_piano(notes=scale_notes):
                    playable = [n for n in notes if n in NOTE_NAMES]
                    if playable:
                        self.world_piano.highlight_notes(playable, 'scale')
                piano_btn = QPushButton("Show on Piano")
                piano_btn.setFont(QFont('Segoe UI', 9, QFont.Bold))
                piano_btn.setStyleSheet("""
                    QPushButton { padding: 4px 12px; border: 1px solid #3498db; border-radius: 10px;
                                  background: #3498db; color: white; }
                    QPushButton:hover { background: #2980b9; }
                """)
                piano_btn.clicked.connect(_highlight_on_world_piano)
                piano_row = QHBoxLayout()
                piano_row.addStretch()
                piano_row.addWidget(piano_btn)
                piano_row.addStretch()
                cl.addLayout(piano_row)

            layout.addWidget(card)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)
        return widget

    def _create_instruments_tab(self):
        from music_engine import INSTRUMENT_ENCYCLOPEDIA
        widget = QWidget()
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        desc = QLabel("Explore musical instruments from around the world. Each instrument embodies the musical aesthetics, materials, and cultural values of its tradition.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        colors = {"Keyboard": "#3498db", "String": "#e74c3c", "Percussion": "#e67e22", "Wind": "#2ecc71", "Ensemble": "#9b59b6"}
        for name, info in INSTRUMENT_ENCYCLOPEDIA.items():
            itype = info['type']
            color = colors.get(itype, "#7f8c8d")
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-left: 4px solid {color}; border-radius: 10px; padding: 15px; margin: 5px 0; }}")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(15, 12, 15, 12)

            header_row = QHBoxLayout()
            name_l = QLabel(name)
            name_l.setFont(QFont('Segoe UI', 14, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            header_row.addWidget(name_l)

            type_badge = QLabel(itype)
            type_badge.setFont(QFont('Segoe UI', 9, QFont.Bold))
            type_badge.setStyleSheet(f"color: white; background: {color}; border-radius: 8px; padding: 2px 8px;")
            header_row.addWidget(type_badge)
            header_row.addStretch()
            cl.addLayout(header_row)

            detail_fields = [
                ("Origin", info.get('origin', ''), "#2c3e50"),
                ("Range", info.get('range', ''), "#555"),
                ("Classification", info.get('classification', ''), "#8e44ad"),
            ]
            for field_label, field_val, field_color in detail_fields:
                if field_val:
                    row = QLabel(f"<b>{field_label}:</b> {field_val}")
                    row.setFont(QFont('Segoe UI', 10))
                    row.setStyleSheet(f"color: {field_color}; padding: 1px 0;")
                    cl.addWidget(row)

            desc_l = QLabel(info['description'])
            desc_l.setWordWrap(True)
            desc_l.setFont(QFont('Segoe UI', 10))
            desc_l.setStyleSheet("color: #555; line-height: 1.6; margin-top: 5px;")
            cl.addWidget(desc_l)

            layout.addWidget(card)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)
        return widget

    def _create_latin_tab(self):
        widget = QWidget()
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        desc = QLabel("Latin American music is a rich fusion of Indigenous, African, and European musical traditions. Each region has developed unique harmonic, rhythmic, and melodic systems that have influenced global music.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        colors = ["#e74c3c", "#2ecc71", "#3498db", "#e67e22", "#9b59b6"]
        for i, (name, info) in enumerate(LATIN_AMERICAN_MUSIC.items()):
            color = colors[i % len(colors)]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-left: 4px solid {color}; border-radius: 10px; padding: 15px; margin: 5px 0; }}")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(15, 12, 15, 12)

            name_l = QLabel(name)
            name_l.setFont(QFont('Segoe UI', 14, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            cl.addWidget(name_l)

            mood_l = QLabel(f"Character: {info['mood']}")
            mood_l.setFont(QFont('Segoe UI', 11))
            mood_l.setStyleSheet("color: #555;")
            cl.addWidget(mood_l)

            desc_l = QLabel(info['description'])
            desc_l.setWordWrap(True)
            desc_l.setFont(QFont('Segoe UI', 11))
            desc_l.setStyleSheet("color: #555; line-height: 1.6; margin-top: 8px;")
            cl.addWidget(desc_l)

            tech_l = QLabel("Techniques: " + ", ".join(info['techniques']))
            tech_l.setWordWrap(True)
            tech_l.setFont(QFont('Segoe UI', 10, QFont.Bold))
            tech_l.setStyleSheet("color: #2980b9; margin-top: 5px;")
            cl.addWidget(tech_l)

            inst_l = QLabel("Instruments: " + ", ".join(info['instruments']))
            inst_l.setWordWrap(True)
            inst_l.setFont(QFont('Segoe UI', 10))
            inst_l.setStyleSheet("color: #8e44ad; margin-top: 3px;")
            cl.addWidget(inst_l)

            if 'clave_pattern' in info:
                clave_l = QLabel(f"Clave: {info['clave_pattern']}")
                clave_l.setFont(QFont('Segoe UI', 10))
                clave_l.setStyleSheet("color: #c0392b; margin-top: 3px; font-family: monospace;")
                cl.addWidget(clave_l)

            layout.addWidget(card)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)
        return widget

    def _create_native_american_tab(self):
        widget = QWidget()
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: list
        list_panel = QWidget()
        list_layout = QVBoxLayout(list_panel)
        list_layout.setContentsMargins(5, 5, 5, 5)
        
        search = QLineEdit()
        search.setPlaceholderText("Search Native American traditions...")
        search.setFont(QFont('Segoe UI', 11))
        search.textChanged.connect(lambda text: self._filter_na_list(text))
        list_layout.addWidget(search)
        
        self.na_list = QListWidget()
        self.na_list.setFont(QFont('Segoe UI', 11))
        na_colors = ["#8B4513", "#D2691E", "#CD853F", "#A0522D", "#DEB887", "#F4A460", "#DAA520", "#B8860B", "#BC8F8F"]
        for i, name in enumerate(NATIVE_AMERICAN_MUSIC.keys()):
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, name)
            self.na_list.addItem(item)
        self.na_list.currentRowChanged.connect(self._on_na_selected)
        list_layout.addWidget(self.na_list)
        
        splitter.addWidget(list_panel)
        
        # Right: detail + piano
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        self.na_detail = QWidget()
        self.na_detail_layout = QVBoxLayout(self.na_detail)
        self.na_detail_layout.setSpacing(10)
        
        welcome = QLabel("Select a Native American music tradition to explore.")
        welcome.setFont(QFont('Segoe UI', 14))
        welcome.setStyleSheet("color: #7f8c8d; padding: 40px;")
        welcome.setAlignment(Qt.AlignCenter)
        self.na_detail_layout.addWidget(welcome)
        
        # Piano for Native American tab
        self.na_piano = PianoWidget(start_octave=3, num_octaves=2)
        self.na_piano.show_labels(True)
        self.na_piano_frame = QFrame()
        self.na_piano_frame.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 10px; padding: 5px; }")
        np_layout = QVBoxLayout(self.na_piano_frame)
        np_layout.setContentsMargins(10, 5, 10, 5)
        
        na_piano_header = QHBoxLayout()
        na_piano_label = QLabel("Piano (approximate)")
        na_piano_label.setFont(QFont('Segoe UI', 10))
        na_piano_label.setStyleSheet("color: #7f8c8d;")
        na_piano_header.addWidget(na_piano_label)
        
        self.na_play_btn = PlayButton("Play Scale")
        self.na_play_btn.clicked.connect(self._play_na_scale)
        na_piano_header.addWidget(self.na_play_btn)
        
        na_clear_btn = QPushButton("Clear")
        na_clear_btn.setFont(QFont('Segoe UI', 10))
        na_clear_btn.setStyleSheet("""
            QPushButton { padding: 6px 14px; border: 1px solid #dce1e3; border-radius: 12px;
                          background: white; color: #7f8c8d; }
            QPushButton:hover { background: #f5f6fa; }
        """)
        na_clear_btn.clicked.connect(lambda: self.na_piano.clear_highlights())
        na_piano_header.addWidget(na_clear_btn)
        na_piano_header.addStretch()
        np_layout.addLayout(na_piano_header)
        np_layout.addWidget(self.na_piano)
        self.na_detail_layout.addWidget(self.na_piano_frame)
        
        self.na_detail_layout.addStretch()
        right_scroll.setWidget(self.na_detail)
        splitter.addWidget(right_scroll)
        splitter.setSizes([300, 700])
        
        outer.addWidget(splitter)
        return widget

    def _filter_na_list(self, text):
        """Filter Native American list items."""
        for i in range(self.na_list.count()):
            item = self.na_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def _on_na_selected(self, row):
        """Handle Native American tradition selection."""
        if row < 0:
            return
        name = self.na_list.item(row).data(Qt.UserRole)
        if name not in NATIVE_AMERICAN_MUSIC:
            return
        info = NATIVE_AMERICAN_MUSIC[name]
        
        # Clear existing detail widgets (keep piano frame)
        while self.na_detail_layout.count() > 0:
            item = self.na_detail_layout.takeAt(0)
            w = item.widget()
            if w and w != self.na_piano_frame:
                w.deleteLater()
        
        # Title
        title = QLabel(name)
        title.setFont(QFont('Segoe UI', 22, QFont.Bold))
        title.setStyleSheet("color: #8B4513;")
        self.na_detail_layout.insertWidget(0, title)
        
        # Notes
        if 'notes' in info and info['notes']:
            notes_frame = QFrame()
            notes_frame.setStyleSheet("background: #f8f9fa; border-radius: 10px; padding: 10px;")
            nl = QHBoxLayout(notes_frame)
            for note in info['notes']:
                badge = QLabel(note)
                badge.setAlignment(Qt.AlignCenter)
                badge.setStyleSheet("background: #D2691E; color: white; border-radius: 6px; padding: 5px 10px; font-weight: bold; font-size: 13px; margin: 2px;")
                badge.setFixedSize(45, 30)
                nl.addWidget(badge)
            self.na_detail_layout.insertWidget(1, notes_frame)
            
            # Highlight on piano
            playable_notes = []
            for note in info['notes']:
                clean = note.replace('~', '').replace('#', '').replace('b', '')
                if clean in NOTE_NAMES:
                    playable_notes.append(clean)
            self.na_piano.highlight_notes(playable_notes, 'scale')
        
        # Info cards
        cards = []
        if 'mood' in info:
            cards.append(("Character / Mood", info['mood'], "#D2691E"))
        if 'techniques' in info:
            cards.append(("Key Techniques", ", ".join(info['techniques']), "#2ecc71"))
        if 'instruments' in info:
            cards.append(("Traditional Instruments", ", ".join(info['instruments']), "#8e44ad"))
        
        for title_text, content, color in cards:
            card = InfoCard(title_text, content, color)
            self.na_detail_layout.addWidget(card)
        
        # Description
        desc = QLabel(info['description'])
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #555; line-height: 1.7; margin-top: 10px; padding: 15px; background: white; border-radius: 10px; border: 1px solid #e8ecf0;")
        self.na_detail_layout.addWidget(desc)
        
        # Re-add piano frame
        self.na_detail_layout.addWidget(self.na_piano_frame)
        self.na_detail_layout.addStretch()

    def _play_na_scale(self):
        """Play the currently highlighted Native American scale."""
        notes = self.na_piano.get_current_scale_with_octaves(4)
        if notes:
            audio_engine.play_sequence(notes, interval_ms=500)

    def _create_comparison_tab(self):
        widget = QWidget()
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        title = QLabel("Cross-Cultural Comparison")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        desc = QLabel("Music theory concepts appear across many cultures, often with fascinating parallels. These comparisons show how different traditions approach similar musical ideas.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        layout.addWidget(desc)

        comparisons = [
            {
                "title": "Pentatonic Scales Across Cultures",
                "comparisons": [
                    ("Western", "Major Pentatonic: C-D-E-G-A", "#3498db"),
                    ("Chinese", "Gong mode: C-D-E-G-A (Earth element)", "#e74c3c"),
                    ("Korean", "Pyeongjo: C-D-E-F-G-A-B (major-like)", "#1abc9c"),
                    ("African (Akan)", "Akan Pentatonic: C-Eb-F-G-Bb", "#e67e22"),
                    ("Andean", "Andean Pentatonic: C-Eb-F-G-Bb", "#2ecc71"),
                    ("Japanese", "In scale: C-Db-F-G-Ab (minor 2nd)", "#9b59b6"),
                    ("Celtic", "Often Dorian/Mixolydian pentatonic", "#27ae60"),
                ],
                "note": "The pentatonic scale is arguably the most universal musical structure, found in virtually every culture worldwide. Despite sharing only 5 notes, each culture creates vastly different music through rhythm, ornamentation, and phrasing.",
            },
            {
                "title": "Minor / Sad-Sounding Scales",
                "comparisons": [
                    ("Western", "Natural Minor (Aeolian): W-H-W-W-H-W-W", "#3498db"),
                    ("Indian", "Raga Bhairavi: all komal (flat) notes except M", "#e74c3c"),
                    ("Arabic", "Maqam Kurd: identical to natural minor", "#e67e22"),
                    ("Japanese", "In Scale: C-Db-F-G-Ab (dark, ancient)", "#9b59b6"),
                    ("Chinese", "Yu (羽) mode: melancholic, winter element", "#e74c3c"),
                    ("Korean", "Gyeongmyeongjo: 'han' - bittersweet sorrow", "#1abc9c"),
                    ("Celtic", "Aeolian mode: laments and slow airs", "#27ae60"),
                ],
                "note": "Every culture has developed scales that convey sadness or introspection, though the specific intervals differ. The universal human experience of melancholy finds expression through different combinations of intervals.",
            },
            {
                "title": "Microtonal and Non-Equal Temperament Systems",
                "comparisons": [
                    ("Arabic", "Quarter tones (24 notes per octave)", "#e67e22"),
                    ("Indian", "22 shrutis (microtones) per octave", "#e74c3c"),
                    ("Turkish", "Unique comma divisions (Arel-Ezgi-Uzdilek)", "#c0392b"),
                    ("Indonesian", "Slendro: 5 equal divisions (~240 cents each)", "#2ecc71"),
                    ("Indonesian", "Pelog: 7 unequal divisions", "#2ecc71"),
                    ("Western (standard)", "12-tone equal temperament", "#3498db"),
                    ("Western (historical)", "Meantone, well temperament, just intonation", "#3498db"),
                ],
                "note": "While Western music standardized on 12 equal divisions, many traditions use microtones or unequal divisions. These systems create expressive possibilities that are impossible in 12-TET, including notes 'between' the piano keys.",
            },
            {
                "title": "Rhythmic Complexity Across Traditions",
                "comparisons": [
                    ("West African", "Polyrhythms (3:2, 4:3, 6:4), timeline patterns", "#e67e22"),
                    ("Indian", "Tala system: 16, 7, 10, 14 beat cycles with subdivisions", "#e74c3c"),
                    ("Balkan", "Odd meters: 7/8 (2+2+3), 9/8, 11/8", "#9b59b6"),
                    ("Arabic", "Iqa'at: wahda, masmoudi, maqsum, baladi", "#e67e22"),
                    ("Indonesian", "Colotomic structure: gong cycles marking form sections", "#2ecc71"),
                    ("Korean", "Jangdan: jeongganpo notation system", "#1abc9c"),
                    ("Western (modern)", "Expanding beyond 4/4: 5/4, 7/8, 11/8 in progressive music", "#3498db"),
                ],
                "note": "Rhythmic systems vary enormously between cultures. Western music is relatively simple rhythmically compared to West African polyrhythms, Indian talas, or Balkan odd meters. Many non-Western traditions treat rhythm as equal in importance to melody.",
            },
            {
                "title": "Maqam / Raga / Dastgah: Modal Systems Compared",
                "comparisons": [
                    ("Arabic Maqam", "7+ maqam families, quarter tones, iqa'at (rhythmic cycles)", "#e67e22"),
                    ("Indian Raga (Hindustani)", "10+ thaats, 22 shrutis, 7+ jatis, vadi/samvadi system", "#e74c3c"),
                    ("Indian Raga (Carnatic)", "72 melakarta ragas, gamakas, tala system, composed works", "#c0392b"),
                    ("Persian Dastgah", "7 dastgahs + avaz modes, gusheh system, forud (cadences), tahrir", "#2c3e50"),
                    ("Turkish Makam", "200+ makams, Arel-Ezgi-Uzdilek comma system, taksim", "#9b59b6"),
                    ("Western Modes", "7 modes of major scale, 12-TET, functional harmony", "#3498db"),
                    ("Indonesian Pathet", "3 pathets per tuning, colotomic gong cycles, slendro/pelog", "#2ecc71"),
                ],
                "note": "Every major Eastern tradition has a modal system that goes far beyond Western major/minor. These systems define not just which notes to play, but HOW to approach them (ornamentation, microtones, emphasis). The concept of 'maqam' or 'raga' encompasses melody, rhythm, emotion, time of day, and cultural context all at once.",
            },
            {
                "title": "String Instruments Across Cultures",
                "comparisons": [
                    ("India (Sitar)", "Sympathetic strings, jawari bridge buzz, meend (glides)", "#e74c3c"),
                    ("Iran (Tar/Setar)", "Double-course strings, skin membrane, dramatic ornamentation", "#2c3e50"),
                    ("Turkey (Baglama/Saz)", "Fretted long-neck lute, microtonal frets, folk-classical bridge", "#9b59b6"),
                    ("China (Erhu/Guqin)", "2-string bowed lute / 7-string zither, silk strings, sliding pitches", "#e74c3c"),
                    ("Japan (Koto/Shamisen)", "13-string zither / 3-string lute, sawari buzz, bending", "#9b59b6"),
                    ("West Africa (Kora)", "21-string harp-lute, pentatonic tuning, griot tradition", "#e67e22"),
                    ("Celtic (Harp/Fiddle)", "Clarsach (lever harp), ornamental cuts/rolls, drone", "#27ae60"),
                ],
                "note": "String instruments are the primary melodic instruments in most world music traditions. Each culture has developed unique approaches to string instrument design: resonators, sympathetic strings, fret systems, and bowing/plucking techniques that create distinctive timbres and expressive possibilities impossible on Western guitar or violin alone.",
            },
        ]

        for comp in comparisons:
            card = QFrame()
            card.setStyleSheet("QFrame { background: white; border: 2px solid #e8ecf0; border-radius: 12px; padding: 15px; margin: 5px 0; }")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(15, 12, 15, 12)

            t = QLabel(comp['title'])
            t.setFont(QFont('Segoe UI', 13, QFont.Bold))
            t.setStyleSheet("color: #2c3e50;")
            cl.addWidget(t)

            for culture, desc_text, color in comp['comparisons']:
                row = QLabel(f"  <b>{culture}:</b> {desc_text}")
                row.setWordWrap(True)
                row.setFont(QFont('Segoe UI', 10))
                row.setStyleSheet(f"color: #555; padding: 3px 5px; border-left: 3px solid {color}; margin-left: 10px;")
                cl.addWidget(row)

            note = QLabel(comp['note'])
            note.setWordWrap(True)
            font = QFont('Segoe UI', 10)
            font.setItalic(True)
            note.setFont(font)
            note.setStyleSheet("color: #7f8c8d; margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 8px;")
            cl.addWidget(note)

            layout.addWidget(card)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)
        return widget


# ============================================================
# MAIN WINDOW
# ============================================================
class MusicTheoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self._favorites = []
        self.setWindowTitle("Music Theory Explorer - Western | Eastern | World")
        self.setMinimumSize(1100, 750)
        self.resize(1300, 870)
        self._setup_ui()
        self._apply_style()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Navigation bar
        nav_bar = QFrame()
        nav_bar.setFixedHeight(60)
        nav_bar.setStyleSheet("QFrame { background: white; border-bottom: 2px solid #ecf0f1; }")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(20, 8, 20, 8)

        logo = QLabel("Music Theory Explorer")
        logo.setFont(QFont('Segoe UI', 15, QFont.Bold))
        logo.setStyleSheet("color: #2c3e50;")
        nav_layout.addWidget(logo)

        # Audio status indicator
        audio_status = QLabel("Audio: " + ("ON" if audio_engine.is_available else "OFF (install numpy + sounddevice)"))
        audio_status.setFont(QFont('Segoe UI', 9))
        audio_status.setStyleSheet(f"color: {'#27ae60' if audio_engine.is_available else '#e74c3c'}; background: {'#eafaf1' if audio_engine.is_available else '#fdedec'}; padding: 3px 10px; border-radius: 10px;")
        nav_layout.addWidget(audio_status)

        # Wave type selector
        nav_layout.addWidget(QLabel("Sound:"))
        self.wave_combo = QComboBox()
        from piano_widget import WAVE_TYPES
        self.wave_combo.addItems([v for v in WAVE_TYPES.values()])
        self.wave_combo.setFixedWidth(100)
        self.wave_combo.setFont(QFont('Segoe UI', 9))
        self.wave_combo.setStyleSheet("QComboBox { min-width: 80px; font-size: 10px; padding: 3px 6px; }")
        nav_layout.addWidget(self.wave_combo)
        self.wave_combo.currentIndexChanged.connect(self._on_wave_changed)

        # Mute button
        self.mute_btn = QPushButton("Mute" if audio_engine.is_available else "No Audio")
        self.mute_btn.setCheckable(True)
        self.mute_btn.setFont(QFont('Segoe UI', 9, QFont.Bold))
        self.mute_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border: 1px solid #dce1e3; border-radius: 10px;
                          background: white; color: #7f8c8d; }
            QPushButton:checked { background: #e74c3c; color: white; border-color: #e74c3c; }
        """)
        if not audio_engine.is_available:
            self.mute_btn.setEnabled(False)
        self.mute_btn.clicked.connect(self._toggle_mute)
        nav_layout.addWidget(self.mute_btn)

        # Dark mode toggle
        self.dark_mode_btn = QPushButton("Dark Mode")
        self.dark_mode_btn.setCheckable(True)
        self.dark_mode_btn.setFont(QFont('Segoe UI', 9, QFont.Bold))
        self.dark_mode_btn.setStyleSheet("""
            QPushButton { padding: 4px 12px; border: 1px solid #dce1e3; border-radius: 10px;
                          background: white; color: #7f8c8d; }
            QPushButton:checked { background: #2c3e50; color: white; border-color: #2c3e50; }
        """)
        self.dark_mode_btn.clicked.connect(self._toggle_dark_mode)
        nav_layout.addWidget(self.dark_mode_btn)

        nav_layout.addStretch()

        self.nav_buttons = []
        nav_items = [("Western", "western"), ("Eastern", "eastern"), ("World", "world"), ("Symbols", "symbols"), ("Search", "search"), ("Quiz", "quiz")]
        for text, page_id in nav_items:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setFont(QFont('Segoe UI', 11, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty('page_id', page_id)
            btn.clicked.connect(lambda checked, pid=page_id: self._switch_page(pid))
            btn.setStyleSheet("""
                QPushButton { padding: 8px 20px; border: 2px solid transparent; border-radius: 20px;
                              background: transparent; color: #7f8c8d; }
                QPushButton:hover { background: #f0f8ff; color: #3498db; }
                QPushButton:checked { background: #3498db; color: white; border-color: #3498db; }
            """)
            nav_layout.addWidget(btn)
            self.nav_buttons.append((btn, page_id))

        # Favorites button (separate from nav)
        self.fav_btn = QPushButton("Favorites")
        self.fav_btn.setFont(QFont('Segoe UI', 10))
        self.fav_btn.setCursor(Qt.PointingHandCursor)
        self.fav_btn.setStyleSheet("""
            QPushButton { padding: 6px 14px; border: 1px solid #dce1e3; border-radius: 15px;
                          background: #fef9e7; color: #f39c12; font-weight: bold; }
            QPushButton:hover { background: #f9e79f; }
        """)
        self.fav_btn.clicked.connect(self._show_favorites)
        nav_layout.addWidget(self.fav_btn)

        main_layout.addWidget(nav_bar)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.western_page = WesternModule()
        self.stack.addWidget(self.western_page)

        self.eastern_page = EasternModule()
        self.stack.addWidget(self.eastern_page)

        self.world_page = WorldModule()
        self.stack.addWidget(self.world_page)

        self.symbols_page = self._create_symbols_page()
        self.stack.addWidget(self.symbols_page)

        self.search_page = self._create_search_page()
        self.stack.addWidget(self.search_page)

        self.quiz_page = QuizWidget()
        self.stack.addWidget(self.quiz_page)

        self._switch_page('western')

        # Keyboard shortcuts
        QShortcut(QKeySequence('Ctrl+1'), self, lambda: self._switch_page('western'))
        QShortcut(QKeySequence('Ctrl+2'), self, lambda: self._switch_page('eastern'))
        QShortcut(QKeySequence('Ctrl+3'), self, lambda: self._switch_page('world'))
        QShortcut(QKeySequence('Ctrl+4'), self, lambda: self._switch_page('symbols'))
        QShortcut(QKeySequence('Ctrl+5'), self, lambda: self._switch_page('search'))
        QShortcut(QKeySequence('Ctrl+6'), self, lambda: self._switch_page('quiz'))
        QShortcut(QKeySequence('Ctrl+M'), self, self.mute_btn.click)
        QShortcut(QKeySequence('Ctrl+D'), self, self.dark_mode_btn.click)

        self.statusBar().showMessage("Ready - Explore music theory across cultures! (Ctrl+1-5: Switch pages, Ctrl+M: Mute, Ctrl+D: Dark mode)")
        self.statusBar().setStyleSheet("QStatusBar { background: #2c3e50; color: #ecf0f1; padding: 4px 10px; font-size: 12px; }")

    def _toggle_mute(self):
        muted = audio_engine.toggle_mute()
        self.mute_btn.setText("Unmute" if muted else "Mute")

    def _toggle_dark_mode(self):
        if self.dark_mode_btn.isChecked():
            self.setStyleSheet(DARK_STYLE)
            # Update nav bar for dark mode
            for widget in self.findChildren(QWidget):
                if widget.objectName() == "":
                    pass  # Style is inherited
            # Update nav buttons
            for btn, pid in self.nav_buttons:
                btn.setStyleSheet("""
                    QPushButton { padding: 8px 20px; border: 2px solid transparent; border-radius: 20px;
                                  background: transparent; color: #a0a0a0; }
                    QPushButton:hover { background: #0f3460; color: #e94560; }
                    QPushButton:checked { background: #e94560; color: white; border-color: #e94560; }
                """)
            # Update logo
            self.findChildren(QLabel)[0].setStyleSheet("color: #e0e0e0;")
            self.statusBar().setStyleSheet("QStatusBar { background: #16213e; color: #e0e0e0; padding: 4px 10px; font-size: 12px; }")
        else:
            self.setStyleSheet(GLOBAL_STYLE)
            for btn, pid in self.nav_buttons:
                btn.setStyleSheet("""
                    QPushButton { padding: 8px 20px; border: 2px solid transparent; border-radius: 20px;
                                  background: transparent; color: #7f8c8d; }
                    QPushButton:hover { background: #f0f8ff; color: #3498db; }
                    QPushButton:checked { background: #3498db; color: white; border-color: #3498db; }
                """)
            self.findChildren(QLabel)[0].setStyleSheet("color: #2c3e50;")
            self.statusBar().setStyleSheet("QStatusBar { background: #2c3e50; color: #ecf0f1; padding: 4px 10px; font-size: 12px; }")

    def _add_favorite(self, category, name):
        if (category, name) not in self._favorites:
            self._favorites.append((category, name))
            self.statusBar().showMessage(f"Added '{name}' to favorites! ({len(self._favorites)} total)")
            self.fav_btn.setText(f"Favorites ({len(self._favorites)})")

    def _remove_favorite(self, category, name):
        if (category, name) in self._favorites:
            self._favorites.remove((category, name))
            self.statusBar().showMessage(f"Removed '{name}' from favorites")
            self.fav_btn.setText(f"Favorites ({len(self._favorites)})" if self._favorites else "Favorites")
            # If favorites dialog is open, refresh it
            if hasattr(self, '_fav_dialog') and self._fav_dialog.isVisible():
                self._show_favorites()

    def _is_favorite(self, category, name):
        return (category, name) in self._favorites

    def _show_favorites(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout as DLayout, QLabel as DLabel, QPushButton as DButton, QScrollArea as DScroll
        from PySide6.QtCore import Qt as DQt

        if hasattr(self, '_fav_dialog') and self._fav_dialog.isVisible():
            self._fav_dialog.close()

        self._fav_dialog = QDialog(self)
        self._fav_dialog.setWindowTitle(f"Favorites ({len(self._favorites)})")
        self._fav_dialog.resize(500, 600)
        self._fav_dialog.setStyleSheet("""
            QDialog { background: white; }
            QLabel { color: #2c3e50; }
            QPushButton { padding: 8px 16px; border-radius: 15px; font-weight: bold; font-size: 12px; }
        """)

        dlayout = DLayout(self._fav_dialog)
        dlayout.setSpacing(10)
        dlayout.setContentsMargins(20, 20, 20, 20)

        title = DLabel("Your Favorites")
        title.setFont(QFont('Segoe UI', 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        dlayout.addWidget(title)

        scroll = DScroll()
        scroll.setWidgetResizable(True)
        content = QWidget()
        cl = DLayout(content)
        cl.setSpacing(8)

        if not self._favorites:
            empty = DLabel("No favorites yet! Browse scales and traditions, then click the star to save them here.")
            empty.setWordWrap(True)
            empty.setFont(QFont('Segoe UI', 12))
            empty.setStyleSheet("color: #95a5a6; padding: 30px;")
            empty.setAlignment(DQt.AlignCenter)
            cl.addWidget(empty)
        else:
            cat_colors = {"Western": "#3498db", "Eastern": "#9b59b6", "African": "#e67e22", "Native American": "#8B4513", "Latin": "#e74c3c", "Celtic": "#2ecc71", "Balkan": "#1abc9c"}
            for category, name in self._favorites:
                row_w = QWidget()
                rl = QHBoxLayout(row_w)
                rl.setContentsMargins(5, 5, 5, 5)

                color = cat_colors.get(category, "#3498db")
                cat_lbl = DLabel(category)
                cat_lbl.setFont(QFont('Segoe UI', 9, QFont.Bold))
                cat_lbl.setStyleSheet(f"color: white; background: {color}; border-radius: 8px; padding: 3px 8px;")
                cat_lbl.setFixedWidth(90)
                rl.addWidget(cat_lbl)

                name_lbl = DLabel(name)
                name_lbl.setFont(QFont('Segoe UI', 12, QFont.Bold))
                name_lbl.setStyleSheet(f"color: {color};")
                rl.addWidget(name_lbl, 1)

                remove_btn = DButton("Remove")
                remove_btn.setStyleSheet("QPushButton { background: #e74c3c; color: white; border: none; } QPushButton:hover { background: #c0392b; }")
                remove_btn.clicked.connect(lambda checked, c=category, n=name: self._remove_favorite(c, n))
                rl.addWidget(remove_btn)

                cl.addWidget(row_w)

        cl.addStretch()
        scroll.setWidget(content)
        dlayout.addWidget(scroll)

        close_btn = DButton("Close")
        close_btn.setStyleSheet("QPushButton { background: #3498db; color: white; border: none; } QPushButton:hover { background: #2980b9; }")
        close_btn.clicked.connect(self._fav_dialog.close)
        dlayout.addWidget(close_btn)

        self._fav_dialog.exec()

    def _create_search_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(10)

        title = SectionTitle("Global Search", "Search across all music traditions - Western, Eastern, and World")
        layout.addWidget(title)

        # Search box
        self.global_search = QLineEdit()
        self.global_search.setPlaceholderText("Type to search scales, ragas, maqams, instruments, moods, techniques...")
        self.global_search.setFont(QFont('Segoe UI', 13))
        self.global_search.setFixedHeight(45)
        self.global_search.textChanged.connect(self._do_global_search)
        layout.addWidget(self.global_search)

        # Category filter
        filter_row = QHBoxLayout()
        self.search_filter_btns = []
        categories = [("All", True), ("Western", False), ("Eastern", False), ("African", False), ("Native American", False), ("Latin", False), ("Celtic", False), ("Balkan", False)]
        for cat_name, checked in categories:
            btn = QPushButton(cat_name)
            btn.setCheckable(True)
            btn.setChecked(checked)
            btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton { padding: 6px 14px; border: 2px solid #dce1e3; border-radius: 15px;
                              background: white; color: #7f8c8d; }
                QPushButton:hover { background: #f0f8ff; }
                QPushButton:checked { background: #3498db; color: white; border-color: #3498db; }
            """)
            btn.clicked.connect(self._do_global_search)
            filter_row.addWidget(btn)
            self.search_filter_btns.append(btn)
        filter_row.addStretch()
        layout.addLayout(filter_row)

        # Results
        self.search_scroll = QScrollArea()
        self.search_scroll.setWidgetResizable(True)
        self.search_results_widget = QWidget()
        self.search_results_layout = QVBoxLayout(self.search_results_widget)
        self.search_results_layout.setSpacing(8)
        
        welcome = QLabel("Start typing to search across all music traditions...")
        welcome.setFont(QFont('Segoe UI', 13))
        welcome.setStyleSheet("color: #95a5a6; padding: 30px;")
        welcome.setAlignment(Qt.AlignCenter)
        self.search_results_layout.addWidget(welcome)
        
        self.search_scroll.setWidget(self.search_results_widget)
        layout.addWidget(self.search_scroll)

        return page

    def _get_searchable_data(self):
        """Build a flat list of all searchable items."""
        items = []
        # Western scales
        for name, info in WESTERN_SCALES.items():
            text = f"{name} {info.get('mood', '')} {info.get('description', '')}"
            items.append(('Western', name, info, text))
        # Indian ragas
        for name, info in INDIAN_RAGAS.items():
            text = f"{name} {info.get('mood', '')} {info.get('thaat', '')} {info.get('time', '')} {info.get('description', '')}"
            items.append(('Eastern', name, info, text))
        # Arabic maqams
        for name, info in ARABIC_MAQAMS.items():
            text = f"{name} {info.get('mood', '')} {info.get('region', '')} {info.get('description', '')}"
            items.append(('Eastern', name, info, text))
        # Persian
        for name, info in PERSIAN_DASTGAHS.items():
            text = f"{name} {info.get('mood', '')} {info.get('region', '')} {info.get('description', '')}"
            items.append(('Eastern', name, info, text))
        # Carnatic
        for name, info in CARNATIC_RAGAS.items():
            text = f"{name} {info.get('mood', '')} {info.get('melakarta', '')} {info.get('description', '')}"
            items.append(('Eastern', name, info, text))
        # Chinese
        for name, info in CHINESE_SCALES.items():
            text = f"{name} {info.get('mood', '')} {info.get('element', '')} {info.get('usage', '')} {info.get('description', '')}"
            items.append(('Eastern', name, info, text))
        # Japanese
        for name, info in JAPANESE_SCALES.items():
            text = f"{name} {info.get('mood', '')} {info.get('usage', '')} {info.get('description', '')}"
            items.append(('Eastern', name, info, text))
        # Korean
        for name, info in KOREAN_SCALES.items():
            text = f"{name} {info.get('mood', '')} {info.get('usage', '')} {info.get('description', '')}"
            items.append(('Eastern', name, info, text))
        # Indonesian
        for name, info in INDONESIAN_SCALES.items():
            text = f"{name} {info.get('mood', '')} {info.get('usage', '')} {info.get('description', '')}"
            items.append(('Eastern', name, info, text))
        # African
        for name, info in AFRICAN_MUSIC.items():
            text = f"{name} {info.get('mood', '')} {' '.join(info.get('instruments', []))} {' '.join(info.get('techniques', []))} {info.get('description', '')}"
            items.append(('African', name, info, text))
        # Native American
        for name, info in NATIVE_AMERICAN_MUSIC.items():
            text = f"{name} {info.get('mood', '')} {' '.join(info.get('instruments', []))} {' '.join(info.get('techniques', []))} {info.get('description', '')}"
            items.append(('Native American', name, info, text))
        # Latin American
        for name, info in LATIN_AMERICAN_MUSIC.items():
            text = f"{name} {info.get('mood', '')} {' '.join(info.get('instruments', []))} {info.get('description', '')}"
            items.append(('Latin', name, info, text))
        # Celtic
        for name, info in CELTIC_MUSIC.items():
            text = f"{name} {info.get('mood', '')} {' '.join(info.get('instruments', []))} {info.get('description', '')}"
            items.append(('Celtic', name, info, text))
        # Balkan
        for name, info in BALKAN_MUSIC.items():
            text = f"{name} {info.get('mood', '')} {' '.join(info.get('instruments', []))} {info.get('description', '')}"
            items.append(('Balkan', name, info, text))
        # Chord types
        for name, info in CHORD_TYPES.items():
            text = f"{name} {info.get('quality', '')} {info.get('formula', '')}"
            items.append(('Western', name, info, text))
        return items

    def _do_global_search(self, text=None):
        query = self.global_search.text().lower().strip()
        
        # Get active category filter
        active_filter = "All"
        for btn, cat in zip(self.search_filter_btns, ["All", "Western", "Eastern", "African", "Native American", "Latin", "Celtic", "Balkan"]):
            if btn.isChecked():
                active_filter = cat
                break

        # Clear results
        while self.search_results_layout.count():
            item = self.search_results_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        if not query:
            placeholder = QLabel("Start typing to search across all music traditions...")
            placeholder.setFont(QFont('Segoe UI', 13))
            placeholder.setStyleSheet("color: #95a5a6; padding: 30px;")
            placeholder.setAlignment(Qt.AlignCenter)
            self.search_results_layout.addWidget(placeholder)
            return

        all_items = self._get_searchable_data()
        results = []
        for category, name, info, text in all_items:
            if active_filter != "All" and category != active_filter:
                continue
            if query in text.lower() or query in name.lower():
                results.append((category, name, info))

        if not results:
            nope = QLabel(f"No results found for '{query}'")
            nope.setFont(QFont('Segoe UI', 13))
            nope.setStyleSheet("color: #e74c3c; padding: 30px;")
            nope.setAlignment(Qt.AlignCenter)
            self.search_results_layout.addWidget(nope)
            return

        count_label = QLabel(f"Found {len(results)} result{'s' if len(results) != 1 else ''}")
        count_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        count_label.setStyleSheet("color: #27ae60; margin: 5px 0;")
        self.search_results_layout.addWidget(count_label)

        cat_colors = {"Western": "#3498db", "Eastern": "#9b59b6", "African": "#e67e22", "Native American": "#8B4513", "Latin": "#e74c3c", "Celtic": "#2ecc71", "Balkan": "#1abc9c"}
        
        for category, name, info in results[:50]:
            color = cat_colors.get(category, "#3498db")
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-left: 4px solid {color}; border-radius: 10px; padding: 12px 15px; margin: 3px 0; }}")
            cl = QHBoxLayout(card)
            cl.setContentsMargins(12, 8, 12, 8)
            
            cat_badge = QLabel(category)
            cat_badge.setFont(QFont('Segoe UI', 9, QFont.Bold))
            cat_badge.setStyleSheet(f"color: white; background: {color}; border-radius: 10px; padding: 3px 10px;")
            cat_badge.setFixedWidth(100)
            cl.addWidget(cat_badge)
            
            name_l = QLabel(name)
            name_l.setFont(QFont('Segoe UI', 12, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            cl.addWidget(name_l)
            
            mood = info.get('mood', info.get('quality', ''))
            if mood:
                mood_l = QLabel(mood)
                mood_l.setFont(QFont('Segoe UI', 10))
                mood_l.setStyleSheet("color: #7f8c8d;")
                mood_l.setWordWrap(True)
                cl.addWidget(mood_l, 1)
            
            cl.addStretch()
            self.search_results_layout.addWidget(card)

        self.search_results_layout.addStretch()

    def _create_symbols_page(self):
        """Create the Music Symbols & Notation reference page."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(10)

        title = SectionTitle("Music Symbols & Notation", "Comprehensive guide to musical symbols, dynamics, articulations, and ornaments")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setFont(QFont('Segoe UI', 11))
        tabs.addTab(self._create_symbols_notation_tab(), "Notation")
        tabs.addTab(self._create_symbols_dynamics_tab(), "Dynamics")
        tabs.addTab(self._create_symbols_articulations_tab(), "Articulations & Ornaments")
        tabs.addTab(self._create_symbols_tempo_tab(), "Tempo")
        tabs.addTab(self._create_symbols_form_tab(), "Form & Accidentals")
        layout.addWidget(tabs)
        return widget

    def _create_symbols_notation_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        desc = QLabel("The staff, clefs, and note values form the foundation of Western music notation. Understanding these symbols is the first step to reading music fluently.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        # Group symbols by category
        categories = {}
        for name, info in MUSICAL_SYMBOLS.items():
            cat = info.get('category', 'Other')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((name, info))

        cat_colors = {
            'Clefs': '#3498db', 'Note Values': '#e74c3c', 'Rests': '#e67e22',
            'Accidentals': '#9b59b6', 'Dynamics': '#27ae60', 'Articulations': '#e84393',
            'Form & Structure': '#1abc9c', 'Time Signatures': '#f39c12',
        }

        for cat_name, symbols in categories.items():
            if cat_name in ('Dynamics', 'Articulations', 'Form & Structure'):
                continue  # These have their own tabs
            color = cat_colors.get(cat_name, '#3498db')

            group = QGroupBox(cat_name)
            gl = QVBoxLayout(group)
            gl.setSpacing(8)

            for sym_name, sym_info in symbols:
                card = QFrame()
                card.setStyleSheet(f"QFrame {{ background: white; border-left: 4px solid {color}; border-radius: 8px; padding: 10px 12px; margin: 3px 0; }}")
                cl = QVBoxLayout(card)

                header_row = QHBoxLayout()
                name_l = QLabel(sym_name)
                name_l.setFont(QFont('Segoe UI', 12, QFont.Bold))
                name_l.setStyleSheet(f"color: {color};")
                header_row.addWidget(name_l)

                unicode_val = sym_info.get('unicode', '')
                if unicode_val:
                    sym_l = QLabel(f"Symbol: {unicode_val}")
                    sym_l.setFont(QFont('Segoe UI', 18))
                    sym_l.setStyleSheet("color: #2c3e50;")
                    header_row.addWidget(sym_l)
                header_row.addStretch()
                cl.addLayout(header_row)

                desc_l = QLabel(sym_info.get('description', ''))
                desc_l.setWordWrap(True)
                desc_l.setFont(QFont('Segoe UI', 10))
                desc_l.setStyleSheet("color: #555; line-height: 1.5;")
                cl.addWidget(desc_l)

                # Show extra fields
                for key, label in [('instruments', 'Instruments'), ('range_hint', 'Range'),
                                   ('beats_44', 'Beats in 4/4'), ('equivalent', 'Equivalent'),
                                   ('effect', 'Effect'), ('example', 'Example'),
                                   ('notation', 'Notation'), ('meaning', 'Meaning'),
                                   ('also_known_as', 'Also known as')]:
                    if key in sym_info:
                        field_l = QLabel(f"{label}: {sym_info[key]}")
                        field_l.setWordWrap(True)
                        field_l.setFont(QFont('Segoe UI', 9))
                        field_l.setStyleSheet("color: #2c3e50; margin-top: 2px;")
                        cl.addWidget(field_l)

                mem = sym_info.get('memory_tip', '')
                if mem:
                    mem_l = QLabel(f"Memory tip: {mem}")
                    mem_l.setWordWrap(True)
                    mem_l.setFont(QFont('Segoe UI', 9))
                    mem_l.setStyleSheet("color: #8e44ad; background: #f5eef8; padding: 6px; border-radius: 6px; margin-top: 3px;")
                    cl.addWidget(mem_l)

                gl.addWidget(card)

            layout.addWidget(group)

        layout.addStretch()
        scroll.setWidget(content)
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        return widget

    def _create_symbols_dynamics_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        desc = QLabel("Dynamic markings indicate the volume and intensity of music. Italian terms are used universally. The dynamic range from quietest to loudest is a powerful expressive tool.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        # Visual dynamic scale
        scale_group = QGroupBox("Dynamic Scale (ppp to fff)")
        scale_layout = QVBoxLayout(scale_group)
        max_level = max(d['level'] for d in DYNAMIC_MARKINGS if isinstance(d.get('level'), int) and d['level'] <= 8)
        for d in DYNAMIC_MARKINGS:
            if not isinstance(d.get('level'), int) or d['level'] > 8:
                continue
            row = QHBoxLayout()
            sym_l = QLabel(d['symbol'])
            sym_l.setFont(QFont('Segoe UI', 16, QFont.Bold))
            sym_l.setFixedWidth(50)
            sym_l.setAlignment(Qt.AlignCenter)
            intensity = d['level'] / max_level
            r = int(52 + (231 - 52) * intensity)
            g = int(152 + (76 - 152) * intensity)
            b = int(219 + (60 - 219) * intensity)
            bg_color = f"rgb({r},{g},{b})"
            sym_l.setStyleSheet(f"color: white; background: {bg_color}; border-radius: 8px; padding: 4px;")
            row.addWidget(sym_l)

            name_l = QLabel(d['name'])
            name_l.setFont(QFont('Segoe UI', 11, QFont.Bold))
            name_l.setStyleSheet("color: #2c3e50;")
            name_l.setFixedWidth(140)
            row.addWidget(name_l)

            meaning_l = QLabel(d['meaning'])
            meaning_l.setFont(QFont('Segoe UI', 10))
            meaning_l.setStyleSheet("color: #555;")
            row.addWidget(meaning_l)

            # Visual bar
            bar_bg = QFrame()
            bar_bg.setFixedHeight(20)
            bar_bg.setStyleSheet("QFrame { background: #ecf0f1; border-radius: 10px; }")
            bar_bg.setFixedWidth(int(200 * intensity))
            bar_bg_l = QHBoxLayout(bar_bg)
            bar_bg_l.setContentsMargins(0, 0, 0, 0)
            row.addWidget(bar_bg)

            row.addStretch()
            scale_layout.addLayout(row)

        layout.addWidget(scale_group)

        # Dynamics symbols from MUSICAL_SYMBOLS
        dyn_symbols = {k: v for k, v in MUSICAL_SYMBOLS.items() if v.get('category') == 'Dynamics'}
        if dyn_symbols:
            dyn_group = QGroupBox("Dynamic Symbols Detail")
            dyn_layout = QVBoxLayout(dyn_group)
            for sym_name, sym_info in dyn_symbols.items():
                card = QFrame()
                card.setStyleSheet("QFrame { background: white; border-left: 4px solid #27ae60; border-radius: 8px; padding: 10px 12px; margin: 3px 0; }")
                cl = QVBoxLayout(card)
                name_l = QLabel(sym_name)
                name_l.setFont(QFont('Segoe UI', 12, QFont.Bold))
                name_l.setStyleSheet("color: #27ae60;")
                cl.addWidget(name_l)
                desc_l = QLabel(sym_info.get('description', ''))
                desc_l.setWordWrap(True)
                desc_l.setFont(QFont('Segoe UI', 10))
                desc_l.setStyleSheet("color: #555; line-height: 1.5;")
                cl.addWidget(desc_l)
                for key, label in [('direction', 'Direction'), ('symbol_shape', 'Symbol Shape'), ('range', 'Range'), ('scale_position', 'Position')]:
                    if key in sym_info:
                        f_l = QLabel(f"{label}: {sym_info[key]}")
                        f_l.setFont(QFont('Segoe UI', 9))
                        f_l.setStyleSheet("color: #2c3e50; margin-top: 2px;")
                        cl.addWidget(f_l)
                mem = sym_info.get('memory_tip', '')
                if mem:
                    mem_l = QLabel(f"Memory tip: {mem}")
                    mem_l.setWordWrap(True)
                    mem_l.setFont(QFont('Segoe UI', 9))
                    mem_l.setStyleSheet("color: #8e44ad; background: #f5eef8; padding: 6px; border-radius: 6px; margin-top: 3px;")
                    cl.addWidget(mem_l)
                dyn_layout.addWidget(card)
            layout.addWidget(dyn_group)

        layout.addStretch()
        scroll.setWidget(content)
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        return widget

    def _create_symbols_articulations_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        desc = QLabel("Articulation marks tell you HOW to play notes (short, connected, emphasized). Ornaments add decorative notes for expressiveness and flair.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        # Articulations from MUSICAL_SYMBOLS
        art_symbols = {k: v for k, v in MUSICAL_SYMBOLS.items() if v.get('category') == 'Articulations'}
        colors_art = ["#e84393", "#e74c3c", "#e67e22", "#f39c12", "#9b59b6", "#3498db"]
        if art_symbols:
            art_group = QGroupBox("Articulation Marks")
            art_layout = QVBoxLayout(art_group)
            art_layout.setSpacing(6)
            for i, (sym_name, sym_info) in enumerate(art_symbols.items()):
                color = colors_art[i % len(colors_art)]
                card = QFrame()
                card.setStyleSheet(f"QFrame {{ background: white; border-left: 4px solid {color}; border-radius: 8px; padding: 10px 12px; margin: 3px 0; }}")
                cl = QVBoxLayout(card)
                name_l = QLabel(sym_name)
                name_l.setFont(QFont('Segoe UI', 12, QFont.Bold))
                name_l.setStyleSheet(f"color: {color};")
                cl.addWidget(name_l)
                desc_l = QLabel(sym_info.get('description', ''))
                desc_l.setWordWrap(True)
                desc_l.setFont(QFont('Segoe UI', 10))
                desc_l.setStyleSheet("color: #555; line-height: 1.5;")
                cl.addWidget(desc_l)
                for key, label in [('effect', 'Effect'), ('notation', 'Notation')]:
                    if key in sym_info:
                        f_l = QLabel(f"{label}: {sym_info[key]}")
                        f_l.setFont(QFont('Segoe UI', 9))
                        f_l.setStyleSheet("color: #2c3e50; margin-top: 2px;")
                        cl.addWidget(f_l)
                mem = sym_info.get('memory_tip', '')
                if mem:
                    mem_l = QLabel(f"Memory tip: {mem}")
                    mem_l.setWordWrap(True)
                    mem_l.setFont(QFont('Segoe UI', 9))
                    mem_l.setStyleSheet("color: #8e44ad; background: #f5eef8; padding: 6px; border-radius: 6px; margin-top: 3px;")
                    cl.addWidget(mem_l)
                art_layout.addWidget(card)
            layout.addWidget(art_group)

        # Ornamentation symbols
        orn_group = QGroupBox("Ornamentation Symbols")
        orn_layout = QVBoxLayout(orn_group)
        orn_layout.setSpacing(6)
        for i, (orn_name, orn_info) in enumerate(ORNAMENTATION_SYMBOLS.items()):
            color = colors_art[i % len(colors_art)]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-top: 3px solid {color}; border-radius: 8px; padding: 10px 12px; margin: 4px 0; }}")
            cl = QVBoxLayout(card)
            name_l = QLabel(orn_name)
            name_l.setFont(QFont('Segoe UI', 12, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            cl.addWidget(name_l)
            abbr_l = QLabel(f"Notation: {orn_info.get('abbreviation', '')}")
            abbr_l.setFont(QFont('Segoe UI', 10))
            abbr_l.setStyleSheet("color: #2c3e50; margin-top: 2px;")
            cl.addWidget(abbr_l)
            desc_l = QLabel(orn_info.get('description', ''))
            desc_l.setWordWrap(True)
            desc_l.setFont(QFont('Segoe UI', 10))
            desc_l.setStyleSheet("color: #555; line-height: 1.5;")
            cl.addWidget(desc_l)
            exec_l = QLabel(f"How to execute: {orn_info.get('execution', '')}")
            exec_l.setWordWrap(True)
            exec_l.setFont(QFont('Segoe UI', 9))
            exec_l.setStyleSheet("color: #2980b9; background: #eaf2f8; padding: 6px; border-radius: 6px; margin-top: 3px;")
            cl.addWidget(exec_l)
            for key, label in [('period', 'Period'), ('example_work', 'Example Work')]:
                if key in orn_info:
                    f_l = QLabel(f"{label}: {orn_info[key]}")
                    f_l.setWordWrap(True)
                    f_l.setFont(QFont('Segoe UI', 9))
                    f_l.setStyleSheet("color: #8e44ad; margin-top: 2px;")
                    cl.addWidget(f_l)
            mem = orn_info.get('memory_tip', '')
            if mem:
                mem_l = QLabel(f"Memory tip: {mem}")
                mem_l.setWordWrap(True)
                mem_l.setFont(QFont('Segoe UI', 9))
                mem_l.setStyleSheet("color: #e67e22; background: #fef5e7; padding: 6px; border-radius: 6px; margin-top: 3px;")
                cl.addWidget(mem_l)
            orn_layout.addWidget(card)
        layout.addWidget(orn_group)

        layout.addStretch()
        scroll.setWidget(content)
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        return widget

    def _create_symbols_tempo_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        desc = QLabel("Tempo markings indicate the speed of music. Italian terms are the universal standard. The BPM (Beats Per Minute) range gives the approximate speed in quarter-note beats.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        # Tempo speed scale
        scale_group = QGroupBox("Tempo Scale (Slowest to Fastest)")
        scale_layout = QVBoxLayout(scale_group)
        scale_layout.setSpacing(6)

        tempo_colors = ["#2980b9", "#3498db", "#1abc9c", "#27ae60", "#f39c12", "#e67e22", "#e74c3c", "#c0392b", "#8e44ad", "#9b59b6", "#2c3e50", "#16a085"]
        for i, (tempo_name, tempo_info) in enumerate(TEMPO_MARKINGS.items()):
            color = tempo_colors[i % len(tempo_colors)]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-left: 4px solid {color}; border-radius: 8px; padding: 8px 12px; margin: 2px 0; }}")
            cl = QHBoxLayout(card)
            name_l = QLabel(tempo_name)
            name_l.setFont(QFont('Segoe UI', 12, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            name_l.setFixedWidth(160)
            cl.addWidget(name_l)
            bpm_l = QLabel(tempo_info.get('bpm_range', ''))
            bpm_l.setFont(QFont('Segoe UI', 10, QFont.Bold))
            bpm_l.setStyleSheet("color: #e74c3c; background: #fdedec; border-radius: 10px; padding: 3px 10px;")
            bpm_l.setFixedWidth(140)
            cl.addWidget(bpm_l)
            meaning_l = QLabel(tempo_info.get('meaning', ''))
            meaning_l.setFont(QFont('Segoe UI', 10))
            meaning_l.setStyleSheet("color: #555;")
            cl.addWidget(meaning_l)
            cl.addStretch()
            scale_layout.addWidget(card)

            char_l = QLabel(tempo_info.get('character', ''))
            char_l.setWordWrap(True)
            char_l.setFont(QFont('Segoe UI', 9))
            char_l.setStyleSheet("color: #7f8c8d; padding-left: 170px; margin-bottom: 4px;")
            scale_layout.addWidget(char_l)

        layout.addWidget(scale_group)

        layout.addStretch()
        scroll.setWidget(content)
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        return widget

    def _create_symbols_form_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)

        desc = QLabel("Form and structure symbols tell you how a piece of music is organized. Accidentals (sharps, flats, naturals) modify the pitch of notes.")
        desc.setWordWrap(True)
        desc.setFont(QFont('Segoe UI', 11))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(desc)

        # Form symbols from MUSICAL_SYMBOLS
        form_symbols = {k: v for k, v in MUSICAL_SYMBOLS.items() if v.get('category') == 'Form & Structure'}
        if form_symbols:
            form_group = QGroupBox("Form & Structure Symbols")
            form_layout = QVBoxLayout(form_group)
            for sym_name, sym_info in form_symbols.items():
                card = QFrame()
                card.setStyleSheet("QFrame { background: white; border-left: 4px solid #1abc9c; border-radius: 8px; padding: 10px 12px; margin: 3px 0; }")
                cl = QVBoxLayout(card)
                name_l = QLabel(sym_name)
                name_l.setFont(QFont('Segoe UI', 12, QFont.Bold))
                name_l.setStyleSheet("color: #1abc9c;")
                cl.addWidget(name_l)
                desc_l = QLabel(sym_info.get('description', ''))
                desc_l.setWordWrap(True)
                desc_l.setFont(QFont('Segoe UI', 10))
                desc_l.setStyleSheet("color: #555; line-height: 1.5;")
                cl.addWidget(desc_l)
                for key, label in [('effect', 'Effect'), ('notation', 'Notation'), ('meaning', 'Meaning'), ('also_known_as', 'Also known as')]:
                    if key in sym_info:
                        f_l = QLabel(f"{label}: {sym_info[key]}")
                        f_l.setFont(QFont('Segoe UI', 9))
                        f_l.setStyleSheet("color: #2c3e50; margin-top: 2px;")
                        cl.addWidget(f_l)
                mem = sym_info.get('memory_tip', '')
                if mem:
                    mem_l = QLabel(f"Memory tip: {mem}")
                    mem_l.setWordWrap(True)
                    mem_l.setFont(QFont('Segoe UI', 9))
                    mem_l.setStyleSheet("color: #8e44ad; background: #f5eef8; padding: 6px; border-radius: 6px; margin-top: 3px;")
                    cl.addWidget(mem_l)
                form_layout.addWidget(card)
            layout.addWidget(form_group)

        # Accidentals guide
        acc_group = QGroupBox("Accidentals Reference")
        acc_layout = QVBoxLayout(acc_group)
        acc_layout.setSpacing(8)

        acc_colors = {"Sharp (#)": "#e74c3c", "Flat (b)": "#3498db", "Natural": "#27ae60"}
        for acc_name, acc_info in ACCIDENTAL_RULES.items():
            color = acc_colors.get(acc_name, "#7f8c8d")
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background: white; border-top: 3px solid {color}; border-radius: 8px; padding: 10px 12px; margin: 4px 0; }}")
            cl = QVBoxLayout(card)
            name_l = QLabel(acc_name)
            name_l.setFont(QFont('Segoe UI', 12, QFont.Bold))
            name_l.setStyleSheet(f"color: {color};")
            cl.addWidget(name_l)
            for key, label in [('effect', 'Effect'), ('example', 'Example'), ('cancels', 'Cancels'), ('double_form', 'Double Form'), ('order_in_signature', 'Order in Key Signature')]:
                if key in acc_info:
                    f_l = QLabel(f"{label}: {acc_info[key]}")
                    f_l.setWordWrap(True)
                    f_l.setFont(QFont('Segoe UI', 10))
                    f_l.setStyleSheet("color: #555; margin-top: 2px;")
                    cl.addWidget(f_l)
            acc_layout.addWidget(card)

        layout.addWidget(acc_group)

        layout.addStretch()
        scroll.setWidget(content)
        outer = QVBoxLayout(widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)
        return widget

    def _on_wave_changed(self, index):
        from piano_widget import WAVE_TYPES
        wave_keys = list(WAVE_TYPES.keys())
        if 0 <= index < len(wave_keys):
            audio_engine.wave_type = wave_keys[index]

    def _switch_page(self, page_id):
        page_map = {'western': 0, 'eastern': 1, 'world': 2, 'symbols': 3, 'search': 4, 'quiz': 5}
        self.stack.setCurrentIndex(page_map.get(page_id, 0))
        for btn, pid in self.nav_buttons:
            btn.setChecked(pid == page_id)
        names = {'western': 'Western Music Theory', 'eastern': 'Eastern Music Theory',
                 'world': 'World Music Theory', 'symbols': 'Music Symbols & Notation',
                 'search': 'Global Search', 'quiz': 'Music Theory Quiz'}
        self.statusBar().showMessage(f"Viewing: {names.get(page_id, '')}")

    def _apply_style(self):
        self.setStyleSheet(GLOBAL_STYLE)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    font = QFont('Segoe UI', 10)
    app.setFont(font)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(248, 249, 250))
    palette.setColor(QPalette.WindowText, QColor(44, 62, 80))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(44, 62, 80))
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    palette.setColor(QPalette.ButtonText, QColor(44, 62, 80))
    palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    window = MusicTheoryApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()