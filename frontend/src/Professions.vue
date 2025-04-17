<template>
    <div>
      <EditableTable
          :headers="headers"
          :items="items"
          @updateField="updateItem($event.field, $event.id, $event.value)"
      >
      </EditableTable>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import type {EditableTableHeader, Item} from "./components/EditableTable.vue";
import EditableTable from "./components/EditableTable.vue";

export default defineComponent({
  setup() {

    const headers: EditableTableHeader[] = [
      {text: 'Номер', value: 'id', sortable: true},
      {text: 'Название профессии', value: 'name', sortable: true, width: 400, editable: true},
      {text: 'Подготовка разряд 1', value: 'category_1'},
      {text: 'Подготовка разряд 2', value: 'category_2'},
      {text: 'Подготовка разряд 3', value: 'category_3'},
      {text: 'Подготовка разряд 4', value: 'category_4'},
      {text: 'Подготовка разряд 5', value: 'category_5'},
      {text: 'Подготовка разряд 6', value: 'category_6'},
      {text: 'Подготовка разряд 7', value: 'category_7'},
      {text: 'Подготовка разряд 8', value: 'category_8'},
      {text: 'Переподготовка разряд 1', value: 'category_1_re'},
      {text: 'Переподготовка разряд 2', value: 'category_2_re'},
      {text: 'Переподготовка разряд 3', value: 'category_3_re'},
      {text: 'Переподготовка разряд 4', value: 'category_4_re'},
      {text: 'Переподготовка разряд 5', value: 'category_5_re'},
      {text: 'Переподготовка разряд 6', value: 'category_6_re'},
      {text: 'Переподготовка разряд 7', value: 'category_7_re'},
      {text: 'Переподготовка разряд 8', value: 'category_8_re'},
      {text: 'Название профессии в программе бондаренко', value: 'bondarenko', editable: true, width: 280},
      {text: 'Комментарии', value: 'comments', editable: true, width: 300},
    ];

    const items = ref<Item[]>([]);

    const loadProfessions = async () => {
        try {
          const professions_response = await fetch('http://localhost:8001/professions');
          if (!professions_response.ok) {
            throw new Error('Network response was not ok ' + professions_response.statusText);
          }
          const hours_response = await fetch('http://localhost:8001/professions_hours');
          if (!hours_response.ok) {
            throw new Error('Network response was not ok ' + hours_response.statusText);
          }
          const professions: {id: number, name: string, education_categories: string[], education_durations: string[], [key: string]: any}[] = await professions_response.json();
          const hours: {duration: number, theory_hours: number, practice_hours: number}[] = await hours_response.json();
          for (const profession of professions) {
              const categories = profession.education_categories.flatMap(c => c.split(',')) ?? [];
              for (const category of categories) {
                  if (profession.education_durations) {
                      const term = parseFloat(profession.education_durations[profession.education_categories.findIndex(c => c.includes(category))]) ?? 0;
                      const profession_hours = hours.find(hours => hours.duration == term) ?? { theory_hours: 0, practice_hours: 0 };
                      const term_re = +(term * 0.6).toFixed(1);
                      const profession_hours_re = hours.find(hours => hours.duration == term_re) ?? { theory_hours: 0, practice_hours: 0 };
                      profession[`category_${category}`] = [term, profession_hours.theory_hours, profession_hours.practice_hours];
                      profession[`category_${category}_re`] = [term_re, profession_hours_re.theory_hours, profession_hours_re.practice_hours];
                  }
              }
          }
          items.value = professions;
        } catch (error) {
          console.error('Fetch error: ', error);
        }
    };

    onMounted(async () => {
      await loadProfessions();
    });

    const updateItem = (field: string, id: number, value: string) => {
      const item = items.value.find(item => item.id === id);
      if (item) {
        item[field] = value;
      }
    };

    return {
      headers,
      items,
      updateItem,
    };
  },
  components: {
    EditableTable,
  },
});
</script>
