<template>
    <div class="page">
        <div class="tabs">
            <div :class="{'tab': true, 'active': activeTab == index}" v-for="(tab, index) in tabs" @click="activeTab = index">{{ tab }}</div>
        </div>
        <div>
            <Students :graduating_students="graduating_students" v-if="activeTab == 0" />
            <Professions v-if="activeTab == 1" />
            <Graduation :students="graduating_students" v-if="activeTab == 2" />
        </div>
    </div>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';

export default defineComponent({
    setup() {
        const tabs = ['Слушатели', 'Профессии', 'Выпуск'];
        const activeTab = ref(0);
        const graduating_students = ref([]);
        return {
            tabs,
            activeTab,
            graduating_students,
        };
    },
});
</script>

<style>
body {
    margin: 0;
    padding: 0;
}

.tabs {
    display: flex;
    width: 100%;
    background: #ccc;
}

.tab {
    width: 100px;
    padding: 10px;
    border-right: 1px solid #aaa;
    font-size: 14px;
    text-align: center;
}

.tab:hover {
    background: #ddd;
    cursor: pointer;
}

.tab.active {
    background: #fff;
}

.page {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
