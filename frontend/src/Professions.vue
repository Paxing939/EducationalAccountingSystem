<template>
    <div>
      <div style="margin: 10px;">
          <span>Поиск: </span>
          <input type="text" v-model="searchValue" />
      </div>
      <EditableTable
          :headers="headers"
          :items="items"
          :search-field="searchField"
          :search-value="searchValue"
          :rows-items="[100, 500, 1000]"
          :rows-per-page="100"
          :body-row-class-name="rowEditedStyle"
          table-class-name="professions-table"
          sort-by="id"
          @updateField="updateItem($event.field, $event.id, $event.value)"
      >
        <template #expand="item">
            <div class="expand-container">
                <div style="display: flex; gap: 10px;">
                    <button @click="sendData(item.id)" :disabled="!modified_items.includes(item.id)">Отправить</button>
                    <span v-if="data_sent" :class="data_sent_good ? 'text-success' : 'text-danger'">{{ send_data_info }}</span>
                </div>
            </div>
        </template>
        <template v-for="header in headers.slice(2, 10)" #[`item-${header.value}`]="item">
            <div class="terms-wrapper">
                <EditableCell :value="item[header.value][0]" @update="updateDuration(item.id, header.value.slice(9, 10), $event)" postfix=" мес." />
                <span v-for="val in item[header.value].slice(1)">{{ val }}</span>
            </div>
        </template>
        <template v-for="header in headers.slice(10, -7)" #[`item-${header.value}`]="item">
            <div class="terms-wrapper">
                <span>{{ item[header.value][0] ? item[header.value][0] + ' мес.' : ''}}</span>
                <span v-for="val in item[header.value].slice(1)">{{ val }}</span>
            </div>
        </template>
        <template #item-advance="item">
            <div class="terms-wrapper">
                <EditableCell :value="item.advance[0]" @update="updateItem('advance', item.id, $event)" postfix=" мес." />
                <span v-for="val in item.advance.slice(1)">{{ val }}</span>
            </div>
        </template>
      </EditableTable>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import type {EditableTableHeader, Item} from "./components/EditableTable.vue";
import EditableTable from "./components/EditableTable.vue";
import EditableCell from "./components/EditableCell.vue";

export default defineComponent({
  setup() {

    const headers: EditableTableHeader[] = [
      {text: 'Номер', value: 'id', fixed: true, sortable: true},
      {text: 'Название профессии', value: 'name', sortable: true, width: 400, fixed: true, editable: true},
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
      {text: 'Повышение квалификации', value: 'advance'},
      {text: 'Название профессии в программе бондаренко', value: 'bondarenko', editable: true, width: 280},
      {text: 'Белорусское Название профессии', value: 'name_bel', editable: true, width: 200},
      {text: 'Есть гугл ссылка', value: 'has_google_link', editable: true, type: 'checkbox'},
      {text: 'Есть зачеты', value: 'has_grades', editable: true, type: 'checkbox'},
      {text: 'Есть дневник', value: 'has_diary', editable: true, type: 'checkbox'},
      {text: 'Комментарии', value: 'comments', editable: true, width: 300},
    ];

    const items = ref<Item[]>([]);
    const hours = ref<{duration: number, theory_hours: number, practice_hours: number}[]>([])
    const searchField = 'name';
    const searchValue = ref<string>('');

    const modified_items = ref<number[]>([]);
    const data_sent = ref<Boolean>(false);
    const data_sent_good = ref<Boolean>(false);
    const send_data_info = ref<String>('');

    interface Profession {
        id: number,
        name: string,
        education_categories: string[],
        education_durations: string[],
        [key: string]: any
    };

    const parseProfessionCategories = async (profession: Profession | Item) => {
        try {
          if (hours.value.length == 0) {
              const hours_response = await fetch('http://localhost:8001/professions_hours');
              if (!hours_response.ok) {
                throw new Error('Network response was not ok ' + hours_response.statusText);
              }
              hours.value = await hours_response.json();
          }
          const categories = profession.education_categories.flatMap((c: string) => c.split(',')) ?? [];
          for (var i = 1; i <= 8; i++) {
              profession[`category_${i}`] = ['', '', ''];
              profession[`category_${i}_re`] = ['', '', ''];
          }
          for (const category of categories) {
              if (profession.education_durations) {
                  const term = parseFloat(profession.education_durations[profession.education_categories.findIndex((c: string) => c.includes(category))]) ?? 0;
                  const profession_hours = hours.value.find(hours => hours.duration == term) ?? { theory_hours: 0, practice_hours: 0 };
                  const term_re = +(term * 0.6).toFixed(1);
                  const profession_hours_re = hours.value.find(hours => hours.duration == term_re) ?? { theory_hours: 0, practice_hours: 0 };
                  profession[`category_${category}`] = [term, profession_hours.theory_hours, profession_hours.practice_hours];
                  profession[`category_${category}_re`] = [term_re, profession_hours_re.theory_hours, profession_hours_re.practice_hours];
              }
          }
          if (profession.advance) {
              const advance_hours = hours.value.find(hours => hours.duration == profession.advance) ?? { theory_hours: 0, practice_hours: 0 };
              profession['advance'] = [profession.advance, advance_hours.theory_hours, advance_hours.practice_hours];
          }
          else {
              profession['advance'] = ['', '', ''];
          }
        } catch (error) {
            console.error('Fetch error: ', error);
        }
    };

    const loadProfessions = async () => {
        try {
          const professions_response = await fetch('http://localhost:8001/professions');
          if (!professions_response.ok) {
            throw new Error('Network response was not ok ' + professions_response.statusText);
          }
          const professions: [] = await professions_response.json();
          for (const profession of professions) {
            await parseProfessionCategories(profession);
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
        if (!modified_items.value.includes(id)) {
          modified_items.value.push(id);
        }
        if (field == 'advance') {
          parseProfessionCategories(item);
        }
      }
    };

    const updateDuration = async (id: number, category: string, value: number) => {
      const item = items.value.find(item => item.id === id);
      if (item) {
        const index = item.education_categories.findIndex((c: string) => c.includes(category));
        if (index == -1) {
          item.education_categories.push(category);
          item.education_durations.push(value);
        }
        else {
          item.education_durations[index] = value;
        }
        await parseProfessionCategories(item);
        if (!modified_items.value.includes(id)) {
          modified_items.value.push(id);
        }
      }
    };

    const rowEditedStyle = (item: Item, rowNumber: number) => {
      if (modified_items.value.includes(item.id)) {
        return 'edited';
      }
      return '';
    };

    const sendData = async (id: number) => {
        try {
            const item = items.value.find(item => item.id === id);
            if (item) {
                const entity = JSON.parse(JSON.stringify(item));
                for (var i = 1; i <= 8; i++) {
                    delete entity[`category_${i}`];
                    delete entity[`category_${i}_re`];
                }
                delete entity.advance;
                entity.comments = entity.comments ?? '';
                const response = await fetch('http://localhost:8001/professions/edit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(entity),
                });
                data_sent.value = true;
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                    data_sent_good.value = false;
                    send_data_info.value = 'Что-то пошло не так';
                }
                else {
                    data_sent_good.value = true;
                    send_data_info.value = 'Данные успешно отправлены';
                    modified_items.value = modified_items.value.filter(id => id !== item.id);
                }
            }
        } catch (error) {
            console.error('Fetch error: ', error);
        }
    };

    return {
      headers,
      items,
      searchField,
      searchValue,
      updateItem,
      updateDuration,
      rowEditedStyle,
      modified_items,
      data_sent,
      data_sent_good,
      send_data_info,
      sendData,
    };
  },
  components: {
    EditableTable,
    EditableCell,
  },
});
</script>

<style>
.terms-wrapper {
    display: flex;
    height: 100%;
}

.terms-wrapper > * {
    flex: 1;
    text-align: center;
    padding: 5px;
}

.terms-wrapper > *:first-child {
    border-right: 1px solid #22242626;
    font-weight: bold;
    font-size: 1.2em;
}

.terms-wrapper > *:last-child {
    border-left: 1px solid #22242626;
}

.terms-wrapper > *:not(:first-child):not(:last-child) {
    border-left: 1px solid #22242626;
    border-right: 1px solid #22242626;
}

.professions-table table th:nth-child(n+4), .professions-table table td:nth-child(n+4) {
    background-color: #FF000030 !important;
}

.professions-table table th:nth-child(n+12), .professions-table table td:nth-child(n+12) {
    background-color: #00FF0030 !important;
}

.professions-table table th:nth-child(20), .professions-table table td:nth-child(20) {
    background-color: #0000FF30 !important;
}

.professions-table table th:nth-child(n+21) {
    background-color: var(--easy-table-header-background-color) !important;
}

.professions-table table td:nth-child(n+21) {
    background-color: var(--easy-table-row-background-color) !important;
}
</style>
