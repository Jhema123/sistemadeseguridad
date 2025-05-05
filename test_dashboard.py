import sys
from PyQt5.QtWidgets import QApplication
from view.dashboard_view import DashboardView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    vista = DashboardView("admin")
    vista.show()
    sys.exit(app.exec_())
