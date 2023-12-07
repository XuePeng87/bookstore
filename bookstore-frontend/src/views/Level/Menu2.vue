<template>
  <ContentWrap :title="t('levelDemo.menu')">
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
      <el-table-column fixed="right" label="Operations" width="240">
        <template #default>
          <el-button link type="primary">Detail</el-button>
          <el-button link type="primary">Edit</el-button>
          <el-button link type="primary">Remove</el-button>
        </template>
      </el-table-column>
    </el-table>
  </ContentWrap>
</template>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import { onMounted, reactive, toRefs } from 'vue'
import { queryByISBN, query, queryById, create, update, remove } from '@/api/book'

defineOptions({
  name: 'Menu2'
})

const { t } = useI18n()

const state = reactive({
  books: []
})

const { books } = toRefs(state)

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
</script>
