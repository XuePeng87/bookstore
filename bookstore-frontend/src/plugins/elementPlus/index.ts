import type { App } from 'vue'

// 需要全局引入一些组件，如ElScrollbar，不然一些下拉项样式有问题
import { ElLoading, ElScrollbar, ElTable, ElTag, ElButton } from 'element-plus'

const plugins = [ElLoading]

const components = [ElScrollbar]

const elTable = [ElTable]

const elTag = [ElTag]

const elButton = [ElButton]

export const setupElementPlus = (app: App<Element>) => {
  plugins.forEach((plugin) => {
    app.use(plugin)
  })

  elTable.forEach((plugin) => {
    app.use(plugin)
  })

  elTag.forEach((plugin) => {
    app.use(plugin)
  })

  elButton.forEach((plugin) => {
    app.use(plugin)
  })

  components.forEach((component) => {
    app.component(component.name, component)
  })
}
