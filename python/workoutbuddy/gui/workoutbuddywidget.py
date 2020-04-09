# stdlib modules
import datetime
import calendar

# tool modules
from workoutbuddy import __version__
from workoutbuddy import workoutbuddy
from workoutbuddy.models import Log
from workoutbuddy.models import ExerciseSet
from workoutbuddy.models import Exercise

# third party modules
from PySide2 import QtWidgets, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd


class WorkoutBuddyWidget(QtWidgets.QWidget):

    dataframe_changed = QtCore.Signal(pd.DataFrame)

    def __init__(self, *args, **kwargs):
        super(WorkoutBuddyWidget, self).__init__(*args, **kwargs)
        self._dataframe = None
        self._build_ui()
        self._connect_signals()
        self._initialize()
        self.refresh()

    # =========================================================================
    # private
    # =========================================================================
    def _build_ui(self):
        # date start
        self.date_start = QtWidgets.QDateEdit()
        self.date_start.setDisplayFormat("dd/MM/yyyy")

        # date end
        self.date_end = QtWidgets.QDateEdit()
        self.date_end.setDisplayFormat("dd/MM/yyyy")

        # exercises
        self.list_exercises = QtWidgets.QListView()

        # settings
        group_settings = QtWidgets.QGroupBox("Settings:")
        group_settings_layout = QtWidgets.QFormLayout()
        group_settings_layout.addRow("Date Start:", self.date_start)
        group_settings_layout.addRow("Date End:", self.date_end)
        group_settings_layout.addRow("Exercises:", self.list_exercises)
        group_settings.setLayout(group_settings_layout)

        # canvas
        fig = Figure(dpi=72, tight_layout=True)
        self.canvas = FigureCanvas(fig)
        win = QtWidgets.QMainWindow()
        win.addToolBar(NavigationToolbar(self.canvas, win))
        win.setCentralWidget(self.canvas)

        # main layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(group_settings)
        layout.addWidget(win)
        layout.setStretch(1, 1)
        self.setLayout(layout)

        # window settings
        self.setWindowTitle(f"WorkoutBuddy - v{__version__}")
        self.setWindowFlags(QtCore.Qt.Window)

    def _connect_signals(self):
        self.date_start.dateChanged.connect(self._date_start_changed)
        self.date_end.dateChanged.connect(self._date_end_changed)
        self.dataframe_changed.connect(self._plot_data)

    def _initialize(self):
        date_end = datetime.date.today()
        self.date_end.setDate(date_end)

        days = calendar.monthrange(date_end.year, date_end.month)[1]
        date_start = date_end - datetime.timedelta(days=days + 1)
        self.date_start.setDate(date_start)

    def _date_start_changed(self, _date):
        self.refresh()

    def _date_end_changed(self, _date):
        self.refresh()

    def _get_dataframe(self):
        session = workoutbuddy.create_session()
        query = session.query(Log.date, Exercise.name, ExerciseSet.reps)
        query = query.join(ExerciseSet, ExerciseSet.id == Log.exercise_set_id)
        query = query.join(Exercise, Exercise.id == ExerciseSet.id)
        df = pd.read_sql(query.statement, session.bind)

        date_start = self.date_start.date().toPython()
        date_end = self.date_end.date().toPython()
        df = df[df["date"] < date_end]
        df = df[df["date"] > date_start]

        return df

    def _plot_data(self):
        self.canvas.figure.clear()
        date_start = self.date_start.date().toPython()
        date_end = self.date_end.date().toPython()

        by_name = self.dataframe.groupby("name")
        ax = self.canvas.figure.add_subplot(111)

        for name in by_name.groups:
            df = by_name.get_group(name)
            df.plot(x="date", ax=ax, label=name, alpha=.75)

        ax.set_xlim(date_start, date_end)
        ax.legend(by_name.groups)
        self.canvas.draw()

    # =========================================================================
    # public
    # =========================================================================
    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value):
        self._dataframe = value
        self.dataframe_changed.emit(value)

    def refresh(self):
        self.dataframe = self._get_dataframe()
