<template>
    <div style="position: relative;">
      <RegistrationModal v-if="showModal" @closeModal="closeRegistrationModal()" />
      <button style="margin: 10px;" @click="showRegistrationModal()">Добавить слушателя</button>
      <EditableTable
        :headers="headers"
        :items="items"
        :body-row-class-name="rowEditedStyle"
        sort-by="id"
        @update-field="updateItem($event.field, $event.id, $event.value)"
        @expand-row="graduating.includes($event.id) ? graduating.splice(graduating.indexOf($event.id), 1) : undefined"
      >
          <template #expand="item">
              <div class="expand-container">
                  <div style="display: flex; gap: 10px;">
                      <button @click="sendData(item.id)" :disabled="!modified_items.includes(item.id)">Отправить</button>
                      <span v-if="data_sent" :class="data_sent_good ? 'text-success' : 'text-danger'">{{ send_data_info }}</span>
                      <button @click="deleteData(item.id)">Удалить запись</button>
                      <button @click="calculateDates(item.id)">Рассчитать даты обучения</button>
                      <button @click="calculateDefaultDates(item.id)">Даты обучения по умолчанию</button>
                      <button @click="graduating.includes(item.id) ? graduating.splice(graduating.indexOf(item.id), 1) : graduating.push(item.id)">Выпуск</button>
                  </div>
                  <div v-if="graduating.includes(item.id)" style="display: flex; gap: 10px; width: 200px;">
                      <label for="start_date">Начало обучения</label>
                      <input type="date" id="start_date" :value="item.start_date" />
                      <label for="end_date">Окончание обучения</label>
                      <input type="date" id="end_date" :value="item.end_date" />
                      <label for="full_name">ФИО_Рус</label>
                      <input type="text" id="full_name" :value="item.full_name" />
                      <label for="education_type_id">Тип обучения</label>
                      <select id="education_type_id">
                          <option v-for="education_type in education_types" :value="education_type.id" :selected="education_type.id == item.education_type_id">{{ education_type.text }}</option>
                      </select>
                      <label for="profession">Профессия_Рус</label>
                      <input type="text" id="profession" :value="item.profession" />
                      <label for="degree">Разряд</label>
                      <input type="number" id="degree" :value="item.degree" />
                      <label for="grade_1">Оценка 1</label>
                      <input type="number" id="grade_1" :value="item.grade_1 ?? 8" />
                      <label for="grade_2">Оценка 2</label>
                      <input type="number" id="grade_2" :value="item.grade_2 ?? 8" />
                      <label for="full_name_bel">ФИО_Бел</label>
                      <input type="text" id="full_name_bel" :value="item.full_name_bel" />
                      <label for="profession_bel">Профессия_Бел</label>
                      <input type="text" id="profession_bel" :value="item.profession_bel" />
                      <label for="protocol_number">Протокол</label>
                      <input type="text" id="protocol_number" :value="item.protocol_number" />
                      <label for="grad_id">Рег. №</label>
                      <input type="text" id="grad_id" :value="item.grad_id" />
                      <label for="certificate_number">Свидетельство №</label>
                      <input type="text" id="certificate_number" :value="item.certificate_number" />
                  </div>
              </div>
          </template>
          <template #item-profession="item">
              <DropdownCell :options="professions" :value="item.profession" @update="updateProfession(item.id, $event)" />
          </template>
          <template #item-education_type_id="item">
              <SelectableCell :options="education_types" :value="item.education_type_id" @update="updateItem('education_type_id', item.id, $event); checkEducationType(item.id)" />
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
          <template #item-payments="item">
              <PaymentsCell :value="item.payments" @update="updateItem('payments', item.id, $event)" />
          </template>
          <template #item-total_payments="item">
              <span style="font-weight: bold;">{{ item.payments.reduce((aac, payment) => aac + payment.amount, 0) }}</span>
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
import moment from 'moment-business-days';
import Holidays from 'date-holidays';
import PaymentsCell from "./components/PaymentsCell.vue";

const holidays = new Holidays('BY');
moment.updateLocale('ru', {
    workingWeekdays: [1, 2, 3, 4, 5],
    holidays: holidays.getHolidays().map(h => h.date.split(' ')[0]),
    holidayFormat: 'YYYY-MM-DD',
});

export default defineComponent({
  setup() {

    const headers: EditableTableHeader[] = [
      {text: 'Кем направлен', value: 'referrer_organization', width: 350, editable: true},
      {text: '№ п/п', value: 'id', sortable: true},
      {text: 'Группа', value: 'group', editable: true, match: '^[0-9]+-[0-9][0-9]$'},
      {text: 'ФИО', value: 'full_name', sortable: true, width: 280, editable: true},
      {text: 'Срок обучения', value: 'term', sortable: true, editable: true, type: 'number', float_precision: 1, max: 100, min: 0},
      {text: 'Дата начала обучения', value: 'start_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата конца теории', value: 'theory_end_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата начала практики', value: 'practice_start_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата конца практики', value: 'practice_end_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата окончания занятий', value: 'end_date', sortable: true, editable: true, type: 'date'},
      {text: 'Дата экзамена', value: 'exam_date', sortable: true, width: 250, editable: true},
      {text: 'Профессия', value: 'profession', sortable: true, width: 280},
      {text: 'Разряд', value: 'degree'},
      {text: 'Тип обучения', value: 'education_type_id', sortable: true},
      {text: 'Телефон/логин для здачи зачетов', value: 'login', editable: true},
      {text: 'Эл. Почта', value: 'email', editable: true, match: '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
      {text: 'Год рождения', value: 'birth_date', sortable: true, editable: true, type: 'date'},
      {text: 'Образование', value: 'education_id', sortable: true},
      {text: 'Профессия до обучения', value: 'previous_profession', sortable: true, width: 250, editable: true},
      {text: 'Оплата', value: 'payment', sortable: true, editable: true, type: 'number', float_precision: 2, min: 0},
      {text: 'Организация где работает', value: 'organization', editable: true, width: 350},
      {text: '№ прот.', value: 'protocol_number', sortable: true},
      {text: 'Свидетельство', value: 'certificate_number', sortable: true},
      {text: 'Рег №', value: 'grad_id', sortable: true},
      {text: 'Теория, дни', value: 'theory_hours', editable: true},
      {text: 'Практика, дни', value: 'practice_hours', editable: true},
      {text: 'Организация для прохождения практики', value: 'practice_organization', editable: true, width: 350},
      {text: 'Статус', value: 'status', sortable: true},
      {text: 'Платежи', value: 'payments'},
      {text: 'Всего оплачено', value: 'total_payments'},
      {text: 'Комментарии', value: 'comments', editable: true, width: 350},
    ];

    const items = ref<Item[]>([]);
    const professions = ref<DropdownOption[]>([]);
    const education_types = ref<SelectOption[]>([]);
    const educations = ref<SelectOption[]>([]);
    const student_statuses = ref<SelectOption[]>([]);

    interface ProfessionsHours {
        id: number;
        duration: number;
        theory_hours: number;
        practice_hours: number;
    }

    const professions_hours = ref<ProfessionsHours[]>([]);

    const modified_items = ref<number[]>([]);
    const graduating = ref<number[]>([]);

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
          for (const item of items.value) {
            item.payments = item.payments ?? [];
          }
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
            console.error('Fetch error: ', error);
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

    const loadProfessionsHours = async () => {
        try {
            const response = await fetch('http://localhost:8001/professions_hours');
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            professions_hours.value = await response.json();
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
        await loadProfessionsHours();
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

    const checkEducationType = (student_id: number) => {
        const item = items.value.find(item => item.id === student_id);
        if (item) {
            if (item.education_type_id == 3) {
                updateItem('previous_profession', student_id, `${item.profession} ${item.degree - 1}-го разряда`);
            }
        }
    }

    const sendData = async (id: number) => {
        try {
            const item = items.value.find(item => item.id === id);
            if (item) {
                const entity = JSON.parse(JSON.stringify(item));
                delete entity.education_categories;
                entity.comments = entity.comments ?? '';
                const response = await fetch('http://localhost:8000/students/edit', {
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

    const calculateDates = (id: number) => {
        const item = items.value.find(item => item.id === id);
        if (item) {
            const term = item.term;
            const hours = professions_hours.value.find(hours => hours.duration == term) ?? { theory_hours: 0, practice_hours: 0 };
            item.theory_hours = hours.theory_hours;
            item.practice_hours = hours.practice_hours;
            item.theory_end_date = moment(item.start_date).businessAdd(hours.theory_hours - 2);
            item.practice_start_date = item.theory_end_date.businessAdd(1);
            item.practice_end_date = item.practice_start_date.businessAdd(hours.practice_hours - 1);
            item.end_date = item.practice_end_date.businessAdd(1);
            modified_items.value.push(id);
        }
    }

    const calculateDefaultDates = async (id: number) => {
        try {
            const item = items.value.find(item => item.id === id);
            if (item) {
                const result = await fetch(`http://localhost:8001/professions/by/name/${item.profession}`);
                if (!result.ok) {
                    throw new Error('Network response was not ok ' + result.statusText);
                }
                const profession = await result.json();
                item.term = ((profession?.education_durations[profession?.education_categories.findIndex((c: string) => c.includes(item.degree.toString()))] ?? 0) * (item.education_type_id == 2 ? 0.6 : 1)).toFixed(1);
                calculateDates(id);
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
        await loadProfessionCategories();
    }

    return {
      headers,
      items,
      professions,
      education_types,
      educations,
      student_statuses,
      modified_items,
      graduating,
      data_sent,
      data_sent_good,
      send_data_info,
      getHeaderIndex,
      getValueByIndex,
      updateItem,
      updateProfession,
      checkEducationType,
      sendData,
      deleteData,
      calculateDates,
      calculateDefaultDates,
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
    PaymentsCell,
  },
});
</script>

<style>
.expand-container {
  padding: 15px;
  display: flex;
  gap: 10px;
  flex-direction: column;
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
