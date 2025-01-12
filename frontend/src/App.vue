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
    <template #item-full_name="{ full_name }">
      <div class="input-wrapper">
        <input
          type="text"
          :value="full_name"
          @input="inputHandler(full_name, $event)"
        />
      </div>
    </template>
    <template #item-term="{ term }">
      <div class="input-wrapper">
        <input
          type="text"
          :value="term"
          @input="inputHandler(term, $event)"
        />
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

    const inputHandler = (some_value: string, e: string) => {
      some_value = e;
    };

    const isEditing = ref(false);

    const deleteItem = (val: Item) => {
      items.value = items.value.filter((item) => item.id !== val.id);
    };

    return {
      headers,
      items,
      deleteItem,
      isEditing,
      inputHandler,
    };
  },
});
</script>

<style>
.input-wrapper {
  padding: 2px;
  box-sizing: border-box;
  max-height: 3em !important; /* Adjust this value as needed */
  overflow: hidden !important;
  display: flex !important;
  align-items: center !important;
  line-height: 1.5 !important; /* Adjust line height */
  border: none !important; /* Remove border from input wrapper */
}

.input-wrapper input {
  box-sizing: border-box !important;
  max-height: 100% !important;
  width: 100% !important; /* Make sure the input field uses the full width of the cell */
  white-space: pre-wrap !important; /* Make sure text wraps properly */
  word-wrap: break-word !important;
  line-height: inherit !important; /* Inherit line height from the wrapper */
  border: none !important; /* Remove border from the input field */
  outline: none !important; /* Remove outline from the input field */
}
</style>
