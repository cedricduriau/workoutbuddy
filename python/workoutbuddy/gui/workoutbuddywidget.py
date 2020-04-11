# stdlib modules
import datetime
import calendar

# tool modules
from workoutbuddy import __version__
from workoutbuddy import workoutbuddy
from workoutbuddy.models import Log
from workoutbuddy.models import Exercise
from workoutbuddy.gui.checkablestringlistmodel import CheckableStringListModel

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
        self._initialize()
        self._connect_signals()
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
        self.list_exercises.model().item_checked.connect(self._list_exercises_item_checked)
        self.dataframe_changed.connect(self._plot_data)

    def _initialize(self):
        today = datetime.date.today()

        date_start = datetime.date(today.year, today.month, 1)
        self.date_start.setDate(date_start)

        days = calendar.monthrange(today.year, today.month)[1]
        date_end = datetime.date(today.year, today.month, days)
        self.date_end.setDate(date_end)

        session = workoutbuddy.create_session()
        result = session.query(Exercise.name).all()
        exercices = [i[0] for i in result]
        self.list_exercises.setModel(CheckableStringListModel(exercices))

    def _date_start_changed(self, *args, **kwargs):
        self.refresh()

    def _date_end_changed(self, *args, **kwargs):
        self.refresh()

    def _list_exercises_item_checked(self, *args, **kwargs):
        self.refresh()

    def _get_dataframe(self):
        session = workoutbuddy.create_session()
        query = session.query(Log, Exercise).join(Exercise)
        df = pd.read_sql(query.statement, session.bind)
        return df

    def _plot_data(self):
        # clear canvas
        self.canvas.figure.clear()

        # filter date
        date_start = self.date_start.date().toPython()
        date_end = self.date_end.date().toPython()

        df = self.dataframe.copy()
        df = df[df["date"] < date_end]
        df = df[df["date"] > date_start]

        # area plot
        ax = self.canvas.figure.add_subplot()
        names = self.list_exercises.model().get_checked_items()
        if names:
            pivot_df = df.pivot(index="date", columns="name", values="reps")
            if not pivot_df.empty:
                pivot_df.loc[:, names].plot.area(stacked=True, ax=ax, alpha=0.75)

        ax.set_xlim(date_start, date_end)
        self.canvas.figure.autofmt_xdate()
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
