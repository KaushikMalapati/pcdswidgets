from pydm.widgets.enum_button import PyDMEnumButton
from qtpy.QtCore import QSize, Qt, Property, Q_ENUMS
from qtpy.QtWidgets import QVBoxLayout, QSizePolicy

from .base import PCDSSymbolBase, ContentLocation
from .mixins import InterlockMixin, ErrorMixin, OpenCloseStateMixin
from ..icons.valves import PneumaticValveSymbolIcon, FastShutterSymbolIcon


class PneumaticValve(InterlockMixin, ErrorMixin, OpenCloseStateMixin,
                     PCDSSymbolBase, ContentLocation):
    """
    A Symbol Widget representing a Pneumatic Valve with the proper icon and
    controls.

    Parameters
    ----------
    parent : QWidget
        The parent widget for the symbol

    Notes
    -----
    This widget allow for high customization through the Qt Stylesheets
    mechanism.
    As this widget is composed by internal widgets, their names can be used as
    selectors when writing your stylesheet to be used with this widget.
    Properties are also available to offer wider customization possibilities.

    **Internal Components**

    +-----------+--------------+---------------------------------------+
    |Widget Name|Type          |What is it?                            |
    +===========+==============+=======================================+
    |interlock  |QFrame        |The QFrame wrapping this whole widget. |
    +-----------+--------------+---------------------------------------+
    |controls   |QFrame        |The QFrame wrapping the controls panel.|
    +-----------+--------------+---------------------------------------+
    |icon       |BaseSymbolIcon|The widget containing the icon drawing.|
    +-----------+--------------+---------------------------------------+

    **Additional Properties**

    +-----------+-------------------------------------------------------+
    |Property   |Values                                                 |
    +===========+=======================================================+
    |interlocked|`true` or `false`                                      |
    +-----------+-------------------------------------------------------+
    |error      |`Vented`, `At Vacuum`, `Differential Pressure` or      |
    |           |`Lost Vacuum`                                          |
    +-----------+-------------------------------------------------------+
    |state      |`Open`, `Close` or `INVALID`                           |
    +-----------+-------------------------------------------------------+

    Examples
    --------

    .. code-block:: css

        PneumaticValve [interlocked="true"] #interlock {
            border: 5px solid red;
        }
        PneumaticValve [interlocked="false"] #interlock {
            border: 0px;
        }
        PneumaticValve [interlocked="true"] #icon {
            qproperty-interlockBrush: #FF0000;
        }
        PneumaticValve [interlocked="false"] #icon {
            qproperty-interlockBrush: #00FF00;
        }
        PneumaticValve [error="Lost Vacuum"] #icon {
            qproperty-penStyle: "Qt::DotLine";
            qproperty-penWidth: 2;
            qproperty-brush: red;
        }
        PneumaticValve [state="Open"] #icon {
            qproperty-penColor: green;
            qproperty-penWidth: 2;
        }

    """
    _interlock_suffix = ":OPN_OK"
    _error_suffix = ":STATE"
    _open_state_suffix = ":OPN_DI"
    _close_state_suffix = ":CLS_DI"

    Q_ENUMS(ContentLocation)
    NAME = "Pneumatic Valve"

    def __init__(self, parent=None, **kwargs):
        super(PneumaticValve, self).__init__(
            parent=parent,
            interlock_suffix=self._interlock_suffix,
            error_suffix=self._error_suffix,
            open_suffix=self._open_state_suffix,
            close_suffix=self._close_state_suffix,
            **kwargs)

        self.open_close_btn = PyDMEnumButton()
        self.icon = PneumaticValveSymbolIcon(self)
        self.icon.setMinimumSize(16, 16)
        self.icon.setSizePolicy(QSizePolicy.Expanding,
                                QSizePolicy.Expanding)
        self.icon.setVisible(self._show_icon)
        self.iconSize = 32

        self.controls_layout = QVBoxLayout()
        self.controls_layout.setSpacing(0)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_frame.setLayout(self.controls_layout)
        self.controls_frame.layout().addWidget(self.open_close_btn)

        self.assemble_layout()
        self.update_status_tooltip()

    @Property(ContentLocation)
    def controlsLocation(self):
        """
        Property controlling where the controls frame will be displayed.

        Returns
        -------
        location : ContentLocation
        """
        return self._controls_location

    @controlsLocation.setter
    def controlsLocation(self, location):
        """
        Property controlling where the controls frame will be displayed.

        Parameters
        ----------
        location : ContentLocation
        """
        if location != self._controls_location:
            self._controls_location = location
            self.assemble_layout()

    def sizeHint(self):
        """
        Suggested initial size for the widget.

        Returns
        -------
        size : QSize
        """
        return QSize(200, 200)

    def assemble_layout(self):
        """
        Assembles the widget's inner layout depending on the ContentLocation
        and other configurations set and adjust the orientation of the control
        button depending on the location.
        """
        super(PneumaticValve, self).assemble_layout()
        if self.controlsLocation in [ContentLocation.Top,
                                     ContentLocation.Bottom]:
            self.open_close_btn.orientation = Qt.Horizontal
            self.open_close_btn.setMinimumSize(100, 40)
        else:
            self.open_close_btn.orientation = Qt.Vertical
            self.open_close_btn.setMinimumSize(100, 80)

    def create_channels(self):
        """
        Method invoked when the channels associated with the widget must be
        created.
        This method also sets the channel address for the control button.
        """
        super(PneumaticValve, self).create_channels()
        if self._channels_prefix:
            self.open_close_btn.channel = "{}{}".format(self._channels_prefix,
                                                        ":OPN_SW")

    def destroy_channels(self):
        """
        Method invoked when the channels associated with the widget must be
        destroyed.
        This method also clears the channel address for the control button.
        """
        super(PneumaticValve, self).destroy_channels()
        self.open_close_btn.channel = None

    def interlock_value_changed(self, value):
        """
        Callback invoked when the value changes for the Interlock Channel.
        This method is responsible for enabling/disabling the controls frame
        depending on the interlock status.

        Parameters
        ----------
        value : int
            The value from the channel will be either 0 or 1 with 1 meaning
            that the widget is interlocked.
        """
        InterlockMixin.interlock_value_changed(self, value)
        self.controls_frame.setEnabled(not self._interlocked)


class FastShutter(InterlockMixin, ErrorMixin, OpenCloseStateMixin,
                  PCDSSymbolBase, ContentLocation):
    """
    A Symbol Widget representing a Fast Shutter with the proper icon and
    controls.

    Parameters
    ----------
    parent : QWidget
        The parent widget for the symbol

    Notes
    -----
    This widget allow for high customization through the Qt Stylesheets
    mechanism.
    As this widget is composed by internal widgets, their names can be used as
    selectors when writing your stylesheet to be used with this widget.
    Properties are also available to offer wider customization possibilities.

    **Internal Components**

    +-----------+--------------+---------------------------------------+
    |Widget Name|Type          |What is it?                            |
    +===========+==============+=======================================+
    |interlock  |QFrame        |The QFrame wrapping this whole widget. |
    +-----------+--------------+---------------------------------------+
    |controls   |QFrame        |The QFrame wrapping the controls panel.|
    +-----------+--------------+---------------------------------------+
    |icon       |BaseSymbolIcon|The widget containing the icon drawing.|
    +-----------+--------------+---------------------------------------+

    **Additional Properties**

    +-----------+-------------------------------------------------------------+
    |Property   |Values                                                       |
    +===========+=============================================================+
    |interlocked|`true` or `false`                                            |
    +-----------+-------------------------------------------------------------+
    |error      |`true`, or `false`                                           |
    +-----------+-------------------------------------------------------------+
    |state      |`Open`, `Close` or `INVALID`                                 |
    +-----------+-------------------------------------------------------------+

    Examples
    --------

    .. code-block:: css

        FastShutter [interlocked="true"] #interlock {
            border: 5px solid red;
        }
        FastShutter [interlocked="false"] #interlock {
            border: 0px;
        }
        FastShutter [error="true"] #icon {
            qproperty-penStyle: "Qt::DotLine";
            qproperty-penWidth: 2;
            qproperty-brush: red;
        }
        FastShutter [state="Open"] #icon {
            qproperty-penColor: green;
            qproperty-penWidth: 2;
        }

    """
    _interlock_suffix = ":OPN_OK"
    _error_suffix = ":ERROR"
    _open_state_suffix = ":OPN_DI"
    _close_state_suffix = ":CLS_DI"

    Q_ENUMS(ContentLocation)
    NAME = "Fast Shutter"

    def __init__(self, parent=None, **kwargs):
        super(FastShutter, self).__init__(
            parent=parent,
            interlock_suffix=self._interlock_suffix,
            error_suffix=self._error_suffix,
            open_suffix=self._open_state_suffix,
            close_suffix=self._close_state_suffix,
            **kwargs)

        self.open_close_btn = PyDMEnumButton()
        self.icon = FastShutterSymbolIcon(self)
        self.icon.setMinimumSize(16, 16)
        self.icon.setSizePolicy(QSizePolicy.Expanding,
                                QSizePolicy.Expanding)
        self.icon.setVisible(self._show_icon)
        self.iconSize = 32

        self.controls_layout = QVBoxLayout()
        self.controls_layout.setSpacing(0)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_frame.setLayout(self.controls_layout)
        self.controls_frame.layout().addWidget(self.open_close_btn)

        self.assemble_layout()
        self.update_status_tooltip()

    @Property(ContentLocation)
    def controlsLocation(self):
        """
        Property controlling where the controls frame will be displayed.

        Returns
        -------
        location : ContentLocation
        """
        return self._controls_location

    @controlsLocation.setter
    def controlsLocation(self, location):
        """
        Property controlling where the controls frame will be displayed.

        Parameters
        ----------
        location : ContentLocation
        """
        if location != self._controls_location:
            self._controls_location = location
            self.assemble_layout()

    def sizeHint(self):
        """
        Suggested initial size for the widget.

        Returns
        -------
        size : QSize
        """
        return QSize(200, 200)

    def assemble_layout(self):
        """
        Assembles the widget's inner layout depending on the ContentLocation
        and other configurations set and adjust the orientation of the control
        button depending on the location.
        """
        super(FastShutter, self).assemble_layout()
        if self.controlsLocation in [ContentLocation.Top,
                                     ContentLocation.Bottom]:
            self.open_close_btn.orientation = Qt.Horizontal
            self.open_close_btn.setMinimumSize(100, 40)
        else:
            self.open_close_btn.orientation = Qt.Vertical
            self.open_close_btn.setMinimumSize(100, 80)

    def create_channels(self):
        """
        Method invoked when the channels associated with the widget must be
        created.
        This method also sets the channel address for the control button.
        """
        super(FastShutter, self).create_channels()
        if self._channels_prefix:
            self.open_close_btn.channel = "{}{}".format(self._channels_prefix,
                                                        ":OPN_SW")

    def destroy_channels(self):
        """
        Method invoked when the channels associated with the widget must be
        destroyed.
        This method also clears the channel address for the control button.
        """
        super(FastShutter, self).destroy_channels()
        self.open_close_btn.channel = None

    def interlock_value_changed(self, value):
        """
        Callback invoked when the value changes for the Interlock Channel.
        This method is responsible for enabling/disabling the controls frame
        depending on the interlock status.

        Parameters
        ----------
        value : int
            The value from the channel will be either 0 or 1 with 1 meaning
            that the widget is interlocked.
        """
        InterlockMixin.interlock_value_changed(self, value)
        self.controls_frame.setEnabled(not self._interlocked)
