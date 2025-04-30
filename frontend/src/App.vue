<template>
    <div class="page">
        <div class="tabs">
            <div :class="{'tab': true, 'active': activeTab == index}" v-for="(tab, index) in tabs" @click="activeTab = index">{{ tab }}</div>
        </div>
        <div>
            <Students v-if="activeTab == 0" />
            <Professions v-if="activeTab == 1" />
        </div>
    </div>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';

export default defineComponent({
    setup() {
        const tabs = ['Студенты', 'Профессии'];
        const activeTab = ref(0);
        return {
            tabs,
            activeTab,
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
