<template>
  <ContentWrap :title="t('levelDemo.menu')">
    <el-form :inline="true" :model="queryForm">
      <el-form-item label="书名">
        <el-input v-model="queryForm.bookName" clearable />
      </el-form-item>
      <el-form-item label="类型">
        <el-select v-model="queryForm.clcName" clearable>
          <el-option label="Zone one" value="shanghai" />
          <el-option label="Zone two" value="beijing" />
        </el-select>
      </el-form-item>
      <el-form-item label="作者">
        <el-input v-model="queryForm.author" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="queryBook">查询</el-button>
      </el-form-item>
    </el-form>
    <el-button type="primary" @click="createBook">创建</el-button>
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
        <template #default>
          <el-button link type="primary">详情</el-button>
          <el-button link type="primary">修改</el-button>
          <el-button link type="primary">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="margin-top: 10px">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="100"
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
        <el-button type="primary">保存</el-button>
        <el-button>重置</el-button>
        <el-button type="danger" @click="close">关闭</el-button>
      </div>
    </template>
    <el-form :model="bookForm" label-width="120px" status-icon>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="ISBN" prop="isbn">
            <el-input v-model="bookForm.isbn" :prefix-icon="Search" @keyup.enter="isbn" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="名称" prop="bookName">
            <el-input v-model="bookForm.bookName" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="简介" prop="bookDesc">
        <el-input v-model="bookForm.bookDesc" type="textarea" :rows="10" />
      </el-form-item>
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
      <el-row :gutter="24">
        <el-col :span="4" />
        <el-col :span="20">
          <div v-for="pic in bookForm.pictures" :key="pic">
            <el-image style="width: 100px; height: 150px" :src="pic" />
          </div>
        </el-col>
      </el-row>
    </el-form>
  </el-dialog>
</template>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import { onMounted, reactive, toRefs, ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { queryByISBN, query, queryById, create, update, remove } from '@/api/book'

defineOptions({
  name: 'Menu2'
})

const { t } = useI18n()

const dialogFormVisible = ref(false)

const queryForm = reactive({
  bookName: '',
  clcName: '',
  author: '',
  page: 1
})

interface Book {
  author: string
  binding: string
  bookDesc: string
  bookName: string
  clcCode: string
  clcName: string
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
  readOver: false
})

const state = reactive({
  books: []
})

const { books } = toRefs(state)

const inputRef = ref<Nullable<any>>(null)

onMounted(() => {
  // queryByISBN('9787020024759')
  query({}).then((r) => {
    state.books = r.data
  })
  // queryById('656ee18a77548c3097e837f2')
  // create({ name: 'java' })
  // update('656ee5db77548c3097e837f6', { name: 'python' })
  // remove('656ee54f77548c3097e837f4')
})

const isbn = () => {
  queryByISBN(bookForm.isbn).then((r) => {
    if (r) {
      r.data.price = (r.data.price / 100).toFixed(2)
      r.data.pictures = eval(r.data.pictures)
      Object.assign(bookForm, r.data)
      console.info('bookForm', bookForm)
    }
  })
}

const queryBook = () => {}

const createBook = () => {
  dialogFormVisible.value = true
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
