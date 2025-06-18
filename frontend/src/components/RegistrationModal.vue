<template>
    <dialog class="student-registration-modal" @close="close">
        <form class="student-registration-form" v-on:submit.prevent>
            <label for="referrer_organization">Кем направлен</label>
            <input type="text" id="referrer_organization" v-model="referrer_organization" @blur="$event.target.value ? this.organization = $event.target.value : undefined">
            <label for="group">Группа</label>
            <input type="text" id="group" v-model="group">
            <label for="full_name">ФИО</label>
            <input type="text" id="full_name" v-model="full_name">
            <label for="profession">Профессия</label>
            <ModelListSelect
                :list="professions"
                option-value="id"
                option-text="name"
                v-model="profession_id"
                id="profession"
                @update:modelValue="fillPreviousProfession()"
            />
            <label for="degree">Разряд</label>
            <ModelSelect
                :options="getProfessionCategories(profession_id)"
                v-model="degree"
                :isDisabled="profession_id === 0"
                id="degree"
                @update:modelValue="fillPreviousProfession()"
            />
            <label for="start_date">Дата начала обучения</label>
            <input type="date" id="start_date" v-model="start_date" @blur="checkStartDate($event.target.value) ? undefined : this.start_date = ''">
            <label for="education_type_id">Тип обучения</label>
            <ModelListSelect
                :list="getEducationTypes(profession_id)"
                option-value="id"
                option-text="name"
                v-model="education_type_id"
                id="education_type_id"
                @update:modelValue="fillPreviousProfession()"
                :isDisabled="this.education_id == 1"
            />
            <label for="birth_date">Дата рождения</label>
            <input type="date" id="birth_date" v-model="birth_date" @blur="checkBirthDate($event.target.value) ? undefined : this.birth_date = ''">
            <label for="education_id">Образование</label>
            <ModelListSelect
                :list="educations"
                option-value="id"
                option-text="name"
                v-model="education_id"
                id="education_id"
                @update:modelValue="this.education_id == 1 ? this.education_type_id = 2 : undefined"
            />
            <label for="previous_profession">Профессия до обучения</label>
            <input type="text" id="previous_profession" v-model="previous_profession">
            <label for="payment">Оплата</label>
            <input type="number" id="payment" v-model="payment">
            <label for="organization">Организация где работает</label>
            <input type="text" id="organization" v-model="organization">
            <label for="comments">Комментарии</label>
            <textarea id="comments" v-model="comments"></textarea>
            <button @click="addStudent">Добавить</button>
        </form>
        <button @click="close">Назад</button>
    </dialog>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { ModelListSelect, ModelSelect } from "vue-search-select";
import "vue-search-select/dist/VueSearchSelect.css";
import moment from 'moment-business-days';
import Holidays from 'date-holidays';

const holidays = new Holidays('BY');
moment.updateLocale('ru', {
    workingWeekdays: [1, 2, 3, 4, 5],
    holidays: holidays.getHolidays().map(h => h.date.split(' ')[0]),
    holidayFormat: 'YYYY-MM-DD',
});

export default defineComponent({
  setup() {
    const referrer_organization = ref<string>('');
    const group = ref<string>('');
    const full_name = ref<string>('');
    const start_date = ref<Date>(new Date());
    const profession_id = ref<number>(0);
    const degree = ref<number>(0);
    const education_type_id = ref<number>(0);
    const birth_date = ref<Date>(new Date());
    const education_id = ref<number>(0);
    const previous_profession = ref<string>('');
    const payment = ref<number>(0);
    const organization = ref<string>('');
    const comments = ref<string>('');

    interface Profession {
        id: number;
        name: string;
        education_categories: string[];
        education_durations: number[];
        retraining_only: boolean;
    }

    interface Education {
        id: number;
        name: string;
    }

    interface EducationType {
        id: number;
        name: string;
    }
    
    interface ProfessionsHours {
        id: number;
        duration: number;
        theory_hours: number;
        practice_hours: number;
    }

    const professions = ref<Profession[]>([]);
    const educations = ref<Education[]>([]);
    const education_types = ref<EducationType[]>([]);
    const education_types_retraining_only = ref<EducationType[]>([]);
    const professions_hours = ref<ProfessionsHours[]>([]);
    
    onMounted(async () => {
      try {
        var response = await fetch('http://localhost:8000/professions');
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        professions.value = await response.json();

        response = await fetch('http://localhost:8000/educations');
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        educations.value = await response.json();

        response = await fetch('http://localhost:8000/education_types');
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        education_types.value = await response.json();
        education_types_retraining_only.value = education_types.value.filter(type => type.id != 1 && type.id != 4);

        response = await fetch('http://localhost:8000/professions_hours');
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        professions_hours.value = await response.json();
      } catch (error) {
        console.error('Fetch error: ', error);
      }
    });

    const getEducationTypes = (profession_id: number) => {
        const profession = professions.value.find(profession => profession.id === profession_id);
        if (profession) {
            return profession.retraining_only ? education_types_retraining_only.value : education_types.value;
        }
        return education_types.value;
    }

    const getProfessionCategories = (profession_id: number) => 
        professions.value.find(profession => profession.id === profession_id)?.education_categories.flatMap(c => c.split(',').map(c => ({ value: c.trim(), text: c.trim() }))) ?? [];


    return {
        referrer_organization,
        group,
        full_name,
        start_date,
        profession_id,
        degree,
        education_type_id,
        birth_date,
        education_id,
        previous_profession,
        payment,
        organization,
        comments,
        professions,
        educations,
        education_types,
        professions_hours,
        getEducationTypes,
        getProfessionCategories,
    };
  },
  mounted() {
    this.$el.showModal();
  },
  methods: {
    async close() {
        this.$emit('closeModal');
    },
    checkStartDate(start_date: string | Date) {
        const date = moment(start_date);
        const today = moment();
        const diff_days = today.diff(date, 'days');
        if (diff_days > 10) {
            alert('Дата начала не может быть раньше 10 дней от текущей даты')   
            return false;
        }
        const diff_months = today.diff(date, 'months', true);
        if (diff_months < -3) {
            alert('Дата начала не может быть позже 3 месяцев от текущей даты')
            return false;
        }
        return true;
    },
    fillPreviousProfession() {
        if (this.education_type_id == 3) {
            const profession = this.professions.find(profession => profession.id === this.profession_id)?.name;
            if (profession && this.degree > 1) {
                this.previous_profession = profession + ` ${this.degree - 1}-го разряда`;
            }
        }
    },
    checkBirthDate(birth_date: string | Date) {
        const date = moment(birth_date);
        const today = moment();
        const diff_days = today.diff(date, 'years', true);
        if (diff_days > 100) {
            alert('Дата рождения не может быть раньше 100 лет от текущей даты')
            return false;
        }
        if (diff_days < 17.5) {
            alert('Дата рождения не может быть позже 17 лет и 6 месяцев от текущей даты')
            return false;
        }
        return true;
    },
    async addStudent () {
        try {
            if (this.profession_id === 0) {
                alert('Профессия не выбрана');
                throw new Error('Profession is not selected');
            }
            if (!this.checkStartDate(this.start_date)) {
                throw new Error('Start date is invalid');
            }
            const profession = this.professions.find(profession => profession.id === this.profession_id);
            const term = (profession?.education_durations[profession?.education_categories.findIndex(c => c.includes(this.degree.toString()))] ?? 0) * (this.education_type_id == 2 ? 0.6 : 1);
            const hours = this.professions_hours.find(hours => hours.duration == term) ?? { theory_hours: 0, practice_hours: 0 };
            const theory_end_date = moment(this.start_date).businessAdd(hours.theory_hours - 2);
            const practice_start_date = theory_end_date.businessAdd(1);
            const practice_end_date = practice_start_date.businessAdd(hours.practice_hours - 1);
            const end_date = practice_end_date.businessAdd(1);

            const response = await fetch('http://localhost:8000/students/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    referrer_organization: this.referrer_organization,
                    group: this.group,
                    full_name: this.full_name,
                    term: term,
                    start_date: moment(this.start_date).format('YYYY-MM-DD'),
                    theory_end_date: theory_end_date.format('YYYY-MM-DD'),
                    practice_start_date: practice_start_date.format('YYYY-MM-DD'),
                    practice_end_date: practice_end_date.format('YYYY-MM-DD'),
                    end_date: end_date.format('YYYY-MM-DD'),
                    exam_date: undefined,
                    profession: profession?.name,
                    degree: this.degree,
                    education_type_id: this.education_type_id,
                    login: '',
                    email: undefined,
                    birth_date: moment(this.birth_date).format('YYYY-MM-DD'),
                    education_id: this.education_id,
                    previous_profession: this.previous_profession,
                    payment: this.payment,
                    organization: this.organization ?? this.referrer_organization,
                    protocol_number: '',
                    certificate_number: undefined,
                    grad_id: undefined,
                    theory_hours: hours.theory_hours,
                    practice_hours: hours.practice_hours,
                    practice_organization: this.referrer_organization,
                    status: 1,
                    payments: [],
                    comments: this.comments,
                    graduation_date: end_date.format('YYYY-MM-DD'),
                    grade_1: undefined,
                    grade_2: undefined,
                    full_name_bel: '',
                    profession_bel: '',
                }),
            });
            
            this.close();
        } catch (error) {
            console.error('Fetch error: ', error);
        }
    }
  },
  components: {
    ModelListSelect,
    ModelSelect,
  },
});
</script>

<style>
.student-registration-modal {
    width: 500px;
    max-width: 80%;
    max-height: 90%;
    overflow-x: hidden;
}

.student-registration-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
}

.student-registration-form input, .student-registration-form textarea {
    border: 1px solid #22242626;
    height: 2em;
    border-radius: 5px;
}
</style>
