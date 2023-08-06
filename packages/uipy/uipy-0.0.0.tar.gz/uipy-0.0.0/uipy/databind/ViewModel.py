import uipy as ui
import mupy as mu


class ViewModel(ui.Dispatcher):

    def __init__(this):
        super(ViewModel, this).__init__()

    def bind(this):

        ui.BINDER.viewModel = this

        def callback(child):

            child.dispatcher = ui.Dispatcher()
            child.on = child.dispatcher.on
            child.off = child.dispatcher.off
            child.fire = child.dispatcher.fire

            child.databinder = ui.Databinder(child)
            child.databinder.bind()

        # 遍历所有控件，做好初始化
        ui.eachChild(callback)
