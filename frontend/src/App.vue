<template>
  <EasyDataTable
      :headers="headers"
      :items="items"
      alternating
      border-cell
  >
    <template #expand="item">
      <div style="padding: 15px">
        {{ item.full_name }} will study for {{ item.term }} months
      </div>
    </template>
<!--    <template #item-full_name="{ full_name }">-->
<!--      <div class="input-wrapper">-->
<!--        <input-->
<!--          type="text"-->
<!--          :value="full_name"-->
<!--          @input="inputHandler(full_name, $event)"-->
<!--        />-->
<!--      </div>-->
<!--    </template>-->
<!--    <template #item-term="{ term }">-->
<!--      <div class="input-wrapper">-->
<!--        <input-->
<!--          type="text"-->
<!--          :value="term"-->
<!--          @input="inputHandler(term, $event)"-->
<!--        />-->
<!--      </div>-->
<!--    </template>-->

<!--    <template v-for="header in headers" :key="header.value" v-slot:[`item-${header.value}`]="{ item }">-->
<!--      <EditableCell-->
<!--          :value="getValueByIndex(item, getHeaderIndex(header.value))"-->
<!--          @update="updateItem(header.value, item.id, $event)"-->
<!--      />-->
<!--    </template>-->
    <template #item-full_name="{ full_name }">
<!--      {{ full_name }}-->
      <EditableCell
          :value="full_name"
          @update="updateItem('full_name', item.id, $event)"
      />
    </template>

  </EasyDataTable>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import type {Header, Item} from "vue3-easy-data-table";
import EditableCell from "./components/EditableCell.vue";

export default defineComponent({
  setup() {

// 'Дата начала обучения', 'Дата конца теории', 'Дата начала практики', 'Дата конца практики',
// 'Дата окончания занятий', 'Дата экзамена',
// 'Телефон/логин для сдачи зачетов', 'Эл. Почта',
// '№ прот.', 'Свидетельство', 'Рег №', 'Теория часы', 'Практика часы',
// 'Комментарии'

    const headers: Header[] = [
      {text: 'Кем направлен', value: 'referrer_organization'},
      {text: '№ п/п', value: 'id', sortable: true},
      {text: 'Группа', value: 'group'},
      {text: 'ФИО', value: 'full_name', sortable: true},
      {text: 'Срок обучения', value: 'term', sortable: true},
      {text: 'Профессия', value: 'profession', sortable: true},
      {text: 'Разряд', value: 'degree'},
      {text: 'Тип обучения', value: 'education_type_id', sortable: true},
      {text: 'Год рождения', value: 'birth_date', sortable: true},
      {text: 'Образование', value: 'education_id', sortable: true},
      {text: 'Профессия до обучения', value: 'previous_profession', sortable: true},
      {text: 'Оплата', value: 'payment', sortable: true},
      {text: 'Организация где работает', value: 'organization'},
      {text: 'Организация для прохождения практики', value: 'practice_organization'},
      {text: 'Статус', value: 'status', sortable: true},
    ];

    const items = ref<Item[]>([]);

    onMounted(async () => {
      try {
        const response = await fetch('http://localhost:8000/students');
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        items.value = await response.json();
      } catch (error) {
        console.error('Fetch error: ', error);
      }
    });

    const getHeaderIndex = (value: string) => {
      return headers.findIndex(header => header.value === value);
    };

    const getValueByIndex = (item: Item, index: number) => {
      const key = headers[index].value;
      return item[key];
    };

    const updateItem = (field: string, id: number, value: string) => {
      const item = items.value.find(item => item.id === id);
      if (item) {
        item[field] = value;
      }
    };

    return {
      headers,
      items,
      getHeaderIndex,
      getValueByIndex,
      updateItem,
    };
  },
});
</script>

<style>
.input-wrapper {
  padding: 2px;
  box-sizing: border-box;
  max-height: 3em !important;
  overflow: hidden !important;
  display: flex !important;
  align-items: center !important;
  line-height: 1.5 !important;
  border: none !important;
}

.input-wrapper input {
  box-sizing: border-box !important;
  max-height: 100% !important;
  width: 100% !important;
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
  line-height: inherit !important;
  border: none !important;
  outline: none !important;
}
</style>
