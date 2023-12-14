<template>
  <ContentWrap :title="t('levelDemo.menu')">
    <el-form :inline="true" :model="queryForm">
      <el-form-item label="书名">
        <el-input v-model="queryForm.bookName" clearable />
      </el-form-item>
      <el-form-item label="类型">
        <el-select v-model="queryForm.clcName" clearable multiple>
          <el-option v-for="clc in clcs" :key="clc" :label="clc" :value="clc" />
        </el-select>
      </el-form-item>
      <el-form-item label="类型">
        <el-select v-model="queryForm.tags" clearable multiple>
          <el-option v-for="tag in tags" :key="tag" :label="tag" :value="tag" />
        </el-select>
      </el-form-item>
      <el-form-item label="作者">
        <el-input v-model="queryForm.author" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="queryBook(1)">查询</el-button>
      </el-form-item>
    </el-form>
    <div style="margin-bottom: 10px">
      <el-button type="primary" @click="openBookForm(undefined, formRef)">创建</el-button>
    </div>
    <el-table :data="books" stripe style="width: 100%">
      <el-table-column prop="bookName" label="书名" />
      <el-table-column prop="edition" label="版次" />
      <el-table-column prop="clcName" label="类型" />
      <el-table-column prop="press" label="出版社" />
      <el-table-column prop="pressDate" label="出版时间" />
      <el-table-column prop="author" label="作者" />
      <el-table-column prop="pages" label="页数" />
      <el-table-column prop="price" label="价格">
        <template #default="scope">
          <span>
            {{ $filters.currencyRMB(scope.row.price) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="readOver" label="已读">
        <template #default="scope">
          <el-tag :type="scope.row.tag === true ? 'success' : 'danger'">
            {{ $filters.boolToStr(scope.row.readOver) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="240">
        <template #default="scope">
          <el-button link type="primary" @click="openBookForm(scope.row._id, undefined)"
            >修改</el-button
          >
          <el-popover :visible="visible" placement="top" :width="160">
            <p>确认要删除吗?</p>
            <div style="text-align: right; margin: 0">
              <el-button size="small" text @click="visible = false">cancel</el-button>
              <el-button size="small" type="primary" @click="removeBook(scope.row._id)"
                >confirm</el-button
              >
            </div>
            <template #reference>
              <el-button link type="primary" @click="visible = true">删除</el-button>
            </template>
          </el-popover>
        </template>
      </el-table-column>
    </el-table>
    <div style="margin-top: 10px">
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        @current-change="queryBook"
      />
    </div>
  </ContentWrap>
  <!-- 弹出窗 -->
  <el-dialog
    v-model="dialogFormVisible"
    fullscreen
    :close-on-press-escape="false"
    :show-close="false"
  >
    <template #header="{ close }">
      <div style="padding-top: 10px; padding-right: 15px; text-align: right">
        <el-button type="primary" @click="saveBook(formRef)">保存</el-button>
        <el-button @click="resetForm(formRef)">重置</el-button>
        <el-button type="danger" @click="close">关闭</el-button>
      </div>
    </template>
    <el-form ref="formRef" :model="bookForm" label-width="120px" status-icon>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="ISBN" prop="isbn">
            <el-input v-model="bookForm.isbn" :prefix-icon="Search" @keyup.enter="isbn" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="名称" prop="bookName">
            <el-input v-model="bookForm.bookName" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="简介" prop="bookDesc">
            <el-input v-model="bookForm.bookDesc" type="textarea" :rows="13" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="封面">
            <div v-for="pic in bookForm.pictures" :key="pic">
              <el-image style="width: 200px; height: 283px" content="no-referrer" :src="pic" />
            </div>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="标签">
            <el-tag
              v-for="tag in bookForm.tags"
              :key="tag"
              closable
              :disable-transitions="false"
              style="margin-left: 10px"
              @close="handleClose(tag)"
            >
              {{ tag }}
            </el-tag>
            <el-input
              style="margin-left: 10px; width: 100px"
              v-if="inputVisible"
              v-model="inputValue"
              size="small"
              @keyup.enter="handleInputConfirm"
              @blur="handleInputConfirm"
            />
            <el-button v-else size="small" style="margin-left: 10px" @click="showInput"
              >添加</el-button
            >
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="类型编号" prop="clcCode">
            <el-input v-model="bookForm.clcCode" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="类型名称" prop="clcName">
            <el-input v-model="bookForm.clcName" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="作者" prop="author">
            <el-input v-model="bookForm.author" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="语言" prop="language">
            <el-input v-model="bookForm.language" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="页数" prop="pages">
            <el-input v-model="bookForm.pages" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="字数" prop="words">
            <el-input v-model="bookForm.words" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="出版社" prop="press">
            <el-input v-model="bookForm.press" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="出版日期" prop="pressDate">
            <el-date-picker v-model="bookForm.pressDate" type="date" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="出版地" prop="pressPlace">
            <el-input v-model="bookForm.pressPlace" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="价格" prop="price">
            <el-input
              v-model="bookForm.price"
              :formatter="(value) => `¥ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')"
              :parser="(value) => value.replace(/\$\s?|(,*)/g, '')"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="版次" prop="edition">
            <el-input v-model="bookForm.edition" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="封装" prop="binding">
            <el-input v-model="bookForm.binding" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="裁剪" prop="format">
            <el-input v-model="bookForm.format" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="已读" prop="readOver">
            <el-checkbox v-model="bookForm.readOver" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </el-dialog>
</template>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import { onMounted, reactive, toRefs, ref } from 'vue'
import { ElMessage, FormInstance } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import {
  queryByISBN,
  query,
  queryById,
  create,
  update,
  remove,
  queryClcs,
  queryTags
} from '@/api/book'

defineOptions({
  name: 'Menu2'
})

// 国际化
const { t } = useI18n()

// 列表对象
const state = reactive({
  books: [],
  clcs: [],
  tags: []
})

const { books } = toRefs(state)
const { clcs } = toRefs(state)
const { tags } = toRefs(state)

const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 查询条件对象
const queryForm = reactive({
  bookName: '',
  clcName: [],
  tags: [],
  author: '',
  page: 1
})

const visible = ref(false)

// 表单是否显示
const dialogFormVisible = ref(false)

// 标签输入框
const inputVisible = ref(false)

// 标签
const inputValue = ref('')

let bookId = ''

// 表单对象
interface Book {
  author: string
  binding: string
  bookDesc: string
  bookName: string
  clcCode: string
  clcName: any
  edition: string
  format: string
  isbn: string
  language: string
  pages: string
  pictures: string[]
  press: string
  pressDate: string
  pressPlace: string
  price: number
  words: string
  readOver: boolean
  tags: string[]
}

const bookForm = reactive<Book>({
  author: '',
  binding: '',
  bookDesc: '',
  bookName: '',
  clcCode: '',
  clcName: '',
  edition: '',
  format: '',
  isbn: '',
  language: '',
  pages: '',
  pictures: [],
  press: '',
  pressDate: '',
  pressPlace: '',
  price: 0.0,
  words: '',
  readOver: false,
  tags: []
})

// 页面初始化事件
onMounted(() => {
  findTypes()
  findTags()
  queryBook(1)
})

// 查询图书分类
const findTypes = () => {
  queryClcs().then((r) => {
    if (r) {
      state.clcs = r.data
    }
  })
}

// 查询图书标签
const findTags = () => {
  queryTags().then((r) => {
    if (r) {
      state.tags = r.data
    }
  })
}

// 查询图书列表
const queryBook = (p: number) => {
  currentPage.value = p
  queryForm.page = p
  query(queryForm).then((r) => {
    if (r) {
      state.books = r.data.data
      total.value = r.data.total
    }
  })
}

// 删除图书
const removeBook = (id: string) => {
  visible.value = false
  remove(id).then((r) => {
    if (r) {
      ElMessage({
        message: '删除图书成功',
        type: 'success'
      })
      queryBook(1)
    }
  })
}

// 根据主键查询图书
const findBookById = (id: string) => {
  queryById(id).then((r) => {
    if (r) {
      r.data.clcName = r.data.clcName.join('、')
      Object.assign(bookForm, r.data)
    }
  })
}

// 打开表单
const formRef = ref<FormInstance>()

const openBookForm = (id: string | undefined, formEl: FormInstance | undefined) => {
  dialogFormVisible.value = true
  if (id) {
    findBookById(id)
    bookId = id
  } else {
    bookId = ''
    resetForm(formEl)
  }
}

// 标签处理
const showInput = () => {
  inputVisible.value = true
}

const handleInputConfirm = () => {
  if (inputValue.value) {
    bookForm.tags.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

const handleClose = (tag: string) => {
  bookForm.tags.splice(bookForm.tags.indexOf(tag), 1)
}

// 关闭表单
const closeBookForm = () => {
  dialogFormVisible.value = false
}

// 根据isbn查询图书
const isbn = () => {
  queryByISBN(bookForm.isbn).then((r) => {
    if (r) {
      r.data.price = (r.data.price / 100).toFixed(2)
      r.data.pictures = eval(r.data.pictures)
      Object.assign(bookForm, r.data)
    }
  })
}

// 保存图书
const saveBook = (formEl: FormInstance | undefined) => {
  let book = { ...bookForm }
  book.clcName = book.clcName.split('、')
  if (!bookId) {
    create(book).then((r) => {
      if (r) {
        ElMessage({
          message: '创建图书成功',
          type: 'success'
        })
        resetForm(formEl)
        closeBookForm()
        queryBook(1)
      }
    })
  } else {
    delete book['_id']
    update(bookId, book).then((r) => {
      if (r) {
        ElMessage({
          message: '修改图书成功',
          type: 'success'
        })
        closeBookForm()
        queryBook(1)
      }
    })
  }
}

// 重置表单
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
  bookForm.pictures = []
}
</script>

<style scoped>
.my-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding-top: 10px;
}
</style>
