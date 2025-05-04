<template>
    <div>
        <div style="display: flex; gap: 10px; margin: 10px;">
            <button @click="checkedAll = checkAll()">Проверить</button>
            <span v-if="checked" class="text-success">Все данные введены</span>
            <button @click="graduateAll()">Проверить и выпустить</button>
        </div>
        <EasyDataTable 
            :headers="headers"
            :items="students"
            alternating
            border-cell
        >
            <template #expand="item">
                <div class="expand-container">
                    <div style="display: flex; gap: 10px;">
                        <button @click="check(item.id) ? (checked_students.includes(item.id) ? undefined : checked_students.push(item.id)) : (checked_students.includes(item.id) ? checked_students.splice(checked_students.indexOf(item.id), 1) : undefined)">Проверить</button>
                        <span v-if="checked(item.id)" class="text-success">Все данные введены</span>
                        <button @click="graduate(item.id)">Проверить и выпустить</button>
                    </div>
                    <div style="display: flex; gap: 10px; width: 200px;">
                        <label for="start_date">Начало обучения</label>
                        <input type="date" id="start_date" :value="item.start_date" disabled />
                        <label for="end_date">Окончание обучения</label>
                        <input type="date" id="end_date" :value="item.end_date" disabled />
                        <label for="full_name">ФИО_Рус</label>
                        <input type="text" id="full_name" :value="item.full_name" disabled />
                        <label for="education_type_id">Тип обучения</label>
                        <select id="education_type_id" disabled>
                            <option>{{ education_types.find(education_type => education_type.id == item.education_type_id)?.name }}</option>
                        </select>
                        <label for="profession">Профессия_Рус</label>
                        <input type="text" id="profession" :value="item.profession" disabled />
                        <label for="degree">Разряд</label>
                        <input type="number" id="degree" :value="item.degree" disabled />
                        <label for="grade_1">Оценка 1</label>
                        <input type="number" id="grade_1" :value="item.grade_1" disabled />
                        <label for="grade_2">Оценка 2</label>
                        <input type="number" id="grade_2" :value="item.grade_2" disabled />
                        <label for="full_name_bel">ФИО_Бел</label>
                        <input type="text" id="full_name_bel" :value="item.full_name_bel" disabled />
                        <label for="profession_bel">Профессия_Бел</label>
                        <input type="text" id="profession_bel" :value="item.profession_bel" disabled />
                        <label for="protocol_number">Протокол</label>
                        <input type="text" id="protocol_number" :value="item.protocol_number" disabled />
                        <label for="grad_id">Рег. №</label>
                        <input type="text" id="grad_id" :value="item.grad_id" disabled />
                        <label for="certificate_number">Свидетельство №</label>
                        <input type="text" id="certificate_number" :value="item.certificate_number" disabled />
                    </div>
                </div>
            </template>
            <template #item-total_payments="item">
                <span style="font-weight: bold;">{{ item.payments.reduce((aac, payment) => aac + payment.amount, 0) }}</span>
            </template>
            <template #item-status="item">
                <span>{{ student_statuses.find(status => status.id == item.status)?.name }}</span>
            </template>
            <template #item-education_id="item">
                <span>{{ educations.find(education => education.id == item.education_id)?.name }}</span>
            </template>
            <template #item-education_type_id="item">
                <span>{{ education_types.find(education_type => education_type.id == item.education_type_id)?.name }}</span>
            </template>
        </EasyDataTable>
    </div>
</template>

<script lang="ts">
import {defineComponent, ref, onMounted, PropType} from 'vue';
import type {Header} from "vue3-easy-data-table";

interface Student {
    id: number,
    start_date: string,
    end_date: string,
    full_name: string,
    education_type_id: number,
    profession: string,
    degree: number,
    grade_1: number,
    grade_2: number,
    full_name_bel: string,
    profession_bel: string,
    protocol_number: string,
    grad_id: string,
    certificate_number: string,
    status: number,
    education_categories?: {'text': string, 'value': string}[],
}

export default defineComponent({
    props: {
        students: {
            type: Array as PropType<Student[]>,
            required: true,
        },
    },
    setup() {
        const headers: Header[] = [
          {text: 'Кем направлен', value: 'referrer_organization', width: 350},
          {text: '№ п/п', value: 'id', sortable: true},
          {text: 'Группа', value: 'group'},
          {text: 'ФИО', value: 'full_name', sortable: true, width: 280},
          {text: 'Срок обучения', value: 'term', sortable: true},
          {text: 'Дата начала обучения', value: 'start_date', sortable: true},
          {text: 'Дата конца теории', value: 'theory_end_date', sortable: true},
          {text: 'Дата начала практики', value: 'practice_start_date', sortable: true},
          {text: 'Дата конца практики', value: 'practice_end_date', sortable: true},
          {text: 'Дата окончания занятий', value: 'end_date', sortable: true},
          {text: 'Дата экзамена', value: 'exam_date', sortable: true, width: 250},
          {text: 'Профессия', value: 'profession', sortable: true, width: 280},
          {text: 'Разряд', value: 'degree'},
          {text: 'Тип обучения', value: 'education_type_id', sortable: true},
          {text: 'Телефон/логин для здачи зачетов', value: 'login'},
          {text: 'Эл. Почта', value: 'email'},
          {text: 'Год рождения', value: 'birth_date', sortable: true},
          {text: 'Образование', value: 'education_id', sortable: true},
          {text: 'Профессия до обучения', value: 'previous_profession', sortable: true, width: 250},
          {text: 'Оплата', value: 'payment', sortable: true},
          {text: 'Организация где работает', value: 'organization', width: 350},
          {text: '№ прот.', value: 'protocol_number', sortable: true},
          {text: 'Свидетельство', value: 'certificate_number', sortable: true},
          {text: 'Рег №', value: 'grad_id', sortable: true},
          {text: 'Теория, дни', value: 'theory_hours'},
          {text: 'Практика, дни', value: 'practice_hours'},
          {text: 'Организация для прохождения практики', value: 'practice_organization', width: 350},
          {text: 'Статус', value: 'status', sortable: true},
          {text: 'Платежи', value: 'payments'},
          {text: 'Всего оплачено', value: 'total_payments'},
          {text: 'Комментарии', value: 'comments', width: 350},
        ];

        const education_types = ref<[]>([]);
        const educations = ref<[]>([]);
        const student_statuses = ref<[]>([]);

        const checkedAll = ref<boolean>(false);
        const checked_students = ref<number[]>([]);

        const loadEducationTypes = async () => {
            try {
                const response = await fetch('http://localhost:8000/education_types');
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                education_types.value = await response.json();
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
                educations.value = await response.json();
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
                student_statuses.value = await response.json();
            } catch (error) {
                console.error('Fetch error: ', error);
            }
        }

        onMounted(async () => {
            const expand_buttons: NodeListOf<HTMLElement> = document.querySelectorAll('td.can-expand');
            for (const button of expand_buttons) {
                button.click();
                button.style.pointerEvents = 'none';
                const icon = button.querySelector('i');
                if (icon) {
                    icon.style.display = 'none';
                }
            }

            await loadEducationTypes();
            await loadEducations();
            await loadStudentStatuses();
        });

        return {
            headers,
            education_types,
            educations,
            student_statuses,
            checkedAll,
            checked_students,
        };
    },
    methods: {
        check(id: number) {
            const student = this.students.find(s => s.id == id);
            if (!student) {
                return false;
            }
            const label = `У слушателя №${student.id} `;
            if (!student.start_date)
            {
                alert(label + 'не указана дата начала обучения');
                return false;
            }
            if (!student.end_date)
            {
                alert(label + 'не указана дата окончания обучения');
                return false;
            }
            if (!student.full_name)
            {
                alert(label + 'не указан ФИО');
                return false;
            }
            if (!student.education_type_id)
            {
                alert(label + 'не указан тип обучения');
                return false;
            }
            if (!student.profession)
            {
                alert(label + 'не указана профессия');
                return false;
            }
            if (!student.degree)
            {
                alert(label + 'не указан разряд');
                return false;
            }
            if (!student.grade_1)
            {
                alert(label + 'не указана оценка 1');
                return false;
            }
            if (!student.grade_2)
            {
                alert(label + 'не указана оценка 2');
                return false;
            }
            if (!student.full_name_bel)
            {
                alert(label + 'не указан ФИО Бел');
                return false;
            }
            if (!student.profession_bel)
            {
                alert(label + 'не указана профессия Бел');
                return false;
            }
            if (!student.protocol_number)
            {
                alert(label + 'не указан протокол');
                return false;
            }
            if (!student.grad_id)
            {
                alert(label + 'не указан рег. №');
                return false;
            }
            if (!student.certificate_number)
            {
                alert(label + 'не указано свидетельство');
                return false;
            }
            return true;
        },
        checkAll() {
            for (const student of this.students) {
                if (!this.check(student.id)) {
                    return false;
                }
            }
            return true;
        },
        checked(id: number) {
            return this.checked_students.includes(id);
        },
        graduate(id: number) {
            if (this.check(id)) {
                const student = this.students.find(s => s.id == id);
                if (student) {
                    this.students.splice(this.students.indexOf(student), 1);
                    if (student) {
                        student.status = 3;
                        delete student.education_categories;
                        fetch(`http://localhost:8000/students/edit`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(student),
                        });
                    }
                }
            }
        },
        async graduateAll() {
            if (this.checkAll()) {
                while (this.students.length) {
                    const student = this.students.shift();
                    if (student) {
                        this.graduate(student.id);
                    }
                }
            }
        },
    },
});
</script>

<style>
</style>
