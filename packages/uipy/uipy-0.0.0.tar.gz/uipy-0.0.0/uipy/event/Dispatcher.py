from PySide6.QtCore import Signal, QObject
import uuid as uid


class Dispatcher(QObject):
    """派发器
    注：最多支持10个自定义信号。
    """

    triggers = {}
    uuid = ''

    # 继承 QObject 才能使用信号，并且需要作为成员属性，因此没法用数组
    signal1 = Signal(object)
    signal2 = Signal(object)
    signal3 = Signal(object)
    signal4 = Signal(object)
    signal5 = Signal(object)
    signal6 = Signal(object)
    signal7 = Signal(object)
    signal8 = Signal(object)
    signal9 = Signal(object)
    signal10 = Signal(object)

    signalUsedMaxId = 0

    def __init__(this):

        super(Dispatcher, this).__init__()
        this.uuid = uid.uuid4().hex

    def _getUnusedSignal(this):
        this.signalUsedMaxId += 1
        if this.signalUsedMaxId > 10:
            raise RuntimeError("Dispatcher: no more usable signal!")

        return getattr(this, 'signal' + str(this.signalUsedMaxId))

    def on(this, signal, slot):
        if isinstance(signal, str):
            # 自动增补，如果没有
            if signal not in this.triggers:
                this.triggers[signal] = this._getUnusedSignal()

            this.triggers[signal].connect(slot)
        else:
            signal.connect(slot)

    def off(this, signal, slot):
        if isinstance(signal, str):
            this.triggers[signal].disconnect(slot)
        else:
            signal.disconnect(slot)

    def fire(this, signal, *args):
        if isinstance(signal, str):
            this.triggers[signal].emit(args[0])
        else:
            signal.emit(args[0])
