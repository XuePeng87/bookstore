import type { App } from 'vue'

// 需要全局引入一些组件，如ElScrollbar，不然一些下拉项样式有问题
import {
  ElLoading,
  ElScrollbar,
  ElTable,
  ElTag,
  ElButton,
  ElPagination,
  ElIcon,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElDatePicker,
  ElCheckbox,
  ElImage,
  ElDialog,
  ElRow,
  ElCol,
  ElDivider
} from 'element-plus'

const plugins = [ElLoading]

const components = [ElScrollbar]

const ui = [
  ElTable,
  ElTag,
  ElButton,
  ElPagination,
  ElIcon,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElDatePicker,
  ElCheckbox,
  ElImage,
  ElDialog,
  ElRow,
  ElCol,
  ElDivider
]

export const setupElementPlus = (app: App<Element>) => {
  plugins.forEach((plugin) => {
    app.use(plugin)
  })

  components.forEach((component) => {
    app.component(component.name, component)
  })

  ui.forEach((plugin) => {
    app.use(plugin)
  })
}
