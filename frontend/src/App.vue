<template>
    <div style="position: relative;">
      <RegistrationModal v-if="showModal" @closeModal="closeRegistrationModal()" />
      <button @click="showRegistrationModal()">Добавить слушателя</button>
      <EditableTable
        :headers="headers"
        :items="items"
        :body-row-class-name="rowEditedStyle"
        @updateField="updateItem($event.field, $event.id, $event.value)"
      >
          <template #expand="item">
              <div class="expand-container">
                  <button @click="sendData(item.id)" :disabled="!modified_items.includes(item.id)">Отправить</button>
                  <span v-if="data_sent" :class="data_sent_good ? 'text-success' : 'text-danger'">{{ send_data_info }}</span>
                  <button @click="deleteData(item.id)">Удалить запись</button>
              </div>
          </template>
          <template #item-profession="item">
              <DropdownCell :options="professions" :value="item.profession" @update="updateProfession(item.id, $event)" />
          </template>
          <template #item-education_type_id="item">
              <SelectableCell :options="education_types" :value="item.education_type_id" @update="updateItem('education_type_id', item.id, $event)" />
          </template>
          <template #item-education_id="item">
              <SelectableCell :options="educations" :value="item.education_id" @update="updateItem('education_id', item.id, $event)" />
          </template>
          <template #item-degree="item">
              <SelectableCell :options="item.education_categories ?? []" :value="item.degree" @update="updateItem('degree', item.id, $event)" />
          </template>
          <template #item-status="item">
              <SelectableCell :options="student_statuses" :value="item.status" @update="updateItem('status', item.id, $event)" />
          </template>
      </EditableTable>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import type {Header, Item} from "vue3-easy-data-table";
import EditableCell from "./components/EditableCell.vue";
import RegistrationModal from "./components/RegistrationModal.vue";
import type { EditableTableHeader } from "./components/EditableTable.vue";
import EditableTable from "./components/EditableTable.vue";
import type { DropdownOption } from "./components/DropdownCell.vue";
import DropdownCell from "./components/DropdownCell.vue";
import type { SelectOption } from "./components/SelectableCell.vue";
import SelectableCell from "./components/SelectableCell.vue";

export default defineComponent({
  setup() {

    const headers: EditableTableHeader[] = [
      {text: 'Кем направлен', value: 'referrer_organization', width: 200, editable: true},
      {text: '№ п/п', value: 'id', sortable: true},
      {text: 'Группа', value: 'group', editable: true},
      {text: 'ФИО', value: 'full_name', sortable: true, width: 280, editable: true},
      {text: 'Срок обучения', value: 'term', sortable: true, editable: true, type: 'number', float_precision: 1, max: 100, min: 0},
      {text: 'Дата начала обучения', value: 'start_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата конца теории', value: 'theory_end_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата начала практики', value: 'practice_start_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата конца практики', value: 'practice_end_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата окончания занятий', value: 'end_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата экзамена', value: 'exam_date', sortable: true, editable: true, type: 'date'},
      {text: 'Профессия', value: 'profession', sortable: true, width: 280},
      {text: 'Разряд', value: 'degree'},
      {text: 'Тип обучения', value: 'education_type_id', sortable: true},
      {text: 'Телефон/логин для здачи зачетов', value: 'login', editable: true},
      {text: 'Эл. Почта', value: 'email', editable: true},
      {text: 'Год рождения', value: 'birth_date', sortable: true, editable: true, type: 'date'},
      {text: 'Образование', value: 'education_id', sortable: true},
      {text: 'Профессия до обучения', value: 'previous_profession', sortable: true, width: 200, editable: true},
      {text: 'Оплата', value: 'payment', sortable: true, editable: true, type: 'number', float_precision: 2, min: 0},
      {text: 'Организация где работает', value: 'organization', editable: true, width: 200},
      {text: '№ прот.', value: 'protocol_number', sortable: true},
      {text: 'Свидетельство', value: 'certificate_number', sortable: true},
      {text: 'Рег №', value: 'grad_id', sortable: true},
      {text: 'Теория, часы', value: 'theory_hours', editable: true},
      {text: 'Практика, часы', value: 'practice_hours', editable: true},
      {text: 'Организация для прохождения практики', value: 'practice_organization', editable: true, width: 200},
      {text: 'Статус', value: 'status', sortable: true},
      {text: 'Комментарии', value: 'comments', editable: true, width: 300},
    ];

    const items = ref<Item[]>([]);
    const professions = ref<DropdownOption[]>([]);
    const education_types = ref<SelectOption[]>([]);
    const educations = ref<SelectOption[]>([]);
    const student_statuses = ref<SelectOption[]>([]);

    const modified_items = ref<number[]>([]);

    const data_sent = ref<Boolean>(false);
    const data_sent_good = ref<Boolean>(false);
    const send_data_info = ref<String>('');

    const showModal = ref<Boolean>(false);

    const loadStudents = async () => {
        try {
          const response = await fetch('http://localhost:8000/students');
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
          items.value = await response.json();
        } catch (error) {
          console.error('Fetch error: ', error);
        }
    };

    const loadProfessions = async () => {
        try {
          const response = await fetch('http://localhost:8001/professions');
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
          const professions_entity: [{id: number, name: String}] = await response.json();
          professions.value = professions_entity.map(profession => ({ value: profession.id, text: profession.name }));
        } catch (error) {
          console.error('Fetch error: ', error);
        }
    };

    const loadEducationTypes = async () => {
        try {
            const response = await fetch('http://localhost:8000/education_types');
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            education_types.value = (await response.json()).map((education_type: {id: number, name: String}) => ({ value: education_type.id, text: education_type.name }));
        } catch (error) {
            console.error('Fetch error: ', error);
        }
    }

    const loadEducations = async () => {
        try {
            const response = await fetch('http://localhost:8000/educations');
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            educations.value = (await response.json()).map((education: {id: number, name: String}) => ({ value: education.id, text: education.name }));
        } catch (error) {
            console.error('Fetch error: ', error);
        }
    }

    const loadStudentStatuses = async () => {
        try {
            const response = await fetch('http://localhost:8000/student_statuses');
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            student_statuses.value = (await response.json()).map((education: {id: number, name: String}) => ({ value: education.id, text: education.name }));
        } catch (error) {
            console.log('Fetch error: ', error);
        }
    }

    const loadProfessionCategories = async () => {
        try {
            const response = await fetch('http://localhost:8001/professions');
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const professions_entity: [{id: number, name: String, education_categories: String[]}] = await response.json();
            for (const student of items.value) {
                const profession = professions_entity.find(profession => profession.name === student.profession);
                if (profession) {
                    const categories = profession.education_categories.flatMap(c => c.split(',').map(c => ({ value: c.trim(), text: c.trim() })));
                    student.education_categories = categories;
                }
            }
        } catch (error) {
            console.error('Fetch error: ', error);
        }
    }

    onMounted(async () => {
        await loadStudents();
        await loadProfessions();
        await loadEducationTypes();
        await loadEducations();
        await loadStudentStatuses();
        await loadProfessionCategories();
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

    const updateProfession = async (student_id: number, profession_id: number) => {
        const item = items.value.find(item => item.id === student_id);
        if (item) {
            try {
                const profession = await fetch(`http://localhost:8001/professions/${profession_id}`);
                if (!profession.ok) {
                    throw new Error('Network response was not ok ' + profession.statusText);
                }
                const profession_entity: {name: string, education_categories: String[]} = await profession.json();
                item.profession = profession_entity.name;
                const categories = profession_entity.education_categories.flatMap(c => c.split(',').map(c => ({ value: parseInt(c.trim()), text: c.trim() })));
                item.education_categories = categories;
                if (!categories.find(category => category.value == item.degree)) {
                    item.degree = categories[0].value;
                }
                if (!modified_items.value.includes(student_id)) {
                    modified_items.value.push(student_id);
                }
            } catch (error) {
                console.error('Fetch error: ', error);
            }
        }
    };

    const sendData = async (id: number) => {
        try {
            const item = items.value.find(item => item.id === id);
            if (item) {
                const response = await fetch('http://localhost:8000/students/edit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(item),
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

    const deleteData = async (id: number) => {
        try {
            const item = items.value.find(item => item.id === id);
            if (item) {
                const response = await fetch(`http://localhost:8000/students/delete/${id}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                else {
                    items.value = items.value.filter(item => item.id !== id);
                }
            }
        } catch (error) {
            console.error('Fetch error: ', error);
        }
    }

    const showRegistrationModal = async () => {
        showModal.value = true;
    }

    const closeRegistrationModal = async () => {
        showModal.value = false;
        await loadStudents();
    }

    return {
      headers,
      items,
      professions,
      education_types,
      educations,
      student_statuses,
      modified_items,
      data_sent,
      data_sent_good,
      send_data_info,
      getHeaderIndex,
      getValueByIndex,
      updateItem,
      updateProfession,
      sendData,
      deleteData,
      showModal,
      showRegistrationModal,
      closeRegistrationModal,
      rowEditedStyle,
    };
  },
  components: {
    EditableCell,
    RegistrationModal,
    EditableTable,
    DropdownCell,
    SelectableCell,
  },
});
</script>

<style>
.expand-container {
  padding: 15px;
  display: flex;
  gap: 10px;
}

.text-success, .text-danger {
  font-weight: bold;
  font-size: 1.1em;
}

.text-success {
  color: #28a745;
}

.text-danger {
  color: #dc3545;
}

.edited td {
  background-color: #00a07c !important;
}
</style>
