<template>
  <div class="input-wrapper" @dblclick="edit">
    <input
      v-if="isEditing"
      :value
      :type
      @input="$emit('update', $event.target.value)"
      @blur="isEditing = false"
      @keyup.enter="isEditing = false"
    />
    <span v-else>{{ value }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    value: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: false,
      default: 'text',
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
      this.$el.querySelector('input').focus();
    },
  },
});
</script>

<style>
.input-wrapper {
  display: flex;
  align-items: center;
}

.input-wrapper input {
  flex: 1;
  width: 100%;
  border: none;
  outline: none;
  background: none;
  font: inherit;
}

.input-wrapper input:focus {
    width: 100%;
}

.input-wrapper span {
  display: inline-block;
  width: 100%;
  padding: 4px;
}
</style>
