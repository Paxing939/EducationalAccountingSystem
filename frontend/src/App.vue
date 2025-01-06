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
  </EasyDataTable>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import type {Header, Item} from "vue3-easy-data-table";

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

    return {
      headers,
      items
    };
  },
});
</script>
