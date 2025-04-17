<template>
  <div class="input-wrapper" @dblclick="edit">
    <dialog class="dropdown-modal">
        <ModelSelect
          :options
          :model-value="value"
          @update:model-value="newValue => $emit('update', newValue)"
          @blur="stop"
          id="model-select"
        />
    </dialog>
    <span v-if="!isEditing">{{ value }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue';
import { ModelSelect } from "vue-search-select";

export interface DropdownOption {
    value: any,
    text: String
}

export default defineComponent({
  props: {
    value: {
      required: true,
    },
    options: {
      type: Array as PropType<DropdownOption[]>,
      required: true,
    },
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
      this.$el.querySelector('dialog').showModal();
      this.$el.querySelector('#model-select').focus();
    },
    async stop() {
      this.isEditing = false;
      this.$el.querySelector('dialog').close();
    },
  },
  components: {
    ModelSelect,
  },
});
</script>

<style>
.input-wrapper {
  display: flex;
  align-items: center;
}

.input-wrapper span {
  display: inline-block;
  width: 100%;
  padding: 4px;
}

.dropdown-modal {
    min-height: 30%;
    min-width: 400px;
}
</style>
