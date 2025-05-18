<template>
  <div class="input-wrapper" @dblclick="edit">
    <dialog class="dropdown-modal" @close="stop">
        <table>
            <thead>
                <tr>
                    <th>Дата</th>
                    <th>Сумма</th>
                    <th></th>
                </tr>
            </thead>
            <tbody> 
                <tr v-for="payment in value" :key="payment.date">
                    <td><input type="date" :value="payment.date" @input="payment.date = $event.target.value" /></td>
                    <td><input type="number" :value="payment.amount" @input="payment.amount = parseFloat($event.target.value)" /></td>
                    <td><button @click="value.splice(value.indexOf(payment), 1)">Удалить</button></td>
                </tr>
            </tbody>
        </table>
        <button @click="add">Добавить</button>
        <button @click="stop">Применить</button>
    </dialog>
    <span v-if="!isEditing">{{ value.map(payment => payment.amount).join(', ') }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue';

export default defineComponent({
  props: {
    value: {
      type: Array as PropType<{date: string, amount: number}[]>,
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
    },
    async stop() {
      this.isEditing = false;
      this.$el.querySelector('dialog').close();
      this.$emit('update', this.value);
    },
    async add() {
      this.value.push({date: new Date().toISOString().split('T')[0], amount: 0});
    }
  },
  components: {
  },
});
</script>

<style>
</style>
