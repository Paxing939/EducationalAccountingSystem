<template>
  <div class="input-wrapper" @dblclick="edit">
    <input
      v-if="isEditing"
      :value
      :type
      @input="type == 'text' ? input($event) : undefined"
      @blur="stopEditing()"
      @keyup.enter="stopEditing()"
      :checked="type == 'checkbox' && value"
    />
    <span v-else>{{ type == 'date' && value ? new Date(value).toLocaleDateString() : (type == 'checkbox' ? (value ? 'да' : '') : value) }}{{ value ? postfix : '' }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    value: {
      required: true,
    },
    type: {
      type: String,
      required: false,
      default: 'text',
    },
    match: {
      type: String,
      required: false,
      default: '.*',
    },
    postfix: {
      type: String,
      required: false,
      default: '',
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
      const input = this.$el.querySelector('input');
      if (this.type == 'text') {
          input.style.width = '0px';
          input.style.width = `${input.scrollWidth}px`;
      }
      input.focus();
    },
    async stopEditing() {
      if (this.isEditing) {
          this.isEditing = false;
          const value = this.type == 'checkbox' ? this.$el.querySelector('input').checked : this.$el.querySelector('input').value;
          if (new RegExp(this.match).test(value)) {
            if (this.value != value) {
              this.$emit('update', value);
            }
          } else {
            alert('Неверный формат');
          }
      }
    },
    input(event: any) {
        event.target.style.width = '0px';
        event.target.style.width = `${event.target.scrollWidth}px`
    },
  },
});
</script>

<style>
.input-wrapper {
    
}

.input-wrapper input {
  border: none;
  outline: none;
  background: none;
  font: inherit;
}

.input-wrapper input:focus {
}

.input-wrapper span {
  display: inline-block;
  width: 100%;
  padding: 4px;
}
</style>
