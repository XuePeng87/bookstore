<template>
  <ContentWrap :title="t('levelDemo.menu')">
    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column prop="date" label="Date" width="180" />
      <el-table-column prop="name" label="Name" width="180" />
      <el-table-column prop="address" label="Address" />
    </el-table>
  </ContentWrap>
</template>

<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import { onMounted } from 'vue'
import { queryByISBN, query, queryById, create, update, remove } from '@/api/book'

defineOptions({
  name: 'Menu2'
})

onMounted(() => {
  // queryByISBN('9787020024759')
  query({
    id: 1,
    name: ''
  })
  queryById('656ee18a77548c3097e837f2')
  // create({ name: 'java' })
  // update('656ee5db77548c3097e837f6', { name: 'python' })
  remove('656ee54f77548c3097e837f4')
})

const { t } = useI18n()

const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles'
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles'
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles'
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles'
  }
]
</script>
