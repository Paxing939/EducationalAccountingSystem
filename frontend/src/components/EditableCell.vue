<template>
  <div class="input-wrapper" @dblclick="edit">
    <input
      v-if="isEditing"
      type="text"
      :value="value"
      @input="$emit('update', $event.target.value)"
      @blur="isEditing = false"
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
  },
  setup() {
    const isEditing = ref(false);

    const edit = () => {
      isEditing.value = true;
    };

    return {
      isEditing,
      edit,
    };
  },
});
</script>

<style>
.input-wrapper {
  display: flex;
  align-items: center;
}

.input-wrapper input {
  width: 100%;
  border: none;
  outline: none;
}

.input-wrapper span {
  display: inline-block;
  width: 100%;
  padding: 4px;
}
</style>
