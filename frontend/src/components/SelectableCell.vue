<template>
  <div class="input-wrapper" @dblclick="edit">
    <select
      v-if="isEditing"
      @change="$emit('update', $event.target.value); isEditing = false"
      @blur="isEditing = false"
    >
        <option v-for="option in options" :value="option.value" :selected="option.value == value">{{ option.text }}</option>
    </select>
    <span v-else>{{ options.find(option => option.value == value)?.text }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue';

export interface SelectOption {
    value: any,
    text: String
}

export default defineComponent({
  props: {
    value: {
      required: true,
    },
    options: {
      type: Array as PropType<SelectOption[]>,
      required: true,
    }
  },
  setup() {
    const isEditing = ref(false);

    return {
      isEditing,
    };
  },
  methods: {
    async edit() {
      this.isEditing = true;
      await this.$nextTick();
      this.$el.querySelector('select').focus();
      this.$el.querySelector('select').showPicker();
    },
  },
});
</script>

<style>
</style>
