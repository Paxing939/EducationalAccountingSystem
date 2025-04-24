<template>
    <div style="display: flex; flex-direction: column; gap: 10px;">
        <div style="display: flex; gap: 10px;">
            <button v-for="(tab, index) in tabs" :key="index" @click="activeTab = index" :disabled="activeTab == index">{{ tab }}</button>
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
</style>
