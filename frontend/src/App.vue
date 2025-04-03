<template>
    <div>
      <RegistrationModal v-if="showModal" @closeModal="closeRegistrationModal()" />
      <button @click="showRegistrationModal()">Добавить слушателя</button>
      <EasyDataTable
          :headers="headers"
          :items="items"
          alternating
          border-cell
      > <template #expand="item">
          <div class="expand-container">
              <button @click="sendData(item.id)">Отправить</button>
              <span v-if="data_sent" :class="data_sent_good ? 'text-success' : 'text-danger'">{{ send_data_info }}</span>
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
        <template #item-full_name="{ id, full_name }">
    <!--      {{ full_name }}-->
          <EditableCell
              :value="full_name"
              @update="updateItem('full_name', id, $event)"
          />
        </template>

      </EasyDataTable>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import type {Header, Item} from "vue3-easy-data-table";
import EditableCell from "./components/EditableCell.vue";
import RegistrationModal from "./components/RegistrationModal.vue";

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
      {text: 'ФИО', value: 'full_name', sortable: true, width: 200},
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

    onMounted(async () => {
        await loadStudents();
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
                }
            }
        } catch (error) {
            console.error('Fetch error: ', error);
        }
    };

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
      data_sent,
      data_sent_good,
      send_data_info,
      getHeaderIndex,
      getValueByIndex,
      updateItem,
      sendData,
      showModal,
      showRegistrationModal,
      closeRegistrationModal,
    };
  },
  components: {
    EditableCell,
    RegistrationModal,
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
</style>
